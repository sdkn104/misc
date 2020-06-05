
* Edge Chromium Extension : (https://docs.microsoft.com/en-us/microsoft-edge/extensions-chromium/)
  * install extension in developing phase (side loading)
    * Edge menu, ... -> extension -> (enabling developper mode) -> load unpacked (展開して読み込み) -> select the folder
* 解説：https://qiita.com/k7a/items/26d7a22233ecdf48fed8
* Chrome Extension https://developer.chrome.com/extensions
  * Extension API ref: https://developer.chrome.com/extensions/api_index

* 概要
  * Browser Action (or Page Action): Chromeのツールバーにボタンを追加。押すと開く画面(popup)をhtmlで定義。
  * Content Scripts: ページのurlが指定したパタンにマッチしたとき指定したjsを実行する。
  * Background Script: イベントハンドラ。ブラウザのイベント発生時にjsを実行する。
  * UI Element: Context menu, keyboard shortcut, omnibox, etc.

* Native Messaging (https://developer.chrome.com/extensions/nativeMessaging)
  * Nativeアプリ(native messaging host)を起動しそれと通信する。stdin/stdoutでjsonで通信する。
  * アプリのバイナリのパスをレジストリに登録する
  * https://laiso.hatenablog.com/entry/2013/12/15/Google_Chrome%E3%81%A7%E3%83%88%E3%83%AC%E3%82%A4%E3%81%8B%E3%82%89CD%E3%82%92%E6%8E%92%E5%87%BA%E3%81%A7%E3%81%8D%E3%82%8B%E3%83%96%E3%83%A9%E3%82%A6%E3%82%B6%E6%8B%A1%E5%BC%B5%E3%82%92%E3%81%A4%E3%81%8F
  * http://hdszk2015.hatenablog.com/entry/2015/11/29/110426
  * https://codeday.me/jp/qa/20190301/322848.html
  * 概要
    * Create manufest file that includes name, path of exe, etc.
    * Place manufest file in the mahine and Register path of manufest file in Registry
    * Extension app call API with the name
    
* [配布](https://developer.chrome.com/webstore) 
  * 拡張のインストールは、Chrome Storeを開いてクリックするか、External Installationかどちらか。どちらの場合も、Chrome Storeに登録は必須。
  * External Installation
    * レジストリに、拡張のIDとWeb StoreのURLと拡張のバージョンを登録する。
    * Chrome起動時に自動的にインストールや更新が実行される。
  * [Chrome StoreへのPublish](https://developer.chrome.com/webstore/publish)
    * [Chrome Web Store Developp]er(https://developer.chrome.com/webstore/register) に登録 (初回$5)
    * pack extension files to zip format
    * in developper dash board, upload zip and publish
  * [Chrome Web Store Developper登録](https://developer.chrome.com/webstore/register)
    * "We suggest using a new account just for your app instead of your personal account."
    * "Group publishers note that only members of the group who've paid the registration fee can publish updates."
    * "2.3 You represent and warrant that you have full power, capacity, and authority to accept this Agreement. If you are agreeing to be bound by this Agreement on behalf of your employer or other entity, you represent and warrant that you have full legal authority to bind your employer or such entity to this Agreement."
    * アカウントの取り方
      * 組織の代理として Google サービスを使用する(https://policies.google.com/terms?hl=ja)
      
    
