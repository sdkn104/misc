import xml.etree.ElementTree as ET
import pandas as pd
from typing import Optional
from lxml import html

def convTag2Table(xml_text: str, df: pd.DataFrame) -> None:
    """
    XMLテキストをテーブル形式に変換してdataFrameに格納する
    
    Args:
        xml_text: XML形式のテキスト
        df: 変換結果を格納するpandas DataFrame（参照で更新）
    """

    doc = html.fromstring(xml_text) 
    xml_text = html.tostring(doc, encoding="utf-8", pretty_print=True, method="xml")

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"XMLパースエラー: {e}")
        return
    
    rows = []
    current_row = {}
    
    def dfs(element, level: int) -> None:
        """
        DFS探索してXMLを処理する
        
        Args:
            element: 処理するXML要素
            level: 階層レベル（1から始まる）
        """
        nonlocal current_row
        
        col_name = str(level)
        
        # テキストを持つかどうかを判定
        has_text = element.text and element.text.strip()
        
        # テキストがある場合のみ、値を書き込む処理を行う
        if has_text:
            value = element.text.strip()
            
            # 同じレベルに既に値がある場合は、新しい行を開始
            if col_name in current_row:
                # 前の行を保存
                rows.append(current_row.copy())
                # 新しい行を準備（前の行の値をコピー）
                new_row = {}
                for k, v in current_row.items():
                    level_k = int(k)
                    if level_k < level:
                        new_row[k] = "" # v
                current_row = new_row
            
            # 値を書き込む
            current_row[col_name] = value
        else:
            # テキストを持たない場合は、タグ名を「TAG:タグ名」形式で出力
            # ただし、同じレベルに既に値がある場合は、行を進めず値も書き出さない
            if col_name not in current_row:
                value = f"TAG:{element.tag}"
                current_row[col_name] = value
        
        # 子要素を処理
        for child in element:
            dfs(child, level + 1)
    
    # ルート要素からDFS開始
    dfs(root, 1)
    
    # 最後の行を追加
    if current_row:
        rows.append(current_row)
    
    # DataFrameに変換
    if rows:
        temp_df = pd.DataFrame(rows)
        # 列の順序を調整（1, 2, 3...の順）
        level_cols = sorted(temp_df.columns, key=lambda x: int(x) if x.isdigit() else float('inf'))
        for col in level_cols:
            df[col] = temp_df[col]


def convTag2TableFile(xml_file: str, csv_file: str) -> None:
    """
    XMLファイルを読み込み、テーブル形式に変換してCSVファイルに出力する
    
    Args:
        xml_file: 入力XMLファイルのパス
        csv_file: 出力CSVファイルのパス
    """
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            xml_text = f.read()
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {xml_file}")
        return
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")
        return
    
    df = pd.DataFrame()
    convTag2Table(xml_text, df)
    
    try:
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"CSV出力完了: {csv_file}")
    except Exception as e:
        print(f"CSV出力エラー: {e}")


if __name__ == "__main__":
    # テスト用サンプルコード
    sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <parent1>
        <child1>value1</child1>
        <child2>value2</child2>
    </parent1>
    <parent2>text_content</parent2>
</root>"""
    
    df = pd.DataFrame()
    #convTag2Table(sample_xml, df)
    print(df)
    #convTag2TableFile("348AC0000000117_20250601_504AC0000000068.xml", "output_xml.csv")
    convTag2TableFile("L_202500040EN.000101.fmx.xml.html", "output_html.csv")
