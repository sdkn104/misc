"""
Outlook返信監視ツール
実行中の旧Outlookを監視し、返信/転送画面の重要度を監視してHTTPリクエストを投げる

必要ライブラリ: pip install pywin32 requests

【フロー】
1. 返信/転送画面が開いたら検出し、重要度を最大 MONITOR_DURATION 秒間監視
2. その間に重要度が「低」に設定されたら:
   a. 本文に PLACEHOLDER_TEXT を挿入
   b. メール情報（件名・本文）をHTTP POSTリクエストで送信（別スレッド）
3. レスポンスが返ったら PLACEHOLDER_TEXT をレスポンステキストに置換
4. MONITOR_DURATION 秒以内に「低」にならなければ何もしない
"""

import sys
import os
import time
import concurrent.futures
from datetime import datetime
import win32com.client
import pythoncom
import requests

# =====================================================
# 設定
# =====================================================
PLACEHOLDER_TEXT     = "AIによる回答作成中..."
MONITOR_DURATION     = 10   # 重要度を監視する秒数
HTTP_URL             = "http://localhost:8000/generate"  # ← 変更してください
HTTP_TIMEOUT         = 60   # HTTPリクエストのタイムアウト秒数
# =====================================================

POLL_INTERVAL = 0.5  # 秒

# Outlook 定数
OL_MAIL_ITEM         = 43
OL_FORMAT_HTML       = 2
OL_IMPORTANCE_LOW    = 0
OL_IMPORTANCE_NORMAL = 1

# HTTP リクエスト用スレッドプール
_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


# ---------------------------------------------------------------------------
# HTTP リクエスト（別スレッドで実行）
# COMオブジェクトはスレッド間で使えないため、呼び出し前にデータを抽出しておく
# ---------------------------------------------------------------------------

