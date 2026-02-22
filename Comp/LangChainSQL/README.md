# MySQL と CSV ローダー (Windows向け)

このリポジトリでは、`store-sales-time-series-forecasting` フォルダ内の CSV ファイルを MySQL に読み込むためのスクリプトを提供します。

**追加されたファイル**
- `load_csvs.py`: CSV を読み、テーブルを作成してデータを挿入する Python スクリプト
- `requirements.txt`: 必要な Python パッケージ
- `config.ini.template`: 接続設定のテンプレート

**準備（Windows）**
1. MySQL Community Server をインストール（公式ダウンロード: https://dev.mysql.com/downloads/mysql/）。
   - インストール時に root パスワードを設定してください。
   - Windows のサービスとして起動するオプションを有効にしてください。
2. MySQL Workbench 等でログインし、データベースとユーザーを作成します（例）:

```sql
CREATE DATABASE store_sales CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER 'csv_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON store_sales.* TO 'csv_user'@'localhost';
FLUSH PRIVILEGES;
```

3. `config.ini.template` をコピーして `config.ini` を作成し、接続情報を編集します:

```
copy config.ini.template config.ini
# その後 editor で user/password/database を編集
```

**Python 環境**
1. リポジトリルートで仮想環境を作成・有効化（PowerShell の例）:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**実行方法**
デフォルトで `store-sales-time-series-forecasting` フォルダを読みます。フォルダ名を変えた場合は `--folder` を指定してください。

```powershell
python load_csvs.py --config config.ini --folder store-sales-time-series-forecasting
```

スクリプトは各 CSV に対してテーブル名を CSV のファイル名（拡張子除く）から作成し、推定したカラム型でテーブルを作成してデータを挿入します。

**注意点**
- カラム名に特殊文字やスペースがある場合は `_` に変換されます。
- 型推定は単純なルールに基づきます。必要に応じて `load_csvs.py` の `dtype_to_sql` を調整してください。
- 大容量データの読み込みではメモリと MySQL の設定に注意してください。

問題があれば `load_csvs.py` と `config.ini` を教えてください。実行を確認する手順も補助します。

**サンプル `config.ini`**

以下はそのまま使えるサンプル `config.ini` の内容例です。実際に使用する場合は `user`、`password`、`database` を環境に合わせて変更してください。ファイル名を `config.ini` として保存します。

```ini
[mysql]
host = 127.0.0.1
port = 3306
user = csv_user
password = strong_password
database = store_sales
charset = utf8mb4
table_prefix =
```

コピー例（PowerShell）:

```powershell
copy config.ini.template config.ini
# そしてエディタで編集するか、上の内容を貼り付けて保存してください。
```
