from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI

def query_rag():
    """RAGに問い合わせを行い、結果を表示し、回答を生成する"""
    # ベクトルストアのロード
    vectorstore = FAISS.load_local("email_vectorstore", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

    # LLMの初期化
    llm = OpenAI(temperature=0.7)

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
            print(f"ファイル名: {result.metadata.get('file_path', '不明')}")  # ファイル名を表示
            print(f"件名: {result.metadata.get('subject', '不明')}")  # 件名を表示
            print(f"日時: {result.metadata.get('date', '不明')}")  # 日時を表示
            print(f"差出人: {result.metadata.get('sender', '不明')}")  # 差出人を表示
            print(f"スコア: {score}")  # スコアを表示
            print(result.page_content)
            print("\n-------------------------------------------------------------\n")

        # 検索結果を基に回答を生成
        combined_content = "\n".join([result.page_content for result, _ in results])
        prompt = f"以下の情報を基に、質問に対する回答を作成してください:\n\n{combined_content}\n\n質問: {query}"
        answer = llm(prompt)

        print("\n=== 回答 ===")
        print(f"質問: {query}")
        print(f"回答: {answer}")
        print("\n---\n")

if __name__ == "__main__":
    query_rag()