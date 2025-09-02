import requests
import json
from pprint import pprint 

API_URL = 'http://meia9dbc/v1/workflows/run'
API_KEY = 'app-phZFYzXjkmKtDASnWL8u1ynb'  # ここに実際のAPIキーを入力してください

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# http://www2.hin.mei.melco.co.jp:41414/file/KOSYOU/2258/q2258004.pdf
# https://www.pref.kyoto.jp/kenkoshishin/documents/001_012.pdf
data = {
    "inputs": {"pdf_file": "http://www2.hin.mei.melco.co.jp:41414/file/KOSYOU/2258/q2258004.pdf"},
    "response_mode": "blocking",
    "user": "sadakane.toshiyuki@aj.mitsubishielectric.co.jp"
}

response = requests.post(API_URL, headers=headers, data=json.dumps(data), stream=True)
pprint(response.json())

