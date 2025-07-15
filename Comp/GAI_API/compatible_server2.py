
from flask import Flask, request, jsonify, make_response, Response, stream_with_context
import json
import time

app = Flask(__name__)

# output log
@app.before_request
def log_request_info():
    print("--------------------------------------------------------------------")
    print(request)
    print(request.url)
    print(request.headers)
    print(request.data)
    if request.content_type == 'application/json':
        print(request.get_json())


@app.after_request
def log_response_info(response):
    print("--------------------------------------------------------------------")
    print(response)
    print(response.headers)
    print(response.get_data(as_text=True))
    return response


#@app.errorhandler(404)
#def handle_404(e):
#    return jsonify({"error": "Not found (compatible server error)"}), 404


# OPTIONS
@app.route('/v1/chat/completions', methods=['OPTIONS'])
def options_handler():
    # response to OPTIONS requests
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Chat endpoints
@app.route('/v1/chat/completions', methods=['POST'])
def create_chat_completion():
    payload = request.get_json()
    stream = payload.get("stream", False)
    # index.md: CreateChatCompletionResponse
    resp_obj = {
        "id": "chatcmpl-stub-id",
        "object": "chat.completion",
        "created": 1738960610,
        "model": "gpt-4.1",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello! This is a stub response.",
                    "refusal": None,
                    "tool_calls": None,
                    "annotations": []
                },
                "finish_reason": "stop",
                "logprobs": None
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15
        },
        "service_tier": "default"
    }
    stream_obj = {
        "id":"chatcmpl-123",
        "object":"chat.completion.chunk",
        "created":1694268190,
        "model":"gpt-4o-mini", 
        "system_fingerprint": 
        "fp_44709d6fcb", 
        "choices":[
            {
                "index":0,
                "delta":{
                    "role":"assistant",
                    "content":"chank x",
                    "refusal":None,
                },
                "logprobs": None,
                "finish_reason":None
            }
        ]
    }
    resp = jsonify(resp_obj)
    #print(resp)
    if stream:
        def generate():
            for i in range(5):
                stream_obj["choices"][0]["delta"]["content"] = f"chunk {i+1} "
                if i == 4:
                    stream_obj["choices"][0]["finish_reason"] = "stop"
                    stream_obj["choices"][0]["delta"] = {}
                yield "data: " + json.dumps(stream_obj) + "\n\n"
                time.sleep(2)
            yield "data: [DONE]\n\n"
        res = Response(stream_with_context(generate()), mimetype='text/event-stream')   
        #res.headers['Content-Type'] = 'text/event-stream'
        res.headers['Cache-Control'] = 'no-cache'
        del res.headers['Connection']
        res.headers['Connection'] = 'keep-alive'
        #res.headers['Transfer-Encoding'] = 'chunked'
        #res.headers.pop('Content-Length', None)
        return res
    else:
        return resp

@app.route('/v1/chat/completions/<completion_id>', methods=['DELETE'])
def delete_chat_completion(completion_id):
    # index.md: ChatCompletionDeleted
    return jsonify({
        "object": "chat.completion.deleted",
        "id": completion_id,
        "deleted": True
    })

@app.route('/v1/chat/completions/<completion_id>', methods=['GET'])
def get_chat_completion(completion_id):
    # index.md: CreateChatCompletionResponse
    return jsonify({
        "id": completion_id,
        "object": "chat.completion",
        "created": 1738960610,
        "model": "gpt-4.1",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello! This is a stub response.",
                    "refusal": None,
                    "tool_calls": None,
                    "annotations": []
                },
                "finish_reason": "stop",
                "logprobs": None
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15
        },
        "service_tier": "default"
    })

@app.route('/v1/chat/completions/<completion_id>/messages', methods=['GET'])
def get_chat_completion_messages(completion_id):
    # index.md: ChatCompletionMessageList
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": f"{completion_id}-0",
                "role": "user",
                "content": "write a haiku about ai",
                "name": None,
                "content_parts": None
            }
        ],
        "first_id": f"{completion_id}-0",
        "last_id": f"{completion_id}-0",
        "has_more": False
    })

@app.route('/v1/chat/completions', methods=['GET'])
def list_chat_completions():
    # index.md: ChatCompletionList
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": "chatcmpl-stub-id",
                "object": "chat.completion",
                "created": 1738960610,
                "model": "gpt-4.1",
                "choices": [],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "total_tokens": 15
                },
                "service_tier": "default"
            }
        ],
        "first_id": "chatcmpl-stub-id",
        "last_id": "chatcmpl-stub-id",
        "has_more": False
    })

@app.route('/v1/chat/completions/<completion_id>', methods=['POST'])
def update_chat_completion(completion_id):
    # index.md: CreateChatCompletionResponse
    return jsonify({
        "id": completion_id,
        "object": "chat.completion",
        "created": 1738960610,
        "model": "gpt-4.1",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Metadata updated (stub)",
                    "refusal": None,
                    "tool_calls": None,
                    "annotations": []
                },
                "finish_reason": "stop",
                "logprobs": None
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15
        },
        "service_tier": "default"
    })

# Completions endpoint
@app.route('/v1/completions', methods=['POST'])
def create_completion():
    # index.md: CreateCompletionResponse
    return jsonify({
        "id": "cmpl-stub-id",
        "object": "text_completion",
        "created": 1738960610,
        "model": "gpt-3.5-turbo-instruct",
        "choices": [
            {
                "text": "This is a stub completion.",
                "index": 0,
                "logprobs": None,
                "finish_reason": "length"
            }
        ],
        "usage": {
            "prompt_tokens": 5,
            "completion_tokens": 7,
            "total_tokens": 12
        }
    })

# Models endpoints
@app.route('/v1/models/<model>', methods=['DELETE'])
def delete_model(model):
    # index.md: DeleteModelResponse
    return jsonify({
        "id": model,
        "object": "model",
        "deleted": True
    })

@app.route('/v1/models', methods=['GET'])
def list_models():
    # index.md: ListModelsResponse
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": "model-id-0",
                "object": "model",
                "created": 1686935002,
                "owned_by": "organization-owner"
            }
        ]
    })

@app.route('/v1/models/<model>', methods=['GET'])
def retrieve_model(model):
    # index.md: Model
    return jsonify({
        "id": model,
        "object": "model",
        "created": 1686935002,
        "owned_by": "openai"
    })

# any other endpoint
@app.route('/xxx/<path:anything>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def catch_all(anything):
    log_request_info()
    return jsonify({"error": "No endpoint matched", "path": anything}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
