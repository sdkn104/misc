import configparser
from urllib import response

import gradio as gr
import PyPDF2
from openai import AzureOpenAI
from pprint import pprint
import os
import json
from pprint import pprint
import datetime
import logging
import math

from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
print("Imports completed")

# ログ設定: INFO レベル以上をファイルに記録
logging.basicConfig(
    level=logging.INFO,
    filename="logs/gradio.log",
    encoding="utf-8",
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("Application started")

stream = False


# Azure OpenAI の接続情報を環境変数から取得
# 利用可能なモデルの一覧と各モデルの接続パラメータ
# $env:LLM_MODELS =  @"
# [
#     {"deployment": "gpt-4.1-azure", "endpoint": "$env:AZURE_OPENAI_ENDPOINT", "subscription_key": "$env:AZURE_OPENAI_API_KEY", "api_version": "$env:OPENAI_API_VERSION"},
#     {"deployment": "gpt-5-mini",    "endpoint": "$env:AZURE_OPENAI_ENDPOINT", "subscription_key": "$env:AZURE_OPENAI_API_KEY", "api_version": "$env:OPENAI_API_VERSION"},
#     {"deployment": "gpt-5.4",       "endpoint": "$env:AZURE_OPENAI_ENDPOINT", "subscription_key": "$env:AZURE_OPENAI_API_KEY", "api_version": "$env:OPENAI_API_VERSION"}
# ]
# "@
models = json.loads(os.getenv("LLM_MODELS", "[]"))
pprint(models)

# 各モデルに対応する AzureOpenAI クライアントを初期化してモデル情報に格納
for m in models:
    m["client"] = AzureOpenAI(
        azure_endpoint=m["endpoint"],
        api_key=m["subscription_key"],
        api_version=m["api_version"],
    )


# --------------------------------------------------------------------------------
# --- エージェント用ツール定義
# --------------------------------------------------------------------------------

@tool
def get_current_datetime() -> str:
    """現在の日付と時刻を返す"""
    return datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")


@tool
def calculate(expression: str) -> str:
    """数式を計算して結果を返す。例: '2 + 3 * 4', 'sqrt(16)', 'sin(3.14)'"""
    try:
        # math モジュールの関数のみ許可し、組み込み関数は無効化してサンドボックス化
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(result)
    except Exception as e:
        return f"計算エラー: {e}"


@tool
def count_words(text: str) -> str:
    """テキストの文字数と単語数を返す"""
    chars = len(text)
    words = len(text.split())
    return f"文字数: {chars}, 単語数(スペース区切り): {words}"


# エージェントが使用するツール一覧
AGENT_TOOLS = [get_current_datetime, calculate, count_words]

# --------------------------------------------------------------------------------
# -- エージェントモードの応答生成
# --------------------------------------------------------------------------------
def run_agent(model_name: str, prompt: str, history: list) -> str:
    """指定モデルで LangChain エージェントを実行して応答を返す"""
    m = next((m for m in models if m["deployment"] == model_name), models[0])
    llm = AzureChatOpenAI(
        azure_endpoint=m["endpoint"],
        api_key=m["subscription_key"],
        api_version=m["api_version"],
        azure_deployment=model_name,
        temperature=0,
    )
    llm_with_tools = llm.bind_tools(AGENT_TOOLS)
    tools_map = {t.name: t for t in AGENT_TOOLS}

    chat_history = []
    for entry in history:
        if isinstance(entry, dict):
            if entry["role"] == "user":
                chat_history.append(HumanMessage(content=entry["content"]))
            elif entry["role"] == "assistant":
                chat_history.append(AIMessage(content=entry["content"]))
        elif isinstance(entry, (list, tuple)) and len(entry) == 2:
            chat_history.append(HumanMessage(content=entry[0]))
            chat_history.append(AIMessage(content=entry[1]))

    messages = [
        SystemMessage(content="あなたは役立つAIアシスタントです。必要に応じてツールを使って回答してください。"),
        *chat_history,
        HumanMessage(content=prompt),
    ]

    out_messages = []
    while True:
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        if not response.tool_calls:
            out_messages.append({
                "role": "assistant", 
                "content": response.content,
            })
            yield out_messages
            break
        for tc in response.tool_calls:
            out_messages.append({
                "role": "assistant", 
                "content": f"  - ツールを実行します ({tc['name']}) ...",
            })
            yield out_messages
            result = tools_map[tc["name"]].invoke(tc["args"])
            out_messages.append({
                "role": "assistant", 
                "content": result,
                "metadata": {"title": f"🛠️ 結果({tc['name']})", "status": "done"}
            })
            yield out_messages
            messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))


# --------------------------------------------------------------------------------
# --- DBエージェント
# --------------------------------------------------------------------------------

