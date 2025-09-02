from flask import Flask, request, send_file, jsonify, send_from_directory
from markitdown import MarkItDown
import tempfile
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'ファイルがアップロードされていません'}), 400

        file = request.files['file']
        filename = file.filename

        # 一時ファイルとしてバイナリ保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1], mode='wb') as temp_in:
            file.stream.seek(0)
            temp_in.write(file.read())
            temp_in_path = temp_in.name

        # MarkItDownで変換
        md = MarkItDown(enable_plugins=False)
        result = md.convert(temp_in_path)
        md_text = result.text_content

        # mdファイルとして一時保存
        with tempfile.NamedTemporaryFile(delete=False, suffix='.md', mode='w', encoding='utf-8') as temp_out:
            temp_out.write(md_text)
            temp_out_path = temp_out.name

        # mdファイルをダウンロード用に返却
        response = send_file(
            temp_out_path,
            as_attachment=True,
            download_name=f"{os.path.splitext(filename)[0]}.md",
            mimetype='text/markdown'
        )

        # 後始末（リクエスト終了後に一時ファイル削除）
        @response.call_on_close
        def cleanup():
            os.remove(temp_in_path)
            os.remove(temp_out_path)

        return response
    except Exception as e:
        return jsonify({'error': f'サーバーエラー: {str(e)}'}), 500

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
