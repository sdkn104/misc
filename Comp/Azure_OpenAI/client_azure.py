import os
from openai import AzureOpenAI
import openai
from pprint import pprint
#import tiktoken
import pprint
import sys
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
response = client.chat.completions.create(
    model=deployment, # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "世界一高い山の名前は？単語１つで答えてください。"},
#        {"role": "user", "content": "以下の文章を要約して：\n\n" + extract_text_from_pdf(sys.argv[1])},
    ],
    stream=stream, 
)

print(response)

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

