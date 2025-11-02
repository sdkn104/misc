import pdfplumber
from pprint import pprint

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

        first_page = pdf.pages[0]
        #print(first_page.extract_text())
        #with open(in_file + '.plumber.json', 'w', encoding='utf-8') as fout:
        #    fout.write(first_page.to_json())
        #with open(in_file + '.plumber.dict', 'w', encoding='utf-8') as fout:
        #    pprint(first_page.to_dict(), fout)
        im = first_page.to_image()
        im.draw_rects(first_page.extract_words(), stroke="blue")
        #im.draw_rects(first_page.extract_text_lines(), stroke="red")
        tboxes = first_page.objects.get("textboxhorizontal","")
        im.draw_rects([(b.get("x0",0),b.get("top",0), b.get("x1",1), b.get("bottom",1)) for b in first_page.objects.get("textboxhorizontal",[])], stroke="red")
        #im.draw_rects(first_page.extract_tables(), stroke="green")
        im.show()
        im.save(in_file + '.plumber.png')

