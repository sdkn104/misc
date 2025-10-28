import PDFreader.test_pdfplumber as test_pdfplumber

with test_pdfplumber.open('CorpStrategy2025.pdf') as pdf:
    text = pdf.pages[15].extract_text()
    print("=== ページ全体のテキスト ===")
    print(text) 