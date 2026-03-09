
# 概要

以下は **IISでWindows統合認証を行い、Pythonアプリにユーザー名を渡す最も実用的な構成**です。
（**IISが認証 → Pythonはアプリ処理のみ**）

構成：

```
Browser (社内ユーザー)
      ↓ Windows統合認証
IIS
      ↓ Reverse Proxy
ARR
      ↓ HTTP
Python server (uvicorn / waitress)
      ↓
Python Web App (Flask / FastAPI)
```

使用する主要コンポーネント

* Microsoft Internet Information Services
* Application Request Routing
* Flask（例）

---

# 1 IISをインストール

**Control Panel** for Windows 10/11

```
Programs
Windows機能の有効・無効
↓
IISにチェックを入れる
以下の「追加する機能」にチェックを入れる
OKを押す
```

**Server Manager** for Windows server

```
Programs
Add Roles and Features
↓
Web Server (IIS)
・・・
```

追加する機能

```
Web Server
 ├ Security
 │   └ Windows Authentication
 └ Application Development
     └ WebSocket (任意)
```

重要
**Windows Authentication を有効にする**

---

# 2 ARRをインストール

https://learn.microsoft.com/ja-jp/iis/extensions/configuring-application-request-routing-arr/creating-a-forward-proxy-using-application-request-routing

公式モジュール

Application Request Routing
https://www.microsoft.com/en-us/download/details.aspx?id=47333

インストールすると

```
URL Rewrite
ARR
```

がIISに追加されます。

URL Rewriteを別途インストールする必要ある場合あり。
以下からインストール。
https://learn.microsoft.com/ja-jp/iis/extensions/url-rewrite-module/using-the-url-rewrite-module
https://prod-iis-landing.azurewebsites.net/downloads/microsoft/url-rewrite

---

# 3 Pythonアプリ作成

例：Flask

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    user = request.headers.get("X-Auth-User")
    return f"Hello {user}"

if __name__ == "__main__":
    app.run(port=8000)
```

起動

```
python test.py
```

アクセステスト

```
http://localhost:8000
```

---

# 4 IISサイト作成

IIS Manager

```
Sites
↓
Add Website
```

例

```
Site name : AuthProxy
Port : 8080
Physical path : C:\inetpub\AuthProxy
```

フォルダは空でOKです。

---

# 5 Windows認証設定

IIS Manager

```
Site
↓
AuthProxy
↓
Authentication
```

設定

| 設定                       | 値       |
| ------------------------ | ------- |
| Anonymous Authentication | Disable |
| Windows Authentication   | Enable  |

これで

**ブラウザのWindowsログインが自動認証されます**

---

# 6 ARR Reverse Proxy設定

IIS Manager

```
Server
↓
Application Request Routing Cache
↓
Server Proxy Settings
```

有効化

```
Enable proxy ✔
```

---

# 7 URL Rewrite設定

IIS Manager

```
Site
↓
AuthProxy
↓
URL Rewrite
↓
Add Rule
↓
Reverse Proxy
```

「URLの書き換え」

```
localhost:8000  # http://はいらない。重複してしまう。
```

「サーバ変数」

```
変数名：HTTP_X_AUTH_USER
値：{REMOTE_USER}
```

site -> AuthProxy -> URL Rewrite　-> View Server Variables -> Add

```
HTTP_X_AUTH_USER
```


すると自動でルールが生成されます。

例

```xml
<rule name="ReverseProxyInboundRule1">
 <match url="(.*)" />
 <action type="Rewrite" url="http://localhost:8000/{R:1}" />
</rule>
```

---

# 8 テスト

以下を開くとユーザ名が表示されます。

http://localhost:8080

---

IISはユーザー名を

```
{REMOTE_USER}
```

として保持しています。

URL Rewriteの **Server Variables** を追加します。

```
HTTP_X_AUTH_USER
```

値

```
{REMOTE_USER}
```

結果

```
X-Auth-User: DOMAIN\username
```

がPythonに送られます。

---

Pythonでユーザー取得

```python
user = request.headers.get("X-Auth-User")
```

結果

```
COMPANY\tanaka
```

---

# 動作フロー

```
Windowsログイン
      ↓
ブラウザアクセス
      ↓
IIS Windows認証
      ↓
ARR Reverse Proxy
      ↓
Pythonアプリ
```

ログイン画面は出ません。

---

# 企業システムの典型構成

実際の社内システムはこうなります

```
Browser
↓
Load Balancer
↓
IIS (Windows Auth)
↓
ARR Reverse Proxy
↓
Uvicorn / Waitress
↓
Python App
↓
Database
```

---

# PythonサーバはWaitressが安定

Flaskの場合

```
pip install waitress
```

起動

```python
from waitress import serve
serve(app, host="0.0.0.0", port=8000)
```

Waitressは

* Windows向け
* 本番運用OK

---

# よくあるトラブル

### アクセス権でエラー

logsフォルダに編集権を追加
　　IIS IUSERS など

### useKernelMode = false設定がいるか。


### localhostで認証されない

Windows認証は

```
http://localhost
```

だと失敗することがあります。

推奨

```
http://hostname
```

---
