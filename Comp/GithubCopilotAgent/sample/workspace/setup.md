# オンラインPDF販売ECサイト セットアップ手順

## 1. 前提条件
- Windows 10/11
- Python 3.8以降
- MySQL 8.0以降

---

## 2. MySQLのインストール
1. 公式サイトからMySQL Community Serverをダウンロード
   - https://dev.mysql.com/downloads/mysql/
2. インストーラの指示に従いインストール
3. セットアップ中にrootパスワードを設定
4. MySQL Workbenchも同時にインストール推奨

### MySQL初期設定例
```sql
CREATE DATABASE pdf_ec DEFAULT CHARACTER SET utf8mb4;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON pdf_ec.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
```

---

## 3. Python仮想環境の作成・有効化
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

## 4. 必要パッケージのインストール
```powershell
pip install -r requirements.txt
```

---

## 5. .envファイルの作成
- `.env.example` をコピーし `.env` にリネーム
- `SECRET_KEY` と `DATABASE_URL` を編集
  - 例: `DATABASE_URL=mysql://user:password@localhost/pdf_ec`

---

## 6. データベース初期化
```powershell
.\.venv\Scripts\Activate.ps1
python
>>> from app import app, db
>>> with app.app_context():
>>>         db.create_all()
>>> exit()
```

---

## 7. サーバ起動
```powershell
.\.venv\Scripts\Activate.ps1
flask run
```
または VSCode のタスク「Run Flask App」を実行

---

## 8. PDFファイルの配置
- `static/pdfs/` フォルダを作成し、販売するPDFファイルを配置
- 商品情報（Productテーブル）にファイル名を登録

---

## 9. 補足
- 管理者による商品登録はDB直接操作または管理画面で行ってください
- MySQLのパスワードやDB名は適宜変更してください

---

## 10. トラブルシューティング
- MySQL接続エラー時はユーザー名・パスワード・DB名・権限を再確認
- ポート競合時は `app.py` の `run()` 引数でポート指定可能

---

## 11. 参考
- MySQL公式: https://dev.mysql.com/doc/
- Flask公式: https://flask.palletsprojects.com/
