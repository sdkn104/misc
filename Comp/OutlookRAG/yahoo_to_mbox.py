import imaplib
import email
import os
from email.policy import default
import base64

def save_to_mbox(messages, folder='mail'):
    """メールを個別のテキストファイルと添付ファイルに保存する"""
    if not os.path.exists(folder):
        os.makedirs(folder)

    for idx, message in enumerate(messages):
        print(message)
        email_folder = os.path.join(folder, f"email_{idx+1}")
        os.makedirs(email_folder, exist_ok=True)

        # 保存するメールのテキストファイル
        email_file_path = os.path.join(email_folder, "email.txt")
        with open(email_file_path, 'w', encoding='utf-8') as email_file:
            email_file.write(message)

        # 添付ファイルの処理
        msg = email.message_from_string(message)
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename:
                filepath = os.path.join(email_folder, filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))

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

        for email_id in email_ids[:1000]:
            status, msg_data = imap.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1], policy=default)

                    # 本文のデコード処理
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                charset = part.get_content_charset() or "utf-8"
                                body = part.get_payload(decode=True).decode(charset, errors="replace")
                                break
                    else:
                        charset = msg.get_content_charset() or "utf-8"
                        body = msg.get_payload(decode=True).decode(charset, errors="replace")

                    # メール本文を保存
                    email_data.append(body)

        return email_data

    finally:
        imap.logout()

def main():
    """メイン処理"""
    username = "sdkn104@yahoo.co.jp" #input("Yahooメールのメールアドレスを入力してください: ")
    password = "Karatani3" #input("アプリパスワードを入力してください: ")

    emails = fetch_yahoo_emails(username, password)
    save_to_mbox(emails)

if __name__ == '__main__':
    main()