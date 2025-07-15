from playwright.sync_api import sync_playwright

p = sync_playwright()
browser = p.chromium.connect_over_cdp('http://localhost:9222')
context = browser.contexts[0]