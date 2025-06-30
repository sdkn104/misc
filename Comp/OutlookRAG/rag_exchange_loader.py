import json
from exchangelib import Account, DELEGATE, FileAttachment, Credentials, Configuration
from exchangelib.queryset import Q
from datetime import datetime, timedelta
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

"""
exchangelibを使って指定期間のメールを取得しlangchainのDocumentのリストに保存する。
メールは、件名、From, To, Cc, 本文、添付ファイルを取得する。
取得後、リストをJSON形式でファイルに保存する。
exhangelibはwindows環境でSSO認証とする。つまりWindowsのユーザ名とパスワードを使う。
取得したリストを、チャンク分割して、RAGのvectorstoreに登録する。SBERTモデルを使う。
プログラムはrag_exchange_loader.pyという名前とする。
"""

def fetch_emails_to_documents_and_register(start_date, end_date, output_file, vectorstore_path):
    """指定期間のメールを取得し、Documentリストに保存し、RAGのvectorstoreに登録する"""
    print(os.getenv('USER_PASSWORD'))
    credentials = Credentials("QP48568@ad.melco.co.jp", os.getenv('USER_PASSWORD'))  # 環境変数からパスワードを取得
    # credentials = Credentials(username=os.getenv('USER_NAME'), password=os.getenv('USER_PASSWORD'))  # 環境変数からユーザ名とパスワードを取得
    config = Configuration(
        server='outlook.office365.com',
        credentials=credentials)
    account = Account("outlook_833CF429345F53E4@outlook.com", config=config, autodiscover=False, access_type=DELEGATE)

    #account = Account(primary_smtp_address=os.getenv('USER_EMAIL'), autodiscover=True, access_type=DELEGATE)
    #account = Account("outlook_833CF429345F53E4@outlook.com", autodiscover=True, access_type=DELEGATE)

    # 指定期間のメールを取得
    documents = []
    emails = []
    for item in account.inbox.filter(Q(datetime_received__gte=start_date) & Q(datetime_received__lte=end_date)):
        email_data = {
            "subject": item.subject,
            "from": item.sender.email_address if item.sender else "不明",
            "to": [recipient.email_address for recipient in item.to_recipients] if item.to_recipients else [],
            "cc": [recipient.email_address for recipient in item.cc_recipients] if item.cc_recipients else [],
            "body": item.text_body or "",
            "attachments": []
        }

        # 添付ファイルを取得
        for attachment in item.attachments:
            if isinstance(attachment, FileAttachment):
                email_data["attachments"].append(attachment.name)

        emails.append(email_data)

        # Documentリストに追加
        documents.append(Document(
            page_content=email_data["body"],
            metadata={
                "subject": email_data["subject"],
                "from": email_data["from"],
                "to": email_data["to"],
                "cc": email_data["cc"],
                "attachments": email_data["attachments"]
            }
        ))

    # チャンク分割
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunked_documents = text_splitter.split_documents(documents)

    # SBERTモデルを使った文書埋め込み生成
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedded_texts = [model.encode(doc.page_content) for doc in chunked_documents]

    # Vectorstoreに登録
    vectorstore = FAISS.from_embeddings(embedded_texts, chunked_documents)
    vectorstore.save_local(vectorstore_path)

def main():
    """メイン処理"""
    # 取得期間を指定
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)  # 過去7日間
    output_file = "emails.json"  # 保存先ファイル名
    vectorstore_path = "email_vectorstore"  # Vectorstore保存先

    fetch_emails_to_documents_and_register(start_date, end_date, output_file, vectorstore_path)
    print(f"メールを {output_file} に保存し、Vectorstoreに登録しました。")

if __name__ == "__main__":
    main()