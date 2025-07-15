
from flask import Flask, request, jsonify, make_response, Response, stream_with_context
import json
import time
import datetime
import os
from waitress import serve
import logging
from logging.handlers import RotatingFileHandler
from openai import AzureOpenAI

app = Flask(__name__)

# OpenAI compatible API server

# Azure OpenAI API settings
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "")
COMPATIBLE_MODEL_NAME = os.getenv("COMPATIBLE_MODEL_NAME", "gpt-4.1")
client = AzureOpenAI(  
    azure_endpoint=AZURE_OPENAI_ENDPOINT,  
    api_key=AZURE_OPENAI_API_KEY,  
    api_version=OPENAI_API_VERSION,  # Use the latest API version
)  

# デフォルトログの設定(flask, weitressからのログの設定)
logging.basicConfig(
    filename='flask_system.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# カスタムロガー設定
custom_logger = logging.getLogger("custom")
#handler = logging.FileHandler("flask_custom.log", mode='a', encoding='utf-8')
handler = RotatingFileHandler(
    filename='flask_custom.log',
    mode='a',
    maxBytes=5 * 1024 * 1024,  # 最大5MB
    backupCount=3,             # 最大3つのバックアップファイル
    encoding='utf-8',
    delay=False
)
formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
custom_logger.addHandler(handler)
custom_logger.setLevel(logging.INFO)

# Timestamp function
def get_time_stamp():
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S') + f'{int(now.microsecond / 1000):03d}'
    return timestamp


# Log for request and response
@app.before_request
def log_request_info():
    print("----- request ---------------------------------------------------------------")
    print(request)
    print(request.headers)
    if request.content_type == 'application/json':
        print(request.get_json())
    else:
        print(request.data)

@app.after_request
def log_response_info(response):
    print("----- response ---------------------------------------------------------------")
    print(response)
    print(response.headers)
    print(response.get_data(as_text=True))
    
    # access log
    referer = request.referrer or "-"
    user_agent = request.headers.get('User-Agent') or "-"
    log_entry = '{} "{} {} {}" {} {} "{}" "{}"'.format(
        request.remote_addr,
        request.method,
        request.path,
        request.environ.get('SERVER_PROTOCOL'),
        response.status_code,
        response.content_length or '-',
        referer,
        user_agent
    )
    custom_logger.info(log_entry)

    return response

#@app.errorhandler(404)
#def handle_404(e):
#    return jsonify({"error": "Not found (compatible server error)"}), 404


# OPTIONS request handler
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
    timestamp = get_time_stamp()

    payload = request.get_json()
    stream = payload.get("stream", False)
    model = payload.get("model", "")

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME, # model = "deployment_name".
        messages=payload.get("messages", []),
        max_completion_tokens=payload.get("max_completion_tokens", None),
        temperature=payload.get("temperature", None),
        stream=stream, 
    )

    # index.md: CreateChatCompletionResponse
    if stream == False:
        print(response.choices[0].message.content)
        resp_obj = {
            "id": f"chatcmpl-stub-{timestamp}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response.choices[0].message.content,
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
    else:
        stream_obj = {
            "id": f"chatcmpl-stub-{timestamp}",
            "object":"chat.completion.chunk",
            "created":int(time.time()),
            "model":model, 
            "system_fingerprint": "fp_abcdefg1234", 
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

        def generate2():
            lis = list(response)
            l = len(lis)
            for i in range(l):
                chunk = lis[i]
                if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                    stream_obj["choices"][0]["index"] = i
                    stream_obj["choices"][0]["delta"]["content"] = chunk.choices[0].delta.content if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content') else ""
                    if i == l - 1:
                        stream_obj["choices"][0]["finish_reason"] = "stop"
                        stream_obj["choices"][0]["delta"] = {}
                    yield "data: " + json.dumps(stream_obj) + "\n\n"
            yield "data: [DONE]\n\n"

        res = Response(stream_with_context(generate2()), mimetype='text/event-stream')   
        res.headers["Content-Type"] = "text/event-stream; charset=utf-8"
        res.headers['Cache-Control'] = 'no-cache'
        #del res.headers['Connection']
        res.headers['Connection'] = 'keep-alive'
        #res.headers['Transfer-Encoding'] = 'chunked'
        #res.headers.pop('Content-Length', None)
        return res
    else:
        res = jsonify(resp_obj)
        return res



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
                "id": COMPATIBLE_MODEL_NAME,
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
        "owned_by": "organization-owner"
    })

# any other endpoint
#@app.route('/<path:anything>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
#def catch_all(anything):
#    #log_request_info()
#    return jsonify({"error": "No endpoint matched", "path": anything}), 404


# Run the server
developmentMode = False
if __name__ == '__main__':
    if developmentMode == True:
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        print('Starting Waitress server...')
        serve(app, host='0.0.0.0', port=5000,
            connection_limit=100,  # default is 100
            threads=4,  # default is 4
            channel_timeout=120, # default is 120 seconds
        )

