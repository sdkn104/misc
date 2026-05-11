# input_queue フォルダを 1 秒ごとに監視し、Outlook メールを取得して
# 条件チェック後に Azure OpenAI API を非同期で呼び出すスタンドアロンスクリプト。
# API 呼び出しはバックグラウンドスレッドの asyncio イベントループで実行する。

import asyncio
import base64
import json
import os
import threading
import time
from pathlib import Path
from typing import Optional

import win32com.client
from openai import AsyncAzureOpenAI, APIStatusError
from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------------------------------
# 設定
# ----------------------------------------------------------------
INPUT_QUEUE = 'input_queue'   # 処理待ちファイルを置くフォルダ
OUTPUT_STORE = 'output_store' # API 結果を保存するフォルダ

# ----------------------------------------------------------------
# Azure OpenAI クライアント初期化
# ----------------------------------------------------------------
client = AsyncAzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-12-01-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

# ----------------------------------------------------------------
# バックグラウンドスレッドで asyncio イベントループを起動
# API 呼び出しコルーチンはこのループに投入する。
# win32com の COM オブジェクトはスレッドアフィニティがあるため
# Outlook アクセスはメインスレッドのみで行い、API 呼び出しのみをここで処理する。
# ----------------------------------------------------------------
_loop = asyncio.new_event_loop()
threading.Thread(target=_loop.run_forever, daemon=True).start()


# ----------------------------------------------------------------
# ユーティリティ
# ----------------------------------------------------------------
def message_id_to_filename(message_id: str) -> str:
    """message-id を base64 エンコードし、/ を _ に置換してファイル名として返す。"""
    return base64.b64encode(message_id.encode()).decode().replace('/', '_')


def get_smtp_address(address_entry) -> str:
    """AddressEntry から SMTP アドレスを取得する。
    Exchange ユーザーの場合は PrimarySmtpAddress を優先し、失敗時は Address にフォールバック。"""
    try:
        return address_entry.GetExchangeUser().PrimarySmtpAddress
    except Exception:
        return address_entry.Address


