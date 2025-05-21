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
    vectorstore_path = "rag_dataset_vectorstore"

    print("CSV読み込み...", datetime.now())
    download_pdfs_from_csv(csv_path, "RAG-Evaluation-Dataset-JA")

    add_text_column_from_local_pdfs_and_save_json(csv_path, "RAG-Evaluation-Dataset-JA", json_path)
    print("PDFテキスト抽出完了", datetime.now())
    # JSONファイルを読み込む
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # DataFrameに変換
    df = pd.DataFrame(data)  
    # Documentリスト作成
    documents = []
    for _, row in df.iterrows():
        documents.append(Document(
            page_content=row.get("text", ""),
            metadata={
                "title": row.get("title", ""),
                "domain": row.get("domain", ""),
                "file_name": row.get("file_name", ""),
                "publisher": row.get("publisher", ""),
                "url": row.get("url", "")
            }
        ))
    print("Documentリスト作成完了", datetime.now())

    # チャンク分割
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunked_documents = text_splitter.split_documents(documents)
    print("チャンク分割完了", datetime.now())

    # 埋め込み生成
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunked_documents, embeddings)
    print("Vectorstore作成完了", datetime.now())
    vectorstore.save_local(vectorstore_path)
    print(f"Vectorstore保存先: {vectorstore_path}", datetime.now())

if __name__ == "__main__":
    main()
