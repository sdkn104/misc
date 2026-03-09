
import argparse
import configparser
import os
import re
from pprint import pprint
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy import create_engine

def load_ps1_env(ps1_path: str):
    """Parse simple $env:VAR = "value" lines in a PowerShell .ps1 and set os.environ entries.
    This avoids hardcoding secrets into code and mirrors the user's instruction to reference `secret.ps1`.
    """
    if not os.path.exists(ps1_path):
        return
    pattern = re.compile(r'^\$env:([A-Z0-9_]+)\s*=\s*"(.*)"')
    with open(ps1_path, "r", encoding="utf-8") as f:
        for line in f:
            m = pattern.search(line.strip())
            if m:
                key, val = m.group(1), m.group(2)
                # do not print secrets
                os.environ.setdefault(key, val)


def build_sqlalchemy_uri(cfg_section) -> str:
    user = cfg_section.get("user")
    password = cfg_section.get("password")
    host = cfg_section.get("host", "127.0.0.1")
    port = cfg_section.get("port", "3306")
    database = cfg_section.get("database")
    # using mysql+mysqlconnector driver (mysql-connector-python)
    return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.ini")
    parser.add_argument("--ps1", default="secret.ps1", help="path to secret.ps1")
    args = parser.parse_args()

    # Load env from secret.ps1 if variables not already set
    load_ps1_env(args.ps1)

    # Read DB config
    cfg = configparser.ConfigParser()
    cfg.read(args.config)
    if "mysql" not in cfg:
        raise SystemExit("[mysql] section missing in config file")

    db_cfg = cfg["mysql"]
    uri = build_sqlalchemy_uri(db_cfg)

    # Create SQLAlchemy engine
    engine = create_engine(uri)


    # Azure OpenAI model wrapper
    from langchain_openai import AzureChatOpenAI
    llm = AzureChatOpenAI(
        deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
        openai_api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        openai_api_version=os.environ.get("OPENAI_API_VERSION"),
        temperature=0,
    )

    # Create SQLDatabase from SQLAlchemy engine
    db = SQLDatabase(engine)
        
    # Create a simple chain/agent that can answer SQL questions
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()
    for tool in tools:
        print(f"{tool.name}: {tool.description}\n")

    system_prompt = """
    You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct {dialect} query to run,
    then look at the results of the query and return the answer. Unless the user
    specifies a specific number of examples they wish to obtain, always limit your
    query to at most {top_k} results.

    You can order the results by a relevant column to return the most interesting
    examples in the database. Never query for all the columns from a specific table,
    only ask for the relevant columns given the question.

    You MUST double check your query before executing it. If you get an error while
    executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
    database.

    To start you should ALWAYS look at the tables in the database to see what you
    can query. Do NOT skip this step.

    Then you should query the schema of the most relevant tables.
    """.format(
        dialect=db.dialect,
        top_k=5,
    )

    from langchain.agents import create_agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    question = "データベース中のテーブルをリストアップし、それぞれを短く説明をしてください。"
    print("Question:", question)
    for step in agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()


    question = "trainの年毎のsalesの平均値を教えてください。"
    print("Question:", question)
    steps = agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",
    )
    data_str = None
    for step in steps:
        if "sql_db_query" in str(step["messages"][-1]):
            data_str = step["messages"][-1].content
        step["messages"][-1].pretty_print()
        #pprint(step)
    print("data:")
    print(data_str)

    import ast
    data = ast.literal_eval(data_str)
    df = pd.DataFrame(data)
    print(df)

    import matplotlib.pyplot as plt
    df.plot(x="0", y="1", kind="bar")
    plt.show()



if __name__ == "__main__":
    main()
