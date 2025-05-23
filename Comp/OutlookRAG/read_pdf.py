import os
import glob
import json
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List

try:
    from PyPDF2 import PdfReader
except ImportError:
    raise ImportError("PyPDF2 is required. Please install it with 'pip install PyPDF2'.")

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_pdfs_from_folder_as_dict(folder_path: str):
    """Load all PDFs from a folder and return as a list of dicts (with 'text' and 'source')."""
    pdf_files = glob.glob(os.path.join(folder_path, '*.pdf'))
    pdf_list = []
    for pdf_file in pdf_files:
        text = extract_text_from_pdf(pdf_file)
        print(text)
        pdf_list.append({
            "text": text,
            "source": os.path.basename(pdf_file)
        })
    return pdf_list

def main():
    docs_folder = "docs"  # Folder containing PDF files
    vectorstore_path = "pdf_vectorstore"  # Output vectorstore path
    pdfs = load_pdfs_from_folder_as_dict(docs_folder)
    print("取得したPDF数:", len(pdfs))
    with open("pdfs.json", "w", encoding="utf-8") as f:
        json.dump(pdfs, f, indent=4)


if __name__ == "__main__":
    main()
