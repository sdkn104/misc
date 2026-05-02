from urllib import response

import gradio as gr
import PyPDF2
from openai import AzureOpenAI
from pprint import pprint
import os
import datetime
import logging

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")  
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "")  

print(endpoint)
print(deployment)
print(subscription_key)


logging.basicConfig(
    level=logging.INFO,
    filename="logs/gradio.log",
    encoding="utf-8",
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("Application started")

stream = False

models = [
    {"deployment": deployment, "endpoint": endpoint, "subscription_key": subscription_key, "api_version": "2024-10-21"},
    {"deployment": "gpt-5-mini", "endpoint": endpoint, "subscription_key": subscription_key, "api_version": "2024-10-21"},
    {"deployment": "gpt-5.4", "endpoint": endpoint, "subscription_key": subscription_key, "api_version": "2024-10-21"},
]

for m in models:
    client = AzureOpenAI(  
        azure_endpoint=m["endpoint"],
        api_key=m["subscription_key"],
        api_version=m["api_version"],
    )
    m["client"] = client


def createCompletion(prompt, model):
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


def chat(message, history, request: gr.Request, model, pdf=None):
    #pprint({"message": message, "history": history, "request": request, "model": model, "pdf": pdf})

    ip = request.client.host
    ua = request.headers.get("user-agent", "")
    msg = message[:70].replace('\n', ' ')
    log = f"CHAT_LOG | IP={ip} | model={model} | msg={msg}"
    logging.info(log)

    text = ""
    if pdf:
        reader = PyPDF2.PdfReader(pdf.name)
        text = "\n".join([p.extract_text() for p in reader.pages])
        prompt = f"{message}\n\n======= PDF内容 =======:\n{text}\n"
    else:
        prompt = message

    #print("prompt:", prompt)
    res = createCompletion(prompt, model)
    #print("response:", res)

    return res


gr.ChatInterface(
    fn=chat,
    additional_inputs=[
        gr.Radio(choices=[m["deployment"] for m in models], label="Model", value=models[0]["deployment"]),
        gr.File(label="PDFを添付"), 
    ],
    title="AI Chat",
    description="PDFをアップロードして、内容に基づいて質問してください。",
    analytics_enabled=False,
).launch()
