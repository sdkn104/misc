from flask import Flask, request, send_from_directory, jsonify, abort
import os

app = Flask(__name__)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/files")
def list_files():
    return jsonify(os.listdir(UPLOAD_DIR))

@app.post("/files")
def upload_file():
    if "file" not in request.files:
        abort(400, "No file part")
    f = request.files["file"]
    if f.filename == "":
        abort(400, "Empty filename")
    path = os.path.join(UPLOAD_DIR, f.filename)
    f.save(path)
    return jsonify({"fileId": f.filename, "status": "uploaded"}), 201

@app.get("/files/<fileId>")
def download_file(fileId):
    if not os.path.exists(os.path.join(UPLOAD_DIR, fileId)):
        abort(404)
    return send_from_directory(UPLOAD_DIR, fileId, as_attachment=True)

@app.delete("/files/<fileId>")
def delete_file(fileId):
    path = os.path.join(UPLOAD_DIR, fileId)
    if not os.path.exists(path):
        abort(404)
    os.remove(path)
    return jsonify({"fileId": fileId, "status": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
