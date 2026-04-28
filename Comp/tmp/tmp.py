from flask import Flask, request, render_template_string, send_file, Response
from werkzeug.utils import secure_filename
from io import BytesIO
import os

ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)

UPLOAD_FORM_HTML = """<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>PDF → Markdown 変換</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; }
    input[type=file] { margin-bottom: 12px; }
    textarea { width: 100%; height: 320px; }
    .box { max-width: 800px; margin: auto; }
  </style>
</head>
<body>
  <div class="box">
    <h1>PDF → Markdown 変換</h1>
    <p>PDFファイルをアップロードするとMarkdown形式でダウンロードできます。</p>
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="pdf" accept="application/pdf" required />
      <br /><br />
      <button type="submit">変換してダウンロード</button>
    </form>

    <hr />
    <h2>Web API</h2>
    <p>APIとしても利用できます。</p>
    <pre>POST /api/convert
Content-Type: multipart/form-data
Form field: pdf</pre>
    <p>戻り値はMarkdownテキストです。</p>
  </div>
</body>
</html>
"""


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_stream) -> str:
    """PDFを読み込んでテキストを抽出します。"""
    try:
        import pypdf
        reader = pypdf.PdfReader(file_stream)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages)
    except ImportError:
        pass

    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(file_stream)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages)
    except ImportError:
        pass

    try:
        from pdfminer.high_level import extract_text
        file_stream.seek(0)
        return extract_text(file_stream)
    except ImportError:
        pass

    raise RuntimeError(
        "PDF変換ライブラリが見つかりません。`pip install pypdf` または `pip install PyPDF2` をインストールしてください。"
    )


def convert_text_to_markdown(text: str) -> str:
    """抽出したテキストを簡易Markdown形式に整形します。"""
    lines = [line.rstrip() for line in text.splitlines()]
    md_lines = ["# PDF converted to Markdown", ""]

    page_num = 1
    current_page = []

    for line in lines:
        if line.strip().lower().startswith("page ") and line.strip().endswith(str(page_num)):
            if current_page:
                md_lines.append(f"## Page {page_num}")
                md_lines.extend(current_page)
                md_lines.append("")
                current_page = []
                page_num += 1
            continue

        if line == "":
            if current_page and current_page[-1] != "":
                current_page.append("")
        else:
            current_page.append(line)

    if current_page:
        md_lines.append(f"## Page {page_num}")
        md_lines.extend(current_page)

    return "\n".join(md_lines).strip() + "\n"


def build_markdown_attachment(markdown_text: str, original_filename: str):
    buffer = BytesIO()
    buffer.write(markdown_text.encode("utf-8"))
    buffer.seek(0)
    md_name = secure_filename(os.path.splitext(original_filename)[0] + ".md")
    return send_file(
        buffer,
        as_attachment=True,
        download_name=md_name,
        mimetype="text/markdown; charset=utf-8",
    )


def process_pdf_upload(pdf_file):
    if pdf_file.filename == "" or not allowed_file(pdf_file.filename):
        raise ValueError("有効なPDFファイルをアップロードしてください。")

    pdf_bytes = pdf_file.stream.read()
    return convert_text_to_markdown(extract_text_from_pdf(BytesIO(pdf_bytes)))


@app.route("/", methods=["GET"])
def index():
    return render_template_string(UPLOAD_FORM_HTML)


@app.route("/upload", methods=["POST"])
@app.route("/api/convert", methods=["POST"])
def upload_or_convert():
    if "pdf" not in request.files:
        return "PDFファイルが選択されていません。", 400

    pdf_file = request.files["pdf"]
    try:
        markdown_text = process_pdf_upload(pdf_file)
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        return f"PDF変換に失敗しました: {e}", 500

    return build_markdown_attachment(markdown_text, pdf_file.filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
