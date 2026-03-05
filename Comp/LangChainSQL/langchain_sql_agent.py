
"""
Sample LangChain SQL Agent using Azure OpenAI and MySQL.

Usage (PowerShell):
  # load secrets into environment (or run the secret.ps1 in the current shell)
  . .\secret.ps1
  # then run the script
  python langchain_sql_agent.py --config config.ini

The script will:
 - parse `secret.ps1` (if not already in env) to populate Azure OpenAI env vars
 - read MySQL connection info from `config.ini`
 - create a LangChain SQL agent and run an example query

Note: This is a minimal example. Adjust parameters / model names to your LangChain/OpenAI SDK versions.
"""

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

    try:
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
        agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,        # 実行ログを出す
            agent_type="tool-calling",  # 最新推奨 agent_type
        )
        agent2 = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,        # 実行ログを出す
            agent_type="tool-calling",  # 最新推奨 agent_type
            return_intermediate_steps=True
        )

        # Example: ask for tables in the database
        question = "データベース中のテーブルをリストアップし、それぞれを短く説明をしてください。"
        print("Question:", question)
        answer = agent.invoke(question)
        print("Answer:\n")
        print(answer["output"])

        question = "trainの年毎のsalesの平均値を教えてください。"
        print("Question:", question)
        answer = agent.invoke(question)
        print("Answer:\n")
        print(answer["output"])

        question = "trainの年毎のsalesの平均値をJSON形式の表で返してください。"
        print("Question:", question)
        answer = agent2.invoke(question)
        print(answer)
        print("Answer with intermediate steps:\n")
        for step in answer["intermediate_steps"]:
            print(step)
        intermediate_steps = answer["intermediate_steps"]
        sql_query = None
        for step in intermediate_steps:
            action = step[0]
            if action.tool == "sql_db_query":
                sql_query = action.tool_input

        print("生成SQL:")
        print(sql_query)


        data = answer["output"]
        df = pd.DataFrame(data)
        print(df)

        import matplotlib.pyplot as plt

        df.plot(x="month", y="sales", kind="bar")
        plt.show()


    except Exception as e:
        print("Failed to create LangChain agent or run query:", e)

if __name__ == "__main__":
    main()
