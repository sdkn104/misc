
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
Web Server (IIS)
```

**Server Manager** for Windows server

```
Programs
Add Roles and Features
↓
Web Server (IIS)
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

公式モジュール

Application Request Routing

インストールすると

```
URL Rewrite
ARR
```

がIISに追加されます。

---

# 3 Pythonアプリ作成

例：Flask

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    user = request.headers.get("X-Forwarded-User")
    return f"Hello {user}"

if __name__ == "__main__":
    app.run(port=8000)
```

起動

```
python app.py
```

アクセス

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
Site name : python_app
Port : 80
Physical path : C:\inetpub\python_app
```

フォルダは空でOKです。

---

# 5 Windows認証設定

IIS Manager

```
Site
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

サイトの

```
URL Rewrite
↓
Add Rule
↓
Reverse Proxy
```

設定

```
http://localhost:8000
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

# 8 WindowsユーザーをPythonに渡す

IISはユーザー名を

```
{REMOTE_USER}
```

として保持しています。

URL Rewriteの **Server Variables** を追加します。

```
HTTP_X_FORWARDED_USER
```

値

```
{REMOTE_USER}
```

結果

```
X-Forwarded-User: DOMAIN\username
```

がPythonに送られます。

---

# 9 Pythonでユーザー取得

```python
user = request.headers.get("X-Forwarded-User")
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

### Chromeで自動ログインしない

ブラウザ設定

```
AuthServerAllowlist
```

例

```
*.company.local
```

---

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
