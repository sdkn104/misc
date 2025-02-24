# ASP.NET Web Forms
* tutorial: https://docs.microsoft.com/ja-jp/aspnet/web-forms/overview/getting-started/getting-started-with-aspnet-45-web-forms/introduction-and-overview
* 〇ASP.NET（Web Forms）を理解する3つの仕組み https://www.atmarkit.co.jp/fdotnet/bookpreview/learnaspnet_0202/learnaspnet_0202_01.html
* UI 
  * pageはaspxファイルと対応。部品(server control)を配置する(aspxに記述かＧＵＩで置く）
  * 部品(update, clickなど)やページ(loadなど)のイベントに対してハンドラを割り付ける
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
       
# Oracle Forms
* (https://en.wikipedia.org/wiki/Oracle_Forms)
  * Oracle Forms is has an IDE that uses PL/SQL.
  * It is Java where it runs in a Java EE container.
    * Applet Container は Java EE containerの一種
         [1](https://docs.oracle.com/cd/E19159-01/820-4604/ablms/index.html) 
         [2](https://docs.oracle.com/javaee/5/tutorial/doc/bnabo.html)
* http://otndnld.oracle.co.jp/products/forms/htdocs/install/Materials/html/o2/o15websystem.html
  * Webブラウザ上のJava Appletとしてリッチクライアント・アプリケーションを実現していく

* プログラミング
  * Oracle Developer Form Builder Reference (https://www.oracle.com/technetwork/documentation/dev-arch-093406.html)
  * Oracle9iDS Forms Developer Reference Guide (https://www.oracle.com/technetwork/developer-tools/forms/documentation/9irefguide-131898.zip)
  * 〇tutorial (http://www.oracleatoz.com/introduction-of-oracle-form-builder)
  * tutorial (https://sheikyerbouti.developpez.com/tutoforms10g/tutoforms10g.htm)
  * 〇tutorial (http://web2.uwindsor.ca/courses/cs/rituch/470/Oracle%20Developer%20-%20A%20Tutorial%20on%20Oracle%20Forms,%20Reports%20and%20Graphics.htm)
  * tutorial (https://www.oracletutorial.org/forms-and-reports/forms-and-reports.php)
              http://web2.uwindsor.ca/courses/cs/rituch/470/resources.html
  * 〇tutorial http://web2.uwindsor.ca/courses/cs/rituch/470/SQLFORMSMaintutorial.doc
  
  * By default, every form in Oracle Forms has the capability to query existing data in a table, modify existing data and add new data (records) to the table. A form is built up using one or more data blocks that correspond to tables in the database. Fields within the data block correspond to columns in the database table.
  * Database Block: displays all the fields from the base table in a canvas without requiring any programming, a master-detail relationship, which is a join-condition between two data blocks, 
  * Non-Database Block: Non-Database Block normally called Control block is not linked with table or view it will create manually and also items put in this block manually. All items of non-database block are non-database items.
  * Canvas: A Canvas will use for draw the different items on it, now we will draw different items on this area and use this area as a home ground of fields. Every item will draw on this area.
  * A trigger is a block of PL/SQL code you write to customize your application.  Although you could create a basic application without writing triggers, using only Oracle Forms' default processing to retrieve, add, delete, and change database records, you will usually need to write triggers to customize your application.  A trigger’s PL/SQL code contains orders to perform certain functions that are triggered by the event it is attached to, such as a button or form event.
  * a record group is a query that returns some collection of records. Record groups can be used to populate blocks or LOVs and they can be used in procedures.
  
  
# Applet-Like 
* Silverlight C#
  * https://www.atmarkit.co.jp/fdotnet/chushin/introsl_01/introsl_01_02.html
* smart client

# Java Applet
* ネットワークを通してWebブラウザに読み込まれ実行されるJavaのアプリケーションの一形態。Java 10まではJava Runtime Environmentに搭載されていてJava 11で廃止。
  * ローカルの資源にアクセスできない（クリップボードやディスクの読み書きができない、印刷機能を扱えないなど）。
  * アプレットのダウンロード元サーバとしか通信できない。
* Programming (https://www.javadrive.jp/applet/)
  * Appletクラスを継承したクラスを作成
  * イメージとしてはAppletクラスは何かを表示したり他の部品を置く為のパネルのようなものです。
  * そのクラスに以下のメソッドを定義する。init
     start
     stop
     destroy
     paint
     repaint
     update
  * 描画：Graphicsクラスで図形を描画
  * イベント：MouseListener等を作成・登録してコールバックを定義する。イベントはright click等で座標値などが取得可能。
  * GUI部品(テキストフィールド、ボタンなど）とそのイベントリスナもAWTで書ける。
  * Parameter: htmlのparamタグの情報をgetParameters()で取得可能。
  * Server: serverとhttp通信可。HttpURLConnection など。
* HTMLに埋め込んでロード時に起動する。<applet code="class_name" width="applet_width" height="applet_height"></applet>

* Java Web Start   -- Java 11で廃止
  * Java製アプリケーションをウェブサーバなどから自動ダウンロード、自動インストール、自動アップデートして、サンドボックス上にて実行可能な仕組み
  * Java Web Start のシステム要件は何ですか ? Java バージョン 1.2.2 以上をサポートするクライアントシステムで Java Web Start を使用できます。Java Web Start はほとんどすべてのブラウザで動作します。
  * サポートされるブラウザは何ですか ? Java Web Start では、主として Internet Explorer 4 以上と Mozilla をサポートしています。ただし、MIME タイプの関連付けを正しく設定してある場合は、どのブラウザでも JNLP ファイルを起動できます。Java Web Start では、ブラウザの設定を使用し、ブラウザを起動して URL を表示することもあります。この機能は、サポートされていないブラウザでは動作しません。

# Java Server side
* Java EE: Java Platform, Enterprise Edition (Java EE) は、Javaで実装されたアプリケーションサーバーの標準規格及びそのAPIを定めたもの
* Servlet, WebSocketなどを含む


