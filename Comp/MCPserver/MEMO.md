# MCP clients

## VS Code MCP setting
https://code.visualstudio.com/docs/copilot/chat/mcp-servers

# MCP servers

## Supergateway (stdio <-> SSE, streamable HTTP)
https://github.com/supercorp-ai/supergateway
https://deepwiki.com/supercorp-ai/supergateway/1-supergateway-overview

- install and start
    ```node
    # stdio -> SSE
    nvm use 22.20
    npm install supergateway
    npx supergateway --stdio "D:\oracle\sqlcl-25.3.0.274.1210\sqlcl\bin\sql.exe -mcp -port 8000"
    ```

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
        - Oracle DB 23ai(23.7) clientをインストール　https://download.oracle.com/otn-pub/otn_software/db-express/WINDOWS.X64_237000_free.zip
            - マイナーバージョンまでsqlclと合わせる必要あり。
            - 直リンクでinstant clientを落とす：https://download.oracle.com/otn_software/nt/instantclient/2370000/instantclient-basic-windows.x64-23.7.0.25.02.zip
                - マイナーバージョンは、ここで調べる：https://yum.oracle.com/repo/OracleLinux/OL8/oracle/instantclient23/x86_64/
        - Oralce Java SE 21をインストール　https://www.oracle.com/java/technologies/downloads/archive/
    -  SQLcl 25.3をダウンロード・解凍。https://www.oracle.com/database/sqldeveloper/technologies/sqlcl/download/
        - zip解凍
        ```cmd
        chcp 65001
        cd path/to/bin
        .\sql.exe sys/freepdb1 as sysdba
        ```
    -  conn -saveコマンドを使ってOracle Databaseへの接続情報を事前設定する。~/.dbtools(~/.sqlcl??)ディレクトリに保存します。→ MCPでは接続名一覧取得と、接続名を使って接続する。`connmgr list` `connmgr delete -conn myconn`
        ```
        CMD> .\sql mcp_user/karatani3@localhost:1521/freepdb1
        SQL> conn -save mcp_user -savepwd mcp_user/karatani3@localhost:1521/freepdb1
        名前: mcp_user
        接続文字列: localhost:1521/freepdb1
        ユーザー: mcp_user
        パスワード: ******
        接続しました.
        ```
    
    -  MCPクライアント（Claude DesktopやClineなど）の設定ファイルで、SQLclの絶対パスと-mcp引数を指定してサーバーの場所を構成します。
    https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.2/sqcug/using-oracle-sqlcl-mcp-server.html

        ```
        Clineの場合：
        {
            "mcpServers": {
                "sqlcl": {
                        "command": "D:/oracle/sqlcl-25.3.0.274.1210/sqlcl/bin/sql.exe",
                        "args": ["-mcp"],
                        "disabled": false
                }    
            }
        }
        ```
    -  クライアントがSQLcl MCP Serverを自動起動・管理しますが、sql -mcpコマンドで手動起動も可能です。
- 使用例:
    - https://docs.oracle.com/en/database/oracle/sql-developer-command-line/25.2/sqcug/example-use-cases-and-prompts.html
    -  自然言語でデータベースに問い合わせて、テーブル一覧の取得や複雑なSQLクエリの自動生成ができます。
    -  「どの職種の従業員が一番多いか」といった質問に対し、LLMが複数のテーブルを結合する適切なSQLを生成し、回答を返した事例があります。
    -  ER図やグラフ、ダッシュボード作成といった高度なワークフローも自然言語の指示で実現可能です。
    