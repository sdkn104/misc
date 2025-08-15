# オンラインPDF販売ECサイト 環境構築・設定手順（Windows版）

## 1. Python仮想環境の作成・有効化

```sh
python -m venv myenv
myenv\Scripts\activate
```

## 2. 必要パッケージのインストール

```sh
pip install -r requirements.txt
```

## 3. MySQLのインストール

- 公式サイト（https://dev.mysql.com/downloads/installer/）からMySQL Installerをダウンロード・インストール
- インストール時に「MySQL Server」「MySQL Workbench」などを選択

## 4. MySQLサーバーの起動・初期設定

- MySQL Workbenchまたはコマンドラインでrootユーザーでログイン

## 5. データベース・ユーザー作成

```sql
CREATE DATABASE pdf_ec_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON pdf_ec_db.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
```

## 6. config.pyの設定確認

- `config.py` の `SQLALCHEMY_DATABASE_URI` が以下のようになっていることを確認
  ```
  SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/pdf_ec_db'
  ```

## 7. テーブル作成（初回のみ）

Pythonシェルまたはスクリプトで以下を実行：

```python
from run import app
from app import db

with app.app_context():
    db.create_all()
```

または、以下の内容で `init_db.py` を作成して実行：

```python
from run import app
from app import db

with app.app_context():
    db.create_all()
```

```sh
python init_db.py
```

## 8. サンプル商品データ・画像・PDFの投入（任意）

- `app/static/images/` に商品画像ファイル（例: book1.jpg）を保存
- `app/static/pdf/` にPDFファイル（例: book1.pdf）を保存
- `app/models.py` のProductモデルの `cover_image` に `static/images/book1.jpg`、`pdf_file` に `static/pdf/book1.pdf` などのパスを登録

## 9. アプリの起動

```sh
python run.py
```

- ブラウザで `http://localhost:8888/` にアクセス
- 画面が表示されれば成功

---

## 補足

- MySQLのrootパスワードやユーザー名・パスワードは適宜変更してください
- ポート番号やDB名も必要に応じて変更可能です
- テーブル作成後、管理画面やSQLで商品データを追加してください

---

この手順通りに操作すれば、ECサイトの画面が動作します。
