# AuthServer - API使用例

このファイルは、AuthServer APIの使用例を示します。

## 1. Difyアプリフロントエンドへのアクセス

### ブラウザでアクセス

```
https://authserver.example.com/difyApp/chatbot/KtFo2mI15fIkZ7lr
```

自動的にWindows認証が実行され、以下のHTMLが返されます：
- Difyアプリをiframeで埋め込んだWebページ
- ユーザー名がログに記録される

### 異なるDifyアプリへのアクセス

```
https://authserver.example.com/difyApp/workflow/abc123def456
https://authserver.example.com/difyApp/text-generation/xyz789
```

パスの部分がDifyアプリのパスとなり、自動的にDifyベースURLと結合されます。

---

## 2. ログ記録API - GET版

### コマンドラインでの実行（curl）

```bash
# Windows認証でログを記録
curl -v --negotiate -u DOMAIN\username:password \
  "https://authserver.example.com/api/log/batch-process?message=データ同期開始"

# 出力
# HTTP/1.1 200 OK
# {"status":"success","message":"Log recorded successfully"}
```

### PowerShellでの実行

```powershell
# Windows認証を使用してAPIを呼び出し
$params = @{
    Uri = "https://authserver.example.com/api/log/batch-process?message=データ同期開始"
    Method = "GET"
    UseDefaultCredentials = $true
    ContentType = "application/json"
}

$response = Invoke-WebRequest @params
Write-Host $response.Content

# 出力
# {"status":"success","message":"Log recorded successfully"}
```

### Pythonでの実行

```python
import requests
from requests_ntlm import HttpNtlmAuth
import json

url = "https://authserver.example.com/api/log/batch-process"
params = {"message": "Python処理完了"}

# Windows認証でリクエスト
response = requests.get(
    url,
    params=params,
    auth=HttpNtlmAuth('DOMAIN\\username', 'password'),
    verify=False  # 自己署名証明書の場合
)

result = response.json()
print(result)
# {'status': 'success', 'message': 'Log recorded successfully'}
```

---

## 3. ログ記録API - POST版（JSON）

### PowerShellでの実行

```powershell
# POSTリクエストでより詳細なログを送信
$body = @{
    message = "バッチ処理完了"
    metadata = "処理対象: 10000件, 処理時間: 125秒, エラー: 0件"
} | ConvertTo-Json

$params = @{
    Uri = "https://authserver.example.com/api/log/batch-process"
    Method = "POST"
    Body = $body
    UseDefaultCredentials = $true
    ContentType = "application/json"
}

$response = Invoke-WebRequest @params
Write-Host $response.Content

# 出力
# {"status":"success","message":"Log recorded successfully"}
```

### Pythonでの実行

```python
import requests
from requests_ntlm import HttpNtlmAuth
import json

url = "https://authserver.example.com/api/log/batch-process"

payload = {
    "message": "バッチ処理完了",
    "metadata": "処理対象: 10000件, 処理時間: 125秒, エラー: 0件"
}

response = requests.post(
    url,
    json=payload,
    auth=HttpNtlmAuth('DOMAIN\\username', 'password'),
    verify=False
)

result = response.json()
print(result)
# {'status': 'success', 'message': 'Log recorded successfully'}
```

### Bashでの実行（curl）

```bash
# JSONボディでPOSTリクエスト
curl -X POST \
  --negotiate -u DOMAIN\username:password \
  -H "Content-Type: application/json" \
  -d '{
    "message": "バッチ処理完了",
    "metadata": "処理対象: 10000件"
  }' \
  https://authserver.example.com/api/log/batch-process
```

---

## 4. VBScriptでの実行例

```vbscript
' Windows認証でAPIを呼び出し
Set objHTTP = CreateObject("MSXML2.XMLHTTP.6.0")
Dim strURL, strMessage

strURL = "https://authserver.example.com/api/log/vbscript-test?message=VBScriptからのログ"

' Windows認証を有効化
objHTTP.SetOption 2, 13056  ' SXH_SERVER_CERT_IGNORE_ALL_SERVER_ERRORS

With objHTTP
    .Open "GET", strURL, False
    .SetRequestHeader "Authorization", "Negotiate"
    .SetCredentials "DOMAIN\username", "password", 1
    .Send
    
    If .Status = 200 Then
        WScript.Echo "ログ記録成功: " & .ResponseText
    Else
        WScript.Echo "エラー: " & .Status & " " & .StatusText
    End If
End With
```

---

## 5. C#での実行例

```csharp
using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json;

class AuthServerClient
{
    static async Task Main()
    {
        var baseAddress = "https://authserver.example.com";
        
        // Windows認証を使用するHttpClientHandler
        var handler = new HttpClientHandler
        {
            Credentials = new NetworkCredential("username", "password", "DOMAIN"),
            UseDefaultCredentials = true
        };
        
        using (var client = new HttpClient(handler))
        {
            client.BaseAddress = new Uri(baseAddress);
            
            // GET リクエスト例
            try
            {
                var response = await client.GetAsync("/api/log/csharp-test?message=CSharpからのログ");
                if (response.IsSuccessStatusCode)
                {
                    string content = await response.Content.ReadAsStringAsync();
                    Console.WriteLine("成功: " + content);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("エラー: " + ex.Message);
            }
            
            // POST リクエスト例
            try
            {
                var logData = new
                {
                    message = "C#からのバッチ処理ログ",
                    metadata = "処理件数: 5000"
                };
                
                var json = JsonConvert.SerializeObject(logData);
                var content = new StringContent(json, System.Text.Encoding.UTF8, "application/json");
                
                var response = await client.PostAsync("/api/log/csharp-batch", content);
                if (response.IsSuccessStatusCode)
                {
                    string responseContent = await response.Content.ReadAsStringAsync();
                    Console.WriteLine("成功: " + responseContent);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("エラー: " + ex.Message);
            }
        }
    }
}
```

