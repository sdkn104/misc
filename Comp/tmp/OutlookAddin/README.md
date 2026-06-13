# Outlook 返信生成アドイン

受信メールの返信文を自動生成する Outlook アドイン（Office.js）のサンプルです。

## ファイル構成

```
OutlookAddin/
├── manifest.xml        ← アドイン定義ファイル
├── package.json        ← npmスクリプト
├── server.js           ← HTTPS開発サーバー
└── src/
    ├── taskpane.html   ← アドインUI
    ├── taskpane.js     ← ロジック（Office.js）
    ├── taskpane.css    ← スタイル
    └── commands.html   ← コマンド用ページ（必須）
```

## セットアップ

### 1. 依存パッケージのインストールと証明書生成

```powershell
npm install
npm run gen-certs
```

> `gen-certs` は管理者権限を求める場合があります。許可してください。

### 2. 開発サーバー起動

```powershell
npm start
```

ブラウザで `https://localhost:3000/taskpane.html` にアクセスし、証明書エラーが出ないことを確認してください。

## Outlookへのインストール（サイドロード）

### Outlook on the web の場合（推奨）

1. [outlook.office.com](https://outlook.office.com) を開く
2. 任意のメールを開く
3. 右上の「**...**（その他の操作）」→「**Get Add-ins**（アドインを取得）」をクリック
4. 左の「**My add-ins**」→「**Custom add-ins**」セクションの「**Add from file...**」
5. `manifest.xml` を選択してアップロード

### Outlook デスクトップ（Microsoft 365）の場合

1. Outlookを開く
2. ホームタブ →「**Get Add-ins**（アドインを取得）」
3. 「**My add-ins**」→「**Custom add-ins**」→「**+ Add from file**」
4. `manifest.xml` を選択

## 使い方

1. メールを開く
2. リボンに表示された「**返信を生成**」ボタンをクリック
3. 右側のタスクペインでスタイルを選択
4. 「返信を生成」ボタンを押す
5. 生成された文章を編集して「**返信フォームに挿入**」

## 返信スタイル

| スタイル | 説明 |
|---|---|
| ビジネス丁寧（フォーマル） | 一般的なビジネスメールの返信 |
| カジュアル | 気軽な雰囲気の返信 |
| お礼・感謝 | 感謝を伝える返信 |
| 確認・了解 | 内容を承認する返信 |
| お断り（丁寧） | 丁寧に断る返信 |

## 注意事項

- 開発中はサーバー（`npm start`）を起動した状態でOutlookを使用してください
- `manifest.xml` の `<Id>` タグのGUIDは本番環境では一意の値に変更してください
- アイコン画像はプレースホルダーを使用しています。本番環境では実際の画像に差し替えてください
