# Outlook返信監視ツール

旧Outlook（クラシック Outlook）の返信・転送画面を監視し、メールの重要度を「低」に設定すると
AIサーバーへHTTPリクエストを送り、返ってきた回答文をメール本文に自動挿入するツールです。

---

## 動作フロー

```
Outlookで返信/転送を開く
        ↓ 検出（0.5秒ポーリング）
  重要度「低」を最大10秒間監視
        │
        ├─ 10秒以内に重要度を「低」に設定
        │       ↓
        │   本文先頭に「AIによる回答作成中...」を挿入
        │       ↓
        │   AIサーバーへ HTTP POST（件名・本文を送信）
        │       ↓
        │   レスポンス受信
        │       ↓
        │   「AIによる回答作成中...」をAI回答文に置換
        │   重要度を「普通」に戻す
        │
        └─ 10秒経過しても「低」にならない → 何もしない
```

---

## 使い方

### 1. Outlookで返信/転送を開く

件名が `RE:` / `FW:` / `転送:` で始まる画面が自動で検出されます。

### 2. AIに回答を作らせたいときは重要度を「低」に設定する

リボンの「タグ」グループ → 重要度「低」ボタンをクリック（↓アイコン）。

```
メッセージ タブ > タグ > 重要度: 低 (↓)
```

### 3. 本文に「AIによる回答作成中...」が表示される

AIサーバーからレスポンスが返ると、自動的にAI回答文に置き換わります。

### 4. 内容を確認して送信する

AI回答文はそのまま送信せず、必ず内容を確認・編集してから送信してください。

---

## HTTP APIの仕様

ツールが送信するリクエスト:

```
POST {HTTP_URL}
Content-Type: application/json

{
  "subject": "RE: 件名テキスト",
  "body":    "返信本文（プレーンテキスト。引用元メールを含む）"
}
```

レスポンス:
- `200 OK` のレスポンスボディ（テキスト）がそのままメール本文に挿入されます
- JSON を返す場合は `outlook_reply_monitor.py` の `_http_request()` 関数を修正してください

```python
# JSON レスポンスから特定フィールドを取り出す例
def _http_request(subject: str, plain_body: str) -> str:
    resp = requests.post(HTTP_URL, json={...}, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    return resp.json()["answer"]   # ← ここを変更
```

---

## 設定値

`outlook_reply_monitor.py` の先頭部分で変更できます。

| 定数 | デフォルト | 説明 |
|---|---|---|
| `PLACEHOLDER_TEXT` | `AIによる回答作成中...` | HTTP待機中に本文に表示するテキスト |
| `MONITOR_DURATION` | `10` 秒 | 重要度「低」を待つ時間 |
| `HTTP_URL` | `http://localhost:8000/generate` | AIサーバーのエンドポイント |
| `HTTP_TIMEOUT` | `60` 秒 | HTTPリクエストのタイムアウト |

---

## 技術仕様

| 項目 | 内容 |
|---|---|
| Outlook接続 | COM (`win32com.client.GetActiveObject`) |
| 検出方式 | ポーリング（0.5秒間隔）。イベント方式はCOM型ライブラリキャッシュ依存のため不採用 |
| 返信判定 | 件名の `RE:` / `FW:` / `FWD:` / `転送:` プレフィックスで判定 |
| 重複防止 | 処理後に重要度を「普通」に戻すことで再検出を防止 |
| HTTP実行 | `ThreadPoolExecutor`（別スレッド）。COMオブジェクトは事前にデータ抽出してから渡す |
| HTML/プレーン | `BodyFormat` で判定し両形式に対応 |
| 起動待機 | Outlook未起動時は10秒間隔でリトライ |

---

## ファイル構成

```
OutlookReply/
├── outlook_reply_monitor.py   # メインスクリプト
├── build.ps1                  # PyInstaller ビルドスクリプト
├── install.bat                # インストーラ（タスクスケジューラ登録）
├── uninstall.bat              # アンインストーラ
├── requirements.txt           # Python 依存ライブラリ
├── BUILD.md                   # ビルド・インストール手順
└── README.md                  # このファイル
```

---

## 注意事項

- **旧Outlook（クラシック Outlook）専用**です。新しいOutlook（One Outlook）には対応していません
- AI回答文は必ず内容を確認してから送信してください
- 件名を変更すると同一ウィンドウが別ウィンドウとして再検出される場合があります（ウィンドウタイトルで識別しているため）
- Windowsサービスとしての起動は非対応です（OutlookのCOM自動化はインタラクティブセッションが必要なため）
