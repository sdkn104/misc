from langchain_community.vectorstores import FAISS
#from langchain.llms import OpenAI
from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_community.llms import OpenAI

#from langchain_openai import OpenAI
from langchain_openai import AzureChatOpenAI 

# Initialize the SBERT model globally
#sbert_model = SentenceTransformer('all-MiniLM-L6-v2')



def query_rag():
    """RAGに問い合わせを行い、結果を表示し、回答を生成する"""
    # ベクトルストアのロード
    vectorstore_path = "email_vectorstore"  # ベクトルストアのパス

    # SBERT系のモデル（Hugging Face Hub上のSentenceTransformer）を指定
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # model  E5
    #embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")

    #vectorstore = FAISS.load_local(vectorstore_path, sbert_model.encode, allow_dangerous_deserialization=True)
    vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    # Vectorstoreファイルを読み出す

    # LLMの初期化
    #llm = OpenAI()
    llm = AzureChatOpenAI (
        deployment_name="gpt-4.1",  # Azure OpenAIのデプロイメント名を指定
        model="gpt-4.1",  # https://ai.azure.com/　でデプロイしたモデル
    )
    print(llm)


    while True:
        # ユーザからの問い合わせを受け取る
        query = input("質問を入力してください (終了するには 'exit' と入力): ")
        if query.lower() == 'exit':
            print("終了します。")
            break

        # RAGに問い合わせ
        results = vectorstore.similarity_search_with_score(query, k=5)  # スコア付き検索

        # 結果を表示
        print("\n=== 検索結果 ===")
        for i, (result, score) in enumerate(results, 1):
            print(f"結果 {i}:")
            print(f"スコア: {score}")  # スコアを表示
            for key in result.metadata:
                print(f"{key}:** {result.metadata.get(key, '不明')}")
            print(result.page_content)
            print("\n-------------------------------------------------------------\n")

        # 検索結果を基に回答を生成
        combined_content = "\n".join([result.page_content for result, _ in results])
        prompt = f"以下の情報を基に、質問に対する回答を作成してください:\n\n{combined_content}\n\n質問: {query}"
        #answer = llm(prompt)
        answer = llm.invoke(prompt)

        print("\n=== 回答 ===")
        print(f"質問: {query}")
        print(f"回答: {answer}")
        print("\n---\n")

if __name__ == "__main__":
    query_rag()