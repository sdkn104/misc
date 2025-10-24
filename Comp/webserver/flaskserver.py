from flask import Flask, request, make_response
#from flask_cors import CORS
import subprocess
import requests

app = Flask(__name__)
#CORS(app)


#部評システムへのリクエストを転送 (http://localhost:5000/WEBUSER/OWA/... -> http://www2.hin.mei.melco.co.jp/WEBUSER/OWA/...)
@app.route('/WEBUSER/OWA/<path:path>') 
def transfer_to_buhyo_system(path): 
    url = "http://www2.hin.mei.melco.co.jp" + request.script_root + request.full_path 
    print("redirecting to "+url) 
    r = requests.get(url) 
    #print(r.encoding)
    return make_response(r.text, r.status_code) 


# http://localhost:5000/ に対する処理
@app.route('/')
@app.route('/test')
def hello_world():
    return "Hello!!!<br><br>I am Local Web Server for BUHYO miscellaneous tasks.<br>To kILL me, click <a href='http://localhost:5000/shutdown'>http://localhost:5000/shutdown</a>"


# WEBサーバ起動。127.0.0.1=localhost
app.run(host='127.0.0.1', port=5000)


