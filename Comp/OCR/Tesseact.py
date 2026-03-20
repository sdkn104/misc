import cv2
import pytesseract
import sys
print("imported")

pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"

def main():
    if len(sys.argv) < 2:
        print("Usage: python Tesseact.py <image_file>")
        sys.exit(1)
    image_path = sys.argv[1]

    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img, lang="jpn")
    print(text)


if __name__ == "__main__":
    main()


