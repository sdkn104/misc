"""
Outlook返信監視ツール
実行中の旧Outlookを監視し、返信・転送画面が開いたときに指定テキストを挿入する

必要ライブラリ: pip install pywin32

【仕組み】
Outlook Application オブジェクトは単一インスタンスCOMサーバーとして登録されている。
そのため DispatchWithEvents("Outlook.Application", ...) は起動済みの Outlook に
接続しつつ、IConnectionPoint 経由でイベントシンクを正しく接続できる。
Application オブジェクト自体に NewInspector イベントが存在するため、
Inspectors コレクション経由よりも確実に動作する。
"""

import time
import win32com.client
import pythoncom

# =====================================================
# 設定: 挿入するテキストをここで変更してください
# =====================================================
INSERT_TEXT = "ここに挿入するテキストを入力してください。"
# =====================================================

# Outlook定数
OL_MAIL_ITEM = 43
OL_FORMAT_HTML = 2


def is_reply_or_forward(subject: str) -> bool:
    s = subject.strip().upper()
    return (
        s.startswith("RE:") or
        s.startswith("FW:") or
        s.startswith("FWD:") or
        s.startswith("転送:")
    )


def insert_text_into_mail(item) -> bool:
    try:
        if item.BodyFormat == OL_FORMAT_HTML:
            html = item.HTMLBody
            html_insert = f"<p style='color:#333;'>{INSERT_TEXT}</p>"

            body_start = html.lower().find("<body")
            if body_start != -1:
                tag_end = html.find(">", body_start)
                if tag_end != -1:
                    pos = tag_end + 1
                    item.HTMLBody = html[:pos] + html_insert + html[pos:]
                    return True
            item.HTMLBody = html_insert + html
        else:
            item.Body = INSERT_TEXT + "\n\n" + item.Body

        return True
    except Exception as e:
        print(f"  [挿入エラー] {e}")
        return False


class OutlookHandler:
    """Application オブジェクトのイベントハンドラー。
    Application に直接 NewInspector イベントがあるためこちらの方が確実。"""

    def OnNewInspector(self, inspector):
        # アイテムが完全に初期化されるまで少し待機
        time.sleep(0.5)

        try:
            item = inspector.CurrentItem

            if item.Class != OL_MAIL_ITEM:
                return

            subject = item.Subject or ""

            if not is_reply_or_forward(subject):
                return

            print(f"[検出] 返信/転送画面: {subject[:70]}")

            if insert_text_into_mail(item):
                print("[OK] テキストを挿入しました")

        except Exception as e:
            print(f"[エラー] {e}")


def main():
    pythoncom.CoInitialize()

    try:
        # Outlookは単一インスタンスCOMサーバーなので、起動済みでも接続される。
        # DispatchWithEvents で接続と同時にイベントシンクを接続する。
        _outlook_app = win32com.client.DispatchWithEvents(
            "Outlook.Application",
            OutlookHandler,
        )

        print("[監視中] 返信・転送画面の検出を開始しました")
        print(f"[設定] 挿入テキスト: {INSERT_TEXT[:70]}")
        print("終了するには Ctrl+C を押してください。\n")

        while True:
            pythoncom.PumpWaitingMessages()
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n[終了] 監視を停止しました。")
    finally:
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
