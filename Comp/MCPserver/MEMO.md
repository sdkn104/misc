## VS Code MCP setting
https://code.visualstudio.com/docs/copilot/chat/mcp-servers

## fetch MCP server
https://github.com/modelcontextprotocol/servers/tree/main/src/fetch

* pip install mcp-server-fetch
* setting VS Code settings.json

## PyMCP-FS (python mcp filesystem)
https://github.com/hypercat/PyMCP-FS

1. install
```
git clone https://github.com/hypercat/PyMCP-FS.git
# start mcp server
python PyMCP-FS\main.py -d path/to/directory
```
2. setting VS code (add the following to settings.json)
```
    "mcp": {
        "servers": {
            "filesystem": {
                "command": "python",
                "args": ["${env:USERPROFILE}/desktop/nosync/misc/comp/mcpserver/PyMCP-FS/main.py", "-d", "${env:USERPROFILE}/downloads"]
            }
        }
    },
```
3. push Tool button to show tools with descriptions, and turn on/off MCP servers
4. type #tool_name (= mcp server name) in copilot prompt to call it

## Context7 MCP server (code documents)
https://github.com/upstash/context7
* prompt: ex. create RAG with langchain. use tool #context7

## Microsoft Learn Docs MCP Server
https://github.com/MicrosoftDocs/mcp
* prompt: ex. describe UserErrorGuestAgentStatusUnavailable, use #msdocsmicrosoft.docs.mcp

## Oracle SQLcl MCP server
https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.2/sqcug/index.html
- インストール手順:
    -  前提条件としてOracle SQLcl 25.2.0以上とJRE 17以上(Oracle Java or OpenJDK)が必要です。
    -  SQLclをダウンロード・セットアップし、JREをインストールします。
    -  conn -saveコマンドを使ってOracle Databaseへの接続情報を事前設定し、~/.dbtoolsディレクトリに保存します。
    -  MCPクライアント（Claude DesktopやClineなど）の設定ファイルで、SQLclの絶対パスと-mcp引数を指定してサーバーの場所を構成します。
    -  クライアントがSQLcl MCP Serverを自動起動・管理しますが、sql -mcpコマンドで手動起動も可能です。
- 使用例:
    -  自然言語でデータベースに問い合わせて、テーブル一覧の取得や複雑なSQLクエリの自動生成ができます。
    -  「どの職種の従業員が一番多いか」といった質問に対し、LLMが複数のテーブルを結合する適切なSQLを生成し、回答を返した事例があります。
    -  ER図やグラフ、ダッシュボード作成といった高度なワークフローも自然言語の指示で実現可能です。
    