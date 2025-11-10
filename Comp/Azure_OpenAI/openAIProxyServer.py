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
import sys
import requests
sys.path.append(os.path.dirname(__file__))

###########################################################################
# OpenAI / Azure OpenAI Proxy Server
###########################################################################

# Server settings
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 5000
developmentMode = True

# Log settings
HTTP_LOG_TRIM_LENGTH = 1000000  # 1,000,000 characters
LOG_FOLDER = 'log/'

# Model names
MODEL_AZURE = "AZURE"

# API Key
def checkAPIKey():
    auth = request.headers.get('Authorization') or ""
    match = re.search(r"_x_(.*)_x_", auth)  # embedded string in API KEY string
    return match.group(1) if match else "-"

# flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_random_secret_key'

# Azure OpenAI API settings
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "")
client = AzureOpenAI(  
    azure_endpoint=AZURE_OPENAI_ENDPOINT,  
    api_key=AZURE_OPENAI_API_KEY,  
    api_version=OPENAI_API_VERSION,  # Use the latest API version
)  

# デフォルトログの設定(flask, weitressからのログの設定)
logging.basicConfig(
    filename=LOG_FOLDER+'flask_system.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# カスタムロガー設定
custom_logger = logging.getLogger("custom")
handler = RotatingFileHandler(
    filename=LOG_FOLDER+'flask_custom.log',
    mode='a',
    maxBytes=8 * 1024 * 1024,  # 最大8MB
    backupCount=3,             # 最大3つのバックアップファイル
    encoding='utf-8', #cp932',  # Windowsのデフォルトエンコーディング
    delay=False
)
formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
custom_logger.addHandler(handler)
custom_logger.setLevel(logging.DEBUG) # DEBUGレベル以上のログを記録
custom_logger.propagate = False  # 親ロガー(デフォルトロガー)への伝播を防ぐ

# Waitressロガー
waitress.logging.basicConfig(level=logging.DEBUG) # Waitressのログ出力条件をDEBUG以上に設定
waitress.logging.propagate = True  # Waitressのログを親ロガー(デフォルトロガー)に伝播する

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
    custom_logger.debug("-- Header:")
    custom_logger.debug(request.headers)
    custom_logger.debug("-- Body:")
    if request.content_type == 'application/json':
        s = pprint.pformat(request.get_json(), compact=True)
        custom_logger.debug(s[:10000])  # Log first 10000 characters of JSON request data
        # --- req.jsonに出力 ---
        with open(LOG_FOLDER+'req.json', 'w', encoding='utf-8') as f:
            json.dump(request.get_json(), f, ensure_ascii=False, indent=2)
    else:
        custom_logger.debug(request.get_data(as_text=True)[:HTTP_LOG_TRIM_LENGTH])  # Log first 10000 bytes of request data
    # Check for Authorization header
    #if checkAPIKey() == "-":
    #    return Response('{"error": {"code":401, "message": "Unauthorized error. API key is incorrect. Contact to IPpro."}}', status=401, mimetype='application/json')

@app.after_request
def log_response_info(response):
    custom_logger.debug("----- response ---------------------------------------------------------------")
    custom_logger.debug(response)
    custom_logger.debug("-- Header: ")
    custom_logger.debug(response.headers)
    custom_logger.debug("-- Body:")
    if response.content_type == 'application/json':
        s = pprint.pformat(response.get_json(), compact=True)
        custom_logger.debug(s[:10000])  # Log first 10000 characters of JSON request data
        # --- res.jsonに出力 ---
        with open(LOG_FOLDER+'res.json', 'w', encoding='utf-8') as f:
            json.dump(response.get_json(), f, ensure_ascii=False, indent=2)
    else:
        response_text = response.get_data(as_text=True)
        custom_logger.debug(response_text[:HTTP_LOG_TRIM_LENGTH])  # Log first 1000 bytes of request data
        # streaming response
        if "\ndata:" in response_text:
            # --- res.jsonに出力 ---
            response_split = ("\n\n" + response_text).split("\n\ndata:")
            response_split = [s for s in response_split if s.strip(" \t\r\n") != ""]  # Remove empty string
            response_split = [s for s in response_split if s.strip(" \t\r\n") != "[DONE]"]  # Remove empty string
            #print("\n\nresponse_split2:", response_split)
            response_json = "{ \"value\": [" + ", ".join(response_split) + "]}"
            #print("response_json:", response_json)
            response_obj = json.loads(response_json)
            #custom_logger.debug("response_json:", response_json)
            with open(LOG_FOLDER+'res.json', 'w', encoding='utf-8') as f:
                json.dump(response_obj, f, ensure_ascii=False, indent=2)
            # message
            contents = [ c["choices"][0].get("delta", {}).get("content", "") for c in response_obj["value"] if len(c["choices"]) > 0 ]
            custom_logger.debug("Response message: " + "".join(contents))  # Join all contents

    # One liner access log
    referer = request.referrer or "-"
    user_agent = request.headers.get('User-Agent') or "-"
    auth = checkAPIKey()
    log_entry = '{} "{} {} {}" {} {} "{}" "{}" {}'.format(
        request.remote_addr,
        request.method,
        request.path,
        request.environ.get('SERVER_PROTOCOL'),
        response.status_code,
        response.content_length or '-',
        referer,
        user_agent,
        auth
    )
    custom_logger.info(log_entry)

    return response

#@app.errorhandler(404)
#def handle_404(e):
#    return jsonify({"error": "Not found (compatible server error)"}), 404

# any other endpoint
@app.route('/v1/resonses', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def catch_all():
    return jsonify({"error": "Block 'responses' endpoint"}), 500


# OPTIONS request handler  for CORS preflight
# @app.route('/v1/chat/completions', methods=['OPTIONS'])
# def options_handler():
#     # response to OPTIONS requests
#     response = make_response()
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
#     return response

# Chat endpoints
@app.route('/<path:anything>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH', 'TRACE', 'HEAD'])
def handle_any(anything):
    timestamp = get_time_stamp()
    payload = request.get_json()
    model = payload.get("model", "")
  
    # completion handler using Azure OpenAI
    def completionsHandlerAzure(payload):
        stream = payload.get("stream", False)
        messages = payload.get("messages", [])

        # Azure OpenAI Completions
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME, # model = "deployment_name".
            messages=messages,
            max_completion_tokens=payload.get("max_completion_tokens", None),
            temperature=payload.get("temperature", None),
            stream=stream, 
        )
        #print(response)

        if stream == False:
            return response
        else:
            def generate():
                responseList = list(response)
                responseLength = len(responseList)
                for i in range(responseLength):
                    chunk = responseList[i]
                    yield "data: " + json.dumps(chunk.to_dict()) + "\n\n"                
                #print(mes)
                yield "data: [DONE]\n\n"

            # Create a streaming response
            res = Response(stream_with_context(generate()), mimetype='text/event-stream')   
            res.headers["Content-Type"] = "text/event-stream; charset=utf-8"
            res.headers['Cache-Control'] = 'no-cache'
            return res

    resp = completionsHandlerAzure(payload)

    return resp




# Run the server
if __name__ == '__main__':
    if developmentMode == True:
        print('Starting Development server (debug mode)...')
        app.run(host=LISTEN_HOST, port=LISTEN_PORT, debug=True)
    else:
        print('Starting Waitress server...')
        waitress.serve(app, host=LISTEN_HOST, port=LISTEN_PORT,
            connection_limit=100,  # default is 100
            threads=4,  # default is 4
            channel_timeout=120, # default is 120 seconds
        )
