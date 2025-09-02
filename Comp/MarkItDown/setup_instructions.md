# MarkItDown Webアプリセットアップ手順

## 1. Python仮想環境の作成・有効化

Windowsの場合（コマンドプロンプト）:

```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

Mac/Linuxの場合（bash/zsh）:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. MarkItDownのインストール

```bash
pip install "markitdown[all]"
```

## 3. Flaskのインストール（バックエンド用）

```bash
pip install flask
```

## 4. サーバー起動例

（後続の実装で `app.py` を作成します）

```bash
python app.py
