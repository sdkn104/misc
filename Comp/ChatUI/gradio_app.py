import configparser

import gradio as gr
import PyPDF2
from openai import AzureOpenAI
from pprint import pprint
import os
import json
import logging

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
print("Imports completed")

# ログ設定: INFO レベル以上をファイルに記録
logging.basicConfig(
    level=logging.INFO,
    filename="logs/gradio.log",
    encoding="utf-8",
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("Application started")

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



def create_agent_messages(user_prompt, system_prompt, history):
    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    for entry in history:
        if isinstance(entry, dict):
            if entry["role"] == "user":
                messages.append(HumanMessage(content=entry["content"]))
            elif entry["role"] == "assistant":
                messages.append(AIMessage(content=entry["content"]))
        elif isinstance(entry, (list, tuple)) and len(entry) == 2:
            messages.append(HumanMessage(content=entry[0]))
            messages.append(AIMessage(content=entry[1]))
    messages.append(HumanMessage(content=user_prompt))
    return messages 


# --------------------------------------------------------------------------------
# -- エージェントモードの応答生成
# --------------------------------------------------------------------------------
import doc_agent

async def init_mcp():
    """MCPサーバーの起動"""
    await doc_agent.mcp_servers.start()

async def shutdown_mcp():
    """MCPサーバーの停止"""
    await doc_agent.mcp_servers.shutdown()

def create_agent():
    """DocAgent を作成して返す（モデル切替は agent.run() の options で行う）"""
    m = models[0]
    client = doc_agent.build_client(
        model=m["deployment"],
        endpoint=m["endpoint"],
        api_key=m["subscription_key"],
        api_version=m["api_version"],
    )
    return client.as_agent(
        name="DocAgent",
        instructions=doc_agent._load_instructions(),
        tools=[doc_agent.search_paper_pdf, doc_agent.read_pdf_from_url, doc_agent.convert_to_markdown] + doc_agent.mcp_servers.tools(),
    )



async def run_agent(agent, prompt: str, history: list, session, model_name: str | None = None, effort: str | None = None):
    """DocAgent を実行して応答を返す"""
    out_messages = history.copy()
    out_messages.append({"role": "user", "content": prompt})
    async for content in doc_agent.agent_run(agent, prompt, session, model=model_name, effort=effort):
        out_messages.append(_content_to_message(content))
        yield out_messages


def _content_to_message(content) -> dict:
    """蓄積済み content を type ごとにまとめて表示する。"""
    def _trunc(s: str, n: int) -> str:
        s = str(s)
        return s[:n] + "..." if len(s) > n else s

    match content.type:
        case "text":
            if content.text:
                return {
                    "role": "assistant", 
                    "content":content.text,
                }
        case "text_reasoning":
            if content.text:
                return {
                    "role": "assistant", 
                    "content": content.text,
                    "metadata": {"title": f"thinking", "status": "done"}
                }
        case "function_call":
            return {
                "role": "assistant", 
                "content": f"  - ツールを実行します ({content.name}({_trunc(content.arguments, 120)}) ...",
            }
        case "function_result":
            return {
                "role": "assistant", 
                "content": content.result,
                "metadata": {"title": f"結果", "status": "done"}
            }
        case "mcp_server_tool_call":
            return {
                "role": "assistant", 
                "content": f"  - ツールを実行します ({content.name}({_trunc(content.arguments, 120)}) ...",
            }
        case "mcp_server_tool_result":
            return {
                "role": "assistant", 
                "content": content.result,
                "metadata": {"title": f"結果", "status": "done"}
            }
    return {"role": "assistant", "content": ""}


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

    messages = create_agent_messages(prompt, None, history)

    events = agent.stream({"messages": messages}, stream_mode="values")
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
            out_messages.append({
                "role": "user", 
                "content": msg.content,
            })
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
                        "content": f"```sql\n{msg.tool_calls[0]['args'].get('query')}\n```",
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


async def chat(message, history, mode, model, effort, pdf, agent, session, request: gr.Request):
    """Gradio ChatInterface のコールバック。モードに応じて通常応答またはエージェント応答を返す"""
    ip = request.client.host
    log_msg = message[:70].replace('\n', ' ')
    logging.info(f"CHAT_LOG | IP={ip} | mode={mode} | model={model} | msg={log_msg}")

    # PDF が添付されている場合はテキストを抽出してプロンプトに追記
    if pdf:
        reader = PyPDF2.PdfReader(pdf.name)
        text = "\n".join([p.extract_text() or "" for p in reader.pages])
        prompt = f"{message}\n\n======= PDF内容 =======:\n{text}\n"
    else:
        prompt = message

    # 初回メッセージまたはチャットクリア後は新規 session を作成
    if session is None or len(history) == 0:
        session = agent.create_session()

    effort_value = effort if effort != "なし" else None

    if mode == "エージェント":
        async for msg in run_agent(agent, prompt, history, session, model_name=model, effort=effort_value):
            yield msg, session
    elif mode == "DBエージェント":
        for msg in run_db_agent(model, prompt, history):
            yield msg, session
    else:
        for msg in createCompletion(prompt, model, history):
            yield msg, session


async def on_load(request: gr.Request):
    """ページロード時にユーザーごとの agent と session を初期化する"""
    mode_val = request.query_params.get("mode") or "通常"
    model_val = request.query_params.get("model") or models[0]["deployment"]
    agent = create_agent()
    session = agent.create_session()
    return mode_val, model_val, agent, session


with gr.Blocks(analytics_enabled=False, fill_height=True) as gradio_app:
    agent_state = gr.State(None)    # ユーザーごとの agent インスタンス
    session_state = gr.State(None)  # ユーザーごとの会話 session

    gr.Markdown("## AI Chat/Agent")
    chatbot = gr.Chatbot(scale=1, editable="all", reasoning_tags=[("query-description","/query-description")])
    with gr.Row():
        msg = gr.Textbox(
            container=False,
            placeholder="質問を入力…",
            scale=8
        )
        pdf = gr.File(label="📎PDF添付", scale=0, min_width=60, height=40)
        send_btn = gr.Button("➤", min_width=40, scale=0)

    with gr.Row():
        mode = gr.Radio(
            choices=["通常", "エージェント", "DBエージェント"],
            label="モード",
            value="通常",
            scale=1
        )

    with gr.Accordion("オプション", open=False):
        model = gr.Radio(
            choices=[m["deployment"] for m in models],
            label="Model",
            value=models[0]["deployment"]
        )
        effort = gr.Radio(
            choices=["なし", "low", "medium", "high"],
            label="Effort",
            value="なし",
        )

    msg.submit(
        chat,
        inputs=[msg, chatbot, mode, model, effort, pdf, agent_state, session_state],
        outputs=[chatbot, session_state]
    ).then(
        lambda: "", inputs=None, outputs=msg  # 送信後に入力欄をクリア
    )

    send_btn.click(
        chat,
        inputs=[msg, chatbot, mode, model, effort, pdf, agent_state, session_state],
        outputs=[chatbot, session_state]
    ).then(
        lambda: "", inputs=None, outputs=msg  # 送信後に入力欄をクリア
    )

    gradio_app.load(fn=on_load, inputs=None, outputs=[mode, model, agent_state, session_state])

from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app):
    await init_mcp()
    yield
    await shutdown_mcp()

from fastapi import FastAPI
fastapi_app = FastAPI(lifespan=lifespan)
app = gr.mount_gradio_app(fastapi_app, gradio_app, path="/")

if __name__ == "__main__":
    #gradio_app.launch()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
