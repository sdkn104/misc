from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.high_level import extract_text
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams
from pprint import pprint
output_string = StringIO()


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
    with open(in_file, 'rb') as fin:
        extract_text_to_fp(fin, output_string, laparams=LAParams(), output_type='text', codec=None)
        with open(in_file + '.miner.txt', 'w', encoding='utf-8') as fout:
            fout.write(output_string.getvalue())

        fin.seek(0)
        output_string.seek(0)
        extract_text_to_fp(fin, output_string, laparams=LAParams(), output_type='html', codec=None)
        with open(in_file + '.miner.htm', 'w', encoding='utf-8') as fout:
            fout.write(output_string.getvalue())

        fin.seek(0)
        output_string.seek(0)
        extract_text_to_fp(fin, output_string, laparams=LAParams(), output_type='xml', codec=None)
        with open(in_file + '.miner.xml', 'w', encoding='utf-8') as fout:
            fout.write(output_string.getvalue())

        fin.seek(0)
        pages = extract_pages(fin)
        pages_obj = [vars(page) for page in pages]
        with open(in_file + '.miner.obj', 'w', encoding='utf-8') as fout:
            pprint(pages_obj, fout)

    for page_layout in extract_pages(in_file):
        pprint(page_layout)
        #print(vars(page_layout))
        #for element in page_layout:
            #print(element)
    