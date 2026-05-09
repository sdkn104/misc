"""
ドキュメント変換 Web サービス

ブラウザからアップロードされたドキュメント（PDF, PPTX など）を
Markdown に変換して返す FastAPI アプリ。

エンドポイント:
  GET  /read              - アップロード UI
  POST /read/api/convert  - ファイル変換 API（複数可、複数時は ZIP 返却）
    クエリパラメータ:
      converter: "docling"（デフォルト）または "pdfminer"
"""

from fastapi import FastAPI, File, UploadFile, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import io
import zipfile
from datetime import datetime
from read_docling import read_document_docling
from read_pdfminer import read_document_pdfminer

app = FastAPI()
# テンプレートディレクトリはこのファイルと同階層の templates/
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


@app.get('/read', response_class=HTMLResponse)
async def index(request: Request):
    """アップロード UI を返す"""
    return templates.TemplateResponse(request, 'index.html')


@app.post('/read/api/convert')
async def convert_documents(
    files: list[UploadFile] = File(...),
    converter: str = Query(default='docling', pattern='^(docling|pdfminer)$'),
):
    """
    アップロードされたファイルを Markdown に変換して返す。
    - 1 ファイル: .md/.txt ファイルをそのまま返す
    - 複数ファイル: ZIP にまとめて返す
    converter クエリパラメータで変換エンジンを指定（docling / pdfminer）。
    """
    if not files:
        return JSONResponse(content={'error': 'No files provided'}, status_code=400)

    converted_docs = {}  # {出力ファイル名: Markdown テキスト}
    errors = []

    for file in files:
        if not file.filename:
            continue

        try:
            print(f"Processing: {file.filename} (converter={converter})", datetime.now())

            content = await file.read()

            if converter == 'pdfminer':
                markdown_content = read_document_pdfminer(io.BytesIO(content))
                output_filename = f"{Path(file.filename).stem}.pdfminer.txt"
            else:
                markdown_content = read_document_docling(io.BytesIO(content))
                output_filename = f"{Path(file.filename).stem}.docling.md"

            converted_docs[output_filename] = markdown_content

            print(f"Completed: {file.filename}", datetime.now())

        except Exception as e:
            error_msg = f"Error processing {file.filename}: {str(e)}"
            errors.append(error_msg)
            print(error_msg, datetime.now())

    # 全ファイルが失敗した場合
    if not converted_docs and errors:
        return JSONResponse(content={'error': 'All files failed to process', 'details': errors}, status_code=500)

    if len(converted_docs) > 1:
        return send_zip_files(converted_docs)
    elif len(converted_docs) == 1:
        out_filename, out_content = list(converted_docs.items())[0]
        return StreamingResponse(
            io.BytesIO(out_content.encode('utf-8')),
            media_type='text/markdown',
            headers={'Content-Disposition': f'attachment; filename="{out_filename}"'}
        )

    return JSONResponse(content={'error': 'No files were converted', 'details': errors}, status_code=400)


def send_zip_files(file_dict: dict) -> StreamingResponse:
    """複数の Markdown ファイルを ZIP に圧縮してストリーム返却する"""
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in file_dict.items():
            zip_file.writestr(filename, content.encode('utf-8'))

    zip_buffer.seek(0)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return StreamingResponse(
        zip_buffer,
        media_type='application/zip',
        headers={'Content-Disposition': f'attachment; filename="converted_documents_{timestamp}.zip"'}
    )


if __name__ == '__main__':
    import uvicorn
    print("Starting FastAPI app...", datetime.now())
    # reload=True でソース変更を自動検知して再起動
    uvicorn.run('web_read_docs:app', host='127.0.0.1', port=5000, reload=True)
