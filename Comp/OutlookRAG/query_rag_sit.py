import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAI

# 初期化（グローバルで一度だけロード）
@st.cache_resource
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    #vectorstore = FAISS.load_local("email_vectorstore", embeddings, allow_dangerous_deserialization=True)
    vectorstore = FAISS.load_local("rag_dataset_vectorstore", embeddings, allow_dangerous_deserialization=True)
    return vectorstore

@st.cache_resource
def load_llm():
    return OpenAI(temperature=0.7)

st.title("RAG メール検索 (Streamlit版)")
st.write("メールベクトルストアに対して自然言語で検索・質問できます。")

query = st.text_input("質問を入力してください", "")

if query:
    vectorstore = load_vectorstore()
    llm = load_llm()
    results = vectorstore.similarity_search_with_score(query, k=5)

    st.subheader("=== 検索結果 ===")
    for i, (result, score) in enumerate(results, 1):
        with st.expander(f"結果 {i} | スコア: {score}"):
            st.write(f"**ファイル名:** {result.metadata.get('file_path', '不明')}")
            st.write(f"**件名:** {result.metadata.get('subject', '不明')}")
            st.write(f"**日時:** {result.metadata.get('date', '不明')}")
            st.write(f"**差出人:** {result.metadata.get('sender', '不明')}")
            st.write(result.page_content)

    combined_content = "\n".join([result.page_content for result, _ in results])
    prompt = f"以下の情報を基に、質問に対する回答を作成してください:\n\n{combined_content}\n\n質問: {query}"
    answer = llm(prompt)

    st.subheader("=== 回答 ===")
    st.write(f"**質問:** {query}")
    st.write(f"**回答:** {answer}")
