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