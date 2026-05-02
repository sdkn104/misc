import csv
from playwright.sync_api import sync_playwright

# SUUMO 検索ページ URL（名古屋市の中古マンション例）
SEARCH_URL = "https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=050&bs=040&sd=1&ta=23&sa=01&ts=1"

def scrape_suumo():
    """SUUMO から物件情報をスクレイピングして CSV に保存する"""
    print("=" * 60)
    print("SUUMO スクレイピング開始")
    print(f"URL: {SEARCH_URL}")
    print("=" * 60)
    
    with sync_playwright() as p:
        # ブラウザを起動
        print("\n[1] ブラウザを起動中...")
        browser = p.chromium.launch(headless=True)
        #browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = browser.new_page()
        print("✓ ブラウザ起動完了")

        # ページを読み込む
        print("\n[2] ページを読み込み中...")
        page.goto(SEARCH_URL)
        page.wait_for_load_state("networkidle")
        print("✓ ページ読み込み完了")

        results = []
        page_count = 0

        while True:
            page_count += 1
            print(f"\n[3] ページ {page_count} をスクレイピング中...")
            
            # 物件カードを取得
            cards = page.locator(".js-cassetLink").all()
            print(f"  → {len(cards)} 件の物件を検出")

            for idx, card in enumerate(cards, 1):
                # 物件情報の抽出（各項目はエラーハンドリング付き）
                try:
                    title = card.locator(".property_inner-title").inner_text().strip()
                    print(f"    [{idx}] タイトル: {title}")
                except Exception as e:
                    title = ""
                    print(f"    [{idx}] タイトル取得エラー: {e}")

                try:
                    price = card.locator(".detailbox-property-point").first.inner_text().strip()
                    print(f"        価格: {price}")
                except Exception as e:
                    price = ""
                    print(f"        価格取得エラー: {e}")

                # --- 1. 新しいタブが開くのを待ちながらクリック ---
                #with context.expect_page() as new_page_info:
                with page.expect_popup() as popup_info:
                    card.get_by_text("詳細を見る").click()   # ← 別タブを開くボタン
                #new_page = new_page_info.value
                new_page = popup_info.value
                
                print(f"        別タブが開きました: {new_page.url}")

                # --- 2. 新しいタブで情報を取得 ---
                new_page.wait_for_load_state("domcontentloaded")
                print("        別タブのページが読み込まれました")

                title2 = new_page.title()
                url = new_page.url
                h1_text = new_page.locator("h1").inner_text()

                madori = new_page.locator(".table_gaiyou tr").nth(0).locator("td").nth(0).inner_text()
                kai = new_page.locator(".table_gaiyou tr").nth(1).locator("td").nth(0).inner_text()
                tikunen = new_page.locator(".table_gaiyou tr").nth(1).locator("td").nth(1).inner_text()

                print("【別タブの情報】")
                print("タイトル:", title)
                print("URL:", madori)
                print("H1:", h1_text)

                # --- 3. 別タブを閉じる ---
                new_page.close()

                # --- 4. 元のタブに戻る ---
                page.bring_to_front()


                # 物件情報をリストに追加
                results.append({
                    "title": title,
                    "price": price,
                    "address": h1_text,
                    "kai": kai,
                    "built_year": tikunen
                })

            # 次ページボタンを確認
            print(f"\n  → 合計 {len(results)} 件のデータを収集済み")
            next_btn = page.locator("a.c-pagination__next")
            print(f"  → 次ページボタン検出: {next_btn.count() > 0}")

            # 次ページボタンがない、または無効の場合はループ終了
            if next_btn.count() == 0:
                print("  → 次ページボタンが見つかりません。スクレイピング完了")
                break

            if "is-disabled" in next_btn.get_attribute("class"):
                print("  → 次ページボタンが無効です。スクレイピング完了")
                break

            print("  → 次ページに移動中...")
            next_btn.click()
            page.wait_for_load_state("networkidle")

        print("\n[4] ブラウザを閉じ中...")
        browser.close()
        print("✓ ブラウザを閉じました")

        # CSV ファイルに出力
        print("\n[5] CSV ファイルに出力中...")
        if results:
            try:
                with open("suumo.csv", "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.DictWriter(f, fieldnames=results[0].keys())
                    writer.writeheader()
                    writer.writerows(results)
                
                print(f"✓ CSV 出力完了: suumo.csv")
                print(f"  → 保存行数: {len(results)} 件")
            except Exception as e:
                print(f"✗ CSV 出力エラー: {e}")
        else:
            print("✗ 出力するデータがありません")
        
        print("\n" + "=" * 60)
        print("SUUMO スクレイピング完了")
        print("=" * 60)

if __name__ == "__main__":
    # メイン処理実行
    try:
        scrape_suumo()
    except Exception as e:
        print(f"\n✗ 予期しないエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
