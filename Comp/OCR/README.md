
# Tesseact OCR
## install

- 公式インストーラをダウンロード
    https://github.com/UB-Mannheim/tesseract/wiki (github.com in Bing)
- インストール時に Japanese（jpn） を必ずチェック
- PATH を通す(不要)
- `pip install pytesseract opencv-python pillow`
- path設定
    ```python
    import pytesseract

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    ```
    