import asyncio
from fastmcp import Client

#client = Client("mcpserver.py") # Assumes my_mcp_server.py exists
client = Client("http://127.0.0.1:9000/mcp")

async def main():
    # Connection is established here
    async with client:
        print(f"Client connected: {client.is_connected()}")

        # Make MCP calls within the context
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

        if any(tool.name == "test_tool" for tool in tools):
            result = await client.call_tool("test_tool", {})
            print(f"Tool result: {result}")

    # Connection is closed automatically here
    print(f"Client connected: {client.is_connected()}")

if __name__ == "__main__":
    asyncio.run(main())