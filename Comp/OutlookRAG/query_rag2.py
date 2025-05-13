from langchain_community.vectorstores import FAISS
#from langchain.llms import OpenAI
from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
#from langchain_community.chat_models import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain import hub

# Initialize the SBERT model globally
#sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

def query_rag():
    """RAGに問い合わせを行い、結果を表示し、回答を生成する"""
    # SBERT系のモデル（Hugging Face Hub上のSentenceTransformer）を指定
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # ベクトルストアのロード
    #vectorstore = FAISS.load_local("email_vectorstore", sbert_model.encode, allow_dangerous_deserialization=True)
    vectorstore = FAISS.load_local("email_vectorstore", embeddings, allow_dangerous_deserialization=True)

    # LLMの初期化
    llm = ChatOpenAI()

    # チャット用プロンプトの取得
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    # 文書統合チェーンの作成
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    # Retrieverを取得
    retriever = vectorstore.as_retriever()
    # Retrieval Chainの作成
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    while True:
        # ユーザからの問い合わせを受け取る
        query = input("質問を入力してください (終了するには 'exit' と入力): ")
        if query.lower() == 'exit':
            print("終了します。")
            break

        # クエリの実行
        response = retrieval_chain.invoke({"input": query})
        print(response)

        # 結果を表示
        print("\n=== 検索結果 ===")
        for i, result in enumerate(response["context"], 1):
            print(f"結果 {i}:")
            #print(f"ファイル名: {result.metadata.get('file_path', '不明')}")  # ファイル名を表示
            print(f"件名: {result.metadata.get('subject', '不明')}")  # 件名を表示
            print(f"日時: {result.metadata.get('date', '不明')}")  # 日時を表示
            print(f"差出人: {result.metadata.get('sender', '不明')}")  # 差出人を表示
            #print(f"スコア: {score}")  # スコアを表示
            print(result.page_content)
            print("\n-------------------------------------------------------------\n")

        answer = response["answer"]
        print("\n=== 回答 ===")
        print(f"質問: {query}")
        print(f"回答: {answer}")
        print("\n---\n")

if __name__ == "__main__":
    query_rag()