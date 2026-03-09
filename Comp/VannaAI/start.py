# All imports at the top
from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool, SaveTextMemoryTool
from vanna.servers.fastapi import VannaFastAPIServer
#from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.azureopenai import AzureOpenAILlmService
from vanna.integrations.oracle import OracleRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
#from vanna.llm import OpenAI_Chat
from openai import AzureOpenAI
import os
from pprint import pprint, pformat

# Configure your LLM
llm = AzureOpenAILlmService(
    model="gpt-4.1-azure",  # Your deployment name
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint ="https://test-openai-999.openai.azure.com/",
    api_version="2024-10-21",
)

# Configure your database
db_tool = RunSqlTool(
    sql_runner=OracleRunner(
        host='127.0.0.1',
        port=1521,
        dsn='FREE',
        user='C##SADAKANE',
        password='karatani3', 
    )
)

# Configure your agent memory
agent_memory = DemoAgentMemory(max_items=1000)

# Configure user authentication
class SimpleUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        user_email = request_context.get_cookie('vanna_email') or 'guest@example.com'
        group = 'admin' if user_email == 'admin@example.com' else 'user'
        return User(id=user_email, email=user_email, group_memberships=[group])
user_resolver = SimpleUserResolver()


# ReadFileTool
from vanna.tools.file_system import ReadFileTool, WriteFileTool, ListFilesTool
from vanna.integrations.local import LocalFileSystem
fs = LocalFileSystem()
read_tool = ReadFileTool(file_system=fs)
write_tool = WriteFileTool(file_system=fs)

# SQLite DB tool
from vanna.integrations.sqlite import SqliteRunner
sqlite_tool = RunSqlTool(
    sql_runner=SqliteRunner(database_path="./test.db")
)

# Create your agent
tools = ToolRegistry()
tools.register_local_tool(read_tool, access_groups=['admin', 'user'])
tools.register_local_tool(write_tool, access_groups=['admin', 'user'])
#tools.register_local_tool(db_tool, access_groups=['admin', 'user'])
tools.register_local_tool(sqlite_tool, access_groups=['admin', 'user'])
tools.register_local_tool(SaveQuestionToolArgsTool(), access_groups=['admin'])
tools.register_local_tool(SearchSavedCorrectToolUsesTool(), access_groups=['admin', 'user'])
tools.register_local_tool(SaveTextMemoryTool(), access_groups=['admin', 'user'])
tools.register_local_tool(VisualizeDataTool(), access_groups=['admin', 'user'])

agent = Agent(
    llm_service=llm,
    tool_registry=tools,
    user_resolver=user_resolver,
    agent_memory=agent_memory
)

results = agent.get_available_tools(user_resolver)
print(results)

# Run the server
server = VannaFastAPIServer(agent)
server.run()  # Access at http://localhost:8000