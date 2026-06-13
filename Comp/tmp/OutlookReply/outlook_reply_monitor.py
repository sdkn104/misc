"""
Outlook返信監視ツール
実行中の旧Outlookを監視し、返信/転送画面の重要度を監視してテキストを挿入する

必要ライブラリ: pip install pywin32

【フロー】
1. 返信/転送画面が開いたら検出し、重要度を最大 MONITOR_DURATION 秒間監視
2. その間に重要度が「低」に設定されたら、本文に PLACEHOLDER_TEXT を挿入
3. PLACEHOLDER_DURATION 秒後に PLACEHOLDER_TEXT を INSERT_TEXT に置換
4. MONITOR_DURATION 秒以内に「低」にならなければ何もしない
"""

import sys
import time
import win32com.client
import pythoncom

# =====================================================
# 設定
# =====================================================
INSERT_TEXT        = "ここに挿入するテキストを入力してください。"
PLACEHOLDER_TEXT   = "AIによる回答作成中..."
MONITOR_DURATION   = 10   # 重要度を監視する秒数
PLACEHOLDER_DURATION = 5  # プレースホルダー表示後、置換するまでの秒数
# =====================================================

POLL_INTERVAL = 0.5  # 秒

# Outlook 定数
OL_MAIL_ITEM      = 43
OL_FORMAT_HTML    = 2
OL_IMPORTANCE_LOW = 0


# ---------------------------------------------------------------------------
# 本文操作
# ---------------------------------------------------------------------------

def _insert_at_top(item, text_plain: str, text_html: str) -> bool:
    """本文の先頭（<body>直後 or 先頭）にテキストを挿入する"""
    try:
        if item.BodyFormat == OL_FORMAT_HTML:
            html = item.HTMLBody
            body_pos = html.lower().find("<body")
            if body_pos != -1:
                tag_end = html.find(">", body_pos)
                if tag_end != -1:
                    pos = tag_end + 1
                    item.HTMLBody = html[:pos] + text_html + html[pos:]
                    print(f"  [本文操作] HTML挿入完了 (pos={pos})")
                    return True
            item.HTMLBody = text_html + html
            print("  [本文操作] HTML先頭に挿入完了（<body>未検出）")
        else:
            item.Body = text_plain + "\n\n" + item.Body
            print("  [本文操作] プレーンテキスト挿入完了")
        return True
    except Exception as e:
        print(f"  [本文操作エラー] {e}")
        return False


def insert_placeholder(item) -> bool:
    """PLACEHOLDER_TEXT を本文先頭に挿入する"""
    print(f"  [プレースホルダー] 「{PLACEHOLDER_TEXT}」を挿入します")
    return _insert_at_top(
        item,
        text_plain=PLACEHOLDER_TEXT,
        text_html=f"<p>{PLACEHOLDER_TEXT}</p>",
    )


def replace_placeholder_with_final(item) -> bool:
    """PLACEHOLDER_TEXT を INSERT_TEXT に置換する"""
    print(f"  [置換] 「{PLACEHOLDER_TEXT}」→ INSERT_TEXT")
    try:
        if item.BodyFormat == OL_FORMAT_HTML:
            html = item.HTMLBody
            if PLACEHOLDER_TEXT in html:
                item.HTMLBody = html.replace(
                    PLACEHOLDER_TEXT,
                    INSERT_TEXT,
                    1,
                )
                print("  [置換] HTML置換完了")
                return True
            # プレースホルダーが見つからない場合は先頭に挿入
            print("  [置換] プレースホルダー未検出 → 先頭に挿入")
        else:
            body = item.Body or ""
            if PLACEHOLDER_TEXT in body:
                item.Body = body.replace(PLACEHOLDER_TEXT, INSERT_TEXT, 1)
                print("  [置換] プレーンテキスト置換完了")
                return True
            print("  [置換] プレースホルダー未検出 → 先頭に挿入")

        return _insert_at_top(
            item,
            text_plain=INSERT_TEXT,
            text_html=f"<p style='color:#333;'>{INSERT_TEXT}</p>",
        )
    except Exception as e:
        print(f"  [置換エラー] {e}")
        return False


# ---------------------------------------------------------------------------
# 監視状態管理
# ---------------------------------------------------------------------------

class MonitoredReply:
    """1つの返信/転送画面の監視状態を保持する"""

    def __init__(self, item, caption: str):
        self.item = item
        self.caption = caption
        self.state = "monitoring"       # "monitoring" → "placeholder" → "done"
        self.state_since = time.time()
        self.last_log_time = 0.0        # ポーリングログの抑制用

    def elapsed(self) -> float:
        return time.time() - self.state_since

    def transition(self, new_state: str):
        self.state = new_state
        self.state_since = time.time()
        print(f"  [状態遷移] {self.caption[:40]!r} → {new_state}")


# キー: inspector.Caption（返信ウィンドウタイトル）
monitored: dict[str, MonitoredReply] = {}


