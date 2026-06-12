# Doc Agent

文書（PDF・Word・Web）を読み込んで内容を解説・回答する対話型エージェント。

## 機能概要

| 機能 | 説明 |
|------|------|
| PDF 検索 | 論文タイトルから Semantic Scholar → arXiv の順に PDF URL を自動検索 |
| PDF 読み込み | URL 指定で PDF をダウンロードしてテキスト抽出 |
| Word / その他ドキュメント | markitdown MCP サーバー経由で .docx 等を処理 |
| ブラウザ操作 | Playwright MCP サーバー経由で Web ページを取得・操作 |
| ローカルファイル | Filesystem MCP サーバー経由でファイルの読み書き |
| システムプロンプト | `SYSTEM.md` を編集することでエージェントの挙動をカスタマイズ可能 |

バックエンドは **Azure OpenAI** (OpenAI API 互換)。API キー認証と Azure CLI 認証の両方に対応。

## インストール

### 前提条件

- Python 3.11 以上
- Node.js 18 以上 (`npx` が使えること)
- Azure OpenAI リソース（またはそれに相当する OpenAI 互換エンドポイント）

### 手順

```bash
# 1. 依存パッケージをインストール
pip install -r requirements.txt
# MCP serversをインストール (node_modules/.bin/markitdown-mcp-npxなどで起動)
npm install @modelcontextprotocol/server-filesystem @playwright/mcp markitdown-mcp-npx


# 2. 環境変数を設定
cp .env.example .env
# .env を編集して各値を入力
```

`.env` の設定項目:

```env
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_API_KEY=<your-api-key>   # 省略時は az login の認証を使用
```

アクセス先制限：

```python
    playwright_mcp = MCPStdioTool(
        name="playwright",
        command="npx",
        args=["-y", "@playwright/mcp", "--browser=msedge", "--allowed-origins=https://*,http://*"],
    )
```

## 使用方法

```bash
python doc_agent.py
```

起動するとプロンプトが表示されます。

```
PDF Agent 起動中。論文タイトルまたはURLを含む質問を入力してください。
You:
```

### 入力例

```
# 論文タイトルで検索して要約
You: Attention Is All You Need を要約して

# PDF URL を直接指定
You: https://arxiv.org/pdf/1706.03762 を読んで貢献をまとめて

# Word ファイルを処理
You: https://example.com/report.docx の内容を要約して

# ブラウザでページを開いて操作
You: https://arxiv.org/abs/1706.03762 をブラウザで開いて要約して

# ローカルファイルを読む
You: ./data/memo.txt を読んで
```

終了するには `quit` または `exit` を入力します。

### システムプロンプトのカスタマイズ

`SYSTEM.md` を編集するとエージェントへの指示を変更できます。再起動後に反映されます。

### ファイルシステムのルートディレクトリ変更

デフォルトでは実行時のカレントディレクトリがファイルアクセスのルートになります。
変更する場合は環境変数 `AGENT_FS_ROOT` を設定します。

```env
AGENT_FS_ROOT=C:\Users\yourname\Documents
```
