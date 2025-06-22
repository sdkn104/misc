# セットアップ手順書

## 1. 前提条件
- Windows 11 PC
- Python 3.x がインストールされていること
- ユーザテーブルCSVファイルが `C:\scan\座席管理システム\user.csv` に存在すること

## 2. 必要なPythonパッケージのインストール
コマンドプロンプトまたはPowerShellで以下を実行してください。

```
pip install win10toast-click
```

## 3. プログラムの配置
- `seatSystemPopup.py` を任意のフォルダ（例: `C:\Users\<ユーザ名>\AppData\Local\Programs\SeatSystemPopup\` など）に配置します。

## 4. タスクスケジューラの設定
1. Windowsの「タスクスケジューラ」を開く
2. 「タスクの作成」から新規タスクを作成
3. 「トリガー」タブで「15分ごと」など定期実行を設定
4. 「操作」タブで「プログラムの開始」→
   - プログラム/スクリプト: `python`
   - 引数の追加: `"<seatSystemPopup.pyのフルパス>"`
5. 「条件」「設定」タブは必要に応じて調整

## 5. EXE化（任意）
PyInstallerでexe化する場合、以下を実行してください。

```
pip install pyinstaller
pyinstaller --onefile seatSystemPopup.py
```
- 生成された `dist/seatSystemPopup.exe` をタスクスケジューラで実行するように設定できます。

## 6. 注意事項
- CSVファイルのパスや座席管理システムのURLは要件定義通りに設定してください。
- 通知が表示されない場合は、Windowsの通知設定を確認してください。
