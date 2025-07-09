import requests
import os

url = "https://melgitgaipoc-03-web.azurewebsites.net/chat-api/session/message/send"
session_id = os.getenv("MELGIT_GAI_API_KEY", "")
user_prompt_text = "愛知県はどこにありますか"
system_prompt_text = "your_system_prompt_text"
file_path = "./sample.txt"  # アップロードしたいファイルのパス

with open(file_path, "rb") as f:
    files = {"Files": f}
    data = {
        "sessionId": session_id,
        "userPromptText": user_prompt_text,
        "systemPromptText": system_prompt_text
    }
    response = requests.post(url, data=data, files=files, verify=False)
    print(response.status_code)
    print(response.text)
