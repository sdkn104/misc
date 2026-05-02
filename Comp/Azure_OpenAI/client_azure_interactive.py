import os
from openai import AzureOpenAI
import openai
from pprint import pprint
#import tiktoken
import pprint
import sys
import datetime
#import PyPDF2

openai.log = "debug"

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")  
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "")  

print(endpoint)
print(deployment)
print(subscription_key)

# PDFファイルの読み込み
#def extract_text_from_pdf(file_path):
    # text = ""
    # with open(file_path, "rb") as f:
    #     reader = PyPDF2.PdfReader(f)
    #     for page in reader.pages:
    #         text += page.extract_text()
    # return text


stream = False

# キーベースの認証を使用して Azure OpenAI クライアントを初期化する
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-10-21",  # Use the latest API version
)  


while True:
    print(">")
    data = sys.stdin.read()
    print(data)

    start = datetime.datetime.now()
    print(start)
    response = client.chat.completions.create(
        model=deployment, # model = "deployment_name".
        messages=[
            {"role": "user", "content": data},
        ],
        stream=stream, 
        reasoning_effort="none"
    )

    print("END:", datetime.datetime.now() - start, "\n")
    print(response.choices[0].message.content)

#encoding = tiktoken.encoding_for_model("gpt-4")
#text = "こんにちは、Azure OpenAI APIを使っています。"
#tokens = encoding.encode(text)
#print(f"トークン数: {len(tokens)}")


if stream == False:
    #pprint(dict(response.headers))
    #print(response.text)
    print("----------")
    #print("Status Code:", response.status_code)
    print("Response:", response.json())
    print("usage tokens: ", response.usage.total_tokens, response.usage.prompt_tokens, response.usage.completion_tokens)
    print("Message: ", response.choices[0].message.content)
else:
    for chunk in response:
        pprint(chunk)
    #for chunk in response:
    #    #pprint(dict(chunk))
    #    if hasattr(chunk, 'choices'):
    #        for choice in chunk.choices:
    #            if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
    #                print(choice.delta.content, end='', flush=True)

