import pdfplumber
from pprint import pprint

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import (
    HOCRConverter,
    HTMLConverter,
    PDFPageAggregator,
    TextConverter,
    XMLConverter,
)
from pdfminer.image import ImageWriter
from pdfminer.layout import LAParams, LTPage
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfexceptions import PDFValueError
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.utils import AnyIO, FileOrName, open_filename

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar


in_files = [
    'test.pdf',
    '04-1.pdf',
    '2021_theme137_2.pdf',
    'CorpStrategy2025.pdf',
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
    print(f'Processing {in_file}...')
    with pdfplumber.open(in_file, laparams={"line_overlap": 0.5 }) as pdf:
        pages_obj = [page.objects for page in pdf.pages]
        with open(in_file + '.plumber.obj', 'w', encoding='utf-8') as fout:
            pprint(pages_obj, fout)

        textbox_obj = [page.objects.get("textboxhorizontal","") for page in pdf.pages]
        with open(in_file + '.plumber.tbox', 'w', encoding='utf-8') as fout:
            pprint(textbox_obj, fout)

        tables_obj = [page.extract_tables() for page in pdf.pages]
        with open(in_file + '.plumber.tbl', 'w', encoding='utf-8') as fout:
            pprint(tables_obj, fout)

        first_page = pdf.pages[1]
        #print(first_page.extract_text())
        #with open(in_file + '.plumber.json', 'w', encoding='utf-8') as fout:
        #    fout.write(first_page.to_json())
        #with open(in_file + '.plumber.dict', 'w', encoding='utf-8') as fout:
        #    pprint(first_page.to_dict(), fout)
        im = first_page.to_image()
        im.draw_rects(first_page.extract_words(), stroke="blue", stroke_width=2)
        tboxes = first_page.objects.get("textboxhorizontal","")
        
        pprint([b for b in first_page.objects.get("textboxhorizontal",[]) if "x0" not in b.keys()])
        pprint([b for b in first_page.objects.get("textboxhorizontal",[]) if "x1" not in b.keys()])
        pprint([b for b in first_page.objects.get("textboxhorizontal",[]) if "top" not in b.keys()])
        pprint([b for b in first_page.objects.get("textboxhorizontal",[]) if "bottom" not in b.keys()])
        im.draw_rects([(b.get("x0",0),b.get("top",0), b.get("x1",1), b.get("bottom",1)) for b in first_page.objects.get("textboxhorizontal",[])], stroke="red", stroke_width=1)
        
        im.show()
        im.save(in_file + '.plumber.png')

        for page_layout in extract_pages(in_file):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        #for character in text_line:
                            #if isinstance(character, LTChar):
                                0#print(character.fontname)
                                #print(character.size)

        #exit()

exit()
import pdfplumber
from pprint import pprint
pdf = pdfplumber.open("test.pdf", laparams={"line_overlap": 0.5 })
pages_obj = [page.objects for page in pdf.pages]
page = pages_obj[0]
pprint(page)
