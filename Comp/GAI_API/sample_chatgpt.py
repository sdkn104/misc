from playwright.sync_api import sync_playwright

context = None

def run(playwright):
    # Edgeブラウザを起動するための設定
    browser = playwright.chromium.launch_persistent_context(
        headless=False,  # ヘッドレスモードを無効にする（ブラウザを表示する）
        #ignore_default_args=["-inprivate", "--incognito"],
        user_data_dir="C:\\Temp",
        channel='msedge'  # Edgeブラウザを指定
        #executable_path='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'  # Edgeの実行可能ファイルのパス
    )
    #context = browser.new_context()
    context = browser
    page = context.new_page()

    # 指定されたURLを開く
    #page.goto('https://melgitgaipreview-cd01001ze.megcloud.melco.co.jp/')
    page.goto('https://copilot.microsoft.com/')
    #page.goto('https://chatgpt.com/')
    # 新しいチャットを開始
    new_chat_button = page.locator('a[title="ChatGPT"]')
    new_chat_button.click()

    # プロンプトを入力
    user_prompt = page.locator('textarea#textareaMessage')
    user_prompt.fill('abcde')
    user_prompt.press("Control+Enter")

    # 回答を取得
    page.wait_for_selector('#MessagesInChatdiv div.toast-body')  # 回答が表示されるまで待機
    replies = page.query_selector_all('#MessagesInChatdiv div.toast-body')
    if replies:
        last_reply = replies[-1]
        print("回答:", last_reply.inner_text())


    # name属性がxxxxのインプットボックスに「あいうえお」を入力
    newButton = page.locator('//span[text()="新しい会話を開始"]')
    print(newButton.inner_text())
    newButton.click()

    generalButton = page.locator('//label[text()="一般知識モード"]')
    generalButton.click()

    userPrompt = page.locator('textarea#textareaMessage')
    userPrompt.fill('あいうえお')
    userPrompt.press("Control+Enter")

    replys = page.query_selector_all('#MessagesInChatdiv div.toast-body')
    lastReply = replys[-1]
    print(lastReply.inner_text())
    
    print("finish")
    

    # 必要な操作をここに追加

    # ブラウザを閉じる
    # browser.close()

with sync_playwright() as playwright:
    run(playwright)


