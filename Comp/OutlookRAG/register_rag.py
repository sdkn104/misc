import json
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

def load_emails_from_json(file_path):
    """JSONファイルからメールデータを読み込む"""
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def register_emails_to_vectorstore(emails, vectorstore_path):
    """メールデータをチャンク分割し、RAGのvectorstoreに登録する"""
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

    # チャンク分割
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunked_documents = text_splitter.split_documents(documents)
    print("split docs", datetime.now())

    # SBERTモデルを使った文書埋め込み生成
    #model = SentenceTransformer('all-MiniLM-L6-v2')
    #embedded_texts = [model.encode(doc.page_content) for doc in chunked_documents]
    #print(3, datetime.now())

    # Vectorstoreに登録
    #vectorstore = FAISS.from_embeddings(embedded_texts, chunked_documents)
    #print(4, datetime.now())
    #vectorstore.save_local(vectorstore_path)
    #print(5, datetime.now())

    # SBERT系のモデル（Hugging Face Hub上のSentenceTransformer）を指定
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Vectorstoreに登録
    vectorstore = FAISS.from_documents(chunked_documents, embeddings)
    print("vectorstore", datetime.now())
    vectorstore.save_local(vectorstore_path)
    print("vectorstore saved", datetime.now())

def main():
    """メイン処理"""
    input_file = "emails.json"  # メールデータが格納されたJSONファイル
    vectorstore_path = "email_vectorstore"  # Vectorstore保存先

    emails = load_emails_from_json(input_file)
    register_emails_to_vectorstore(emails, vectorstore_path)

    print(f"メールデータをVectorstoreに登録しました。保存先: {vectorstore_path}")

if __name__ == "__main__":
    main()
