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


def extract_text_from_local_pdf(pdf_path):
    """ローカルPDFファイルからテキスト抽出"""
    try:
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"[WARN] PDF抽出失敗: {pdf_path} ({e})")
        return ""

def add_text_column_from_local_pdfs_and_save_json(csv_path, pdf_folder, json_path):
    """
    CSVのfile_name列のPDFをpdf_folderから読み出してテキスト抽出し、text列に追加してJSONで保存
    """
    df = pd.read_csv(csv_path)
    texts = []
    for idx, row in df.iterrows():
        file_name = row.get("file_name", "")
        pdf_path = os.path.join(pdf_folder, file_name) if file_name else None
        if file_name and os.path.exists(pdf_path):
            text = extract_text_from_local_pdf(pdf_path)
        else:
            text = ""
        texts.append(text)
        if (idx+1) % 10 == 0:
            print(f"{idx+1}件処理済み: {file_name}", datetime.now())
    df["text"] = texts
    df.to_json(json_path, orient="records", force_ascii=False, indent=2)
    print(f"JSONファイルに保存しました: {json_path}")

def main():
    csv_path = "hf://datasets/allganize/RAG-Evaluation-Dataset-JA/documents.csv"
    download_folder = "RAG-Evaluation-Dataset-JA"
    # 出力するJSONファイルのパス
    json_path = "rag_dataset.json"

    print("開始", datetime.now())
    add_text_column_from_local_pdfs_and_save_json(csv_path, download_folder, json_path)
    print("完了", datetime.now())

if __name__ == "__main__":
    main()
