import pandas as pd
import json
import requests
from io import BytesIO
from PyPDF2 import PdfReader
from datetime import datetime
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

# CSVファイルのパス
csv_path = "hf://datasets/allganize/RAG-Evaluation-Dataset-JA/documents.csv"
# 出力するJSONファイルのパス
json_path = "rag_documents.json"

def download_pdfs_from_csv(csv_path, output_folder):
    """
    CSVのurl列にあるPDFファイルをoutput_folderにダウンロードする。
    既に同名ファイルが存在する場合はスキップ。
    """
    import os
    import requests
    import pandas as pd

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    df = pd.read_csv(csv_path)
    for idx, row in df.iterrows():
        url = row.get("url", "")
        if url and url.endswith(".pdf"):
            file_name = os.path.basename(url.split("?")[0])
            file_path = os.path.join(output_folder, file_name)
            if os.path.exists(file_path):
                print(f"[SKIP] {file_name} (already exists)")
                continue
            try:
                print(f"[DOWNLOAD] {url} -> {file_path}")
                response = requests.get(url, timeout=60)
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    f.write(response.content)
            except Exception as e:
                print(f"[ERROR] {url}: {e}")
    print("PDFダウンロード完了")

def main():
    csv_path = "hf://datasets/allganize/RAG-Evaluation-Dataset-JA/documents.csv"
    download_folder = "RAG-Evaluation-Dataset-JA"
    print("CSV読み込み...", datetime.now())
    download_pdfs_from_csv(csv_path, download_folder)


if __name__ == "__main__":
    main()
