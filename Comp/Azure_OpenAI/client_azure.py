# import os
# from openai import AzureOpenAI
    
# client = AzureOpenAI(
#     api_key=os.getenv(""),  
#     api_version="2024-02-01",
#     azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
#     )
    
# deployment_name='REPLACE_WITH_YOUR_DEPLOYMENT_NAME' #This will correspond to the custom name you chose for your deployment when you deployed a model. Use a gpt-35-turbo-instruct deployment. 
    
# # Send a completion call to generate an answer
# print('Sending a test completion job')
# start_phrase = 'Write a tagline for an ice cream shop. '
# response = client.completions.create(model=deployment_name, prompt=start_phrase, max_tokens=10)
# print(start_phrase+response.choices[0].text)

import os
from openai import AzureOpenAI
import openai
from pprint import pprint

openai.log = "debug"

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")  
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "")  

print(endpoint)
print(deployment)
print(subscription_key)

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
    ],
    stream=stream, 
)

print(response)
#print(list(response))

if stream == False:
    #pprint(dict(response.headers))
    #print(response.text)
    print("----------")
    #print("Status Code:", response.status_code)
    print("Message: ", response.choices[0].message.content)
    #print("Response:", response.json())
else:
    for chunk in response:
        pprint(chunk)
    #for chunk in response:
    #    #pprint(dict(chunk))
    #    if hasattr(chunk, 'choices'):
    #        for choice in chunk.choices:
    #            if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
    #                print(choice.delta.content, end='', flush=True)

