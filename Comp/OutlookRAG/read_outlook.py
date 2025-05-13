import win32com.client
import datetime
import gc  # 必要に応じてガベージコレクションを呼び出す
import json
import pickle

"""
pythonで、outlookのメールを取得し、リストに保存する。メモリ管理に気を付けて。取得するメールは指定日付範囲の全メール。すべてのフォルダ内のメールが対象。取得したメールの件名、From, To, Cc, Sent、添付ファイル名を保存する。
"""

def get_all_subfolders(parent_folder):
    """
    指定したフォルダ直下のすべてのサブフォルダを再帰的に取得する。
    """
    folders = []
    try:
        for folder in parent_folder.Folders:
            folders.append(folder)
            folders.extend(get_all_subfolders(folder))
    except Exception as e:
        print(f"フォルダ取得エラー ({parent_folder.Name}): {e}")
    return folders

def get_emails_in_folder(folder, start_date, end_date):
    """
    指定フォルダ内で、[ReceivedTime] をもとに日付範囲で Restrict し、
    メールアイテム (Class 43) の情報を辞書形式でリストにして返す。
    """
    mails = []
    try:
        # Items の取得・ソート
        items = folder.Items
        items.Sort("[ReceivedTime]", True)
        # Outlook の Restrict では日付のフォーマットは MM/DD/YYYY hh:mm AM/PM で指定
        start_str = start_date.strftime("%m/%d/%Y %I:%M %p")
        end_str   = end_date.strftime("%m/%d/%Y %I:%M %p")
        restriction = "[ReceivedTime] >= '{}' AND [ReceivedTime] <= '{}'".format(start_str, end_str)
        restricted_items = items.Restrict(restriction)
        
        # Outlook のコレクションは 1-indexed なので、1 から Count までループ
        count = restricted_items.Count
        for i in range(1, count + 1):
            mail = restricted_items.Item(i)
            # MailItem の Class 番号は 43 なので、これで判定
            if mail.Class == 43:
                try:
                    messageID = mail.entryID
                    subject = mail.Subject
                    sender  = mail.SenderName
                    to      = mail.To
                    cc      = mail.CC
                    sent    = mail.SentOn
                    body    = mail.Body.strip()
                    # 添付ファイルは 1-indexed、件数が 0 の場合も考慮
                    attachments = []
                    attachmentFiles = []
                    if mail.Attachments.Count > 0:
                        for j in range(1, mail.Attachments.Count + 1):
                            att = mail.Attachments.Item(j)
                            attachmentFiles.append(att)
                            attachments.append(att.FileName)
                            del att  # 添付オブジェクトは使い終わったら削除
                    mails.append({
                        "message-id": messageID,
                        "subject": subject,
                        "from":    sender,
                        "to":      to,
                        "cc":      cc,
                        "sent":    sent.strftime("%Y-%m-%d %H:%M:%S"),
                        "body":    body,
                        "attachments": attachments,
                    })
                        
                except Exception as inner_e:
                    print(f"メールアイテム処理エラー: {inner_e}")
                finally:
                    # COM オブジェクトへの参照は都度削除しておく
                    del mail
        # 不要になった COM オブジェクトを解放
        del restricted_items
        del items
        gc.collect()
    except Exception as e:
        print(f"フォルダ {folder.Name} の処理中エラー: {e}")
    return mails

def get_all_emails(start_date, end_date):
    """
    Outlook のすべてのストア（アカウント）について、ルートフォルダとそのサブフォルダ全体を
    再帰的に走査し、指定した日付範囲内のメールアイテムの情報を取得する。
    """
    all_emails = []
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    try:
        print(999)
        print(outlook.Stores.Count)
        inbox = outlook.GetDefaultFolder(6)
        print(inbox.store)
        print(999)
        # 各ストア（アカウント）ごとにルートフォルダから再帰的にフォルダ一覧を作成
        #for store in outlook.Stores:
        for store in [inbox.store]:
            root_folder = store.GetRootFolder() 
            print("root folder:")
            print(root_folder)
            # ルートと全サブフォルダをまとめる
            folders = [root_folder] + get_all_subfolders(root_folder)
            for folder in folders:
                print("sub folder:")
                print(folder)
                try:
                    folder_emails = get_emails_in_folder(folder, start_date, end_date)
                    if folder_emails:
                        all_emails.extend(folder_emails)
                except Exception as fe:
                    print(f"フォルダ {folder.Name} のメール取得エラー: {fe}")
                finally:
                    del folder
            del folders
            # ルートフォルダの参照も削
            del root_folder
        gc.collect()
    except Exception as e:
        print(f"メール全体取得エラー: {e}")
    finally:
        del outlook
        gc.collect()
    return all_emails

if __name__ == '__main__':
    # 例: 2025年1月1日から2025年1月31日までのメールを取得
    start_date = datetime.datetime(2025, 4, 1, 0, 0, 0)
    end_date   = datetime.datetime(2025, 5, 31, 23, 59, 59)
    emails = get_all_emails(start_date, end_date)    
    print("取得したメール数:", len(emails))
    #with open("emails.pkl", "wb") as f:
    #    pickle.dump(emails, f)
    #with open("emails.pkl", "rb") as f:
    #    emails_loaded = pickle.load(f)

    with open("emails.json", "w", encoding="utf-8") as f:
        json.dump(emails, f, indent=4)
    for mail in emails:
        print("件名:", mail["subject"])
        print("From:", mail["from"])
        print("To:", mail["to"])
        print("Cc:", mail["cc"])
        print("Sent:", mail["sent"])
        print("添付ファイル:", mail["attachments"])
        print("-" * 40)
