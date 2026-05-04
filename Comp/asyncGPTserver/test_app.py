"""Tests for app.py

Required packages: pip install pytest pytest-asyncio httpx
"""
import os
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ダミーの環境変数を設定してからimport (AzureClientの初期化に必要)
os.environ.setdefault('AZURE_OPENAI_API_KEY', 'test-key')
os.environ.setdefault('AZURE_OPENAI_ENDPOINT', 'https://test.openai.azure.com/')

import app as app_module
from app import app as fastapi_app


@pytest.fixture(autouse=True)
def temp_db(tmp_path):
    """全テストでIsolatedな一時DBを使用する"""
    db_path = str(tmp_path / 'test.db')
    with patch.object(app_module, 'DATABASE_PATH', db_path):
        app_module.init_db()
        yield db_path


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    return TestClient(fastapi_app)


# ----------------------------------------------------------------
# DB関数のテスト
# ----------------------------------------------------------------

class TestDbFunctions:
    def test_init_db_creates_tables(self, temp_db):
        import sqlite3
        conn = sqlite3.connect(temp_db)
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        assert {'requests', 'results'}.issubset(tables)

    def test_save_request_sets_processing_status(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'hello', 'gpt-4', None, None, None)
        assert app_module.get_request_status(rid) == 'processing'

    def test_update_request_status(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'hello', 'gpt-4', None, None, None)
        app_module.update_request_status(rid, 'completed')
        assert app_module.get_request_status(rid) == 'completed'

    def test_save_and_get_result(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'hello', 'gpt-4', None, None, None)
        app_module.save_result(rid, result='world')
        row = app_module.get_result(rid)
        assert row['result'] == 'world'
        assert row['error'] is None

    def test_save_result_error(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'hello', 'gpt-4', None, None, None)
        app_module.save_result(rid, error='oops')
        row = app_module.get_result(rid)
        assert row['result'] is None
        assert row['error'] == 'oops'

    def test_get_status_not_found_returns_none(self):
        assert app_module.get_request_status('no-such-id') is None

    def test_get_result_not_found_returns_none(self):
        assert app_module.get_result('no-such-id') is None


# ----------------------------------------------------------------
# generate_text()のテスト
# ----------------------------------------------------------------

class TestGenerateText:
    @pytest.mark.asyncio
    async def test_success(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'hello', 'gpt-4', None, None, None)

        mock_resp = MagicMock()
        mock_resp.choices[0].message.content = 'Generated!'
        with patch.object(app_module.client.chat.completions, 'create', new=AsyncMock(return_value=mock_resp)):
            result = await app_module.generate_text(rid, 'hello', 'gpt-4', None, None, None)

        assert result == 'Generated!'
        assert app_module.get_request_status(rid) == 'completed'
        assert app_module.get_result(rid)['result'] == 'Generated!'

    @pytest.mark.asyncio
    async def test_api_failure_sets_failed_status(self):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'hello', 'gpt-4', None, None, None)

        with patch.object(app_module.client.chat.completions, 'create', new=AsyncMock(side_effect=RuntimeError('API down'))):
            with pytest.raises(RuntimeError, match='API down'):
                await app_module.generate_text(rid, 'hello', 'gpt-4', None, None, None)

        assert app_module.get_request_status(rid) == 'failed'
        assert app_module.get_result(rid)['error'] == 'API down'

    @pytest.mark.asyncio
    async def test_none_params_excluded_from_api_kwargs(self):
        """Noneのパラメータがcreate()のkwargsに含まれないことを確認"""
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'hello', 'gpt-4', None, None, None)

        mock_create = AsyncMock(return_value=MagicMock())
        mock_create.return_value.choices[0].message.content = 'ok'
        with patch.object(app_module.client.chat.completions, 'create', new=mock_create):
            await app_module.generate_text(rid, 'hello', 'gpt-4', None, None, None)

        called_kwargs = mock_create.call_args.kwargs
        assert 'max_completion_tokens' not in called_kwargs
        assert 'reasoning_effort' not in called_kwargs
        assert 'verbosity' not in called_kwargs

    @pytest.mark.asyncio
    async def test_specified_params_included_in_api_kwargs(self):
        """指定されたパラメータのみcreate()のkwargsに含まれることを確認"""
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'hello', 'gpt-4', 200, 'high', None)

        mock_create = AsyncMock(return_value=MagicMock())
        mock_create.return_value.choices[0].message.content = 'ok'
        with patch.object(app_module.client.chat.completions, 'create', new=mock_create):
            await app_module.generate_text(rid, 'hello', 'gpt-4', 200, 'high', None)

        called_kwargs = mock_create.call_args.kwargs
        assert called_kwargs['max_completion_tokens'] == 200
        assert called_kwargs['reasoning_effort'] == 'high'
        assert 'verbosity' not in called_kwargs


# ----------------------------------------------------------------
# POST /generate エンドポイントのテスト
# ----------------------------------------------------------------

class TestGenerateEndpoint:
    def test_returns_processing_status(self, client):
        with patch.object(app_module, 'generate_text', new=AsyncMock(return_value='ok')):
            resp = client.post('/generate', json={'prompt': 'Hello'})
        assert resp.status_code == 200
        data = resp.json()
        assert data['status'] == 'processing'
        assert 'request_id' in data

    def test_custom_request_id_is_used(self, client):
        rid = str(uuid.uuid4())
        with patch.object(app_module, 'generate_text', new=AsyncMock(return_value='ok')):
            resp = client.post('/generate', json={'prompt': 'Hi', 'request_id': rid})
        assert resp.json()['request_id'] == rid

    def test_duplicate_request_id_returns_409(self, client):
        rid = str(uuid.uuid4())
        with patch.object(app_module, 'generate_text', new=AsyncMock(return_value='ok')):
            client.post('/generate', json={'prompt': 'Hi', 'request_id': rid})
            resp = client.post('/generate', json={'prompt': 'Hi', 'request_id': rid})
        assert resp.status_code == 409

    def test_empty_prompt_returns_400(self, client):
        resp = client.post('/generate', json={'prompt': ''})
        assert resp.status_code == 400

    def test_prompt_too_long_returns_400(self, client):
        resp = client.post('/generate', json={'prompt': 'x' * 1_000_001})
        assert resp.status_code == 400


# ----------------------------------------------------------------
# GET /result/{request_id} エンドポイントのテスト
# ----------------------------------------------------------------

class TestResultEndpoint:
    def test_not_found_returns_404(self, client):
        resp = client.get('/result/nonexistent')
        assert resp.status_code == 404

    def test_processing_has_no_result_field(self, client):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'hello', 'gpt-4', None, None, None)
        resp = client.get(f'/result/{rid}')
        data = resp.json()
        assert resp.status_code == 200
        assert data['status'] == 'processing'
        assert 'result' not in data

    def test_completed_includes_result(self, client):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'hello', 'gpt-4', None, None, None)
        app_module.update_request_status(rid, 'completed')
        app_module.save_result(rid, result='Hello World')
        resp = client.get(f'/result/{rid}')
        data = resp.json()
        assert data['status'] == 'completed'
        assert data['result'] == 'Hello World'

    def test_failed_includes_error(self, client):
        rid = str(uuid.uuid4())
        app_module.save_request(rid, 'hello', 'gpt-4', None, None, None)
        app_module.update_request_status(rid, 'failed')
        app_module.save_result(rid, error='API error')
        resp = client.get(f'/result/{rid}')
        data = resp.json()
        assert data['status'] == 'failed'
        assert data['error'] == 'API error'
