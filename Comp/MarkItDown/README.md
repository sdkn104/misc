# MarkItDown Office文書→Markdown変換Webアプリ

## 概要
Officeファイル（Word, Excel, PowerPoint等）をドラッグ＆ドロップでアップロードすると、Markdown形式（.md）に自動変換・ダウンロードできるWebアプリです。  
変換にはMicrosoftのMarkItDown（Pythonライブラリ）を使用しています。

## セットアップ手順

1. Python仮想環境の作成・有効化  
   詳細は `setup_instructions.md` を参照

2. 必要パッケージのインストール
   ```
   pip install "markitdown[all]"
   pip install flask
   ```

3. サーバー起動
   ```
   python app.py
   ```

4. ブラウザで `index.html` を開く  
   （Flaskサーバーはデフォルトで http://localhost:5000 で起動）

## 使い方

1. Webページ上で「ここにWord, Excel, PowerPoint等のファイルをドラッグ＆ドロップ またはクリックして選択」エリアにファイルをアップロード
2. 自動的にMarkdown（.md）ファイルがダウンロードされます

## 動作確認方法

- Flaskサーバー（app.py）を起動
- ブラウザで `index.html` を開く
- Officeファイルをドラッグ＆ドロップ
- mdファイルが自動ダウンロードされることを確認

## 注意事項

- Python 3.10以上が必要です
- MarkItDownの対応フォーマット以外は変換できません
- サーバーはローカル環境で動作します
