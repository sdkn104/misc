from playwright.sync_api import sync_playwright

# "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222

def main():
    with sync_playwright() as p:
        # 既存のEdgeブラウザに接続
        browser = p.chromium.connect_over_cdp('http://localhost:9222')  # Edgeのデバッグポートに接続
        context = browser.contexts[0]
        pages = context.pages

        # 特定のWebアドレスを開いているタブを探す
        target_url = 'https://example.com'  # ここに特定のWebアドレスを入力
        target_page = None
        for page in pages:
            if page.url == target_url:
                target_page = page
                break

        if target_page:
            # テキストボックスに値を書き込む
            target_page.fill('input[name="nnn"]', '111')
            print('テキストボックスに値を書き込みました')
        else:
            print('指定されたURLのタブが見つかりませんでした')

        browser.close()

if __name__ == '__main__':
    main()
    