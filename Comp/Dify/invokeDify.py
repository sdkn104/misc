import requests
import json
from pprint import pprint 

API_URL = 'http://localhost/v1/workflows/run'
API_KEY = 'app-OnwXBcpyMhNjQpo8V1hW01IO'  # ここに実際のAPIキーを入力してください

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

data = {
    "inputs": {"pdf_file": "https://www.pref.kyoto.jp/kenkoshishin/documents/001_012.pdf"},
    "response_mode": "blocking",
    "user": "sdkn104@gmail.com"
}

response = requests.post(API_URL, headers=headers, data=json.dumps(data), stream=True)
pprint(response.json())
