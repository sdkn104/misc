# Links

* [ASP.NET 入門の書(MVC)] (https://qiita.com/Kei18/items/1a9b936216bd2458ec08)
* ？[最新の ASPNET Web アプリケーション電子ブック] (https://docs.microsoft.com/ja-jp/dotnet/standard/modern-web-apps-azure-architecture/)
* 〇ASP.NET Web Forms vs ASP.NET MVC https://techinfoofmicrosofttech.osscons.jp/index.php?ASP.NET%20Web%20Forms%20vs%20ASP.NET%20MVC

* https://codezine.jp/article/detail/9604

* ASP.NET MVC 開発を始める前に理解しておきたいこと https://qiita.com/kazuhisam3/items/f056819172d2b6d36a8c

# 公式
* ASP.NET: https://dotnet.microsoft.com/apps/aspnet
* ASP.NET Web Forms: https://dotnet.microsoft.com/apps/aspnet/web-forms
* ASP.NET MVC: https://dotnet.microsoft.com/apps/aspnet/mvc
* ASP.NET Core: https://docs.microsoft.com/ja-jp/aspnet/core/?view=aspnetcore-2.2

# ASP.NET Web Forms
  * tutorial: https://docs.microsoft.com/ja-jp/aspnet/web-forms/overview/getting-started/getting-started-with-aspnet-45-web-forms/introduction-and-overview
  * 〇ASP.NET（Web Forms）を理解する3つの仕組み https://www.atmarkit.co.jp/fdotnet/bookpreview/learnaspnet_0202/learnaspnet_0202_01.html
  * UI
    * pageはaspxファイルと対応。部品(server control)を配置する(aspxに記述かＧＵＩで置く）
    * 部品(update, clickなど)やページ(loadなど)のイベントに対してハンドラを割り付ける。
      　 * ハンドラからLogicのクラスを操作し、LogicクラスがModelクラスを操作する。Logicは作らなくてもよい。
  * Life cycle, post back, view state
       * https://www.atmarkit.co.jp/fdotnet/bookpreview/learnaspnet_0202/learnaspnet_0202_01.html
       * page loadイベントはサーバで処理されてからpage送信される。
       　その他のイベントが発生すると、内容がサーバに送信され(post back)、サーバでハンドラ実行、更新したページ全体をresponse。
       　* page loadハンドラは、post back時とそれ以外で分けて処理を記述可。
         * post backは<FORM>データが自身のページに送信される。(部品は<form action="自身.aspx">に展開)
       * 入力更新イベントはデフォルトでプール(発生順序無視)され、click系イベント発生時にまとめて送信。ただしプール無効設定AutoPostBackも可。
       * view stateでpost back時に画面の状態(label, 色など)を保持する：
       　　* サーバからページ返信時に、現在の値をタグで埋め込んでおく(view state)。post back時にview stateの内容も送信し、サーバで復元する。
         　* label, colorなどはview stateに保持, formのinput値などはsummit時に最新値が送信されるのでview stateにはいれないが復元される。
  * Model binding [ref](https://docs.microsoft.com/ja-jp/aspnet/web-forms/overview/getting-started/getting-started-with-aspnet-45-web-forms/display_data_items_and_details)
         * ListViewなどにはModel classをバインドできる。表示などの処理が自動化できる。
  * Model
    *Entity Framework is an object-relational mapping (ORM) framework 
      [ref](https://docs.microsoft.com/ja-jp/aspnet/web-forms/overview/getting-started/getting-started-with-aspnet-45-web-forms/create_the_data_access_layer)
    * write Model class for data entity (table schema), then generate RDB table, or write access code. 
    * [LINQ](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/index)
      * Query expressions are written in a declarative query syntax in the code (no SQL).
       
# ASP.NET MVC
* https://qiita.com/kazuhisam3/items/f056819172d2b6d36a8c
* https://docs.microsoft.com/ja-jp/aspnet/core/mvc/overview?view=aspnetcore-2.2
* routing: urlに対してControllerのメソッド（アクションメソッド）を対応づける。
  * アクションメソッドは、response (html, json, etc)を返す。
* Model binding: 
  * client request data (form values, route data, query string parameters, HTTP headers) into objects that the controller can handle.
* View
  * action method名と同じ名前の.aspx, .cshtmlを作成する。
    * reurun View()とすると同名.cshtmlなどが返る。
    * 連想配列viewBag, viewDataなどに値を設定すると、.aspx, cshtmlから参照できる
  * HTMLヘルパー:
    WebFormsのサーバーコントロールに相当する機能。イベントなどがあるわけではなく、単純にHTMLを生成するために使います
* viewの状態保持
  * Session変数 などで明示的に書く。
  * TempDataは、1つのHTTP要求と次のHTTP要求の間でデータを永続化する場合に使用できます。redirectに使うみたい。
  

# Oracle Forms
* (https://en.wikipedia.org/wiki/Oracle_Forms)
  * Oracle Forms is has an IDE that uses PL/SQL.
  * It is Java where it runs in a Java EE container.
    * Applet Container は Java EE containerの一種
         [1](https://docs.oracle.com/cd/E19159-01/820-4604/ablms/index.html) 
         [2](https://docs.oracle.com/javaee/5/tutorial/doc/bnabo.html)
* http://otndnld.oracle.co.jp/products/forms/htdocs/install/Materials/html/o2/o15websystem.html
  * Webブラウザ上のJava Appletとしてリッチクライアント・アプリケーションを実現していく
  
# Applet-Like 
*Silverlight C#
  * https://www.atmarkit.co.jp/fdotnet/chushin/introsl_01/introsl_01_02.html
* smart client


