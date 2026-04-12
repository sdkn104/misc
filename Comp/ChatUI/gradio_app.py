from urllib import response

import gradio as gr
import PyPDF2
#import openai
from openai import AzureOpenAI
from pprint import pprint
#import tiktoken
#import sys
import os

#openai.log = "debug"

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")  
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "")  

print(endpoint)
print(deployment)
print(subscription_key)

stream = False



client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-10-21",  # Use the latest API version
)  

def createCompletion(prompt):
    response = client.chat.completions.create(
        model=deployment, # model = "deployment_name".
        messages=[
            #{"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=stream,
    )
    return response.choices[0].message.content


def chat(message, history=[], model=None, pdf=None):
    #pprint({"message": message, "history": history, "model": model, "pdf": pdf})
    text = ""
    if pdf:
        reader = PyPDF2.PdfReader(pdf.name)
        text = "\n".join([p.extract_text() for p in reader.pages])
        prompt = f"{message}\n\n======= PDF内容 =======:\n{text}\n"
    else:
        prompt = message
    print("prompt:", prompt)

    res = createCompletion(prompt)
    print("response:", res)
    return res


gr.ChatInterface(
    fn=chat,
    additional_inputs=[
        gr.Radio(choices=["GPT-5-mini", "GPT-5.4"], label="Model", value="GPT-5-mini"),
        gr.File(label="PDFを添付"), 
    ],
    title="AI Chat",
    description="PDFをアップロードして、内容に基づいて質問してください。",
).launch()
