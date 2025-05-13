import imaplib
import email
import json
from email.policy import default

"""
pythonでyahooメールから100件のメールを取得してJSON形式でファイルに保存する。read_yahoo.pyファイルにコードを生成する
"""
def fetch_yahoo_emails(username, password):
    """Yahoo Mailからメールを取得する"""
    imap_host = 'imap.mail.yahoo.co.jp'
    imap = imaplib.IMAP4_SSL(imap_host)

    try:
        imap.login(username, password)
        imap.select('inbox')

        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()
        email_data = []

        for email_id in email_ids[:100]:
            status, msg_data = imap.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1], policy=default)

                    # メールの詳細を抽出
                    email_details = {
                        "subject": msg["subject"],
                        "from": msg["from"],
                        "to": msg["to"],
                        "cc": msg["cc"],
                        "date": msg["date"],
                        "message-id": msg["message-id"],
                        "body": ""
                    }

                    # 本文のデコード処理
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                charset = part.get_content_charset() or "utf-8"
                                email_details["body"] = part.get_payload(decode=True).decode(charset, errors="replace")
                                break
                    else:
                        charset = msg.get_content_charset() or "utf-8"
                        email_details["body"] = msg.get_payload(decode=True).decode(charset, errors="replace")

                    email_data.append(email_details)

        return email_data

    finally:
        imap.logout()

def save_emails_to_json(emails, filename="emails.json"):
    """メールをJSON形式で保存する"""
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(emails, json_file, ensure_ascii=False, indent=4)

def main():
    """メイン処理"""
    username = "sdkn104@yahoo.co.jp"  # Yahooメールのメールアドレス
    password = ""  # アプリパスワード

    emails = fetch_yahoo_emails(username, password)
    save_emails_to_json(emails)

if __name__ == '__main__':
    main()