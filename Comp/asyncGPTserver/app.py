# FastAPI Async GPT Server
# 依存関係: fastapi==0.111.1, uvicorn==0.24.0, azure-openai==1.0.0, python-dotenv==1.0.0
# 実行: python app_fastapi.py

import asyncio
import os
import sqlite3
import uuid
from datetime import datetime
from typing import Optional

from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 環境変数読み込み
load_dotenv()

# ----------------------------------------------------------------
# データベース設定
# ----------------------------------------------------------------
DATABASE_PATH = 'async_gpt.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute('PRAGMA journal_mode=WAL;')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            request_id TEXT PRIMARY KEY,
            prompt TEXT NOT NULL,
            model TEXT DEFAULT 'gpt-3.5-turbo',
            max_tokens INTEGER DEFAULT 100,
            temperature REAL DEFAULT 0.7,
            status TEXT DEFAULT 'processing',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            request_id TEXT PRIMARY KEY,
            result TEXT,
            error TEXT,
            FOREIGN KEY (request_id) REFERENCES requests (request_id)
        )
    ''')

    conn.commit()
    conn.close()


def save_request(request_id: str, prompt: str, model: str, max_tokens: int, temperature: float):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (request_id, prompt, model, max_tokens, temperature)
        VALUES (?, ?, ?, ?, ?)
    ''', (request_id, prompt, model, max_tokens, temperature))
    conn.commit()
    conn.close()


def update_request_status(request_id: str, status: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE requests SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE request_id = ?
    ''', (status, request_id))
    conn.commit()
    conn.close()


def save_result(request_id: str, result: Optional[str] = None, error: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO results (request_id, result, error)
        VALUES (?, ?, ?)
    ''', (request_id, result, error))
    conn.commit()
    conn.close()


def get_request_status(request_id: str) -> Optional[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM requests WHERE request_id = ?', (request_id,))
    row = cursor.fetchone()
    conn.close()
    return row['status'] if row else None


def get_result(request_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT result, error FROM results WHERE request_id = ?', (request_id,))
    row = cursor.fetchone()
    conn.close()
    return row


# ----------------------------------------------------------------
# Azure OpenAI クライアント初期化
# ----------------------------------------------------------------
client = AsyncAzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-12-01-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)


class GenerateRequest(BaseModel):
    prompt: str
    request_id: Optional[str] = None
    model: Optional[str] = 'gpt-4.1'
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7

# ----------------------------------------------------------------
# FastAPI 初期化
# ----------------------------------------------------------------
app = FastAPI()

# ----------------------------------------------------------------
# データベース初期化
# ----------------------------------------------------------------
init_db()


# ----------------------------------------------------------------
# ----------------------------------------------------------------
async def generate_text(request_id: str, prompt: str, model: str, max_tokens: int, temperature: float) -> str:
    try:
        update_request_status(request_id, 'processing')

        response = await client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )

        result = response.choices[0].message.content
        update_request_status(request_id, 'completed')
        save_result(request_id, result=result)
        return result

    except Exception as exc:
        update_request_status(request_id, 'failed')
        save_result(request_id, error=str(exc))
        raise

# ----------------------------------------------------------------
# APIエンドポイント
# ----------------------------------------------------------------
@app.post('/generate')
async def generate(request_data: GenerateRequest):
    if not request_data.prompt or not isinstance(request_data.prompt, str):
        raise HTTPException(status_code=400, detail='Prompt is required')

    if len(request_data.prompt) > 1000000:
        raise HTTPException(status_code=400, detail='Prompt too long')

    request_id = request_data.request_id or str(uuid.uuid4())
    if request_data.request_id is not None:
        if get_request_status(request_id) is not None:
            raise HTTPException(status_code=409, detail='Request ID already exists')

    save_request(request_id, request_data.prompt, request_data.model, request_data.max_tokens, request_data.temperature)

    # バックグラウンドタスクで非同期に実行
    asyncio.create_task(generate_text(request_id, request_data.prompt, request_data.model, request_data.max_tokens, request_data.temperature))

    return {
        'request_id': request_id,
        'status': 'processing'
    }


@app.get('/result/{request_id}')
async def get_result_endpoint(request_id: str):
    status = get_request_status(request_id)
    if not status:
        raise HTTPException(status_code=404, detail='Request not found')

    response = {'request_id': request_id, 'status': status}
    if status == 'completed':
        result_data = get_result(request_id)
        if result_data:
            response['result'] = result_data['result']
    elif status == 'failed':
        result_data = get_result(request_id)
        if result_data and result_data['error']:
            response['error'] = result_data['error']

    return response


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=False)
