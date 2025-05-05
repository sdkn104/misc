import json
from exchangelib import Account, DELEGATE, FileAttachment
from exchangelib.queryset import Q
from datetime import datetime, timedelta
import os

"""
exchangelibを使って指定期間のメールを取得しリストに保存する。
メールは、件名、From, To, Cc, 本文、添付ファイルを取得する。
取得後、リストをJSON形式でファイルに保存する。
exhangelibはwindows環境でSSO認証とする。つまりWindowsのユーザ名とパスワードを使う。
プログラムはrag_exchange_loader.pyという名前とする。
"""

def fetch_emails_from_exchange_sso(start_date, end_date, output_file):
    """指定期間のメールをExchangeサーバーから取得し、リストをJSON形式で保存する (SSO認証)"""
    account = Account(primary_smtp_address=os.getenv('USER_EMAIL'), autodiscover=True, access_type=DELEGATE)

    # 指定期間のメールを取得
    emails = []
    for item in account.inbox.filter(Q(datetime_received__gte=start_date) & Q(datetime_received__lte=end_date)):
        email_data = {
            "subject": item.subject,
            "from": item.sender.email_address if item.sender else "不明",
            "to": [recipient.email_address for recipient in item.to_recipients] if item.to_recipients else [],
            "cc": [recipient.email_address for recipient in item.cc_recipients] if item.cc_recipients else [],
            "body": item.text_body or "",
            "attachments": []
        }

        # 添付ファイルを取得
        for attachment in item.attachments:
            if isinstance(attachment, FileAttachment):
                email_data["attachments"].append(attachment.name)

        emails.append(email_data)

    # リストをJSON形式でファイルに保存
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(emails, f, ensure_ascii=False, indent=4)

def main():
    """メイン処理"""
    # 取得期間を指定
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)  # 過去7日間

    output_file = "emails_output.json"  # 保存先ファイル

    fetch_emails_from_exchange_sso(start_date, end_date, output_file)
    print(f"メールを {output_file} に保存しました。")

if __name__ == "__main__":
    main()