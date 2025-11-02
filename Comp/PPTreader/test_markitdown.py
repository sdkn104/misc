from markitdown import MarkItDown

from pprint import pprint


in_files = [
    'test.pptx',
    '04-1.pptx',
    '2021_theme137_2.pptx',
    'generally_02.pptx',
    'nyumon6.pptx',
    'pwhr2020_manual_ref_4_staff.pptx',
    'sdgs_miraikoshien_template-2021.pptx',
    'seiho_slides(2023)_2.pptx',
    'sinnkyouzai.pptx',
]

for in_file in in_files:
    with open(in_file, 'rb') as fin:
        md = MarkItDown(enable_plugins=False) # Set to True to enable plugins
        result = md.convert(in_file)
        with open(in_file + '.markitdown.md', 'w', encoding='utf-8') as fout:
            fout.write(result.text_content)
        with open(in_file + '.markitdown.obj', 'w', encoding='utf-8') as fout:
            pprint(result.markdown, fout)
