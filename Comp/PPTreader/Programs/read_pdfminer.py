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
        result.append(target)
        result.append(f"<!-- Page {i+1} -->\n")
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
    final_markdown = page_break.join(pages)
    # Insert HTML comments indicating page boundaries
    final_markdown = sequential_replace(final_markdown, page_break)

    print_time(f"text created. length={len(final_markdown)}")

    return final_markdown


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
    else:
        input_file = Path("input.pdf")
    result = read_document_pdfminer(input_file)
    if len(sys.argv) > 2:
        out_file = Path(sys.argv[2])
    else:
        out_file = input_file.parent / f"{input_file.name}.pdfminer.txt"

    print_time(f"writing to: {out_file}")
    with out_file.open("w", encoding="utf-8") as fp:
        fp.write(result)