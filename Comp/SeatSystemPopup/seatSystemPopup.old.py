import os
import csv
import time
from datetime import datetime
from win10toast_click import ToastNotifier
import webbrowser

# 設定
CSV_PATH = r"C:\scan\座席管理システム\user.csv"
SEAT_SYSTEM_URL = "http://www.google.com"
TOAST_TITLE = "★座席管理システム"
TOAST_MSG = "状態が「退社」となっています。登録をお願いします。"
CHECK_MINUTES = 15

def get_login_user():
    try:
        return os.getlogin()
    except Exception:
        import getpass
        return getpass.getuser()

def is_csv_recent(path, minutes):
    try:
        mtime = os.path.getmtime(path)
        now = time.time()
        return (now - mtime) < (minutes * 60)
    except Exception:
        return False

def get_user_status(path, login_user):
    try:
        with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['UserID'].startswith(login_user):
                    return row['Status']
    except Exception:
        pass
    return None

def show_toast():
    def open_url():
        webbrowser.open(SEAT_SYSTEM_URL)
    toaster = ToastNotifier()
    toaster.show_toast(
        TOAST_TITLE,
        TOAST_MSG,
        duration=10,
        threaded=True,
        callback_on_click=open_url
    )

def main():
    login_user = get_login_user()
    if not is_csv_recent(CSV_PATH, CHECK_MINUTES):
        return
    status = get_user_status(CSV_PATH, login_user)
    if status == '退社':
        show_toast()

if __name__ == "__main__":
    main()
