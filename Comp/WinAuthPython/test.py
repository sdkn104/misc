
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    user = request.headers.get("X-Auth-User")

    from pprint import pprint
    pprint(dict(request.headers))

    return f"Hello {user}"

if __name__ == "__main__":
    app.run(port=8000)
    