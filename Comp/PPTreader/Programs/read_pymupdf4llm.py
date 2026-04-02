from datetime import datetime
import time
start = time.time()

def print_time(message):
    print(datetime.now(), f"{time.time() - start:.1f}", message)


print_time("loading libraries...")
from io import BytesIO
from typing import Union, BinaryIO
from pathlib import Path
import tempfile
import os
import pymupdf4llm

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


def read_document_pymupdf4llm(source: Union[str, Path, BinaryIO]) -> str:
    """Read PDF using PyMuPDF and return markdown string.

    This mirrors the behavior of read_document_pymupdf and read_document_docling:
    - Accepts path-like or binary file-like object
    - Joins pages with the same page-break placeholder used elsewhere
    - Inserts HTML comments marking page boundaries
    """
    print_time("reading document... " + str(type(source)))

    # Use pymupdf4llm.to_markdown to extract markdown. It accepts a filename
    # and has options such as page_chunks and write_images. For file-like
    # objects we write a temporary file and pass its path to the function.
    tmp_path = None
    try:
        if isinstance(source, (str, Path)):
            src_path = str(source)
            print(src_path)
            page_list = pymupdf4llm.to_markdown(src_path, page_chunks=True)
        else:
            data = source.read()
            if isinstance(data, str):
                data = data.encode()
            # write to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(data)
                tmp_path = tmp.name
            page_list = pymupdf4llm.to_markdown(tmp_path, page_chunks=True)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    # Extract text page by page
    pages = []
    for page in page_list:
        #p = page["metadata"]["page"]
        text = page["text"]
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
    result = read_document_pymupdf4llm(input_file)
    if len(sys.argv) > 2:
        out_file = Path(sys.argv[2])
    else:
        out_file = input_file.parent / f"{input_file.name}.pymupdf4llm.md"

    print_time(f"writing to: {out_file}")
    with out_file.open("w", encoding="utf-8") as fp:
        fp.write(result)
