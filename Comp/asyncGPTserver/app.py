# FastAPI Async GPT Server
# 依存関係: fastapi==0.111.1, uvicorn==0.24.0, openai==1.0.0, python-dotenv==1.0.0
# 実行: python app.py

import asyncio
import json
import os
import sqlite3
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from openai import AsyncAzureOpenAI, APIStatusError
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# 環境変数読み込み
load_dotenv()

# ----------------------------------------------------------------
# データベース設定
# ----------------------------------------------------------------
DATABASE_PATH = 'async_gpt.db'


def get_db_connection():
    """SQLiteデータベース接続を取得"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute('PRAGMA journal_mode=WAL;')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """データベースのテーブルを初期化"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            request_id TEXT PRIMARY KEY,
            prompt TEXT NOT NULL,
            model TEXT DEFAULT 'gpt-4.1',
            status TEXT DEFAULT 'processing',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            request_id TEXT PRIMARY KEY,
            azure_response_status INTEGER,
            azure_response_body TEXT,
            FOREIGN KEY (request_id) REFERENCES requests (request_id)
        )
    ''')

    conn.commit()
    conn.close()


def save_request(request_id: str, azure_openai_body: Dict[str, Any]):
    """リクエスト情報をデータベースに保存"""
    conn = get_db_connection()
    cursor = conn.cursor()
    model = azure_openai_body.get('model')
    cursor.execute('''
        INSERT INTO requests (request_id, prompt, model, created_at)
        VALUES (?, ?, ?, ?)
    ''', (request_id, json.dumps(azure_openai_body), model, datetime.now()))
    conn.commit()
    conn.close()


def update_request_status(request_id: str, status: str):
    """リクエストのステータスを更新"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE requests SET status = ?, updated_at = ? WHERE request_id = ?
    ''', (status, datetime.now(), request_id))
    conn.commit()
    conn.close()


def save_result(request_id: str, azure_response_status: int, azure_response_body: str):
    """Azure OpenAI APIのレスポンスをデータベースに保存"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO results (request_id, azure_response_status, azure_response_body)
        VALUES (?, ?, ?)
    ''', (request_id, azure_response_status, azure_response_body))
    conn.commit()
    conn.close()


def get_request_status(request_id: str) -> Optional[str]:
    """リクエストのステータスを取得"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM requests WHERE request_id = ?', (request_id,))
    row = cursor.fetchone()
    conn.close()
    return row['status'] if row else None


def get_result(request_id: str):
    """リクエストのAzure OpenAI APIレスポンスを取得"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT azure_response_status, azure_response_body FROM results WHERE request_id = ?', (request_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_history():
    """全リクエストの履歴をrequests/resultsテーブルのJOINで取得"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.request_id, r.model, r.status,
               r.created_at, r.updated_at,
               res.azure_response_status, res.azure_response_body
        FROM requests r
        LEFT JOIN results res ON r.request_id = res.request_id
        ORDER BY r.created_at DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows


# ----------------------------------------------------------------
# Azure OpenAI クライアント初期化
# ----------------------------------------------------------------
client = AsyncAzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-12-01-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)


class GenerateRequest(BaseModel):
    request_id: Optional[str] = None
    azure_openai_body: Dict[str, Any]

# ----------------------------------------------------------------
# FastAPI 初期化
# ----------------------------------------------------------------
app = FastAPI()

# ----------------------------------------------------------------
# データベース初期化
# ----------------------------------------------------------------
init_db()


# ----------------------------------------------------------------
# 非同期テキスト生成関数
# ----------------------------------------------------------------
async def generate_text(request_id: str, azure_openai_body: Dict[str, Any]):
    """Azure OpenAI APIを呼び出し、レスポンス全体をDBに保存"""
    try:
        update_request_status(request_id, 'processing')

        response = await client.chat.completions.create(**azure_openai_body)

        update_request_status(request_id, 'completed')
        save_result(request_id, azure_response_status=200, azure_response_body=json.dumps(response.model_dump()))

    except APIStatusError as exc:
        try:
            body = exc.response.json()
        except Exception:
            body = {'error': {'message': str(exc)}}
        try:
            update_request_status(request_id, 'failed')
            save_result(request_id, azure_response_status=exc.status_code, azure_response_body=json.dumps(body))
        except Exception:
            pass

    except asyncio.CancelledError:
        # サーバー終了などによるキャンセル。DB更新後にre-raiseして正常なキャンセル伝播を維持する
        try:
            update_request_status(request_id, 'failed')
            save_result(request_id, azure_response_status=500,
                        azure_response_body=json.dumps({'error': {'message': 'Task cancelled'}}))
        except Exception:
            pass
        raise

    except Exception as exc:
        try:
            update_request_status(request_id, 'failed')
            save_result(request_id, azure_response_status=500,
                        azure_response_body=json.dumps({'error': {'message': str(exc)}}))
        except Exception:
            pass

# ----------------------------------------------------------------
# APIエンドポイント
# ----------------------------------------------------------------
@app.post('/generate')
async def generate(request_data: GenerateRequest):
    """テキスト生成リクエストを受け付け、バックグラウンドで処理を開始"""
    request_id = request_data.request_id or str(uuid.uuid4())
    if request_data.request_id is not None:
        if get_request_status(request_id) is not None:
            raise HTTPException(status_code=409, detail='Request ID already exists')

    save_request(request_id, request_data.azure_openai_body)

    asyncio.create_task(generate_text(request_id, request_data.azure_openai_body))

    return {
        'request_id': request_id,
        'status': 'processing'
    }


@app.get('/result/{request_id}')
async def get_result_endpoint(request_id: str):
    """リクエストIDで処理結果をポーリング"""
    status = get_request_status(request_id)
    if not status:
        raise HTTPException(status_code=404, detail='Request not found')

    if status == 'processing':
        return JSONResponse(status_code=200, content={'request_id': request_id, 'status': 'processing'})

    result_data = get_result(request_id)
    azure_status = result_data['azure_response_status'] if result_data else 500
    azure_body = json.loads(result_data['azure_response_body']) if result_data and result_data['azure_response_body'] else {}

    return JSONResponse(
        status_code=azure_status,
        content={'request_id': request_id, 'status': status, 'azure_openai_body': azure_body},
    )


@app.get('/history')
async def get_history_endpoint():
    """全リクエストの処理履歴を返す"""
    rows = get_history()
    result = []
    for row in rows:
        entry = {
            'request_id': row['request_id'],
            'model': row['model'],
            'status': row['status'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at'],
            'azure_response_status': row['azure_response_status'],
            'azure_openai_body': json.loads(row['azure_response_body']) if row['azure_response_body'] else None,
        }
        result.append(entry)
    return result


if __name__ == '__main__':
    # Uvicornサーバーを起動
    import uvicorn
    # for debug
    #uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
    # for production (pythonw.exeで実行する場合はreload=Falseにすること)
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=False, log_config=None)
