from flask import Flask, render_template, request, send_file, jsonify
from pathlib import Path
import io
import zipfile
from datetime import datetime
from read_docling import read_document_docling

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload


@app.route('/read')
def index():
    """HTML フロントエンドを返す"""
    return render_template('index.html')


@app.route('/read/api/convert', methods=['POST'])
def convert_documents():
    """
    複数のドキュメントを受け取り、markdown に変換して返す
    """
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    if len(files) == 0:
        return jsonify({'error': 'No files selected'}), 400

    # 変換結果を格納
    converted_docs = {}
    errors = []

    for file in files:
        if file.filename == '':
            continue

        try:
            print(f"Processing: {file.filename}", datetime.now())

            # ストリームを直接渡す
            file.stream.seek(0)
            print(type(file))
            markdown_content = read_document_docling(file.stream)

            # ファイル名の拡張子を .md に変更
            original_name = Path(file.filename).stem
            output_filename = f"{original_name}.docling.md"

            converted_docs[output_filename] = markdown_content

            print(f"Completed: {file.filename}", datetime.now())

        except Exception as e:
            error_msg = f"Error processing {file.filename}: {str(e)}"
            errors.append(error_msg)
            print(error_msg, datetime.now())

    if not converted_docs and errors:
        return jsonify({'error': 'All files failed to process', 'details': errors}), 500

    # 複数ファイルの場合は ZIP で返す
    if len(converted_docs) > 1:
        return send_zip_files(converted_docs)
    # 単一ファイルの場合は直接返す
    elif len(converted_docs) == 1:
        filename, content = list(converted_docs.items())[0]
        return send_file(
            io.BytesIO(content.encode('utf-8')),
            mimetype='text/markdown',
            as_attachment=True,
            download_name=filename
        )

    return jsonify({'error': 'No files were converted', 'details': errors}), 500


def send_zip_files(file_dict):
    """
    複数ファイルを ZIP で圧縮して返す
    """
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in file_dict.items():
            zip_file.writestr(filename, content.encode('utf-8'))

    zip_buffer.seek(0)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'converted_documents_{timestamp}.zip'
    )


if __name__ == '__main__':
    print("Starting Flask app...", datetime.now())
    app.run(debug=True, host='127.0.0.1', port=5000)
