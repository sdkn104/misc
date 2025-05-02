import os
from email import message_from_string
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document
from datetime import datetime

def preprocess_files(folder):
    """Preprocess files to ensure consistent encoding."""
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

def load_and_register_emails(email_folder='mail'):
    """
    メールフォルダ内のファイルを読み込み、RAGに登録する
    """
    preprocess_files(email_folder)

    documents = []

    # Iterate over files manually
    print(datetime.now())
    print("メールフォルダの読み込みを開始します...")
    for root, _, files in os.walk(email_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse email metadata
                email_message = message_from_string(content)
                subject = email_message.get('Subject', '不明')
                date = email_message.get('Date', '不明')
                sender = email_message.get('From', '不明')

                documents.append(Document(
                    page_content=content,
                    metadata={
                        "file_path": file_path,
                        "subject": subject,
                        "date": date,
                        "sender": sender
                    }
                ))
            except Exception as e:
                print(f"Skipping problematic file {file_path}: {e}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    print(datetime.now())

    # SBERTモデルを使った文書埋め込み生成
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    # FAISS を利用して、文書をベクトルストアに変換しインデックスを作成
    vectorstore = FAISS.from_documents(texts, embeddings)
    print(datetime.now())

    vectorstore.save_local("email_vectorstore")
    print(datetime.now())

if __name__ == "__main__":
    email_folder = "mail"  # メールフォルダのパス
    if os.path.exists(email_folder):
        load_and_register_emails(email_folder)
    else:
        print(f"メールフォルダが見つかりません: {email_folder}")