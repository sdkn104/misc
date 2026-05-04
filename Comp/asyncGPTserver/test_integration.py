"""Integration tests: 実際のAzure OpenAI APIとSQLite DBを使用

前提条件:
  - .env に AZURE_OPENAI_API_KEY と AZURE_OPENAI_ENDPOINT が設定されていること

実行方法:
  pytest test_integration.py -v
  pytest test_integration.py -v -s   # print出力あり
"""
import asyncio
import os
import uuid
from pathlib import Path
from unittest.mock import patch

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport

load_dotenv()

# 認証情報の有無を記録（skipif判定用）
_has_credentials = bool(os.getenv('AZURE_OPENAI_API_KEY')) and bool(os.getenv('AZURE_OPENAI_ENDPOINT'))

# app.py のモジュールレベル初期化が失敗しないようダミー値をセット
os.environ.setdefault('AZURE_OPENAI_API_KEY', 'dummy-key-for-import')
os.environ.setdefault('AZURE_OPENAI_ENDPOINT', 'https://dummy.openai.azure.com/')

pytestmark = pytest.mark.skipif(
    not _has_credentials,
    reason='AZURE_OPENAI_API_KEY / AZURE_OPENAI_ENDPOINT が未設定'
)

import app as app_module
from app import app as fastapi_app

TEST_DB = 'test_integration.db'


@pytest.fixture(scope='session', autouse=True)
def use_test_db():
    """セッション全体でテスト専用DBを使用し、終了後に削除する"""
    with patch.object(app_module, 'DATABASE_PATH', TEST_DB):
        app_module.init_db()
        yield
    Path(TEST_DB).unlink(missing_ok=True)


# ----------------------------------------------------------------
# DB関数の結合テスト
# ----------------------------------------------------------------

class TestDbIntegration:
    def test_save_request_persists(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'integration test', 'gpt-4.1-azure', None, None, None)
        assert app_module.get_request_status(rid) == 'processing'

    def test_full_request_lifecycle(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'lifecycle test', 'gpt-4.1-azure', 500, 'high', None)

        app_module.update_request_status(rid, 'completed')
        app_module.save_result(rid, result='The answer is 42')

        assert app_module.get_request_status(rid) == 'completed'
        row = app_module.get_result(rid)
        assert row['result'] == 'The answer is 42'
        assert row['error'] is None

    def test_full_request_lifecycle_failed(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'error test', 'gpt-4.1-azure', None, None, None)

        app_module.update_request_status(rid, 'failed')
        app_module.save_result(rid, error='timeout')

        assert app_module.get_request_status(rid) == 'failed'
        row = app_module.get_result(rid)
        assert row['error'] == 'timeout'
        assert row['result'] is None

    def test_result_upsert(self):
        """INSERT OR REPLACEで結果を上書きできること"""
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'upsert test', 'gpt-4.1-azure', None, None, None)
        app_module.save_result(rid, result='first')
        app_module.save_result(rid, result='second')
        assert app_module.get_result(rid)['result'] == 'second'


# ----------------------------------------------------------------
# generate_text() の結合テスト (実際のAzure OpenAI API呼び出し)
# ----------------------------------------------------------------

class TestGenerateTextIntegration:
    @pytest.mark.asyncio
    async def test_generate_text_returns_string(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'Say "hello" in one word.', 'gpt-4.1-azure', 20, None, None)

        result = await app_module.generate_text(rid, 'Say "hello" in one word.', 'gpt-4.1-azure', 20, None, None)

        assert isinstance(result, str)
        assert len(result) > 0
        assert app_module.get_request_status(rid) == 'completed'
        assert app_module.get_result(rid)['result'] == result

    @pytest.mark.asyncio
    async def test_generate_text_result_saved_to_db(self):
        rid = str(uuid.uuid4())
        prompt = 'Reply with only the number 1.'
        app_module.save_request(rid, prompt, 'gpt-4.1-azure', None, None, None)

        await app_module.generate_text(rid, prompt, 'gpt-4.1-azure', None, None, None)

        row = app_module.get_result(rid)
        assert row['result'] is not None
        assert row['error'] is None

    @pytest.mark.asyncio
    async def test_generate_text_with_max_completion_tokens(self):
        """max_completion_tokensを指定して生成できること"""
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'Count from 1 to 3.', 'gpt-4.1-azure', 30, None, None)

        result = await app_module.generate_text(rid, 'Count from 1 to 3.', 'gpt-4.1-azure', 30, None, None)

        assert isinstance(result, str)
        assert app_module.get_request_status(rid) == 'completed'

    @pytest.mark.asyncio
    async def test_generate_text_invalid_model_sets_failed(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'hello', 'nonexistent-model-xyz', None, None, None)

        with pytest.raises(Exception):
            await app_module.generate_text(rid, 'hello', 'nonexistent-model-xyz', None, None, None)

        assert app_module.get_request_status(rid) == 'failed'
        assert app_module.get_result(rid)['error'] is not None


# ----------------------------------------------------------------
# APIエンドポイントの結合テスト
# ----------------------------------------------------------------

class TestEndpointIntegration:
    @pytest.mark.asyncio
    async def test_generate_and_poll_until_complete(self):
        """POST /generate → GET /result をポーリングして完了を確認"""
        async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
            resp = await ac.post('/generate', json={
                'prompt': 'Reply with exactly one word: hello',
                'model': 'gpt-5-mini',
                'max_completion_tokens': 200,
                'reasoning_effort': "medium",
                'verbosity': "low",
            })
            assert resp.status_code == 200
            data = resp.json()
            assert data['status'] == 'processing'
            rid = data['request_id']

            # バックグラウンドタスクが完了するまでポーリング (最大30秒)
            for _ in range(30):
                await asyncio.sleep(1)
                result_resp = await ac.get(f'/result/{rid}')
                result_data = result_resp.json()
                if result_data['status'] in ('completed', 'failed'):
                    break

        assert result_data['status'] == 'completed', f"failed with error: {result_data.get('error')}"
        assert 'result' in result_data
        assert len(result_data['result']) > 0

    @pytest.mark.asyncio
    async def test_generate_with_custom_request_id(self):
        rid = str(uuid.uuid4())
        async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
            resp = await ac.post('/generate', json={
                'prompt': 'Say yes.',
                'model': 'gpt-4.1-azure',
                'request_id': rid,
                'max_completion_tokens': 10,
            })
        assert resp.status_code == 200
        assert resp.json()['request_id'] == rid

    @pytest.mark.asyncio
    async def test_duplicate_request_id_returns_409(self):
        rid = str(uuid.uuid4())
        async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
            await ac.post('/generate', json={'prompt': 'hello', 'model': 'gpt-4.1-azure', 'request_id': rid})
            resp = await ac.post('/generate', json={'prompt': 'hello', 'request_id': rid})
        assert resp.status_code == 409

    @pytest.mark.asyncio
    async def test_result_not_found_returns_404(self):
        async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
            resp = await ac.get('/result/no-such-id-xyz')
        assert resp.status_code == 404
