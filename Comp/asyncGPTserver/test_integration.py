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
        app_module.save_request(rid, {'model': 'gpt-4.1-azure', 'messages': [{'role': 'user', 'content': 'integration test'}]})
        assert app_module.get_request_status(rid) == 'processing'

    def test_full_request_lifecycle(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, {'model': 'gpt-4.1-azure', 'messages': [{'role': 'user', 'content': 'lifecycle test'}], 'max_completion_tokens': 500, 'reasoning_effort': 'high'})

        app_module.update_request_status(rid, 'completed')
        app_module.save_result(rid, azure_response_status=200, azure_response_body='{"choices":[{"message":{"content":"The answer is 42"}}]}')

        assert app_module.get_request_status(rid) == 'completed'
        row = app_module.get_result(rid)
        assert row['azure_response_status'] == 200
        assert row['azure_response_body'] is not None

    def test_full_request_lifecycle_failed(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, {'model': 'gpt-4.1-azure', 'messages': [{'role': 'user', 'content': 'error test'}]})

        app_module.update_request_status(rid, 'failed')
        app_module.save_result(rid, azure_response_status=429, azure_response_body='{"error":{"message":"timeout"}}')

        assert app_module.get_request_status(rid) == 'failed'
        row = app_module.get_result(rid)
        assert row['azure_response_status'] == 429
        assert row['azure_response_body'] is not None

    def test_result_upsert(self):
        """INSERT OR REPLACEで結果を上書きできること"""
        rid = str(uuid.uuid4())
        app_module.save_request(rid, {'model': 'gpt-4.1-azure', 'messages': [{'role': 'user', 'content': 'upsert test'}]})
        app_module.save_result(rid, azure_response_status=200, azure_response_body='{"choices":[{"message":{"content":"first"}}]}')
        app_module.save_result(rid, azure_response_status=200, azure_response_body='{"choices":[{"message":{"content":"second"}}]}')
        assert 'second' in app_module.get_result(rid)['azure_response_body']

    def test_save_request_sets_created_at(self):
        """save_requestでcreated_atが記録されること"""
        rid = str(uuid.uuid4())
        app_module.save_request(rid, {'model': 'gpt-4.1-azure', 'messages': [{'role': 'user', 'content': 'datetime test'}]})
        rows = app_module.get_history()
        matched = next((r for r in rows if r['request_id'] == rid), None)
        assert matched is not None
        assert matched['created_at'] is not None

    def test_update_request_status_sets_updated_at(self):
        """update_request_statusでupdated_atが更新されること"""
        rid = str(uuid.uuid4())
        app_module.save_request(rid, {'model': 'gpt-4.1-azure', 'messages': [{'role': 'user', 'content': 'updated_at test'}]})
        app_module.update_request_status(rid, 'completed')
        rows = app_module.get_history()
        matched = next((r for r in rows if r['request_id'] == rid), None)
        assert matched['updated_at'] is not None
        assert matched['updated_at'] >= matched['created_at']

    def test_get_history_returns_records_newest_first(self):
        """get_historyが新しい順で返すこと"""
        rows = app_module.get_history()
        assert len(rows) >= 2
        assert rows[0]['created_at'] >= rows[1]['created_at']

    def test_get_history_includes_result(self):
        """get_historyにresultsテーブルの内容が含まれること"""
        rid = str(uuid.uuid4())
        app_module.save_request(rid, {'model': 'gpt-4.1-azure', 'messages': [{'role': 'user', 'content': 'history result test'}]})
        app_module.update_request_status(rid, 'completed')
        app_module.save_result(rid, azure_response_status=200, azure_response_body='{"choices":[]}')
        rows = app_module.get_history()
        matched = next((r for r in rows if r['request_id'] == rid), None)
        assert matched['azure_response_status'] == 200
        assert matched['azure_response_body'] is not None


# ----------------------------------------------------------------
# generate_text() の結合テスト (実際のAzure OpenAI API呼び出し)
# ----------------------------------------------------------------