def _http_request(subject: str, plain_body: str) -> str:
    """
    HTTPリクエストを送信し、挿入するテキストを返す。
    レスポンスの取り出し方はここでカスタマイズしてください。

    例) JSON レスポンスから特定フィールドを取り出す場合:
        data = resp.json()
        return data["answer"]
    """
    print(f"  [HTTP] POST {HTTP_URL}  (件名: {subject[:40]!r})")
    resp = requests.post(
        HTTP_URL,
        json={"subject": subject, "body": plain_body},
        timeout=HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    print(f"  [HTTP] レスポンス受信: status={resp.status_code}  {len(resp.text)}文字")
    return resp.text


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
    print(f"  [プレースホルダー] 「{PLACEHOLDER_TEXT}」を挿入します")
    return _insert_at_top(
        item,
        text_plain=PLACEHOLDER_TEXT,
        text_html=f"<p><em>{PLACEHOLDER_TEXT}</em></p>",
    )


def replace_placeholder(item, new_text: str) -> bool:
    """PLACEHOLDER_TEXT を new_text に置換する"""
    print(f"  [置換] プレースホルダー → {new_text[:60]!r}")
    try:
        if item.BodyFormat == OL_FORMAT_HTML:
            html = item.HTMLBody
            if PLACEHOLDER_TEXT in html:
                item.HTMLBody = html.replace(PLACEHOLDER_TEXT, new_text, 1)
                print("  [置換] HTML置換完了")
                return True
            print("  [置換] プレースホルダー未検出 → 先頭に挿入")
        else:
            body = item.Body or ""
            if PLACEHOLDER_TEXT in body:
                item.Body = body.replace(PLACEHOLDER_TEXT, new_text, 1)
                print("  [置換] プレーンテキスト置換完了")
                return True
            print("  [置換] プレースホルダー未検出 → 先頭に挿入")

        return _insert_at_top(
            item,
            text_plain=new_text,
            text_html=f"<p>{new_text}</p>",
        )
    except Exception as e:
        print(f"  [置換エラー] {e}")
        return False


# ---------------------------------------------------------------------------
# 監視状態管理
# ---------------------------------------------------------------------------

class MonitoredReply:
    """1つの返信/転送画面の監視状態を保持する"""

    # state 遷移:
    #   "monitoring"  → 重要度「低」検出待ち
    #   "awaiting"    → HTTPリクエスト中（プレースホルダー表示済み）
    #   (done_keys へ追加して monitored から削除)

    def __init__(self, item, caption: str):
        self.item = item
        self.caption = caption
        self.state = "monitoring"
        self.state_since = time.time()
        self.last_log_time = 0.0
        self.future: concurrent.futures.Future | None = None

    def elapsed(self) -> float:
        return time.time() - self.state_since

    def transition(self, new_state: str):
        self.state = new_state
        self.state_since = time.time()
        print(f"  [状態遷移] {self.caption[:40]!r} → {new_state}")


# キー: inspector.Caption（返信ウィンドウタイトル）
monitored: dict[str, MonitoredReply] = {}


def _is_already_tracked(item) -> bool:
    try:
        body = (item.HTMLBody if item.BodyFormat == OL_FORMAT_HTML else item.Body) or ""
        return PLACEHOLDER_TEXT in body
    except Exception:
        return True


def poll_once(outlook):
    count = outlook.Inspectors.Count

    # ── インスペクターを1回走査: クローズ検出 + 新規検出 ───────────
    open_captions: set[str] = set()
    current: list[tuple[str, object]] = []  # (caption, item)
    for i in range(1, count + 1):
        try:
            inspector = outlook.Inspectors.Item(i)
            cap = inspector.Caption
            open_captions.add(cap)          # Caption は CurrentItem より先に収集
            try:
                current.append((cap, inspector.CurrentItem))
            except Exception as e:
                print(f"  [Inspector {i} CurrentItem エラー] {e}")
        except Exception as e:
            print(f"  [Inspector {i} 取得エラー] {e}")

    for key in [k for k in monitored if k not in open_captions]:
        print(f"  [クローズ検出] ウィンドウが閉じられました: {key[:60]!r}")
        monitored.pop(key)

    for caption, item in current:
        try:
            if item.Class != OL_MAIL_ITEM:
                continue

            if item.Sent:
                continue

            subject = item.Subject or ""
            if not (subject.strip().upper()).startswith(("RE:", "FW:", "FWD:", "転送:")):
                continue

            if caption in monitored:
                continue

            if _is_already_tracked(item):
                print(f"  [スキップ] 処理済み: {subject[:60]!r}")
                continue

            print(f"\n[検出] 返信/転送画面: {subject[:70]!r}")
            print(f"  → {MONITOR_DURATION}秒以内に重要度「低」を検出したらHTTPリクエストを送信します")
            monitored[caption] = MonitoredReply(item, caption)

        except Exception as e:
            print(f"  [Inspector 検出エラー] {e}")

    # ── 監視中アイテムを処理 ─────────────────────────────────────────
    done_keys = []
    now = time.time()

    for key, reply in monitored.items():
        try:
            item = reply.item

            if reply.state == "monitoring":
                importance = item.Importance
                elapsed = reply.elapsed()

                if now - reply.last_log_time >= 2.0:
                    print(f"  [監視中] {reply.caption[:40]!r}  重要度={importance}  経過={elapsed:.1f}s/{MONITOR_DURATION}s")
                    reply.last_log_time = now

                if importance == OL_IMPORTANCE_LOW:
                    print(f"\n  → 重要度「低」検出！")

                    # COMオブジェクトはスレッドを跨げないため、先にデータを抽出する
                    subject = item.Subject or ""
                    plain_body = item.Body or ""
                    print(f"  [データ抽出] 件名={subject[:40]!r}  本文={len(plain_body)}文字")

                    insert_placeholder(item)
                    print(f"  → 「{PLACEHOLDER_TEXT}」を挿入しました")

                    try:
                        reply.future = _executor.submit(_http_request, subject, plain_body)
                        print(f"  → HTTPリクエストを送信しました（レスポンス待機中）")
                        reply.transition("awaiting")
                    finally:
                        try:
                            item.Importance = OL_IMPORTANCE_NORMAL
                            print(f"  [優先度リセット] 重要度を「普通」に戻しました")
                        except Exception as e:
                            print(f"  [優先度リセットエラー] {e}")

                elif elapsed >= MONITOR_DURATION:
                    print(f"\n  → {MONITOR_DURATION}秒経過。重要度「低」未検出 → 何もしません: {reply.caption[:40]!r}")
                    done_keys.append(key)

            elif reply.state == "awaiting":
                if now - reply.last_log_time >= 2.0:
                    print(f"  [HTTP待機中] {reply.caption[:40]!r}  経過={reply.elapsed():.1f}s")
                    reply.last_log_time = now

                if reply.future.done():
                    try:
                        result_text = reply.future.result()
                        print(f"\n  → HTTPレスポンス受信。プレースホルダーを置換します")
                        if replace_placeholder(item, result_text):
                            print(f"[OK] 挿入完了: {reply.caption[:60]!r}")
                    except requests.exceptions.Timeout:
                        err = f"[タイムアウト] HTTPリクエストが{HTTP_TIMEOUT}秒以内に完了しませんでした"
                        print(f"  [HTTPエラー] {err}")
                        replace_placeholder(item, err)
                    except requests.exceptions.RequestException as e:
                        err = f"[HTTPエラー] {e}"
                        print(f"  [HTTPエラー] {e}")
                        replace_placeholder(item, err)
                    except Exception as e:
                        err = f"[エラー] {e}"
                        print(f"  [エラー] {e}")
                        replace_placeholder(item, err)

                    done_keys.append(key)

        except Exception as e:
            print(f"  [監視エラー] {reply.caption!r}: {e}")
            done_keys.append(key)

    for key in done_keys:
        monitored.pop(key, None)


# ---------------------------------------------------------------------------
# メインループ
# ---------------------------------------------------------------------------

class _Tee:
    """print() の出力をコンソールとログファイルの両方に書き込む。
    各行の先頭に HH:MM:SS タイムスタンプを付与してログファイルに保存する。"""

    def __init__(self, log_file, console=None):
        self.log_file = log_file
        self.console = console  # None の場合（--noconsole exe）はログのみ

    def write(self, data):
        if self.console:
            try:
                self.console.write(data)
            except Exception:
                pass
        try:
            ts = datetime.now().strftime('%H:%M:%S')
            # 非空行の先頭にタイムスタンプを付与（空行はそのまま）
            out = '\n'.join(
                f"[{ts}] {line}" if line else ''
                for line in data.split('\n')
            )
            self.log_file.write(out)
        except Exception:
            pass

    def flush(self):
        for s in (self.console, self.log_file):
            if s:
                try:
                    s.flush()
                except Exception:
                    pass


def _setup_logging():
    """コンソールとログファイル（プログラムと同フォルダ）の両方に出力する。
    exe 時は sys.__stdout__ が None のためログファイルのみになる。"""
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    log_path = os.path.join(base_dir, 'monitor.log')
    log_file = open(log_path, 'w', encoding='utf-8', buffering=1)

    sys.stdout = _Tee(log_file, console=sys.__stdout__)
    sys.stderr = _Tee(log_file, console=sys.__stderr__)
    print(f"[ログ] 出力先: {log_path}")


def main():
    _setup_logging()
    print("[起動] pythoncom.CoInitialize() 実行中...")
    pythoncom.CoInitialize()
    print("[起動] CoInitialize() 完了")

    try:
        outlook = None
        while outlook is None:
            try:
                outlook = win32com.client.GetActiveObject("Outlook.Application")
                print("[起動] Outlook接続成功")
            except Exception:
                print("[待機] Outlookが起動していません。10秒後にリトライします...")
                time.sleep(10)

        print(f"\n[設定] 重要度監視: {MONITOR_DURATION}秒")
        print(f"[設定] HTTPエンドポイント: {HTTP_URL}  タイムアウト: {HTTP_TIMEOUT}秒")
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
        print("[終了] スレッドプールをシャットダウン中...")
        _executor.shutdown(wait=False)
        print("[終了] CoUninitialize() 実行中...")
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
