import os
import sys
from pprint import pprint
import pandas as pd
import pptxtopdf

import pdfplumber

#from pdfminer.high_level import extract_pages
#from pdfminer.layout import LTTextContainer, LTChar

#from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
#from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter
#from docling.pipeline.simple_pipeline import SimplePipeline
#from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline


# Usage:
#   % python slides2md.py input.pptx
#   % python slides2md.py input.pdf
#   
#   from slides2md import slides2md
#   md_text = slides2md("input.pptx")


LayParams = {
    "SlideTitleYRatio": 0.15,
    "SlideTitleWidthRatio": 0.15,
}


def slides2md(in_file):
    # Extract Tables using Docling
    print(f"Docling {in_file}...")
    doc_converter = DocumentConverter()
    gen = doc_converter.convert_all([in_file])
    res = next(gen)
    docling_tables = []
    for table_ix, table in enumerate(res.document.tables):
        table_df: pd.DataFrame = table.export_to_dataframe()
        docling_tables.append({
            "table_ix": table_ix, 
            "page_no": table.prov[0].page_no, 
            "bbox": table.prov[0].bbox, 
            "md": table_df.to_markdown(),
        })

    # Convert PPTX to PDF
    if in_file.endswith('.pptx'):
        out_folder = os.path.dirname(in_file)
        print(f'Converting {in_file} to PDF in {out_folder}...')
        pptxtopdf.convert(in_file, out_folder)
        in_file = os.path.splitext(in_file)[0] + '.pdf'

    # Pdfplumber processing
    print(f'Pdfplumber {in_file}...')
    with pdfplumber.open(in_file, laparams={"line_overlap": 0.5 }) as pdf:
        # output files
        #pages_obj = [page.objects for page in pdf.pages]
        #with open(in_file + '.plumber.obj', 'w', encoding='utf-8') as fout:
        #    pprint(pages_obj, fout)
        # textbox_obj = [page.objects.get("textboxhorizontal","") for page in pdf.pages]
        # with open(in_file + '.plumber.tbox', 'w', encoding='utf-8') as fout:
        #     pprint(textbox_obj, fout)
        # tables_obj = [page.extract_tables() for page in pdf.pages]
        # with open(in_file + '.plumber.tbl', 'w', encoding='utf-8') as fout:
        #     pprint(tables_obj, fout)

        # visualize textboxes
        # first_page = pdf.pages[1]
        # im = first_page.to_image()
        # im.draw_rects(first_page.extract_words(), stroke="blue", stroke_width=2)
        # tboxes = first_page.objects.get("textboxhorizontal","")        
        # pprint([b for b in first_page.objects.get("textboxhorizontal",[]) if "x0" not in b.keys()])
        # pprint([b for b in first_page.objects.get("textboxhorizontal",[]) if "x1" not in b.keys()])
        # pprint([b for b in first_page.objects.get("textboxhorizontal",[]) if "top" not in b.keys()])
        # pprint([b for b in first_page.objects.get("textboxhorizontal",[]) if "bottom" not in b.keys()])
        # im.draw_rects([(b.get("x0",0),b.get("top",0), b.get("x1",1), b.get("bottom",1)) for b in first_page.objects.get("textboxhorizontal",[])], stroke="red", stroke_width=1)
        #im.draw_rects([t["bbox"] for t in docling_tables if t["page_no"] == first_page.page_number], stroke="green", stroke_width=1)
        #im.show()
        #im.save(in_file + '.plumber.png')

        # layout analysis
        for page in pdf.pages:
            for tbox in page.objects.get("textboxhorizontal", []):
                if tbox.get("bottom", None) < page.height * LayParams["SlideTitleYRatio"] and tbox.get("width", None) > page.width * LayParams["SlideTitleWidthRatio"]:
                    tbox["lay_title"] = True
                    break

        # create Marp(markdown) for slides
        fout = []
        fout.append("---\nmarp: true\nheader: ' '\nfooter: ' '\n---\n\n")
        for page in pdf.pages:
            # Docling tables on this page
            page_docling_tables = [docling_table for docling_table in docling_tables if docling_table["page_no"] == page.page_number]

            # Remove all objects overlapping with tables
            page2 = page
            for t in page_docling_tables:
                bb = t["bbox"]
                bbx = (bb.l, page.height - bb.t, bb.r, page.height - bb.b)
                page2 = page2.outside_bbox(bbx, relative=False, strict=True)

            # Textboxes
            tboxes = page2.objects.get("textboxhorizontal", [])
            title_list = [tbox.get("text","") for tbox in tboxes if tbox.get("lay_title", False)]
            title_text = " ".join(title_list).replace('\n','').strip()
            fout.append("## " + title_text + '\n\n')
            for tbox in tboxes:
                if "lay_title" not in tbox:
                    fout.append("<div class='textbox'>\n")
                    fout.append(tbox.get("text","") + '\n')
                    fout.append("</div>\n\n")

            ## Pdfplumber tables
            # for table in page.extract_tables():
            #     #pprint(table)
            #     df = pd.DataFrame(table)
            #     #pprint(df)
            #     fout.append("\n<!--- plumber --->\n")
            #     fout.append(df.to_markdown())
            #     fout.append("\n\n")

            # Docling tables
            for table in page_docling_tables:
                fout.append("\n<!--- docling --->\n")
                fout.append(table["md"])
                fout.append("\n\n")  

            fout.append('\n\n------------------------------\n\n')

        return "".join(fout)

        # PDFMiner processing
        # for page_layout in extract_pages(in_file):
        #     for element in page_layout:
        #         if isinstance(element, LTTextContainer):
        #             for text_line in element:
        #                 #for character in text_line:
        #                     #if isinstance(character, LTChar):
        #                         0#print(character.fontname)
        #                         #print(character.size)



if __name__ == "__main__":
    # from tkinter import filedialog
    # def choose_file():
    #     root = tk.Tk()
    #     root.withdraw()
    #     path = filedialog.askopenfilename(
    #         title="ファイルを選択",
    #         filetypes=[("テキストファイル", "*.txt"), ("PDFファイル", "*.pdf"), ("すべて", "*.*")]
    #     )
    #     root.destroy()
    # in_file = choose_file()

    in_file = sys.argv[1]
    md = slides2md(in_file)
    with open(in_file + '.slides.md', 'w', encoding='utf-8') as fout:
        fout.write(md)

