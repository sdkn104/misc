  
import os  
from openai import AzureOpenAI  

endpoint = os.getenv("ENDPOINT_URL", "https://test-openai-999.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "")  

# キーベースの認証を使用して Azure OpenAI クライアントを初期化する
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",  
)  
    
# チャット プロンプトを準備する  
chat_prompt = [
    {
        "role": "system",
        "content": "情報を見つけるのに役立つ AI アシスタントです。"
    },
    {
        "role": "user",
        "content": "ホストコンピュータとは"
    },
    {
        "role": "assistant",
        "content": ""
    }
]  
    
# 音声認識が有効になっている場合は音声結果を含める  
speech_result = chat_prompt  

# 入力候補を生成する  
completion = client.chat.completions.create(  
    model=deployment,  
    messages=speech_result,  
    #past_messages=10,  
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,  
    stop=None,  
    stream=False  
)  
    
print(completion.to_json())  
    