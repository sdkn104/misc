"""
HTMLを簡略化するツール
- 子孫にテキストを含まない要素を削除
- テキストを直接含まない要素の属性（class, id など）を削除
"""

from lxml import html, etree
from pathlib import Path
from typing import Optional


def has_text_content(element) -> bool:
    """
    要素またはその子孫にテキストコンテンツを含むかチェック
    
    Args:
        element: チェック対象の要素
    
    Returns:
        テキストを含む場合 True
    """
    # 要素が直接テキストを含むかチェック
    if element.text and element.text.strip():
        return True
    
    # 子要素を再帰的にチェック
    for child in element:
        if has_text_content(child):
            return True
    
    # tail テキスト（次の要素の前のテキスト）をチェック
    if element.tail and element.tail.strip():
        return True
    
    return False


def remove_empty_elements(element) -> bool:
    """
    テキストを含まない子要素を削除
    
    Args:
        element: 処理対象の要素
    
    Returns:
        この要素自体を削除すべき場合 True
    """
    # 子要素を逆順でイテレート（削除時のインデックスズレを防ぐ）
    for child in list(element):
        # 再帰的に子要素の子要素をチェック
        should_remove = remove_empty_elements(child)
        
        # テキストを含まなければ削除
        if not has_text_content(child):
            element.remove(child)
    
    # この要素自体にテキストがなく、子要素がない場合は削除を推奨
    return not has_text_content(element) and len(element) == 0


def remove_unnecessary_attributes(element):
    """
    テキストを直接含まない要素から属性を削除
    
    Args:
        element: 処理対象の要素
    """
    # テキストを直接含まない場合、属性を削除
    if not (element.text and element.text.strip()):
        # 削除する属性リスト
        attrs_to_remove = list(element.attrib.keys())
        for attr in attrs_to_remove:
            del element.attrib[attr]
    
    # 子要素を再帰的に処理
    for child in element:
        remove_unnecessary_attributes(child)


def unwrap_single_child_elements(element):
    """
    子要素が1つしかない要素で、要素自身が直接テキストを持たない場合に
    その要素を子要素で置き換える（unwrap）処理を行う。

    Args:
        element: 処理対象の要素

    Returns:
        置き換え後にその位置に残る要素（場合によっては子要素）
    """
    # まず子を再帰的に処理して置き換えを反映
    for i, child in enumerate(list(element)):
        new_child = unwrap_single_child_elements(child)
        if new_child is not child:
            element.remove(child)
            element.insert(i, new_child)

    # この要素自身をunwrapするか判定
    if not (element.text and element.text.strip()) and len(element) == 1:
        only = element[0]
        # tail を引き継ぐ
        if (not only.tail or not only.tail.strip()) and element.tail:
            only.tail = element.tail
        return only

    return element


def simplify_html(html_content: str) -> str:
    """
    HTMLを簡略化
    
    Args:
        html_content: 入力HTML文字列
    
    Returns:
        簡略化されたHTML文字列
    """
    # HTMLをパース
    try:
        doc = html.fromstring(html_content)
    except Exception as e:
        print(f"HTMLパースエラー: {e}")
        return html_content
    
    # テキストを含まない要素を削除
    remove_empty_elements(doc)

    # 子要素が一つだけの要素をunwrap（親を削除して子を昇格）
    #new_doc = unwrap_single_child_elements(doc)
    #if new_doc is not doc:
    #    doc = new_doc

    # 不要な属性を削除
    remove_unnecessary_attributes(doc)
    
    # HTML文字列に変換
    result = html.tostring(doc, encoding='unicode', pretty_print=True, method='html')
    
    return result


def simplify_html_file(input_file: str, output_file: Optional[str] = None) -> str:
    """
    ファイルから読み込んでHTMLを簡略化し、結果を保存
    
    Args:
        input_file: 入力HTMLファイルパス
        output_file: 出力ファイルパス（指定なしの場合は _simplified.html を追加）
    
    Returns:
        簡略化されたHTML文字列
    """
    # ファイルを読み込む
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {input_file}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 簡略化
    simplified = simplify_html(html_content)
    
    # 出力ファイルパスの決定
    if output_file is None:
        output_path = input_path.parent / f"{input_path.stem}_simplified.html"
    else:
        output_path = Path(output_file)
    
    # 結果を保存
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(simplified)
    
    print(f"簡略化完了: {output_path}")
    return simplified


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python simplify_html.py <入力ファイル> [出力ファイル]")
        print()
        print("例:")
        print("  python simplify_html.py input.html")
        print("  python simplify_html.py input.html output.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        simplify_html_file(input_file, output_file)
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)
