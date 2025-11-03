
import json
import logging
from pathlib import Path

import yaml

from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
)
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline

_log = logging.getLogger(__name__)


def main():
    input_paths = [
        Path("gen_test.pdf"),        
        Path("pwhr2020_manual_ref_4_staff.pptx"),
        Path("sinnkyouzai.pptx"),
        Path("2021_theme137_2.pptx"),
        Path("sdgs_miraikoshien_template-2021.pptx"),
        Path("nyumon6.pptx"),
        Path("generally_02.pptx"),
        Path("seiho_slides(2023)_2.pptx"),        
        Path("04-1.pptx"),
        Path("地方議会活性化シンポジウム.pdf"),
        Path("CorpStrategy2025.pdf"),
        Path("pwhr2020_manual_ref_4_staff.pdf"),
        Path("sinnkyouzai.pdf"),
        Path("2021_theme137_2.pdf"),
        Path("sdgs_miraikoshien_template-2021.pdf"),
        Path("nyumon6.pdf"),
        Path("generally_02.pdf"),
        Path("seiho_slides(2023)_2.pdf"),        
        Path("04-1.pdf"),
    ]

    ## to customize use:

    # Below we explicitly whitelist formats and override behavior for some of them.
    # You can omit this block and use the defaults (see above) for a quick start.
    doc_converter = DocumentConverter(  # all of the below is optional, has internal defaults.
        allowed_formats=[
            InputFormat.PDF,
            InputFormat.PPTX,
        ],  # whitelist formats, non-matching files are ignored.
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=StandardPdfPipeline, backend=PyPdfiumDocumentBackend
            ),
        },
    )

    ## for defaults use:
    doc_converter = DocumentConverter()

    conv_results = doc_converter.convert_all(input_paths)

    for res in conv_results:
        out_path = Path(".")  # ensure this directory exists before running
        print(
            f"Document {res.input.file.name} converted."
            f"\nSaved markdown output to: {out_path!s}"
        )
        _log.debug(res.document._export_to_indented_text(max_text_len=16))
        # Export Docling document to Markdown:
        with (out_path / f"{res.input.file}.docling.md").open("w", encoding="utf-8") as fp:
            fp.write(res.document.export_to_markdown().encode("utf-8", errors="replace").decode("utf-8"))

        with (out_path / f"{res.input.file}.docling.json").open("w", encoding="utf-8") as fp:
            fp.write(json.dumps(res.document.export_to_dict()))

        with (out_path / f"{res.input.file}.docling.yaml").open("w", encoding="utf-8") as fp:
            fp.write(yaml.safe_dump(res.document.export_to_dict()))

        with (out_path / f"{res.input.file}.docling.htm").open("w", encoding="utf-8") as fp:
            fp.write(res.document.export_to_html().encode("utf-8", errors="replace").decode("utf-8"))

        with (out_path / f"{res.input.file}.docling.tree").open("w", encoding="utf-8") as fp:
            fp.write(res.document.export_to_element_tree())

        with (out_path / f"{res.input.file}.docling.doctags").open("w", encoding="utf-8") as fp:
            fp.write(res.document.export_to_doctags())


if __name__ == "__main__":
    main()
