from img2table.document import Image
from img2table.ocr import TesseractOCR
from img2table.ocr import EasyOCR
import cv2
import sys
import os
print("imported")

# 画像読み込み
if len(sys.argv) < 2:
    print("Usage: python img2tableOCR.py <image_file>")
    sys.exit(1)
img_path = sys.argv[1]

# OCR（EasyOCR を使う場合）
#ocr = EasyOCR(lang=["ja", "en"])

os.environ["PATH"] += os.pathsep + r"D:\Program Files\Tesseract-OCR"
ocr = TesseractOCR(lang="jpn")

# img2table の Image オブジェクト
doc = Image(img_path)

# 表抽出（OCR あり）
#tables = doc.extract_tables(ocr=None)
tables = doc.extract_tables(ocr=ocr)

# 結果表示
print(tables)
for idx, table in enumerate(tables):
    print(f"=== Table {idx} ===")
    print(table.content)
    print(table.df)
    for row in table.content:
        print(row)
