import os
from pprint import pprint
import pandas as pd
import pptxtopdf

import pdfplumber

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

#from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
#from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter
#from docling.pipeline.simple_pipeline import SimplePipeline
#from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline

LayParam = {
    "SlideTitleYRatio": 0.15,
    "SlideTitleWidthRatio": 0.15,
}

in_files = [
    '2021_test.pdf',
    '2021_theme137_2.pdf',
    'CorpStrategy2025.pdf',
    'gen_test.pdf',
    'test.pdf',
    '04-1.pdf',
    'generally_02.pdf',
    'nyumon6.pdf',
    'pdf_test.pdf',
    'pwhr2020_manual_ref_4_staff.pdf',
    'sdgs_miraikoshien_template-2021.pdf',
    'seiho_slides(2023)_2.pdf',
    'sinnkyouzai.pdf',
    '地方議会活性化シンポジウム.pdf',
]

for in_file in in_files:

    # Docling document conversion
    print(f"Document {in_file} converting by Docling...")
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
        pptxtopdf.convert(in_file)
        in_file = os.path.splitext(in_file)[0] + '.pdf'

    # Pdfplumber processing
    print(f'Processing {in_file}...')
    with pdfplumber.open(in_file, laparams={"line_overlap": 0.5 }) as pdf:
        # output files
        #pages_obj = [page.objects for page in pdf.pages]
        #with open(in_file + '.plumber.obj', 'w', encoding='utf-8') as fout:
        #    pprint(pages_obj, fout)
        textbox_obj = [page.objects.get("textboxhorizontal","") for page in pdf.pages]
        with open(in_file + '.plumber.tbox', 'w', encoding='utf-8') as fout:
            pprint(textbox_obj, fout)
        tables_obj = [page.extract_tables() for page in pdf.pages]
        with open(in_file + '.plumber.tbl', 'w', encoding='utf-8') as fout:
            pprint(tables_obj, fout)

        # visualize textboxes
        first_page = pdf.pages[1]
        im = first_page.to_image()
        im.draw_rects(first_page.extract_words(), stroke="blue", stroke_width=2)
        tboxes = first_page.objects.get("textboxhorizontal","")        
        pprint([b for b in first_page.objects.get("textboxhorizontal",[]) if "x0" not in b.keys()])
        pprint([b for b in first_page.objects.get("textboxhorizontal",[]) if "x1" not in b.keys()])
        pprint([b for b in first_page.objects.get("textboxhorizontal",[]) if "top" not in b.keys()])
        pprint([b for b in first_page.objects.get("textboxhorizontal",[]) if "bottom" not in b.keys()])
        im.draw_rects([(b.get("x0",0),b.get("top",0), b.get("x1",1), b.get("bottom",1)) for b in first_page.objects.get("textboxhorizontal",[])], stroke="red", stroke_width=1)
        #im.draw_rects([t["bbox"] for t in docling_tables if t["page_no"] == first_page.page_number], stroke="green", stroke_width=1)
        #im.show()
        #im.save(in_file + '.plumber.png')

        # layout analysis
        for page in pdf.pages:
            for tbox in page.objects.get("textboxhorizontal", []):
                if tbox.get("bottom", None) < page.height * LayParam["SlideTitleYRatio"] and tbox.get("width", None) > page.width * LayParam["SlideTitleWidthRatio"]:
                    tbox["lay_title"] = True
                    break

        # output markdown for slides
        with open(in_file + '.slides.md', 'w', encoding='utf-8') as fout:
            fout.write("---\nmarp: true\nheader: ' '\nfooter: ' '\n---\n\n")
            for page in pdf.pages:
                # Docling tables on this page
                page_docling_tables = [docling_table for docling_table in docling_tables if docling_table["page_no"] == page.page_number]

                # Remove overlapping tables
                page2 = page
                for t in page_docling_tables:
                   bb = t["bbox"]
                   bbx = (bb.l, page.height - bb.t, bb.r, page.height - bb.b)
                   page2 = page2.outside_bbox(bbx, relative=False, strict=True)

                # Textboxes
                tboxes = page2.objects.get("textboxhorizontal", [])
                title_list = [tbox.get("text","") for tbox in tboxes if tbox.get("lay_title", False)]
                print(title_list)
                title_text = "  ".join(title_list).replace('\n','').strip()
                fout.write("## " + title_text + '\n\n')
                for tbox in tboxes:
                    if tbox.get("lay_title", False):
                        continue
                    else:
                        fout.write("<div class='textbox'>\n")
                        fout.write(tbox.get("text","") + '\n')
                        fout.write("</div>\n\n")

                # for table in page.extract_tables():
                #     #pprint(table)
                #     df = pd.DataFrame(table)
                #     #pprint(df)
                #     fout.write("\n<!--- plumber --->\n")
                #     fout.write(df.to_markdown())
                #     fout.write("\n\n")

                # Docling tables
                for table in page_docling_tables:
                    fout.write("\n<!--- docling --->\n")
                    fout.write(table["md"])
                    fout.write("\n\n")  

                fout.write('\n\n------------------------------\n\n')

        # PDFMiner processing
        for page_layout in extract_pages(in_file):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        #for character in text_line:
                            #if isinstance(character, LTChar):
                                0#print(character.fontname)
                                #print(character.size)



exit()

