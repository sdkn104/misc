from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.get_json()
    print(data)
    messages = data.get('messages', [])
    # シンプルな応答例: 最後のuserメッセージをそのまま返す
    user_message = next((m['content'] for m in reversed(messages) if m['role'] == 'user'), "")
    response = {
        "id": f"chatcmpl-{uuid.uuid4()}",
        "object": "chat.completion",
        "created": int(uuid.uuid1().time // 1e7),
        "model": data.get('model', 'gpt-3.5-turbo'),
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"Echo: {user_message}"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
