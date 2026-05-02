# Async GPT Server
# 依存関係: Flask==2.3.3, Flask-Asyncio==0.21.0, azure-openai==1.0.0, python-dotenv==1.0.0
# インストール: pip install Flask Flask-Asyncio azure-openai python-dotenv

import uuid
import sqlite3
import os
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify
from flask_asyncio import FlaskAsyncio
from azure.openai import AsyncAzureOpenAI
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

# ----------------------------------------------------------------
# データベース設定
# ----------------------------------------------------------------
DATABASE_PATH = 'async_gpt.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute('PRAGMA journal_mode=WAL;')  # WALモード有効化
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # リクエストテーブル作成
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

    # 結果テーブル作成
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

def save_request(request_id, prompt, model, max_tokens, temperature):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (request_id, prompt, model, max_tokens, temperature)
        VALUES (?, ?, ?, ?, ?)
    ''', (request_id, prompt, model, max_tokens, temperature))
    conn.commit()
    conn.close()

def update_request_status(request_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE requests SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE request_id = ?
    ''', (status, request_id))
    conn.commit()
    conn.close()

def save_result(request_id, result=None, error=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO results (request_id, result, error)
        VALUES (?, ?, ?)
    ''', (request_id, result, error))
    conn.commit()
    conn.close()

def get_request_status(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM requests WHERE request_id = ?', (request_id,))
    row = cursor.fetchone()
    conn.close()
    return row['status'] if row else None

def get_result(request_id):
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
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

async def generate_text(request_id, prompt, model, max_tokens, temperature):
    try:
        # ステータスをprocessingに設定
        update_request_status(request_id, 'processing')

        # Azure OpenAI API呼び出し
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )

        # 結果取得
        result = response.choices[0].message.content

        # ステータスをcompletedに更新
        update_request_status(request_id, 'completed')
        save_result(request_id, result=result)

    except Exception as e:
        # エラー処理
        update_request_status(request_id, 'failed')
        save_result(request_id, error=str(e))

def start_background_task(request_id, prompt, model, max_tokens, temperature):
    # バックグラウンドで非同期タスクを開始
    asyncio.create_task(generate_text(request_id, prompt, model, max_tokens, temperature))

# ----------------------------------------------------------------
# Flaskアプリ初期化
# ----------------------------------------------------------------
app = FlaskAsyncio(__name__)

# ----------------------------------------------------------------
# データベース初期化
# ----------------------------------------------------------------
init_db()

# ----------------------------------------------------------------
# APIエンドポイント
# ----------------------------------------------------------------
@app.route('/generate', methods=['POST'])
async def generate():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({'error': 'Prompt is required'}), 400

    prompt = data['prompt']
    model = data.get('model', 'gpt-4.1')
    max_tokens = data.get('max_tokens', 100)
    temperature = data.get('temperature', 0.7)
    request_id = data.get('request_id')

    # 入力バリデーション
    if len(prompt) > 1000000:  # 例: プロンプト長さ制限
        return jsonify({'error': 'Prompt too long'}), 400

    if request_id is not None:
        if not isinstance(request_id, str) or not request_id.strip():
            return jsonify({'error': 'request_id must be a non-empty string'}), 400
        if get_request_status(request_id) is not None:
            return jsonify({'error': 'Request ID already exists'}), 409
    else:
        request_id = str(uuid.uuid4())

    # データベースに保存
    save_request(request_id, prompt, model, max_tokens, temperature)

    # バックグラウンドタスク開始
    start_background_task(request_id, prompt, model, max_tokens, temperature)

    return jsonify({
        'request_id': request_id,
        'status': 'processing'
    })

@app.route('/result/<request_id>', methods=['GET'])
async def get_result_endpoint(request_id):
    status = get_request_status(request_id)
    if not status:
        return jsonify({'error': 'Request not found'}), 404

    response = {
        'request_id': request_id,
        'status': status
    }

    if status == 'completed':
        result_data = get_result(request_id)
        if result_data:
            response['result'] = result_data['result']
    elif status == 'failed':
        result_data = get_result(request_id)
        if result_data and result_data['error']:
            response['error'] = result_data['error']

    return jsonify(response)

# ----------------------------------------------------------------
# ----------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