def _is_already_tracked(item) -> bool:
    """INSERT_TEXT またはPLACEHOLDER_TEXT が本文に含まれるか確認"""
    try:
        body = (item.HTMLBody if item.BodyFormat == OL_FORMAT_HTML else item.Body) or ""
        return INSERT_TEXT in body or PLACEHOLDER_TEXT in body
    except Exception:
        return True


def poll_once(outlook):
    global monitored

    count = outlook.Inspectors.Count

    # ── 新しい返信インスペクターを検出 ──────────────────────────────
    for i in range(1, count + 1):
        try:
            inspector = outlook.Inspectors.Item(i)
            item = inspector.CurrentItem

            if item.Class != OL_MAIL_ITEM:
                continue

            subject = item.Subject or ""
            if not (subject.strip().upper()).startswith(("RE:", "FW:", "FWD:", "転送:")):
                continue

            key = inspector.Caption
            if key in monitored:
                continue  # 既に監視中

            if _is_already_tracked(item):
                print(f"  [スキップ] 処理済みのためスキップ: {subject[:60]!r}")
                continue

            print(f"\n[検出] 返信/転送画面: {subject[:70]!r}")
            print(f"  → {MONITOR_DURATION}秒以内に重要度「低」を検出したらテキストを挿入します")
            monitored[key] = MonitoredReply(item, key)

        except Exception as e:
            print(f"  [Inspector {i} 検出エラー] {e}")

    # ── 監視中アイテムを処理 ─────────────────────────────────────────
    done_keys = []
    now = time.time()

    for key, reply in monitored.items():
        try:
            item = reply.item

            if reply.state == "monitoring":
                importance = item.Importance
                elapsed = reply.elapsed()

                # 2秒ごとにログ表示
                if now - reply.last_log_time >= 2.0:
                    print(f"  [監視中] {key[:40]!r}  重要度={importance}  経過={elapsed:.1f}s/{MONITOR_DURATION}s")
                    reply.last_log_time = now

                if importance == OL_IMPORTANCE_LOW:
                    print(f"\n  → 重要度「低」検出！プレースホルダーを挿入します")
                    if insert_placeholder(item):
                        print(f"  → 「{PLACEHOLDER_TEXT}」を挿入しました")
                        print(f"  → {PLACEHOLDER_DURATION}秒後に INSERT_TEXT へ置換します")
                    reply.transition("placeholder")

                elif elapsed >= MONITOR_DURATION:
                    print(f"\n  → {MONITOR_DURATION}秒経過。重要度「低」未検出 → 何もしません: {key[:40]!r}")
                    done_keys.append(key)

            elif reply.state == "placeholder":
                elapsed = reply.elapsed()

                if now - reply.last_log_time >= 2.0:
                    print(f"  [待機中] {key[:40]!r}  置換まで {PLACEHOLDER_DURATION - elapsed:.1f}秒")
                    reply.last_log_time = now

                if elapsed >= PLACEHOLDER_DURATION:
                    print(f"\n  → {PLACEHOLDER_DURATION}秒経過。INSERT_TEXT へ置換します")
                    if replace_placeholder_with_final(item):
                        print(f"[OK] 挿入完了: {key[:60]!r}")
                    done_keys.append(key)

        except Exception as e:
            print(f"  [監視エラー] {key!r}: {e}")
            done_keys.append(key)

    for key in done_keys:
        monitored.pop(key, None)


# ---------------------------------------------------------------------------
# メインループ
# ---------------------------------------------------------------------------

def main():
    print("[起動] pythoncom.CoInitialize() 実行中...")
    pythoncom.CoInitialize()
    print("[起動] CoInitialize() 完了")

    try:
        print("[起動] GetActiveObject('Outlook.Application') 実行中...")
        try:
            outlook = win32com.client.GetActiveObject("Outlook.Application")
            print("[起動] Outlook接続成功")
        except Exception as e:
            print(f"[エラー] Outlookが起動していません: {e}")
            print("  Outlookを起動してから再実行してください。")
            sys.exit(1)

        print(f"\n[設定] 重要度監視: {MONITOR_DURATION}秒 / プレースホルダー待機: {PLACEHOLDER_DURATION}秒")
        print(f"[設定] 挿入テキスト: {INSERT_TEXT[:70]}")
        print(f"[監視中] {POLL_INTERVAL}秒ごとにポーリング開始")
        print("終了するには Ctrl+C を押してください。\n")

        tick = 0
        while True:
            pythoncom.PumpWaitingMessages()

            try:
                poll_once(outlook)
            except Exception as e:
                print(f"[エラー] ポーリング中: {e}")

            time.sleep(POLL_INTERVAL)
            tick += 1
            if tick % 120 == 0:
                print(f"[監視中] {tick * POLL_INTERVAL:.0f}秒経過  監視中ウィンドウ数: {len(monitored)}")

    except KeyboardInterrupt:
        print("\n[終了] 監視を停止しました。")
    finally:
        print("[終了] CoUninitialize() 実行中...")
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
