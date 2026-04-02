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

## pip install -U "opendataloader-pdf[hybrid]"
import opendataloader_pdf

print_time("loaded libraries")

def read_document_opendataloader(source: Union[str, Path, BinaryIO]) -> str:
    """Read a PDF using OpenDataLoader and return markdown text.
    """
    print_time("reading document... " + str(type(source)))

    tmp_path = None
    if isinstance(source, (str, Path)):
        src_path = str(source)
    else:
        data = source.read()
        if isinstance(data, str):
            data = data.encode()
        # write to temporary file and pass path to loader
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        src_path = tmp_path

    def pdf_to_markdown(pdf_path: str) -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            opendataloader_pdf.convert(
                input_path=pdf_path,
                output_dir=tmpdir,
                format="markdown",
                hybrid="docling-fast",
                markdown_page_separator="<!--- Page %page-number% --->"
            )

            md_path = Path(tmpdir) / f"{Path(pdf_path).stem}.md"
            return md_path.read_text(encoding="utf-8")

    markdown_text = pdf_to_markdown(src_path)

    if tmp_path and os.path.exists(tmp_path):
        try:
            os.remove(tmp_path)
        except Exception:
            pass

    print_time("converted.")
    print_time(f"markdown created. length={len(markdown_text)}")

    return markdown_text


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
    else:
        input_file = Path("input.pdf")
    result = read_document_opendataloader(input_file)
    if len(sys.argv) > 2:
        out_file = Path(sys.argv[2])
    else:
        out_file = input_file.parent / f"{input_file.name}.opendataloader.md"

    print_time(f"writing to: {out_file}")
    with out_file.open("w", encoding="utf-8") as fp:
        fp.write(result)
