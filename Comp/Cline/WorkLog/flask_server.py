#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkLog アプリ用テストサーバ
HTML/CSS/JavaScriptアプリをホストするシンプルなFlaskサーバ
"""

from flask import Flask, send_file, send_from_directory
import os
import webbrowser
import threading
import time

app = Flask(__name__)

# 現在のディレクトリを取得
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    """メインページ - worklog.htmlを返す"""
    return send_file('worklog.html')

@app.route('/worklog.html')
def worklog():
    """worklog.htmlを直接返す"""
    return send_file('worklog.html')

@app.route('/favicon.ico')
def favicon():
    """ファビコンリクエストを処理（404を避けるため）"""
    return '', 204

def open_browser():
    """ブラウザを自動で開く"""
    time.sleep(1.5)  # サーバ起動を待つ
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("=" * 50)
    print("WorkLog テストサーバを起動しています...")
    print("=" * 50)
    print(f"作業ディレクトリ: {CURRENT_DIR}")
    print("サーバURL: http://localhost:5000")
    print("終了するには Ctrl+C を押してください")
    print("=" * 50)
    
    # ブラウザを自動で開く
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        # Flaskサーバを起動
        app.run(
            host='localhost',
            port=5000,
            debug=True,
            use_reloader=False  # 自動リロードを無効化（ブラウザ自動起動との競合を避けるため）
        )
    except KeyboardInterrupt:
        print("\nサーバを停止しました。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