def run_db_agent(model_name: str, prompt: str, history: list) -> str:
    """指定モデルで LangChain DB エージェントを実行して応答を返す"""
    m = next((m for m in models if m["deployment"] == model_name), models[0])
    llm = AzureChatOpenAI(
        azure_endpoint=m["endpoint"],
        api_key=m["subscription_key"],
        api_version=m["api_version"],
        azure_deployment=model_name,
    )

    # DB 設定の読み込み
    DB_TYPE = "mysql"  # 接続先データベースを "mysql" または "oracle" で指定
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    db_cfg = cfg[DB_TYPE]

    # DB エージェントの構築と実行
    # ※ DB 設定は config.ini から読み込まれる前提
    from langchain_db_agent import create_db_agent
    agent = create_db_agent(DB_TYPE, db_cfg, llm)

    events = agent.stream({"messages": [{"role": "user", "content": prompt}]}, stream_mode="values")
    answer = None
    msgs = []
    partial = ""
    out_messages = []
    for event in events:
        msg = event["messages"][-1]
        msg.pretty_print()
        print(f"msg.type: {msg.type}")
        #print("msg: ", msg)
        answer = msg.content
        if msg.type == "human":
            pass
        elif msg.type == "tool" :
            out_messages.append({
                "role": "assistant", 
                "content": msg.content,
                "metadata": {"title": f"🛠️ 結果({msg.name})", "status": "done"},
            })
        elif msg.type == "ai":
            if msg.response_metadata and msg.response_metadata.get("finish_reason") == "stop":
                out_messages.append({
                    "role": "assistant", 
                    "content": msg.content,
                })
            elif msg.tool_calls:
                out_messages.append({
                    "role": "assistant", 
                    "content": f"  - ツールを実行します ({msg.tool_calls[0]['name']}) ...",
                })
                if msg.tool_calls[0]['name'] == "sql_db_query":
                    out_messages.append({
                        "role": "assistant", 
                        "content": msg.tool_calls[0]['args'].get('query'),
                        "metadata": {"title": f"SQLクエリ", "status": "done"}
                    })
            else:
                out_messages.append({
                    "role": "assistant", 
                    "content": msg.content,
                    "metadata": {"title": f"{msg.type} {msg.name if msg.name else ''}", "status": "done"}
                })
        yield out_messages

# --------------------------------------------------------------------------------
# --- 通常モードの応答生成
# --------------------------------------------------------------------------------
def createCompletion(prompt, model, history):
    """通常モード: Azure OpenAI にチャット履歴と新規プロンプトを送り応答テキストを返す"""
    client = next((m["client"] for m in models if m["deployment"] == model), None)
    messages = []
    for entry in history:
        if isinstance(entry, dict):
            if entry["role"] == "user":
                messages.append({"role": "user", "content": entry["content"]})
            elif entry["role"] == "assistant":
                messages.append({"role": "assistant", "content": entry["content"]})
        elif isinstance(entry, (list, tuple)) and len(entry) == 2:
            messages.append({"role": "user", "content": entry[0]})
            messages.append({"role": "assistant", "content": entry[1]})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    partial = ""
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            delta = chunk.choices[0].delta.content
            if delta:
                partial += delta
                yield partial


def chat(message, history, request: gr.Request, mode, model, pdf=None):
    """Gradio ChatInterface のコールバック。モードに応じて通常応答またはエージェント応答を返す"""
    ip = request.client.host
    msg = message[:70].replace('\n', ' ')
    logging.info(f"CHAT_LOG | IP={ip} | mode={mode} | model={model} | msg={msg}")

    # PDF が添付されている場合はテキストを抽出してプロンプトに追記
    text = ""
    if pdf:
        reader = PyPDF2.PdfReader(pdf.name)
        text = "\n".join([p.extract_text() for p in reader.pages])
        prompt = f"{message}\n\n======= PDF内容 =======:\n{text}\n"
    else:
        prompt = message

    #yield [{"role": "user", "content": "message1"}, {"role": "assistant", "content": "message2", "metadata":{"title": "using tool 'Weather'"}}]  # ユーザーメッセージと空のアシスタントメッセージを即座に返す
    #return

    if mode == "エージェント":
        for msg in run_agent(model, prompt, history):
            yield msg
    elif mode == "DBエージェント":
        for msg in run_db_agent(model, prompt, history):
            yield msg
    else:
        for msg in createCompletion(prompt, model, history):
            yield msg


# Gradio UI の構築と起動
gr.ChatInterface(
    fn=chat,
    additional_inputs=[
        gr.Radio(choices=["通常", "エージェント", "DBエージェント"], label="モード", value="通常"),
        gr.Radio(choices=[m["deployment"] for m in models], label="Model", value=models[0]["deployment"]),
        gr.File(label="PDFを添付"),
    ],
    title="AI Chat",
    description="PDFをアップロードして、内容に基づいて質問してください。",
    analytics_enabled=False,
    #additional_outputs=[gr.File(label="CSV ダウンロード")],
).launch()
