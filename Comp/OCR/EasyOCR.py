import easyocr
import cv2
import sys
print("imported")

def main():
    if len(sys.argv) < 2:
        print("Usage: python EasyOCR.py <image_file>")
        sys.exit(1)
    image_path = sys.argv[1]


    # 日本語 + 英語モデル
    reader = easyocr.Reader(['ja', 'en'], gpu=False)

    # 画像読み込み
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load image: {image_path}")
        sys.exit(1)
    print("image read")

    # OCR実行
    results = reader.readtext(img)

    # 結果表示
    for bbox, text, prob in results:
        print(f"{text}  {bbox[0]} (confidence={prob:.2f})")

    results = reader.readtext(img)

if __name__ == "__main__":
    main()
