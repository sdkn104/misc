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

def load_pdfs_from_folder(folder_path: str) -> List[Document]:
    """Load all PDFs from a folder and return as Document list."""
    pdf_files = glob.glob(os.path.join(folder_path, '*.pdf'))
    documents = []
    for pdf_file in pdf_files:
        text = extract_text_from_pdf(pdf_file)
        documents.append(Document(
            page_content=text,
            metadata={"source": os.path.basename(pdf_file)}
        ))
    return documents

def register_pdfs_to_vectorstore(docs_folder: str, vectorstore_path: str):
    """Extract text from PDFs, split, embed, and register to vectorstore."""
    documents = load_pdfs_from_folder(docs_folder)
    print(f"Loaded {len(documents)} PDFs", datetime.now())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunked_documents = text_splitter.split_documents(documents)
    print("Split docs", datetime.now())
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunked_documents, embeddings)
    print("Vectorstore created", datetime.now())
    vectorstore.save_local(vectorstore_path)
    print(f"Vectorstore saved to {vectorstore_path}", datetime.now())

def main():
    docs_folder = "docs"  # Folder containing PDF files
    vectorstore_path = "pdf_vectorstore"  # Output vectorstore path
    register_pdfs_to_vectorstore(docs_folder, vectorstore_path)
    print(f"PDFs registered to vectorstore at: {vectorstore_path}")

if __name__ == "__main__":
    main()