# ----------------------------------------------------------------
# Azure OpenAI API 呼び出し（バックグラウンドループで実行）
# ----------------------------------------------------------------
async def generate_text(message_id: str, azure_openai_body: dict):
    """Azure OpenAI API を呼び出し、結果を output_store/{message_id}.json に保存する。"""
    os.makedirs(OUTPUT_STORE, exist_ok=True)
    output_path = Path(OUTPUT_STORE) / f'{message_id_to_filename(message_id)}.json'
    try:
        response = await client.chat.completions.create(**azure_openai_body)
        # 正常終了: レスポンス全体を JSON で保存
        output_path.write_text(
            json.dumps(response.model_dump(), ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
    except APIStatusError as exc:
        # Azure OpenAI API エラー: ステータスコードとエラー本文を保存
        try:
            body = exc.response.json()
        except Exception:
            body = {'error': {'message': str(exc)}}
        try:
            output_path.write_text(
                json.dumps({'azure_response_status': exc.status_code, 'azure_response_body': body},
                           ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
        except Exception:
            pass
    except asyncio.CancelledError:
        # サーバー終了などによるキャンセル: エラー内容を保存後 re-raise
        try:
            output_path.write_text(
                json.dumps({'error': {'message': 'Task cancelled'}}),
                encoding='utf-8'
            )
        except Exception:
            pass
        raise
    except Exception as exc:
        # 予期しないエラー: エラー内容を保存
        try:
            output_path.write_text(
                json.dumps({'error': {'message': str(exc)}}),
                encoding='utf-8'
            )
        except Exception:
            pass


# ----------------------------------------------------------------
# Azure OpenAI API リクエストボディ構築
# ----------------------------------------------------------------
def create_request_body(
    prompt: str,
    model: str = 'gpt-4.1-azure',
    max_completion_tokens: Optional[int] = None,
    reasoning_effort: Optional[str] = None,
    verbosity: Optional[str] = None,
) -> dict:
    """Azure OpenAI API リクエストボディを組み立てる（VBA の CreateRequestBody 相当）。
    prompt はユーザーメッセージ。省略可能パラメータは None の場合ボディに含めない。"""
    body = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
    }
    if max_completion_tokens is not None:
        body['max_completion_tokens'] = int(max_completion_tokens)
    if reasoning_effort is not None:
        body['reasoning_effort'] = reasoning_effort
    if verbosity is not None:
        body['verbosity'] = verbosity
    return body


def build_azure_openai_body(message_id: str, from_addr: str, to_list: list,
                            cc_list: list, subject: str, sent: str, body: str) -> dict:
    """メール各フィールドから Azure OpenAI API リクエストボディを組み立てる。"""
    model = os.getenv('AZURE_OPENAI_MODEL', 'gpt-4.1')
    system_prompt = os.getenv(
        'AZURE_OPENAI_SYSTEM_PROMPT',
        'You are an AI assistant that analyzes business emails.'
    )
    # メール内容をユーザーメッセージとして整形
    email_text = (
        f'MessageID: {message_id}\n'
        f'From: {from_addr}\n'
        f'To: {", ".join(to_list)}\n'
        f'CC: {", ".join(cc_list)}\n'
        f'Subject: {subject}\n'
        f'Sent: {sent}\n\n'
        f'{body}'
    )
    # create_request_body でベースボディを生成し、システムメッセージを先頭に挿入
    request_body = create_request_body(email_text, model)
    request_body['messages'].insert(0, {'role': 'system', 'content': system_prompt})
    return request_body


# ----------------------------------------------------------------
# ファイル処理（メインスレッドで実行）
# ----------------------------------------------------------------
def process_file(file_path: Path, namespace, own_email: str):
    """input_queue の 1 ファイルを読み込み、条件を満たせば API を呼び出す。"""

    # ファイルから EntryID と messageID を取得
    content = file_path.read_text(encoding='utf-8').strip()
    entry_id, message_id = content.split(',', 1)
    entry_id = entry_id.strip()
    message_id = message_id.strip()

    # 読み込み後すぐに削除（再処理防止）
    file_path.unlink()

    # EntryID で Outlook メールを取得
    try:
        mail = namespace.GetItemFromID(entry_id)
    except Exception as e:
        print(f'[ERROR] GetItemFromID failed: {e}')
        return

    # メール各フィールドを取得
    subject = mail.Subject
    sent = str(mail.SentOn)
    body = mail.Body

    # Outlook から internet message-id を取得してファイルの message_id と照合
    # MAPI プロパティ PR_INTERNET_MESSAGE_ID (0x1035001E) で取得する
    try:
        outlook_message_id = mail.PropertyAccessor.GetProperty(
            'http://schemas.microsoft.com/mapi/proptag/0x1035001E'
        ).strip()
    except Exception:
        outlook_message_id = ''
    if outlook_message_id.lower() != message_id.lower():
        msg = (f'[ERROR] message-id mismatch: '
               f'file={message_id!r}, outlook={outlook_message_id!r}, '
               f'subject={subject!r}, sent={sent}')
        print(msg)
        with open('error.txt', 'a', encoding='utf-8') as ef:
            ef.write(msg + '\n')
        return

    # 送信者の SMTP アドレスを取得（Exchange/SMTP 両対応）
    try:
        from_addr = get_smtp_address(mail.Sender)
    except Exception:
        from_addr = mail.SenderEmailAddress

    # 受信者を To / CC に分類して SMTP アドレスを取得（Type: 1=To, 2=CC, 3=BCC）
    to_list = []
    cc_list = []
    for recip in mail.Recipients:
        addr = get_smtp_address(recip.AddressEntry)
        if recip.Type == 1:
            to_list.append(addr)
        elif recip.Type == 2:
            cc_list.append(addr)

    # ----------------------------------------------------------------
    # 条件チェック: いずれか不満の場合は処理を中断
    # ----------------------------------------------------------------
    # 送信者が MitsubishiElectric.co.jp ドメインであること
    if 'mitsubishielectric.co.jp' not in from_addr.lower():
        print(f'[SKIP] From domain not matched: {from_addr}')
        return
    # To に自分自身のアドレスが含まれること
    if own_email not in [a.lower() for a in to_list]:
        print(f'[SKIP] Own address not in To: {own_email}')
        return
    # To の宛先が 8 件以下であること
    if len(to_list) > 8:
        print(f'[SKIP] Too many To recipients: {len(to_list)}')
        return

    azure_openai_body = build_azure_openai_body(
        message_id, from_addr, to_list, cc_list, subject, sent, body
    )

    # バックグラウンドのイベントループに API 呼び出しコルーチンを投入
    asyncio.run_coroutine_threadsafe(generate_text(message_id, azure_openai_body), _loop)
    print(f'[INFO] API call submitted for EntryID: {entry_id}')


# ----------------------------------------------------------------
# メインループ
# ----------------------------------------------------------------
def main():
    # Outlook COM オブジェクトをメインスレッドで初期化（COM スレッドアフィニティのため）
    outlook = win32com.client.Dispatch('Outlook.Application')
    namespace = outlook.GetNamespace('MAPI')
    # カレントユーザーの SMTP アドレスを取得（To 条件チェックに使用）
    own_email = namespace.CurrentUser.AddressEntry.GetExchangeUser().PrimarySmtpAddress.lower()
    print(f'[INFO] Own email: {own_email}')

    os.makedirs(INPUT_QUEUE, exist_ok=True)
    print(f'[INFO] Polling {INPUT_QUEUE}...')

    while True:
        # 1 秒ごとに input_queue を確認し、ファイルが 1 件あれば処理する
        with os.scandir(INPUT_QUEUE) as it:
            for f in it:
                if f.is_file():
                    try:
                        process_file(Path(f.path), namespace, own_email)
                    except Exception as e:
                        print(f'[ERROR] {e}')
                    break  # 1 ループで処理するのは 1 ファイルのみ
        time.sleep(1)


if __name__ == '__main__':
    main()
