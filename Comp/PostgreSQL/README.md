# Postgre HTTP extension
- https://github.com/pramsey/pgsql-http
- https://www.postgresonline.com/journal/archives/371-http-extension.html
- build extension for windows: 
   - https://wiki.postgresql.org/wiki/Building_and_Installing_PostgreSQL_Extension_Modules
   - https://www.postgresql.jp/document/16/html/extend-pgxs.html
   - https://qiita.com/yaju/items/428eaf2920e92198d150
   - 

## 1. PostgreSQL のインストール

1. PostgreSQL for Windows をダウンロード

   * PostgreSQL公式: [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
   * Windows向けインストーラは通常 EnterpriseDB のものを利用
   * Version 16 Windows x86-64

2. インストーラ実行

   * PostgreSQL Server
   * pgAdmin
   * Command Line Tools
     を含めてインストール
   *  Stack Builder は不要

3. セットアップ時に以下を設定

   * ポート: `5432`
   * 管理者ユーザー: `postgres`
   * パスワード: 任意

---

## 2. PostgreSQL の初期セットアップ

1. psql で接続

   START -> PostgreSQL -> SQL Shell(psql)
   - setting default
   - user postgres, password set abobe

2. テスト用DB作成

   ```sql
   CREATE DATABASE testdb;
   ```

3. testdb に接続

   START -> PostgreSQL -> SQL Shell(psql)
   - server: localhost
   - database: testdb
   - port: 5432
   - user postgres
   - client encoding: SJIS
   - passowrd: set at instlation

---

## 3. pgsql-http のインストール

### 手順

1. pgsql-httpバイナリ取得

- https://www.postgresonline.com/journal/archives/371-http-extension.html
   - PostgreSQL 16 w64 http (zip) 7z version

2 copy from `pg16http_w64`  to `D:\Program Files\PostgreSQL\16`
   - copy lib\http.dll to lib\http.dll
   - copy share\extention\* to share\extention\
   - copy bin\*.dll to bin\

* for each the copied file, set セキュリティ許可 in property panel
   
---

## 4. pgsql-http の有効化

- ref: pg16http_w64\README

1. testdb に接続

2. Extension 作成

   ```sql
   CREATE EXTENSION http;
   ```

3. 確認

   ```sql
   \dx
   ```

   `http` が表示されればOK。

---

## 5. PostgreSQL 上で HTTP POST を試す

```sql
--- libcurlのcert設定
SELECT http_set_curlopt('CURLOPT_CAINFO', 'D:\Program Files\PostgreSQL\16\ssl\certs\ca-bundle.crt');
```

```sql
--- URL encode
SELECT urlencode('my special string''s & things?');
--- GET
select * FROM http_get('http://httpbun.com/ip');
--- POST
SELECT content
FROM http_post(
    'https://httpbin.org/post',
    '{"name":"test"}',
    'application/json'
);
```

レスポンスの status が `200` なら成功です。


---

## 6. Python クライアント作成

### 必要ライブラリ

```powershell
pip install psycopg2-binary
```

### サンプルコード

```python
import psycopg2

print("db password: ")
pw = input()
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="testdb",
    user="postgres",
    password=pw
)

cur = conn.cursor()

sql = """
SELECT status, content
FROM http_post(
    'https://httpbin.org/post',
    '{"client":"python","message":"hello from pgsql-http"}',
    'application/json'
);
"""

cur.execute(sql)
result = cur.fetchone()

print("HTTP Status:", result[0])
print("Response:")
print(result[1])

cur.close()
conn.close()
```

---

## 7. 実行

```powershell
python client.py
```

期待結果:

```text
HTTP Status: 200
Response:
...
```

---

## 8. よくあるエラー

* `could not load library "http"`

  * DLL の配置先が誤っている
  * libcurl 関連 DLL が不足

* `CREATE EXTENSION http;` で失敗

  * `http.control` や SQL ファイルが `share/extension` に存在しない

* HTTPS 接続失敗

  * curl/openssl DLL が不足
  * プロキシや社内FWでブロックされている

* Python接続失敗

  * PostgreSQLサービスが起動していない
  * パスワード誤り
  * `pg_hba.conf` の認証設定不足
