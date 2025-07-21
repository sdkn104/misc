
from flask import Flask, request, jsonify, make_response, Response, stream_with_context
import json
import time
import datetime
import os
import re
import waitress
import logging
from logging.handlers import RotatingFileHandler
from openai import AzureOpenAI
import pprint

#
# OpenAI compatible API server
#

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_random_secret_key'

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
    maxBytes=8 * 1024 * 1024,  # 最大5MB
    backupCount=3,             # 最大3つのバックアップファイル
    encoding='cp932',  # Windowsのデフォルトエンコーディング
    delay=False
)
formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
custom_logger.addHandler(handler)
custom_logger.setLevel(logging.DEBUG) # DEBUGレベル以上のログを記録

# Waitress logging
waitress.logging.basicConfig(level=logging.DEBUG) # Waitressのログ出力条件をDEBUG以上に設定

# Timestamp function
def get_time_stamp():
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S') + f'{int(now.microsecond / 1000):03d}'
    return timestamp


# Log before request and before response
@app.before_request
def log_request_info():
    custom_logger.debug("----- request ---------------------------------------------------------------")
    custom_logger.debug(request)
    custom_logger.debug(request.headers)
    if request.content_type == 'application/json':
        s = pprint.pformat(request.get_json(), compact=True)
        custom_logger.debug(s[:10000])  # Log first 10000 characters of JSON request data
    else:
        custom_logger.debug(request.get_data(as_text=True)[:10000])  # Log first 10000 bytes of request data

@app.after_request
def log_response_info(response):
    custom_logger.debug("----- response ---------------------------------------------------------------")
    custom_logger.debug(response)
    custom_logger.debug(response.headers)
    if response.content_type == 'application/json':
        s = pprint.pformat(response.get_json(), compact=True)
        custom_logger.debug(s[:10000])  # Log first 10000 characters of JSON request data
    else:
        custom_logger.debug(response.get_data(as_text=True)[:10000])  # Log first 1000 bytes of request data
    0
    # One liner access log
    referer = request.referrer or "-"
    user_agent = request.headers.get('User-Agent') or "-"
    auth = request.headers.get('Authorization')
    match = re.search(r"___([^_]*)___", auth)  # embedded string in API KEY string
    log_entry = '{} "{} {} {}" {} {} "{}" "{}" {}'.format(
        request.remote_addr,
        request.method,
        request.path,
        request.environ.get('SERVER_PROTOCOL'),
        response.status_code,
        response.content_length or '-',
        referer,
        user_agent,
        match.group(1) if match else "-"
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
    model = payload.get("model", "")

    # response template for non-streaming response
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
                    "content": "",
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
    # response template for streaming response
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
                    "content":"",
                    "refusal":None,
                },
                "logprobs": None,
                "finish_reason":None
            }
        ]
    }

    # completion handler of constant response (test purpose)
    def completionsHandlerConstant(payload, resp_obj, stream_obj):
        stream = payload.get("stream", False)
        if stream == False:
            resp_obj["choices"][0]["message"]["content"] = "こたえは、エベレスト山です。"
            res = jsonify(resp_obj)
            return res  
        else:
            def generate():
                for i in range(5):
                    stream_obj["choices"][0]["delta"]["content"] = f"チャンク{i+1} "
                    yield "data: " + json.dumps(stream_obj) + "\n\n"
                    time.sleep(2)
                stream_obj["choices"][0]["finish_reason"] = "stop"
                stream_obj["choices"][0]["delta"] = {}
                yield "data: " + json.dumps(stream_obj) + "\n\n"
                yield "data: [DONE]\n\n"

            # Create a streaming response
            res = Response(stream_with_context(generate()), mimetype='text/event-stream')   
            res.headers["Content-Type"] = "text/event-stream; charset=utf-8"
            res.headers['Cache-Control'] = 'no-cache'
            return res
        
    # completion handler using Azure OpenAI
    def completionsHandlerAzure(payload, resp_obj, stream_obj):
        stream = payload.get("stream", False)

        # Azure OpenAI Completions
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME, # model = "deployment_name".
            messages=payload.get("messages", []),
            max_completion_tokens=payload.get("max_completion_tokens", None),
            temperature=payload.get("temperature", None),
            stream=stream, 
        )
        #print(response)

        if stream == False:
            print(response.choices[0].message.content)
            resp_obj["choices"][0]["message"]["content"] = response.choices[0].message.content
            res = jsonify(resp_obj)
            return res
        else:
            def generate():
                responseList = list(response)
                responseLength = len(responseList)
                mes = []
                for i in range(responseLength):
                    chunk = responseList[i]
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        stream_obj["choices"][0]["index"] = i
                        ss = chunk.choices[0].delta.content if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content') else ""
                        ss = ss if ss else ""
                        stream_obj["choices"][0]["delta"]["content"] = ss
                        mes.append(ss)
                        yield "data: " + json.dumps(stream_obj) + "\n\n"                
                #print(mes)
                #print(mes.join(''))
                # stop chunk
                stream_obj["choices"][0]["index"] = i+1
                stream_obj["choices"][0]["finish_reason"] = "stop"
                stream_obj["choices"][0]["delta"] = {}
                yield "data: " + json.dumps(stream_obj) + "\n\n"
                yield "data: [DONE]\n\n"

            # Create a streaming response
            res = Response(stream_with_context(generate()), mimetype='text/event-stream')   
            res.headers["Content-Type"] = "text/event-stream; charset=utf-8"
            res.headers['Cache-Control'] = 'no-cache'
            return res

    #resp = completionsHandlerConstant(payload, resp_obj, stream_obj)
    resp = completionsHandlerAzure(payload, resp_obj, stream_obj)
    #resp = completionsHandlerGAI(payload, resp_obj, stream_obj)
    return resp



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
        waitress.serve(app, host='0.0.0.0', port=5000,
            connection_limit=100,  # default is 100
            threads=4,  # default is 4
            channel_timeout=120, # default is 120 seconds
        )

