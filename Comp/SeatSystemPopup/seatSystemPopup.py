import os
import sys
import pandas as pd
import datetime
from win11toast import toast

# 設定
CSV_PATH = r"\\meias92c\scan\座席管理システム\T_USER.csv"
SEAT_SYSTEM_URL = "https://apps.powerapps.com/play/e/default-c5a75b62-4bff-4c96-a720-6621ce9978e5/a/e75a1fdf-505f-43a1-a57d-634127ca95c4?tenantId=c5a75b62-4bff-4c96-a720-6621ce9978e5&sourcetime=1715316486500&screen=ScrnE11ALL"
TOAST_TITLE = "★座席管理システム★"
TOAST_MSG = "「退社」状態になっています。登録をお願いします。"

# 1. ログインユーザ名取得
try:
    login_user = os.getlogin()
except Exception:
    login_user = os.environ.get("USERNAME", "")
if not login_user:
    sys.exit(0)

# 2. CSVファイルの最終アクセス日時確認
try:
    last_access = datetime.datetime.fromtimestamp(os.path.getatime(CSV_PATH))
except Exception:
    sys.exit(0)
if (datetime.datetime.now() - last_access).total_seconds() > 1800:
    sys.exit(0)

# 3. CSV読み込み
try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
except Exception:
    sys.exit(0)
if "UserID" not in df.columns or "WorkStatus" not in df.columns:
    sys.exit(0)

# 4. ログインユーザで前方一致
user_rows = df[df["UserID"].astype(str).str.startswith(login_user)]
if user_rows.empty:
    sys.exit(0)

# 5. WorkStatus判定
status = user_rows.iloc[0]["WorkStatus"]
if str(status) != "退社":
    sys.exit(0)

# 6. トースト警告
try:
    toast(
        TOAST_TITLE,
        TOAST_MSG,
        button={
            'activationType': 'protocol',
            'arguments': SEAT_SYSTEM_URL, 
            'content': '座席管理システムを開く'
        },
        duration="long",
        scenario="urgent"
    )
except Exception:
    pass
