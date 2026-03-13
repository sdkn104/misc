from datetime import datetime
import time
start = time.time()
print("loading libraries...", datetime.now())
#import os
from io import BytesIO
from typing import Union
from typing import BinaryIO
from pathlib import Path

import fitz

def read_document_pymupdf(pdf, type="text"):
    doc = fitz.open(pdf)
    
    text = ""

    if type == "markdown":
        for page in doc:
            text += page.get_text("markdown")# 動作しない

    else:
        for page in doc:
            text += page.get_text()

    return text


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
    else:
        input_file = Path("input.pdf")
    result = read_document_pymupdf(input_file)
    print("text length:", len(result))
    out_path = Path(".")
    with (out_path / f"{input_file}.pymupdf.txt").open("w", encoding="utf-8") as fp:
        fp.write(result)
