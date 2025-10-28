

import fitz

try:
    #doc = fitz.open("pdf_test.pdf")
    doc = fitz.open("CorpStrategy2025.pdf")
    
    page = doc[15]


    text = page.get_text("text", sort=True)
    print("=== ページ全体のテキスト ===")
    print(text)
    print("\n\n")

    # ブロック単位でテキストを抽出
    blocks = page.get_text("blocks", sort=True)
    for block in blocks:
        # block[0:4] にBBox(x0, y0, x1, y1)が、block[4]にテキスト block[5] に番号が入っている
        print(f"block No.: {block[5]}")
        print(f"BBox: {block[0:4]}")
        print(f"Text: {block[4].strip()}")
        print("-" * 20)




    doc.close()
except Exception as e:
    print(f"エラー: {e}")
