from paddleocr import PaddleOCR
from pprint import pprint
import sys
print("imported")

PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK = True

def main():
    if len(sys.argv) < 2:
        print("Usage: python PaddleOCR.py <image_file>")
        sys.exit(1)
    image_path = sys.argv[1]

    ocr = PaddleOCR(
        lang='japan',
        #text_detection_model_dir=None,  # 軽量化
        #text_recognition_model_dir=None,
        use_textline_orientation=True  # 新しいパラメータ
    )
    print("init ocr")

    result = ocr.predict(image_path)  # cls は不要
    print("result", result)
    for line in result:
        print(line)

if __name__ == "__main__":
    main()


