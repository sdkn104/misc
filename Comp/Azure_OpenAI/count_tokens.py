import PyPDF2
import tiktoken
import sys

pdf_path = sys.argv[1]
print(f"Processing file: {pdf_path}")

# PDFファイルの読み込み
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

# トークン数の計算（GPT-4用）
def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)

# 実行
text = extract_text_from_pdf(pdf_path)
token_count = count_tokens(text)

print(f"抽出された文字数: {len(text)}")
print(f"トークン数（{pdf_path}）: {token_count}")
