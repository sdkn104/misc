import json
from datetime import datetime
import yaml
import os

def sanitize_filename(filename):
    """
    WindowsとSharePoint両方で許可されない文字をサニタイズする関数
    削除対象: < > : " / \ | ? * # % &
    
    Args:
        filename (str): ファイル名
        
    Returns:
        str: サニタイズされたファイル名
    """
    # Windows と SharePoint の両方で許可されない文字
    invalid_chars = r'<>:"/\|?*#%&'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename.strip()


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
            # 送信日とメール件名を取得（キー名は適宜調整）
            sent_date = item.get('sent', '')  # 送信日（YYYY-MM-DD形式と想定）
            subject = item.get('subject', 'No Subject')  # メール件名
            
            # subjectをサニタイズ（Windowsで許可されない文字を削除）
            subject = sanitize_filename(subject)
            
            # 日付からYYYYMMDDとYYYYMMを抽出
            if sent_date:
                # "2024-01-15" 形式の場合
                date_str = sent_date.replace('-', '').replace('/', '')[:8]
                folder_name = date_str[:6]  # YYYYMM
            else:
                date_str = "00000000"
                folder_name = "000000"
            
            # ファイル名：YYYYMMDD_件名_ID.txt
            filename = f"{date_str}_{subject}_{i}.txt"
            
            # フォルダを作成：emails/YYYYMM
            os.makedirs(f"emails/{folder_name}", exist_ok=True)
            with open(f"emails/{folder_name}/{filename}", "w", encoding="utf-8") as f:
                f.write(dict_to_formatted_text(item))
            print("write file", datetime.now())
            


if __name__ == "__main__":
    main()

