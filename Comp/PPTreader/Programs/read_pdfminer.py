from datetime import datetime
import time
start = time.time()
def print_time(message):
    print(datetime.now(), f"{time.time() - start:.1f}", message)

print_time("loading libraries...")
from typing import Union, BinaryIO
from pathlib import Path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

print_time("loaded libraries")


def sequential_replace(text, target):
    parts = text.split(target)
    if len(parts) == 1:
        return text
    result = ["<!-- Page 1 -->\n\n"]
    for i, part in enumerate(parts[:-1], 1):
        result.append(part)
        #result.append(target)
        result.append(f"\n\n<!-- Page {i+1} -->\n\n")
    result.append(parts[-1])
    return ''.join(result)

def read_document_pdfminer(source: Union[str, Path, BinaryIO]) -> str:
    """Read a PDF using pdfminer and return a markdown-ish text with page separators.

    The function mirrors the interface of Programs/read_docling.py: it accepts
    a path-like (str or Path) or a file-like object and returns the extracted
    text as a single string. Page-break placeholder used is "\n\n----------\n\n".
    """
    print_time("reading document... "+str(type(source)))

    # Extract text page by page
    pages = []
    for page_layout in extract_pages(source):
        page_text = ""
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                page_text += element.get_text()
        pages.append(page_text.rstrip())

    print_time("converted.")

    # join pages with the same placeholder
    page_break = "\n\n----------\n\n"
    final_text = page_break.join(pages)
    # Insert HTML comments indicating page boundaries
    final_text = sequential_replace(final_text, page_break)

    print_time(f"text created. length={len(final_text)}")

    return final_text


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="PDF をテキストに変換する (pdfminer 使用)"
    )
    parser.add_argument("--input", "-i", required=True, metavar="FILE",
                        help="入力ファイル (PDF)")
    parser.add_argument("--output", "-o", metavar="FILE",
                        help="出力ファイル (省略時: <入力ファイル名>.pdfminer.txt)")
    args = parser.parse_args()

    input_file = Path(args.input)
    result = read_document_pdfminer(input_file)

    out_file = Path(args.output) if args.output else input_file.parent / f"{input_file.name}.pdfminer.txt"
    print_time(f"writing to: {out_file}")
    with out_file.open("w", encoding="utf-8") as fp:
        fp.write(result)
    