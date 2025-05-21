from flask import Flask, render_template_string, request
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI

app = Flask(__name__)

# 初期化（グローバルで一度だけロード）
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#vectorstore = FAISS.load_local("email_vectorstore", embeddings, allow_dangerous_deserialization=True)
vectorstore = FAISS.load_local("pdf_vectorstore", embeddings, allow_dangerous_deserialization=True)
llm = OpenAI(temperature=0.7)
#llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

HTML = '''
<!doctype html>
<title>RAGメール検索</title>
<h1>RAGメール検索</h1>
<form method=post>
  質問: <input type=text name=query size=60 autofocus>
  <input type=submit value=検索>
</form>
{% if results %}
  <h2>=== 検索結果 ===</h2>
  {% for i, (result, score) in items %}
    <div style="border:1px solid #ccc; margin:10px; padding:10px; background-color:#f0f0f0;">
      <b>結果 {{ i }}:</b><br>
      <b>ファイル名:</b> {{ result.metadata.get('file_path', '不明') }}<br>
      <b>件名:</b> {{ result.metadata.get('subject', '不明') }}<br>
      <b>日時:</b> {{ result.metadata.get('date', '不明') }}<br>
      <b>差出人:</b> {{ result.metadata.get('sender', '不明') }}<br>
      <b>スコア:</b> {{ score }}<br>
      <pre>{{ result.page_content }}</pre>
    </div>
  {% endfor %}
  <h2>=== 回答 ===</h2>
  <b>質問:</b> {{ query }}<br>
  <b>回答:</b> {{ answer }}<br>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    answer = None
    query = ''
    if request.method == 'POST':
        query = request.form['query']
        results = vectorstore.similarity_search_with_score(query, k=3)
        combined_content = "\n".join([result.page_content for result, _ in results])
        prompt = f"以下の情報を基に、質問に対する回答を作成してください:\n\n{combined_content}\n\n質問: {query}"
        answer = llm(prompt)

    return render_template_string(HTML, results=results, answer=answer, query=query, items=list(enumerate(results, 1)) if results else None)


if __name__ == "__main__":
    app.run(debug=True)
