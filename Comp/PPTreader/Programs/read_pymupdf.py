from datetime import datetime
import time
start = time.time()
def print_time(message):
    print(datetime.now(), f"{time.time() - start:.1f}", message)

print_time("loading libraries...")
from io import BytesIO
from typing import Union, BinaryIO
from pathlib import Path
import fitz  # PyMuPDF

print_time("loaded libraries")


def sequential_replace(text, target):
    parts = text.split(target)
    if len(parts) == 1:
        return text
    result = ["<!-- Page 1 -->\n\n"]
    for i, part in enumerate(parts[:-1], 1):
        result.append(part)
        result.append(target)
        result.append(f"<!-- Page {i+1} -->\n")
    result.append(parts[-1])
    return ''.join(result)

# 
def read_document_pymupdf(source: Union[str, Path, BinaryIO]) -> str:
    """Read a PDF using PyMuPDF and return a markdown-ish text with page separators.

    The function mirrors the interface of Programs/read_docling.py: it accepts
    a path-like (str or Path) or a file-like object and returns the extracted
    text as a single string. Page-break placeholder used is "\n\n----------\n\n".
    """
    print_time("reading document... "+str(type(source)))

    # Open document from path or file-like stream
    if isinstance(source, (str, Path)):
        doc = fitz.open(str(source))
    else:
        # assume file-like binary object
        data = source.read()
        if isinstance(data, str):
            data = data.encode()
        doc = fitz.open(stream=data, filetype="pdf")

    # Extract text page by page
    pages = []
    for i, page in enumerate(doc, 1):
        try:
            text = page.get_text("text")
        except Exception:
            # fallback to simple extraction
            text = page.get_text()
        # normalize trailing newline
        pages.append(text.rstrip())

    # join pages with the same placeholder used by read_docling
    page_break = "\n\n----------\n\n"
    final_markdown = page_break.join(pages)

    print_time("converted.")

    # Insert HTML comments indicating page boundaries
    final_markdown = sequential_replace(final_markdown, page_break)

    print_time(f"markdown created. length={len(final_markdown)}")

    return final_markdown


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
    else:
        input_file = Path("input.pdf")
    result = read_document_pymupdf(input_file)
    if len(sys.argv) > 2:
        out_file = Path(sys.argv[2])
    else:
        out_file = input_file.parent / f"{input_file.name}.pymupdf.md"

    print_time(f"writing to: {out_file}")
    with out_file.open("w", encoding="utf-8") as fp:
        fp.write(result)