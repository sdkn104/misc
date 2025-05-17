from flask import Flask, render_template_string, request
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain import hub

app = Flask(__name__)

# 初期化（グローバルで一度だけロード）
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("email_vectorstore", embeddings, allow_dangerous_deserialization=True)
llm = ChatOpenAI()
retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
print("retrieval_qa_chat_prompt", retrieval_qa_chat_prompt)
combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
retriever = vectorstore.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

HTML = '''
<!doctype html>
<title>RAGメール検索</title>
<h1>RAGメール検索</h1>
<form method=post>
  質問: <input type=text name=query size=60 autofocus>
  <input type=submit value=検索>
</form>
{% if response %}
  <h2>=== 回答 ===</h2>
  <b>質問:</b> {{ query }}<br>
  <b>回答:</b> {{ response['answer'] }}<br>
  <h2>=== 検索結果 ===</h2>
  {% for i, result in results %}
    <div style="border:1px solid #ccc; margin:10px; padding:10px; background-color:#f0f0f0;">
      <b>結果 {{ i }}:</b><br>
      <b>件名:</b> {{ result.metadata.get('subject', '不明') }}<br>
      <b>日時:</b> {{ result.metadata.get('date', '不明') }}<br>
      <b>差出人:</b> {{ result.metadata.get('sender', '不明') }}<br>
      <pre>{{ result.page_content }}</pre>
    </div>
  {% endfor %}
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    query = ''
    if request.method == 'POST':
        query = request.form['query']
        response = retrieval_chain.invoke({"input": query})
        #print(response)
    return render_template_string(HTML, response=response, query=query, results=list(enumerate(response['context'], 1)) if response else None)


if __name__ == "__main__":
    app.run(debug=True)
