# ビルド・インストール手順

## 前提条件

- Windows 10 以降
- Python 3.10 以降（PATH に通っていること）
- 旧Outlook（クラシック Outlook）がインストール済み

---

## 手順概要

```
1. ライブラリインストール & exeビルド  →  build.ps1
2. exe をインストール & タスク登録      →  install.bat
```

---

## Step 1: ビルド

PowerShell を開き、このフォルダで実行します。

```powershell
powershell -ExecutionPolicy Bypass -File build.ps1
```

内部で以下を実行します。

1. `pip install pywin32 requests pyinstaller`
2. `pyinstaller --onefile --noconsole outlook_reply_monitor.py`

成功すると `dist\outlook_reply_monitor.exe` が生成されます。

### ビルドエラーが出た場合

| エラー内容 | 対処 |
|---|---|
| `pyinstaller` が見つからない | `pip install pyinstaller` を手動実行 |
| `win32timezone` 関連エラー | `build.ps1` に `--hidden-import win32timezone` が含まれているか確認 |
| `requests` が見つからない | `pip install requests` を手動実行 |

---

## Step 2: インストール

エクスプローラーから `install.bat` をダブルクリック、またはコマンドプロンプトで実行します。

```
install.bat
```

内部で以下を実行します。

1. `dist\outlook_reply_monitor.exe` を `%APPDATA%\OutlookReplyMonitor\` にコピー
2. Windowsタスクスケジューラに「ログオン時に自動起動」タスクを登録
   - 権限: 管理者権限不要（現在のユーザーのタスクとして登録）

実行後に `Start now? (y/n)` と聞かれます。`y` で即時起動します。

---

## アンインストール

```
uninstall.bat
```

タスクスケジューラのタスクを停止・削除し、インストールディレクトリを削除します。

---

## 設定の変更

`outlook_reply_monitor.py` の先頭部分を編集してから **ビルドしなおし、再インストール** してください。

```python
PLACEHOLDER_TEXT  = "AIによる回答作成中..."   # 処理中に表示するテキスト
MONITOR_DURATION  = 10                        # 重要度「低」を待つ秒数
HTTP_URL          = "http://localhost:8000/generate"  # AIサーバーのURL
HTTP_TIMEOUT      = 60                        # HTTPタイムアウト秒数
```

---

## ログファイル

exe として動作中の出力は以下に保存されます（起動ごとに上書き）。

```
%APPDATA%\OutlookReplyMonitor\monitor.log
```

動作確認やエラー調査の際はこのファイルを参照してください。

開発時（`python outlook_reply_monitor.py` で実行）はコンソールに直接出力されます。
