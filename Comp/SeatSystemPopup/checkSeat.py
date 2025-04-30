import os
import csv
from win10toast import ToastNotifier

# 1. 実行者のユーザ名を取得する。
# 2. .\user.csvを読み込み、ユーザ名列が実行ユーザ名と一致する行を取得し、状況列の値を取得する
# 3. 値が「退社」のときにポップアップを表示する。


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
    toaster = ToastNotifier()
    toaster.show_toast("Notification", message, duration=10)

# Example usage
if __name__ == "__main__":
    username = get_executing_username()
    print(f"Executing user: {username}")
    
    csv_path = r".\user.csv"
    status = get_user_status(csv_path, username)
    
    if status == "退社":
        show_popup(f"ユーザ {username} は退社しています。")
        