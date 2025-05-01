import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import os

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
    """メールフォルダ内のファイルを読み込み、RAGに登録する"""
    preprocess_files(email_folder)

    documents = []

    # Iterate over files manually
    for root, _, files in os.walk(email_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                documents.append(Document(page_content=content, metadata={"file_path": file_path}))
            except Exception as e:
                print(f"Skipping problematic file {file_path}: {e}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)

    vectorstore.save_local("email_vectorstore")

if __name__ == "__main__":
    email_folder = "mail"  # メールフォルダのパス
    if os.path.exists(email_folder):
        load_and_register_emails(email_folder)
    else:
        print(f"メールフォルダが見つかりません: {email_folder}")