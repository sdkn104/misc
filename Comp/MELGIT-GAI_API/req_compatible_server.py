import requests

url = "http://localhost:8000/v1/chat/completions"
headers = {"Content-Type": "application/json"}
data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "あなたは親切なアシスタントです。"},
        {"role": "user", "content": "愛知県はどこにありますか？"}
    ]
}

response = requests.post(url, headers=headers, json=data)
print("Status Code:", response.status_code)
print("Response:", response.json())
