# Edge Extension Internal Distribution Setup Guide

このスクリプトセットは、Microsoft Edge拡張機能を社内配布するための完全な自動セットアップを提供します。

## 概要

このスクリプトは以下の手順を自動実行します：

1. ✅ 拡張機能のサンプルを作成
2. ✅ 拡張機能署名用のキー構造を準備
3. ✅ 拡張機能IDの情報を保存
4. ✅ update.xml を作成
5. ✅ 自己署名ローカルホスト証明書を作成
6. ✅ Python HTTPS サーバースクリプトを生成
7. ✅ Windows レジストリ設定スクリプトを生成

## ディレクトリ構成

セットアップ後、以下のディレクトリが生成されます：

```
EdgeExtension/
├── progs/                  # このスクリプトセット
│   ├── deploy_extension.ps1
│   ├── deploy_extension.bat
│   └── README.md
├── extension/              # 拡張機能ソース
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
├── output/                 # 出力ファイル
│   ├── extension_key.pem
│   ├── SampleExtension.zip
│   ├── update.xml
│   └── EXTENSION_ID.txt
├── certificates/           # SSL証明書
│   ├── localhost.cer
│   ├── localhost.key
│   └── localhost.pfx
└── server/                 # サーバースクリプト
    ├── https_server.py
    ├── start_server.bat
    └── start_server.ps1
```

## 実行手順

### ステップ 1: セットアップスクリプトの実行

以下のいずれかの方法でセットアップを実行します：

#### 方法A: バッチファイルを使用（推奨）
```cmd
cd progs
deploy_extension.bat
```

#### 方法B: PowerShellを直接使用
```powershell
cd progs
powershell -ExecutionPolicy Bypass -File deploy_extension.ps1
```

#### 方法C: パラメータをカスタマイズして実行
```powershell
powershell -ExecutionPolicy Bypass -File deploy_extension.ps1 `
    -ExtensionName "MyExtension" `
    -Version "1.0.0" `
    -ServerPort 8443 `
    -LocalhostFQDN "localhost"
```

### ステップ 2: 拡張機能に署名

1. Edgeで開く　edge://extensions/
1. 「デベロッパーモード」ON
1. 「拡張機能のパッケージ化」クリック

　　フォルダ指定
　　「秘密キー」は初回は空欄でOK
　　実行

-  生成されるファイル
    - extension.crx  ← 署名済み拡張機能
    - extension.pem  ← 秘密鍵（超重要）
　copy extension.crx to output/SampleExtension.crx

    2回目以降（更新時）は、extension.pemファイルを秘密キーに設定する

### ステップ 3: レジストリの設定（管理者権限が必要）

1. PowerShell を**管理者として実行**
2. 以下のコマンドを実行：
```powershell
powershell -ExecutionPolicy Bypass -File progs\configure_registry.ps1
```

### ステップ 4: HTTPS サーバーの起動

サーバーを起動して、拡張機能の配布を開始します：

#### 方法A: PowerShell スクリプト
```powershell
python server/https_server.py
```

#### 方法B: バッチファイル
```cmd
server/start_server.bat
```

サーバーが `https://localhost:8443` でリッスンを開始します

### ステップ 5: クライアント側の設定

#### オプション A: Group Policy を使用（ドメイン環境）
Windows Group Policy を使用して、拡張機能の更新URLを配布できます：
- `User Configuration\Administrative Templates\Microsoft Edge\Extensions`

#### オプション B: 手動インストール
ユーザーが以下の手順でインストール：
1. Edge を開く → メニュー → 拡張機能
2. 開発者モード をオン
3. 解凍した拡張機能を読み込む

## 証明書について

### 自己署名証明書
セットアップで生成される証明書は自己署名です。クライアント機でこの証明書を信頼するには：

#### Windows に証明書をインストール：
1. `certificates\localhost.cer` をダブルクリック
2. 「証明書のインストール」をクリック
3. 「ローカル マシン」を選択
4. 「信頼されたルート認証局」に配置

#### または、PowerShell で自動インストール：
```powershell
# 管理者実行
$certPath = "certificates\localhost.cer"
Import-Certificate -FilePath $certPath -CertStoreLocation Cert:\LocalMachine\Root
```

## セキュリティに関する注意

⚠️ **本番環境での使用について：**

- 本番環境では、信頼された認証局（CA）から正式な証明書を取得してください
- 自己署名証明書はテスト/内部配布用のみです
- サーバーを公開ネットワークに直接公開しないでください
- 適切なファイアウォール設定とアクセス制御を実装してください

## トラブルシューティング

### Python が見つからない場合
```powershell
# Python のインストール確認
python --version

# Python がない場合：
# https://www.python.org/downloads/ からインストール
# または: choco install python
```

### 証明書エラーが発生する
```powershell
# 証明書をリセット
Remove-Item -Path "certificates\localhost.*" -Force
# セットアップを再実行
```

### ポート 8443 が既に使用されている場合
```powershell
# 別のポートで実行
python server/https_server.py --port 8444
```

### レジストリの権限不足エラー
```powershell
# 管理者として実行し直す
Start-Process powershell -Verb runAs
```

## ファイル説明

| ファイル | 説明 |
|---------|------|
| `deploy_extension.ps1` | メインセットアップスクリプト |
| `deploy_extension.bat` | PowerShell スクリプトの実行ラッパー |
| `server/https_server.py` | Python HTTPS サーバー |
| `configure_registry.ps1` | Windows レジストリ設定スクリプト |

## 参考資料

- [Chromium Edge について](https://docs.microsoft.com/en-us/deployedge/)
- [Edge 拡張機能の開発](https://docs.microsoft.com/en-us/microsoft-edge/extensions-chromium/)
- [拡張機能の配布](https://docs.microsoft.com/en-us/microsoft-edge/extensions-chromium/enterprise/distribute)

## ライセンス

社内使用のみ

## サポート

問題が発生した場合は、出力ログを確認し、以下をチェックしてください：
1. Python が正しくインストールされているか
2. エクスプローラでファイルが正しく生成されているか
3. ファイアウォール設定がポート 8443 をブロックしていないか
