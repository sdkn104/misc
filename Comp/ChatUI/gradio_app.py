from urllib import response

import gradio as gr
import PyPDF2
from openai import AzureOpenAI
from pprint import pprint
import os
import datetime
import logging
import math

from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Azure OpenAI の接続情報を環境変数から取得
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "")

print(endpoint)
print(deployment)
print(subscription_key)


# ログ設定: INFO レベル以上をファイルに記録
logging.basicConfig(
    level=logging.INFO,
    filename="logs/gradio.log",
    encoding="utf-8",
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("Application started")

stream = False

# 利用可能なモデルの一覧と各モデルの接続パラメータ
models = [
    {"deployment": deployment, "endpoint": endpoint, "subscription_key": subscription_key, "api_version": "2024-10-21"},
    {"deployment": "gpt-5-mini", "endpoint": endpoint, "subscription_key": subscription_key, "api_version": "2024-10-21"},
    {"deployment": "gpt-5.4", "endpoint": endpoint, "subscription_key": subscription_key, "api_version": "2024-10-21"},
]

# 各モデルに対応する AzureOpenAI クライアントを初期化してモデル情報に格納
for m in models:
    client = AzureOpenAI(
        azure_endpoint=m["endpoint"],
        api_key=m["subscription_key"],
        api_version=m["api_version"],
    )
    m["client"] = client


# --- エージェント用ツール定義 ---

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

# エージェント用プロンプトテンプレート（チャット履歴と中間思考ステップを含む）
AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "あなたは役立つAIアシスタントです。必要に応じてツールを使って回答してください。"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])


def create_agent(model_name: str) -> AgentExecutor:
    """指定モデルで LangChain エージェントを生成して返す"""
    m = next((m for m in models if m["deployment"] == model_name), models[0])
    llm = AzureChatOpenAI(
        azure_endpoint=m["endpoint"],
        api_key=m["subscription_key"],
        api_version=m["api_version"],
        azure_deployment=model_name,
        temperature=0,
    )
    agent = create_openai_tools_agent(llm, AGENT_TOOLS, AGENT_PROMPT)
    return AgentExecutor(agent=agent, tools=AGENT_TOOLS, verbose=True)


def createCompletion(prompt, model):
    """通常モード: Azure OpenAI に単一プロンプトを送り応答テキストを返す"""
    client = next((m["client"] for m in models if m["deployment"] == model), None)
    response = client.chat.completions.create(
        model=model,
        messages=[
            #{"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=stream,
    )
    return response.choices[0].message.content


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

    if mode == "エージェント":
        # Gradio の履歴形式（dict または tuple）を LangChain のメッセージ形式に変換
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
        agent_executor = create_agent(model)
        result = agent_executor.invoke({"input": prompt, "chat_history": chat_history})
        return result["output"]
    else:
        return createCompletion(prompt, model)


# Gradio UI の構築と起動
gr.ChatInterface(
    fn=chat,
    additional_inputs=[
        gr.Radio(choices=["通常", "エージェント"], label="モード", value="通常"),
        gr.Radio(choices=[m["deployment"] for m in models], label="Model", value=models[0]["deployment"]),
        gr.File(label="PDFを添付"),
    ],
    title="AI Chat",
    description="PDFをアップロードして、内容に基づいて質問してください。",
    analytics_enabled=False,
).launch()
