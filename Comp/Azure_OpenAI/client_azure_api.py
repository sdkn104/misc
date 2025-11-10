import os
from pprint import pprint
import sys
import requests

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")  
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "")  

print(endpoint)
print(deployment)
print(subscription_key)

stream = False

url = endpoint + "/openai/v1/chat/completions"
print(url)
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {subscription_key}",
}
data = {
    "model": "gpt-4.1-azure",
    "messages": [
        {"role": "system", "content": "あなたは親切なアシスタントです。"},
        {"role": "user", "content": "世界一高い山の名前を教えてください。単語１つで答えてください。"},
    ],
    "stream": True,
}
response = requests.post(url, headers=headers, json=data)
#client = SSEClient(response)
#for event in client.events():
#    print(event.data)


print(response)
print("Status Code:", response.status_code)
print("----------")
pprint(dict(response.headers))
print("----------")
if response.headers.get("Content-Type").startswith("application/json"):
    response_json = response.json()
    print("Response(json):\n")
    print(response.json())

if response.headers.get("Content-Type").startswith("text/event-stream"):
    print("Response(event-stream):\n")
    print(response.text)

