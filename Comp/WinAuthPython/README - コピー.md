# AuthServer

Windows認証によるログ機能を提供するASP.NET Core Webアプリケーション

## 概要

AuthServerは、Microsoft Active Directoryドメイン環境で動作し、以下の機能を提供します：

1. **Difyアプリフロントエンド**: Difyで作成したWebアプリをiframeで埋め込み
2. **ログ記録API**: 外部プログラムからのログ記録リクエストを受け付け

## 主要機能

### 1. Difyアプリフロントエンド
- **エンドポイント**: `/difyApp/{path}`
- **認証**: Windows認証（Negotiate）
- **機能**: DifyアプリをiframeでWebページに埋め込む

**使用例**:
```
https://authserver.example.com/difyApp/chatbot/KtFo2mI15fIkZ7lr
↓
http://dify.example.com/chatbot/KtFo2mI15fIkZ7lr をiframeで埋め込み
```

### 2. ログ記録API
- **エンドポイント**: `/api/log/{name}?message={message}` (GET)
- **エンドポイント**: `/api/log/{name}` (POST with JSON body)
- **認証**: Windows認証
- **機能**: 外部プログラムからログを記録

**使用例** (GET):
```
curl -u DOMAIN\username:password https://authserver.example.com/api/log/batch-process?message=started
```

**使用例** (POST):
```powershell
$body = @{
    message = "Processing completed"
    metadata = "10000 records processed"
} | ConvertTo-Json

Invoke-WebRequest -Uri "https://authserver.example.com/api/log/batch-process" `
    -Method POST `
    -Body $body `
    -ContentType "application/json" `
    -UseDefaultCredentials
```

### 3. アクセスログ
- **出力先**: `{AppDirectory}/logs/access-*.txt`
- **ローテーション**: 50MB ごと
- **含有情報**: ユーザー名, URL, ステータスコード, クライアントIP, 日時

## ファイル構成

```
AuthServer/
├── Program.cs                    # アプリケーション起動
├── web.config                    # IIS設定
├── appsettings.json             # 本番設定
├── appsettings.Development.json # 開発設定
├── AuthServer.csproj            # プロジェクトファイル
├── Controllers/
│   ├── DifyAppController.cs     # Difyフロント機能
│   └── LogController.cs         # ログAPI機能
├── logs/                        # ログ出力ディレクトリ
├── 設計書.md                     # 詳細設計書
├── インストール説明書.md         # インストール・運用ガイド
└── README.md                    # このファイル
```

## クイックスタート

### 開発環境

```powershell
# 1. プロジェクトディレクトリに移動
cd d:\NoSync\misc\Comp\AuthServer\proj

# 2. 依存パッケージを復元
dotnet restore

# 3. アプリケーションを実行
dotnet run

# 4. ブラウザでアクセス
# http://localhost:5000/swagger/index.html
```

### 本番環境

詳しくは [インストール説明書.md](インストール説明書.md) を参照

```powershell
# 1. Release ビルド
dotnet publish -c Release -o "C:\inetpub\wwwroot\authserver"

# 2. IIS で設定（詳細は上記ドキュメント参照）

# 3. HTTPS でアクセス
# https://authserver.example.com/difyApp/[path]
```

## 設定

### appsettings.json

#### DifyベースURL
```json
{
  "Dify": {
    "BaseUrl": "http://dify.example.com"
  }
}
```

変更方法：
- 開発環境: `appsettings.Development.json` を編集
- 本番環境: `appsettings.json` を編集してから公開

#### CORS設定
```json
{
  "Cors": {
    "AllowedOrigins": [
      "http://localhost:3000",
      "https://dify.example.com"
    ]
  }
}
```

## トラブルシューティング

### 認証エラー (401)
1. ドメイン環境か確認
2. IIS の Windows Authentication が有効か確認
3. ファイアウォール設定を確認

### ログが出力されない
1. `logs/` ディレクトリが存在するか確認
2. アプリケーション プール アイデンティティにアクセス権があるか確認
3. ディスク容量を確認

詳しくは [インストール説明書.md](インストール説明書.md#4-トラブルシューティング) を参照

## 技術スタック

- **.NET**: 8.0
- **Framework**: ASP.NET Core
- **認証**: Negotiate (Windows Authentication)
- **ロギング**: Serilog
- **ホスト**: IIS 10.0+

## 必要な環境

- **OS**: Windows Server 2019+ または Windows 10/11
- **Runtime**: .NET 8.0 Hosting Bundle
- **IIS**: 10.0+
- **AD**: Active Directory ドメイン

## セキュリティ

- ✅ Windows認証による強力な認証
- ✅ HTTPS通信対応
- ✅ CORS設定で許可されたオリジンのみ
- ✅ セキュリティレスポンスヘッダー設定
- ✅ ログは安全に保存

## ライセンス

内部用

## サポート

問題が発生した場合は、[インストール説明書.md](インストール説明書.md) のトラブルシューティング章を参照するか、サポートチームに連絡してください。

## 変更履歴

### v1.0.0 (2024-12-26)
- 初版リリース
- Difyアプリフロントエンド機能
- ログ記録API機能
- Windows認証対応
