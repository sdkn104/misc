# OpenAI Python client: Chat Completion with streaming response
import os
import openai
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
#OPENAI_API_BASE = "http://localhost:5000/v1"  # Use local server for testing

client = OpenAI(base_url=OPENAI_API_BASE, api_key=OPENAI_API_KEY)

stream = True

response = client.chat.completions.create(
    model="gpt-4.1",  # or your deployed model name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "what is tallest mountain in the world? answer in one word."}
    ],
    stream=stream
)

print(response)
if stream is False:
    print(response.choices[0].message.content)
else:
    contents = []
    for chunk in response:
        print(chunk)
        if chunk.choices:
            delta = chunk.choices[0].delta
            contents.append(delta.content if delta.content else "")
    print("message: ", "".join(contents))