---

## 6. Node.js での実行例

```javascript
const http = require('http');
const https = require('https');

// Windows認証をサポートするライブラリをインストール
// npm install axios ntlm-client

const axios = require('axios');
const { NTLM } = require('ntlm-client');

async function callAuthServer() {
    const domain = 'DOMAIN';
    const username = 'username';
    const password = 'password';
    const workstation = '';
    
    const ntlm = new NTLM({ domain, username, password, workstation });
    
    try {
        // GET リクエスト
        const getResponse = await ntlm.request({
            method: 'GET',
            url: 'https://authserver.example.com/api/log/nodejs-test?message=Node.jsからのログ'
        });
        
        console.log('GET Success:', getResponse.body);
        
        // POST リクエスト
        const postResponse = await ntlm.request({
            method: 'POST',
            url: 'https://authserver.example.com/api/log/nodejs-batch',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: 'Node.jsからのバッチ処理',
                metadata: '処理件数: 3000'
            })
        });
        
        console.log('POST Success:', postResponse.body);
    } catch (error) {
        console.error('エラー:', error.message);
    }
}

callAuthServer();
```

---

## 7. ログファイルの確認

### PowerShellでログを検索

```powershell
# 最新のログファイルを表示
$logPath = "C:\inetpub\wwwroot\authserver\logs"
Get-ChildItem $logPath -Filter "access-*.txt" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | Get-Content | Select-Object -Last 20

# 特定のユーザーのログを検索
Get-Content "$logPath\access-*.txt" | Select-String "DOMAIN\\username"

# 特定の日付範囲のログを検索
Get-ChildItem $logPath -Filter "access-*.txt" | Where-Object { $_.LastWriteTime -ge (Get-Date).AddDays(-7) }

# ステータスコード別にログをカウント
Get-Content "$logPath\access-*.txt" | Select-String "Status:(\d+)" -AllMatches | ForEach-Object { $_.Matches.Groups[1].Value } | Group-Object | Sort-Object -Descending Count
```

### ログファイルの例

```
2024-12-26 14:30:45 [INF] User:DOMAIN\john.doe | URL:/difyApp/chatbot/KtFo2mI15fIkZ7lr | Status:200 | IP:192.168.1.100 |
2024-12-26 14:31:12 [INF] User:DOMAIN\jane.smith | URL:/api/log/batch-process?message=started | Status:200 | IP:192.168.1.101 |
2024-12-26 14:31:45 [INF] LogName:DataSync | Message:10000 records processed | Metadata: | User:DOMAIN\system | IP:10.0.0.5 |
```

---

## 8. エラーハンドリング

### Windows認証に失敗した場合

```powershell
# エラー例：401 Unauthorized
HTTP Error 401.1 - Unauthorized

# 対応
1. ドメイン環境か確認
2. ユーザー名とパスワードを確認
3. ドメイン形式が DOMAIN\username であることを確認
```

### HTTPS証明書エラーの場合

```powershell
# エラー例：SSL/TLS certificate error
The underlying connection was closed: Could not establish trust relationship for the SSL/TLS secure channel.

# 対応（開発環境のみ）
$body = @{
    message = "テスト"
} | ConvertTo-Json

# 証明書検証を無効化（開発時のみ）
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

Invoke-WebRequest -Uri "https://authserver.example.com/api/log/test" `
    -Method GET `
    -UseDefaultCredentials
```

### CORS エラーの場合

```
Access to XMLHttpRequest at 'https://authserver.example.com/api/log/test' 
from origin 'https://other-site.com' has been blocked by CORS policy
```

**対応**: `appsettings.json` の `AllowedOrigins` に該当するオリジンを追加

```json
{
  "Cors": {
    "AllowedOrigins": [
      "https://other-site.com"
    ]
  }
}
```

---

## 9. パフォーマンスチューニング

### バルク処理の場合

複数のログエントリを一度に送信する代わりに、バッチ処理を推奨：

```powershell
# ❌ 非効率: 1000回のAPI呼び出し
for ($i = 1; $i -le 1000; $i++) {
    Invoke-WebRequest -Uri "https://authserver.example.com/api/log/item?message=Item$i" `
        -UseDefaultCredentials
}

# ✅ 効率的: 1回のAPI呼び出し
$body = @{
    message = "バッチ処理完了"
    metadata = "処理済み件数: 1000"
} | ConvertTo-Json

Invoke-WebRequest -Uri "https://authserver.example.com/api/log/batch" `
    -Method POST `
    -Body $body `
    -ContentType "application/json" `
    -UseDefaultCredentials
```

---

## 10. セキュリティベストプラクティス

```powershell
# ❌ パスワードをスクリプトに埋め込まない
$response = Invoke-WebRequest -Uri "..." -Credential (New-Object PSCredential "DOMAIN\user", "password123")

# ✅ 資格情報を安全に取得
$cred = Get-Credential
$response = Invoke-WebRequest -Uri "..." -Credential $cred

# ✅ または Windows認証を使用
$response = Invoke-WebRequest -Uri "..." -UseDefaultCredentials
```
