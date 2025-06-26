#from sentence_transformers import SentenceTransformer
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings


import requests
#import certifi

response = requests.get('https://www.google.com')
print(response.text)

#response = requests.get('https://example.com', verify=certifi.where())
#print(response.text)


def register_emails_to_vectorstore(emails, vectorstore_path):

    # SBERT系のモデル（Hugging Face Hub上のSentenceTransformer）を指定
    #model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("モデルのロード完了")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def main():
    """メイン処理"""
    input_file = "emails.json"  # メールデータが格納されたJSONファイル
    vectorstore_path = "email_vectorstore"  # Vectorstore保存先

    register_emails_to_vectorstore(None, vectorstore_path)


if __name__ == "__main__":
    main()
