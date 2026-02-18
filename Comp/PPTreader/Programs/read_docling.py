from datetime import datetime
print("start", datetime.now())
#import os
from io import BytesIO
from typing import Union
from typing import BinaryIO
from pathlib import Path
#import logging
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat, DocumentStream
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
#from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling_core.types.doc.labels import DocItemLabel

print("library loaded.", datetime.now())

#_log = logging.getLogger(__name__)

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

#def read_document_docling(source: Union[str, Path, BinaryIO]) -> str:
def read_document_docling(source) -> str:
    print("reading document...", type(source), datetime.now())

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_picture_classification = False
    pipeline_options.do_picture_description = False
    pipeline_options.do_table_structure = True
    pipeline_options.do_chart_extraction = False
    pipeline_options.do_code_enrichment = False
    pipeline_options.do_formula_enrichment = False

    doc_converter = DocumentConverter(
        #allowed_formats=[
        #    InputFormat.PDF,
        #    InputFormat.PPTX,
        #],  # whitelist formats, non-matching files are ignored.
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options = pipeline_options,
                pipeline_cls=StandardPdfPipeline, 
                backend=PyPdfiumDocumentBackend,
                layout_batch_size=10,
                table_batch_size=10,
            ),
        },
    )
    doc_converter = DocumentConverter()
    if isinstance(source, (str, Path)):
        conv_result = doc_converter.convert(source)
    else:
        ds = DocumentStream(name="uploaded_file.pdf", stream=BytesIO(source.read()))
        conv_result = doc_converter.convert(ds)
    labels = [
        DocItemLabel.SECTION_HEADER,
        DocItemLabel.PAGE_FOOTER, 
        DocItemLabel.PAGE_HEADER,
        DocItemLabel.PICTURE,
        DocItemLabel.TEXT,
        DocItemLabel.TABLE,
        DocItemLabel.PARAGRAPH,
        DocItemLabel.LIST_ITEM,
        DocItemLabel.TITLE,
        DocItemLabel.REFERENCE,
        DocItemLabel.CAPTION,
        DocItemLabel.CODE,
        DocItemLabel.DOCUMENT_INDEX,
        DocItemLabel.FOOTNOTE,
        DocItemLabel.KEY_VALUE_REGION,
        DocItemLabel.CHART,
        DocItemLabel.FORMULA,
        DocItemLabel.FORM,
    ]
    #final_markdown = conv_result.document.export_to_markdown(page_break_placeholder="\n\n----------\n\n", labels=labels).encode("utf-8", errors="replace").decode("utf-8")
    final_markdown = conv_result.document.export_to_markdown(page_break_placeholder="\n\n----------\n\n").encode("utf-8", errors="replace").decode("utf-8")
    print("converted.", datetime.now())
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
    
    print("markdown created.", datetime.now())
    print("markdown length", len(final_markdown))

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
