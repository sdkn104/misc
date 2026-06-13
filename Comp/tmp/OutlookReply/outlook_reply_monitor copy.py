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
        fmt = item.BodyFormat
        print(f"  [挿入] BodyFormat={fmt} ({'HTML' if fmt == OL_FORMAT_HTML else 'プレーンテキスト'})")

        if fmt == OL_FORMAT_HTML:
            html = item.HTMLBody
            print(f"  [挿入] HTMLBody 取得: {len(html)} 文字")
            html_insert = f"<p style='color:#333;'>{INSERT_TEXT}</p>"

            body_start = html.lower().find("<body")
            if body_start != -1:
                tag_end = html.find(">", body_start)
                if tag_end != -1:
                    pos = tag_end + 1
                    item.HTMLBody = html[:pos] + html_insert + html[pos:]
                    print(f"  [挿入] <body>タグ直後に挿入完了 (pos={pos})")
                    return True
            item.HTMLBody = html_insert + html
            print("  [挿入] <body>タグ未検出のため先頭に挿入完了")
        else:
            item.Body = INSERT_TEXT + "\n\n" + item.Body
            print("  [挿入] プレーンテキスト先頭に挿入完了")

        return True
    except Exception as e:
        print(f"  [挿入エラー] {e}")
        return False


class OutlookHandler:
    """Application オブジェクトのイベントハンドラー。
    Application に直接 NewInspector イベントがあるためこちらの方が確実。"""

    def OnNewInspector(self, inspector):
        print("[イベント] OnNewInspector が呼ばれました")

        # アイテムが完全に初期化されるまで少し待機
        print("[イベント] 0.5秒待機中...")
        time.sleep(0.5)

        try:
            item = inspector.CurrentItem
            print(f"[イベント] CurrentItem 取得: Class={item.Class}")

            if item.Class != OL_MAIL_ITEM:
                print(f"[スキップ] MailItem ではありません (Class={item.Class})")
                return

            subject = item.Subject or ""
            print(f"[イベント] 件名: {subject[:70]!r}")

            if not is_reply_or_forward(subject):
                print("[スキップ] 返信/転送ではありません")
                return

            print(f"[検出] 返信/転送画面: {subject[:70]}")

            if insert_text_into_mail(item):
                print("[OK] テキストを挿入しました")

        except Exception as e:
            print(f"[エラー] {e}")
            import traceback
            traceback.print_exc()


def main():
    print("[起動] pythoncom.CoInitialize() 実行中...")
    pythoncom.CoInitialize()
    print("[起動] CoInitialize() 完了")

    try:
        print("[起動] Outlook.Application に DispatchWithEvents で接続中...")
        _outlook_app = win32com.client.DispatchWithEvents(
            "Outlook.Application",
            OutlookHandler,
        )
        print(f"[起動] 接続成功: {_outlook_app}")

        print("[監視中] 返信・転送画面の検出を開始しました")
        print(f"[設定] 挿入テキスト: {INSERT_TEXT[:70]}")
        print("終了するには Ctrl+C を押してください。\n")

        tick = 0
        while True:
            pythoncom.PumpWaitingMessages()
            time.sleep(0.1)
            tick += 1
            if tick % 100 == 0:  # 10秒ごとに生存確認
                print(f"[監視中] 待機中... ({tick // 10}秒経過)")

    except KeyboardInterrupt:
        print("\n[終了] 監視を停止しました。")
    finally:
        print("[終了] CoUninitialize() 実行中...")
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