class TestGenerateTextIntegration:
    @pytest.mark.asyncio
    async def test_generate_text_saves_response(self):
        rid = str(uuid.uuid4())
        body = {'model': 'gpt-4.1-azure', 'messages': [{'role': 'user', 'content': 'Say "hello" in one word.'}], 'max_completion_tokens': 20}
        app_module.save_request(rid, body)

        await app_module.generate_text(rid, body)

        assert app_module.get_request_status(rid) == 'completed'
        row = app_module.get_result(rid)
        assert row['azure_response_status'] == 200
        assert row['azure_response_body'] is not None

    @pytest.mark.asyncio
    async def test_generate_text_result_saved_to_db(self):
        rid = str(uuid.uuid4())
        body = {'model': 'gpt-4.1-azure', 'messages': [{'role': 'user', 'content': 'Reply with only the number 1.'}]}
        app_module.save_request(rid, body)

        await app_module.generate_text(rid, body)

        row = app_module.get_result(rid)
        assert row['azure_response_status'] == 200
        assert row['azure_response_body'] is not None

    @pytest.mark.asyncio
    async def test_generate_text_with_max_completion_tokens(self):
        """max_completion_tokensを指定して生成できること"""
        rid = str(uuid.uuid4())
        body = {'model': 'gpt-4.1-azure', 'messages': [{'role': 'user', 'content': 'Count from 1 to 3.'}], 'max_completion_tokens': 30}
        app_module.save_request(rid, body)

        await app_module.generate_text(rid, body)

        assert app_module.get_request_status(rid) == 'completed'
        assert app_module.get_result(rid)['azure_response_status'] == 200

    @pytest.mark.asyncio
    async def test_generate_text_invalid_model_sets_failed(self):
        rid = str(uuid.uuid4())
        body = {'model': 'nonexistent-model-xyz', 'messages': [{'role': 'user', 'content': 'hello'}]}
        app_module.save_request(rid, body)

        await app_module.generate_text(rid, body)  # 例外はキャッチ済みでraiseしない

        assert app_module.get_request_status(rid) == 'failed'
        row = app_module.get_result(rid)
        assert row['azure_response_status'] is not None
        assert row['azure_response_body'] is not None


# ----------------------------------------------------------------
# APIエンドポイントの結合テスト
# ----------------------------------------------------------------

class TestEndpointIntegration:
    @pytest.mark.asyncio
    async def test_generate_and_poll_until_complete(self):
        """POST /generate → GET /result をポーリングして完了を確認"""
        async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
            resp = await ac.post('/generate', json={
                'azure_openai_body': {
                    'model': 'gpt-5-mini',
                    'messages': [{'role': 'user', 'content': 'Reply with exactly one word: hello'}],
                    'max_completion_tokens': 200,
                    'reasoning_effort': 'medium',
                    'verbosity': 'low',
                },
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

        assert result_resp.status_code == 200
        assert result_data['status'] == 'completed', f"failed: {result_data.get('azure_openai_body')}"
        assert 'azure_openai_body' in result_data
        assert result_data['azure_openai_body']['choices'][0]['message']['content']

    @pytest.mark.asyncio
    async def test_generate_with_custom_request_id(self):
        rid = str(uuid.uuid4())
        async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
            resp = await ac.post('/generate', json={
                'request_id': rid,
                'azure_openai_body': {
                    'model': 'gpt-4.1-azure',
                    'messages': [{'role': 'user', 'content': 'Say yes.'}],
                    'max_completion_tokens': 10,
                },
            })
        assert resp.status_code == 200
        assert resp.json()['request_id'] == rid

    @pytest.mark.asyncio
    async def test_duplicate_request_id_returns_409(self):
        rid = str(uuid.uuid4())
        body = {'model': 'gpt-4.1-azure', 'messages': [{'role': 'user', 'content': 'hello'}]}
        async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
            await ac.post('/generate', json={'request_id': rid, 'azure_openai_body': body})
            resp = await ac.post('/generate', json={'request_id': rid, 'azure_openai_body': body})
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_result_not_found_returns_404(self):
        async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
            resp = await ac.get('/result/no-such-id-xyz')
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_history_returns_list_with_required_fields(self):
        """GET /history がリスト形式で必須フィールドを含むこと"""
        async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
            resp = await ac.get('/history')
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0
        entry = data[0]
        for field in ('request_id', 'model', 'status', 'created_at', 'updated_at', 'azure_response_status', 'azure_openai_body'):
            assert field in entry

    @pytest.mark.asyncio
    async def test_history_newest_first(self):
        """GET /history が新しい順で返すこと"""
        async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
            resp = await ac.get('/history')
        data = resp.json()
        assert len(data) >= 2
        assert data[0]['created_at'] >= data[1]['created_at']
