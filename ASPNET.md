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

# ASP.NET
* .NETプラットフォーム：.NET Framework (Windowsのみ), .NET Core (クロスプラットフォーム)
* ASP.NET: ASP.NET v1-5 (on .NET Framework only, v6からCoreに統合),  ASP.NET Core (on .NET Framework or.NET Core)
* テンプレート： Web Forms (ASP.NET v1-5 only), MVC

# ASP.NET Core docs
* doc: https://docs.microsoft.com/ja-jp/dotnet/core/
* CLI doc: https://docs.microsoft.com/ja-jp/dotnet/core/tools/

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
       
# ASP.NET MVC
* https://qiita.com/kazuhisam3/items/f056819172d2b6d36a8c
* https://docs.microsoft.com/ja-jp/aspnet/core/
  * MVC tutorial: https://docs.microsoft.com/ja-jp/aspnet/core/tutorials/first-mvc-app/
  * small tutorial: https://dotnet.microsoft.com/learn/web/aspnet-hello-world-tutorial/intro
* Controller
  * Routing: urlに対してControllerクラスのメソッド（アクションメソッド）を対応づける。
    * default routing: URL /{name1}/{name2}/5  ---> call method {nama2} of controller class {name1}Controller with arg 5
    * query stringはアクションメソッドの引数となる
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
* Model
  * Use Entity Framework
  * Scaffolding: scaffolding tool generates pages (V, C) for Create, Read, Update, and Delete (CRUD) operations for Model class.
  
# .NET Entity Framework (OR-mapper)
* Entity Framework Core (on .NET Core)   Entity Framework 6 (old versin, only on .NET Framewwork)
* [concept] https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/ef/overview
* [doc] https://docs.microsoft.com/en-us/ef/core/
  * https://docs.microsoft.com/en-us/ef/core/modeling/index

* Entity Framework is a object-relational mapper (O/RM) for .NET
* Model layer
  * object layer (O): application's domain objects or entity ("O-C" mapping is one-to-one)
  * conceptual model (C, Model): the entities and relationships (object-oriented classes and properties)
                          which are described using the Entity Data Model (EDM) 
  * storage model (S, Database): relational database (tables with foreign key constraints)
* Mapping
  * EF's mapping engine leverages the "C-S" mapping to transform operations against entities
    * Write a code (class and properties) for C, EF generates relational tables and mapping code. [migration]
    * From relational tables, EF generates code for C and mapping code.
  * Migration: Modelの作成・変更に対してDBを変更(create, alter)するツール
　  * https://docs.microsoft.com/en-us/ef/core/managing-schemas/migrations/index

* Query (Language Integrated Query, LINQ)
  * query syntax (method, etc.) for entity classes
     * ```var blogs = context.Blogs.Where(b => b.Url.Contains("dotnet")).ToList();```
     * ```var blogs = context.Blogs.FromSql("SELECT * FROM dbo.Blogs").ToList();```
* Save/Update
  * ```var blog = new Blog { Url = "http://sample.com" }; db.Blogs.Add(blog); db.SaveChanges();```
  * ```var blog = context.Blogs.First(); blog.Url = "http://sample.com/blog"; context.SaveChanges();``` 

* database providers: plug-in libraries throgh that Entity Framework can access many different databases 

* Simple ORM Dapper (https://dapper-tutorial.net/ https://github.com/StackExchange/Dapper)

# Oracle ASP.NET
* Oracle Database 2日で.NET開発者ガイド https://docs.oracle.com/cd/E16338_01/appdev.112/b56266/using_aspnt.htm
* https://www.atmarkit.co.jp/ait/articles/0703/14/news120.html

* items
  * ODP.NET(Oracle Data Provider For .NET)：.NET環境からOracleデータベースに接続するための高機能なミドルウェア。Oracle Database Client上で動作（クライアント／サーバ・システムの場合はクライアント、Webシステムの場合はWebサーバとなる）
    * ODP.NET: https://docs.oracle.com/cd/E57425_01/121/ODPNT/title.htm
    * ODP.NETはADO.NETモデルを使用
    * OracleネイティブAPIを使用して、Oracleデータへの高速で信頼性の高いアクセスを実現
    * 接続型と非接続型
  * ODT：Oracle Developer Tools for Visual Studio. GUI操作でOracleアプリケーション開発を行うためのVisual Studio 2005のアドインツール。開発環境（Visual Studio 2005）上で動作
    * ODTを使ったVisual StudioからのPL/SQL開発 https://www.atmarkit.co.jp/ait/articles/0705/07/news083_4.html

  * ODE.NET：Oracleデータベース上で.NETストアド・プロシージャを実行するための機能。Oracleデータベース・サーバ上で動作

  * Oracle Providers for ASP.NET: Microsoft ASP.NETのコントロールおよびサービスと直接統合され、Webサイトの状態管理機能が提供されます。
    * https://docs.oracle.com/cd/E57425_01/121/ASPNT/IntroOverview.htm
    * ASP.NETアプリケーションは、様々なタイプのアプリケーション状態をOracleデータベースに格納できます。


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


