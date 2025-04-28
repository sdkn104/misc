from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# チャット履歴を保存するリスト
chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'メッセージが空です。'}), 400

    # 簡単な応答ロジック
    bot_response = f"あなたのメッセージ: {user_message}"
    chat_history.append({'user': user_message, 'bot': bot_response})

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)