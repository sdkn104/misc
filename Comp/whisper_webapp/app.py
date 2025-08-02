import os
from flask import Flask, request, render_template, redirect, url_for, flash
import whisper

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"mp3"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "your_secret_key"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = None
    if request.method == "POST":
        if "file" not in request.files:
            flash("ファイルが選択されていません")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("ファイルが選択されていません")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            model_name = request.form.get("model", "base")
            model = whisper.load_model(model_name)
            result = model.transcribe(filepath, language="ja")
            transcript = result["text"]
            os.remove(filepath)
        else:
            flash("許可されていないファイル形式です")
    return render_template("index.html", transcript=transcript)

if __name__ == "__main__":
    app.run(debug=True)
