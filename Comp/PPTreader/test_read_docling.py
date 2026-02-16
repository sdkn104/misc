#import json
#import yaml
import logging
from pathlib import Path
#from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)
#from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline

#_log = logging.getLogger(__name__)

def sequential_replace(text, target):
    parts = text.split(target)
    if len(parts) == 1:
        return text
    result = ["<!-- Page 1 -->/\n\n"]
    for i, part in enumerate(parts[:-1], 1):
        result.append(part)
        result.append(target)
        result.append(f"<!-- Page {i+1} -->\n")
    result.append(parts[-1])
    return ''.join(result)

def read_document_docling(input_file: Path) -> str:
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.ocr_options = None
    
    doc_converter = DocumentConverter(
        #allowed_formats=[
        #    InputFormat.PDF,
        #    InputFormat.PPTX,
        #],  # whitelist formats, non-matching files are ignored.
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options = pipeline_options,
                #PdfPipelineOptions(
                #    do_ocr=False,
                #),
                pipeline_cls=StandardPdfPipeline, 
                #backend=PyPdfiumDocumentBackend,
            ),
        },
    )
    doc_converter = DocumentConverter()
    conv_result = doc_converter.convert(input_file)

    final_markdown = conv_result.document.export_to_markdown(page_break_placeholder="\n\n----------\n\n").encode("utf-8", errors="replace").decode("utf-8")
    final_markdown = sequential_replace(final_markdown, "\n----------\n")
    
    #markdown_lines = []

    #current_page = None
    # for element in conv_result.document.elements:
    #     if not element.provenance:
    #         continue
    #     page_no = element.provenance[0].page_no
    #     if page_no != current_page:
    #         markdown_lines.append(f"\n\n---\n\n# Page {page_no}\n\n")
    #         current_page = page_no
    #     markdown_lines.append(element.text.strip() + "\n")

    # for i, page in enumerate(conv_result.document.pages):
    #     page_md = page.text.strip() + "\n"
    #     markdown_lines.append(f"\n\n---\n\n## Page {i+1}\n\n{page_md}")

    # final_markdown = ''.join(markdown_lines)

    #out_path = Path(".")
    #with (out_path / f"{conv_result.input.file}.docling.tree").open("w", encoding="utf-8") as fp:
    #    fp.write(conv_result.document.export_to_element_tree())

    return final_markdown

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
    else:
        input_file = Path("input.pdf")
    result = read_document_docling(input_file)
    print("markdown length:", len(result))
    out_path = Path(".")
    with (out_path / f"{input_file}.docling.md").open("w", encoding="utf-8") as fp:
        fp.write(result)
