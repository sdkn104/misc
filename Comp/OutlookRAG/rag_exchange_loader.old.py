from exchangelib import Credentials, Account, DELEGATE
from exchangelib.folders import Inbox
from exchangelib.queryset import Q
from datetime import datetime, timedelta

"""
exchangelibを使って指定期間のメールを取得しリストに保存する。
メールは、件名、From, To, Cc, 本文、添付ファイルを取得する。
取得後、リストをファイルに保存する。exhangelibはwindows環境でSSO認証とする。
プログラムはrag_exchange_loader.pyという名前とする。
"""

def fetch_emails_from_exchange(username, password, start_date, end_date):
    """指定期間のメールをExchangeサーバーから取得する"""
    credentials = Credentials(username, password)
    account = Account(username, credentials=credentials, autodiscover=True, access_type=DELEGATE)

    # 指定期間のメールを取得
    emails = []
    for item in account.inbox.filter(Q(datetime_received__gte=start_date) & Q(datetime_received__lte=end_date)):
        emails.append({
            "subject": item.subject,
            "sender": item.sender.email_address if item.sender else "不明",
            "date": item.datetime_received,
            "body": item.text_body or ""
        })

    return emails

def main():
    """メイン処理"""
    username = "your_email@example.com"  # Exchangeメールアドレス
    password = "your_password"  # パスワード

    # 取得期間を指定
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)  # 過去7日間

    emails = fetch_emails_from_exchange(username, password, start_date, end_date)

    # メールをリストに保存
    for email in emails:
        print(f"Subject: {email['subject']}")
        print(f"Sender: {email['sender']}")
        print(f"Date: {email['date']}")
        print(f"Body: {email['body'][:100]}...")  # 本文の最初の100文字を表示
        print("-" * 50)

if __name__ == "__main__":
    main()