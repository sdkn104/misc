import json
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
#from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
import pandas as pd


def load_emails_from_json(file_path):
    """JSONファイルからメールデータを読み込む"""
    with open(file_path, 'r', encoding='utf-8') as json_file:
        emails = json.load(json_file)
    documents = []
    for email in emails:
        documents.append(Document(
            page_content=email["body"],
            metadata={
                "subject": email["subject"],
                "from": email["from"],
                "to": email["to"],
                "cc": email["cc"],
                "attachments": email.get("attachments", [])
            }
        ))
    print("read JSON", datetime.now())
    return documents

def load_rag_dataset():
    dfq = pd.read_csv("hf://datasets/allganize/RAG-Evaluation-Dataset-JA/rag_evaluation_result.csv")
    dfd = pd.read_csv("hf://datasets/allganize/RAG-Evaluation-Dataset-JA/documents.csv")
    documents = []
    for index, row in dfd.iterrows():
        documents.append(Document(
            page_content=row["title"],
            metadata={
                "domain": row["domain"],
                "file_name": row["file_name"],
                "publisher": row["publisher"]
            }
        ))
    print("read docs", datetime.now())
    return documents

def register_emails_to_vectorstore(documents, vectorstore_path):
    """メールデータをチャンク分割し、RAGのvectorstoreに登録する"""


    # チャンク分割
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunked_documents = text_splitter.split_documents(documents)
    print("split docs", datetime.now())

    # SBERT系のモデル（Hugging Face Hub上のSentenceTransformer）を指定
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # other models
    #embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
    #embeddings = HuggingFaceEmbeddings(model_name="pkshatech/GLuCoSE-base-ja")
    
    # Vectorstoreに登録
    vectorstore = FAISS.from_documents(chunked_documents, embeddings)
    print("vectorstore", datetime.now())
    vectorstore.save_local(vectorstore_path)
    print("vectorstore saved", datetime.now())

def main():
    """メイン処理"""
    input_file = "emails.json"  # メールデータが格納されたJSONファイル
    vectorstore_path = "email_vectorstore"  # Vectorstore保存先

    #docs = load_emails_from_json(input_file)
    docs = load_rag_dataset()
    register_emails_to_vectorstore(docs, vectorstore_path)

    print(f"メールデータをVectorstoreに登録しました。保存先: {vectorstore_path}")

if __name__ == "__main__":
    main()
