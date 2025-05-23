import json
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
#from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
import pandas as pd


def load_docs_from_json(file_path, text_key="text"):
    """JSONファイルからメールデータを読み込む"""
    with open(file_path, 'r', encoding='utf-8') as json_file:
        items = json.load(json_file)
    documents = []
    for item in items:
        page_content = item.pop(text_key, None)
        documents.append(Document(
            page_content=page_content,
            metadata=item
        ))
    print("read JSON", datetime.now())
    return documents

def register_docs_to_vectorstore(documents, vectorstore_path):
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
    content_key = "body"  # JSONのテキストキー

    input_file = "pdfs.json"  # メールデータが格納されたJSONファイル
    vectorstore_path = "pdfs_vectorstore"  # Vectorstore保存先
    content_key = "text"  # JSONのテキストキー

    input_file = "rag_dataset.json"  # メールデータが格納されたJSONファイル
    vectorstore_path = "rag_dataset_vectorstore"  # Vectorstore保存先
    content_key = "text"  # JSONのテキストキー

    docs = load_docs_from_json(input_file, content_key)
    register_docs_to_vectorstore(docs, vectorstore_path)

    print(f"データをVectorstoreに登録しました。入力データ: {input_file} 保存先: {vectorstore_path}")

if __name__ == "__main__":
    main()
