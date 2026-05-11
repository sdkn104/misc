

# デスクトップアプリ（CLIバッチ型）版
# 依存関係: openai==1.0.0, python-dotenv==1.0.0
# 実行: python app.py

import json
import os
import uuid
from datetime import datetime
 

from openai import AzureOpenAI, APIStatusError
from dotenv import load_dotenv

INPUT_FILE = "app.input.json"
HISTORY_FILE = "app.history.json"

def load_input():
    """app.input.jsonを読み込む"""
    with open(INPUT_FILE, encoding="utf-8") as f:
        return json.load(f)

def append_history(entry: dict):
    """app.history.jsonに1件追記（ファイルがなければ新規作成）"""
    try:
        with open(HISTORY_FILE, encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    history.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def main():
    load_dotenv()
    # Azure OpenAIクライアント初期化
    client = AzureOpenAI(
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version='2023-12-01-preview',
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
    )

    # 入力読み込み
    try:
        azure_openai_body = load_input()
    except Exception as e:
        print(f"[ERROR] 入力ファイルの読み込みに失敗: {e}")
        return

    request_id = str(uuid.uuid4())
    start_time = datetime.now().isoformat()
    result_entry = {
        "request_id": request_id,
        "request": azure_openai_body,
        "start_time": start_time,
    }

    try:
        # OpenAI API呼び出し
        response = client.chat.completions.create(**azure_openai_body)
        result_entry["status"] = "completed"
        result_entry["azure_response_status"] = 200
        result_entry["azure_response_body"] = response.model_dump()
    except APIStatusError as exc:
        try:
            body = exc.response.json()
        except Exception:
            body = {'error': {'message': str(exc)}}
        result_entry["status"] = "failed"
        result_entry["azure_response_status"] = exc.status_code
        result_entry["azure_response_body"] = body
    except Exception as exc:
        result_entry["status"] = "failed"
        result_entry["azure_response_status"] = 500
        result_entry["azure_response_body"] = {'error': {'message': str(exc)}}

    result_entry["end_time"] = datetime.now().isoformat()
    append_history(result_entry)
    print(f"[INFO] 完了: request_id={request_id}, status={result_entry['status']}")

if __name__ == "__main__":
    main()


