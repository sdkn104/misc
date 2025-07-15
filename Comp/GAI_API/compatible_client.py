import requests
from pprint import pprint
import os
from sseclient import SSEClient

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

url = "http://localhost:5000/v1/chat/completions"
#url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}
data = {
    "model": "gpt-4.1",
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
#print("Response:", response.json())
print("----------")
pprint(dict(response.headers))
print(response.text)
