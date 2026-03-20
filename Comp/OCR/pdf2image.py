

import sys
import os
import fitz  # PyMuPDF

def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf2image.py <input.pdf>")
        sys.exit(1)
    input_path = sys.argv[1]
    ext = os.path.splitext(input_path)[1].lower()
    if ext != ".pdf":
        print("Error: Input file must be a PDF.")
        sys.exit(1)

    pdf = fitz.open(input_path)
    for page_index in range(len(pdf)):
        page = pdf[page_index]
        pix = page.get_pixmap(dpi=300)
        out_path = f"{os.path.splitext(input_path)[0]}_page{page_index}.png"
        pix.save(out_path)
        print(f"Saved: {out_path}")
    print("extracted image from pdf")

if __name__ == "__main__":
    main()
