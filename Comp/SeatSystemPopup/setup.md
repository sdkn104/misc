# セットアップ手順書

## 1. 前提条件
- Windows 11 PC
- Python 3.x インストール済み

## 2. 仮想環境の作成（推奨）
1. コマンドプロンプトまたはPowerShellで作業ディレクトリに移動
2. 仮想環境作成:
   ```powershell
   python -m venv myenv
   .\myenv\Scripts\Activate.ps1
   ```

## 3. 必要なパッケージのインストール
```powershell
pip install pandas win11toast
```

## 4. プログラムの配置
- `seatSystemPopup.py` を任意のディレクトリに配置

## 5. タスクスケジューラへの登録例
1. Windowsの「タスクスケジューラ」を開く
2. 「タスクの作成」→「操作」タブで
   - プログラム/スクリプト: `python`
   - 引数の追加: `seatSystemPopup.py`
   - 開始（作業）フォルダー: スクリプトのあるディレクトリ
3. 「トリガー」タブで15分ごとに実行するよう設定

## 6. 動作確認
- タスクを手動実行し、警告トーストが表示されることを確認

## 7. exe化（任意）
- `pyinstaller`でexe化する場合:
```powershell
pip install pyinstaller
pyinstaller --onefile seatSystemPopup.py
```
- `dist`フォルダ内のexeをタスクスケジューラに登録
