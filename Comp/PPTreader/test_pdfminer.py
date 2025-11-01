from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
output_string = StringIO()
with open('generally_02.pdf', 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(),
                       output_type='html', codec=None)
    print(output_string.getvalue().strip())