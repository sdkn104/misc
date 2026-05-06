
"""
LangChain SQL エージェントのサンプル（Azure OpenAI + MySQL または Oracle DB）。

使い方 (PowerShell):
  # シークレットを環境変数に読み込む（または現在のシェルで secret.ps1 を実行）
  . .\secret.ps1
  # スクリプトを実行
  python langchain_sql_agent.py --config config.ini

処理内容:
 - secret.ps1 をパースして Azure OpenAI の環境変数を設定（未設定の場合）
 - config.ini の [mysql] または [oracle] セクションから DB 接続情報を読み込む
 - LangChain SQL エージェントを作成してサンプルクエリを実行する
"""

# ── DB タイプの切り替え ────────────────────────────────────────────────────────────
# 接続先データベースを "mysql" または "oracle" で指定する
DB_TYPE = "mysql"
# ─────────────────────────────────────────────────────────────────────────────

import argparse
import configparser
import os
import re
from pprint import pprint
from sqlalchemy import create_engine

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
import pandas as pd
from sqlalchemy import create_engine

print("start")

def load_ps1_env(ps1_path: str):
    """secret.ps1 内の $env:VAR = "value" 形式の行をパースして os.environ に設定する。
    シークレットをコードに直書きせず、ユーザーが secret.ps1 を参照できるようにするため。
    """
    if not os.path.exists(ps1_path):
        return
    # $env:変数名 = "値" の行にマッチする正規表現
    pattern = re.compile(r'^\$env:([A-Z0-9_]+)\s*=\s*"(.*)"')
    with open(ps1_path, "r", encoding="utf-8") as f:
        for line in f:
            m = pattern.search(line.strip())
            if m:
                key, val = m.group(1), m.group(2)
                # シークレットは出力しない
                os.environ.setdefault(key, val)


def build_sqlalchemy_uri(db_type: str, cfg_section) -> str:
    """DB タイプと設定セクションから SQLAlchemy 接続 URI を組み立てる。"""
    user = cfg_section.get("user")
    password = cfg_section.get("password")
    host = cfg_section.get("host", "127.0.0.1")

    if db_type == "mysql":
        port = cfg_section.get("port", "3306")
        database = cfg_section.get("database")
        # ドライバ: mysql-connector-python
        return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

    if db_type == "oracle":
        port = cfg_section.get("port", "1521")
        service_name = cfg_section.get("service_name")
        sid = cfg_section.get("sid")
        # ドライバ: python-oracledb（シンモード、Oracle Client 不要）
        if service_name:
            return f"oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={service_name}"
        if sid:
            return f"oracle+oracledb://{user}:{password}@{host}:{port}/{sid}"
        raise ValueError("Oracle の設定には config.ini に 'service_name' または 'sid' が必要です")

    raise ValueError(f"未対応の DB_TYPE: {db_type!r}。'mysql' または 'oracle' を指定してください。")


def create_db_agent(db_type: str, db_cfg, llm):
    """指定した db_type に対応する LangChain SQL エージェントを構築する。

    エンジン作成 → SQLDatabase → ツールキット → エージェント の順に組み立て、
    作成したエージェントを返す。
    """
    # SQLAlchemy エンジンを作成
    uri = build_sqlalchemy_uri(db_type, db_cfg)
    engine = create_engine(uri)

    # 対象テーブル（ビュー含む）を絞り込んで SQLDatabase オブジェクトを生成
    db = SQLDatabase(
        engine,
        view_support=True,
        include_tables=["view_train", "transactions"],
        sample_rows_in_table_info=5,  # テーブル情報にサンプル行を含める数
    )

    # LLM と DB を紐づけるツールキットを作成
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()
    print("tools: ------------------------------")
    for tool in tools:
        print(f"tool: {tool.name}: {tool.description}\n")
    print("context: ------------------------------")
    print(toolkit.get_context())
    print("dialect: ------------------------------")
    print(toolkit.dialect)

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
        system_prompt=system_prompt
    )
    return agent

    # SQL エージェントを作成（tool-calling 方式、中間ステップも返す）
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="tool-calling",
        agent_executor_kwargs={"return_intermediate_steps": True},
    )
    return agent


def main():
    # コマンドライン引数のパース
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.ini")
    parser.add_argument("--ps1", default="secret.ps1", help="secret.ps1 のパス")
    args = parser.parse_args()

    # 環境変数が未設定の場合は secret.ps1 から読み込む
    load_ps1_env(args.ps1)

    # DB 設定の読み込み
    cfg = configparser.ConfigParser()
    cfg.read(args.config)
    if DB_TYPE not in cfg:
        raise SystemExit(f"config ファイルに [{DB_TYPE}] セクションがありません")

    db_cfg = cfg[DB_TYPE]

    try:
        # Azure OpenAI の LLM を初期化
        from langchain_openai import AzureChatOpenAI
        llm = AzureChatOpenAI(
            deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
            openai_api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            openai_api_version=os.environ.get("OPENAI_API_VERSION"),
        )

        # SQL エージェントを構築
        agent = create_db_agent(DB_TYPE, db_cfg, llm)

        def process_events(events):
            answer = None
            result = None
            for event in events:
                msg = event["messages"][-1]
                msg.pretty_print()
                print(f"msg.type: {msg.type}")
                #print("msg: ", msg)
                answer = msg.content
                if msg.type == "tool" : #and msg.name == "sql_db_query":
                    result = msg.content
            return (answer, result)

        # ── クエリ 1: テーブル一覧と説明 ──────────────────────────────────────
        question = "データベース中のテーブルをリストアップし、それぞれを短く説明をしてください。"
        print("Question:", question)
        events = agent.stream({"messages": [{"role": "user", "content": question}]}, stream_mode="values")
        (answer, result) = process_events(events)
        #print("Answer:\n", answer, "\nResult:\n", result)

        # ── クエリ 2: 年毎の売上平均（テキスト形式） ──────────────────────────
        question = "view_trainの年毎のsalesの平均値を教えてください。"
        #question = "view_trainの2016年のデータを100件表示してください。"
        print("Question:", question)
        events = agent.stream({"messages": [{"role": "user", "content": question}]}, stream_mode="values")
        (answer, result) = process_events(events)
        #print("Answer:\n", answer, "\nResult:\n", result)

        # ── クエリ 3: 年毎の売上平均（JSON 形式）＋中間ステップの表示 ──────────
        question = "view_trainの年毎のsalesの平均値をJSON形式の表で返してください。"
        print("Question:", question)
        events = agent.stream({"messages": [{"role": "user", "content": question}]}, stream_mode="values")
        (answer, result) = process_events(events)
        #print("Answer:\n", answer, "\nResult:\n", result)

        print("Final result (raw): ", result)

        # 最終ステップの結果を DataFrame に変換してグラフ表示
        import ast
        data = ast.literal_eval(result)
        df = pd.DataFrame(data, columns=["year", "avg_sales"])
        print(df)

        import matplotlib.pyplot as plt
        df.plot(x="year", y="avg_sales", kind="bar")
        plt.show()

    except Exception as e:
        print("LangChain エージェントの作成またはクエリ実行に失敗しました:", e)


if __name__ == "__main__":
    main()
