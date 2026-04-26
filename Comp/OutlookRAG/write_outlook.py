import json
from datetime import datetime
import yaml
import os

def dict_to_formatted_text(data_dict):
    """
    辞書を以下の形式のテキストに変換する関数
    
    【タグ名】
    内容テキスト
    
    Args:
        data_dict (dict): 変換対象の辞書
        
    Returns:
        str: フォーマットされたテキスト
    """
    lines = []
    for key, value in data_dict.items():
        lines.append(f"【{key}】")
        lines.append(str(value)+"\n")  # 内容の後に改行を追加
    return "\n".join(lines)


def main():
    """メイン処理"""
    input_file = "emails.json"  # メールデータが格納されたJSONファイル

    """JSONファイルからメールデータを読み込む"""
    with open(input_file, 'r', encoding='utf-8') as json_file:
        items = json.load(json_file)
        for (i, item) in enumerate(items):
            #with open(f"emails/{i}.txt", "w", encoding="utf-8") as f:
            #    json.dump(item, f, indent=4, ensure_ascii=False)
            os.makedirs(f"emails/{item['folder']}", exist_ok=True)
            with open(f"emails/{item['folder']}/{i}.txt", "w", encoding="utf-8") as f:
                #yaml.dump(item, f, allow_unicode=True, sort_keys=False)
                f.write(dict_to_formatted_text(item))
            print("write file", datetime.now())
            


if __name__ == "__main__":
    main()

