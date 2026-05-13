# docling を使って PDF/PPTX をマークダウンに変換するモジュール。
# ページ区切りに <!-- Page N --> コメントを挿入して出力する。
from datetime import datetime
import time
start = time.time()
def print_time(message):
    print(datetime.now(), f"{time.time() - start:.1f}", message)

print_time("loading libraries...")
from io import BytesIO
from typing import Union
from typing import BinaryIO
from pathlib import Path
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat, DocumentStream
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling_core.types.doc.labels import DocItemLabel

print_time("loaded libraries")

#_log = logging.getLogger(__name__)

def sequential_replace(text, target):
    # target（ページ区切り文字列）の直後に <!-- Page N --> を挿入する。
    # 先頭には必ず <!-- Page 1 --> を付ける。
    parts = text.split(target)
    if len(parts) == 1:
        return text
    result = ["<!-- Page 1 -->\n\n"]
    for i, part in enumerate(parts[:-1], 1):
        result.append(part)
        #result.append(target)
        result.append(f"\n<!-- Page {i+1} -->\n")
    result.append(parts[-1])
    return ''.join(result)



def read_document_docling(source: Union[str, Path, BinaryIO]) -> str:
    print_time("reading document... "+str(type(source)))

    # NOTE: 上記の個別設定は docling 2.73 では xenable_layout=False で上書きされる。
    # 2.73 以降はコンストラクタ引数で指定するのが正しい方法。
    # pipeline_options = PdfPipelineOptions()
    # pipeline_options.do_ocr = False
    # pipeline_options.do_picture_classification = False
    # pipeline_options.do_picture_description = False
    # pipeline_options.do_table_structure = True
    # pipeline_options.do_chart_extraction = False
    # pipeline_options.do_code_enrichment = False
    # pipeline_options.do_formula_enrichment = False

    # パイプライン設定（docling 2.73 の正しい指定方法。上の個別設定を上書きする）
    pipeline_options = PdfPipelineOptions(
        xenable_layout=False  # レイアウト解析を無効化してシンプルな抽出に絞る
    )

    # allowed_formats を省略すると docling がサポートする全フォーマット（PDF/DOCX/XLSX/PPTX 等）を受け付ける。
    # format_options で PDF のみカスタムパイプラインを指定し、他フォーマットは docling デフォルトを使う。
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
    if isinstance(source, (str, Path)):
        conv_result = doc_converter.convert(source)
    else:
        # docling はファイル名の拡張子でフォーマットを判別するため、正しい名前を渡す必要がある。
        # .filename: Flask FileStorage / FastAPI UploadFile（フォームフィールド名ではなくファイル名を持つ）
        # .name:     組み込み open() で開いたファイルオブジェクト
        name = (Path(source.filename).name if hasattr(source, "filename") and source.filename
                else Path(source.name).name if hasattr(source, "name")
                else "uploaded_file.pdf")
        ds = DocumentStream(name=name, stream=BytesIO(source.read()))
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
    # encode→decode で UTF-8 で表現できない文字を replacement character に変換する
    final_markdown = conv_result.document.export_to_markdown(page_break_placeholder="\n\n----------\n\n").encode("utf-8", errors="replace").decode("utf-8")
    print_time("converted.")
    # ページ区切り文字列の直後に <!-- Page N --> を挿入してページ番号を明示する
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
    
    print_time(f"markdown created. length={len(final_markdown)}")

    return final_markdown

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="PDF/PPTX をマークダウンに変換する (docling 使用)"
    )
    parser.add_argument("--input", "-i", required=True, metavar="FILE",
                        help="入力ファイル (PDF または PPTX)")
    parser.add_argument("--output", "-o", metavar="FILE",
                        help="出力ファイル (省略時: <入力ファイル名>.docling.md)")
    args = parser.parse_args()

    input_file = Path(args.input)
    result = read_document_docling(input_file)

    out_file = Path(args.output) if args.output else input_file.parent / f"{input_file.name}.docling.md"
    print_time(f"writing to: {out_file}")
    with out_file.open("w", encoding="utf-8") as fp:
        fp.write(result)
