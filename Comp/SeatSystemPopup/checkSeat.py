import os
import csv
from win11toast import toast

# これは座席管理システムのためのPythonスクリプトです。以下の指示文により生成しました（一部手修正）。
# 1. 実行者のユーザ名を取得する。
# 2. .\user.csvを読み込み、ユーザ名列が実行ユーザ名と一致する行を取得し、状況列の値を取得する
# 3. 値が「退社」のときにポップアップを表示する。windows11のトーストメッセージを表示するようにしてください。
#      メッセージ内に「座席管理システムを開く」ボタンを配置し、クリックするとhttps://google.comに遷移するようにしてください。
#      メッセージのタイトルは「★座席管理システム」、メッセージ本文は「状態が「退社」となっています。登録をお願いします。」としてください。

def get_executing_username():
    """Retrieve the username of the executing user."""
    return os.getlogin()

def read_user_csv(file_path):
    """Open and read the user.csv file."""
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)  # Example: Print each row, modify as needed

def get_user_status(file_path, username):
    """Retrieve the status of the given username from the CSV file."""
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("ユーザ名") == username:
                return row.get("状況")  # Return the value of the "状況" column
    return None

def show_popup(message):
    """Display a Windows toast notification with the given message."""
    toast("★座席管理システム", 
          message, 
          duration="long", 
          scenario="reminder", 
          button={'activationType': 'protocol', 'arguments': 'https://google.com', 'content': '座席管理システムを開く'}
    )  # For Windows 11

# Example usage
if __name__ == "__main__":
    username = get_executing_username()
    print(f"Executing user: {username}")
    
    csv_path = r".\user.csv"
    status = get_user_status(csv_path, username)
    
    if status == "退社":
        show_popup(f"状態が「退社」となっています。登録をお願いします。")
        