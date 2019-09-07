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

# Docs
* .NET Core docs
  * doc: https://docs.microsoft.com/ja-jp/dotnet/core/
  * CLI doc: https://docs.microsoft.com/ja-jp/dotnet/core/tools/
* ASP.NET Core docs
  * https://qiita.com/kazuhisam3/items/f056819172d2b6d36a8c
  * https://docs.microsoft.com/ja-jp/aspnet/core/
    * tutorial (ASP.NET Core, Razor pages): https://docs.microsoft.com/ja-jp/aspnet/core/tutorials/razor-pages/
    * small tutorial: https://dotnet.microsoft.com/learn/web/aspnet-hello-world-tutorial/intro

# ASP.NET Core/MVC
* Controller
  * Routing: urlに対してControllerクラスのメソッド（アクションメソッド）を対応づける。
    * default routing: URL /{name1}/{name2}/5  ---> call method {nama2} of controller class {name1}Controller with arg 5
    * query stringはアクションメソッドの引数となる
    * アクションメソッドは、response (html, json, etc)を返す。
  * [Model binding](https://docs.microsoft.com/ja-jp/aspnet/core/mvc/models/model-binding)
    * bindig client request data (form values, route data, query string parameters, HTTP headers) 
      to objects (args of action method, args of Razor Pages handler method, Public properties of a controller or PageModel class)
    * binding is specified by attributes in class definition, etc.
   
  * Model validation
    * validation by decorating your model object with data annotation validation attributes. 
    * The validation attributes are checked on the client side before values are posted to the server, 
      as well as on the server before the controller action is called.
    * action method内では、if (ModelState.IsValid)　で結果を取得、また、rendered view内にvalicatin logicが埋め込まれる(jquery validation)。
     
* View
  * action method名と同じ名前の.aspx, .cshtmlを作成する。
    * reurun View()とすると同名.cshtmlなどが返る。
    * 連想配列viewBag, viewData(dict.)などに値を設定すると、.aspx, cshtmlから参照できる　　
    * View()の引数にobject instanceを指定すると、.cshtmlなどから@Modelで参照できる(viewmodel)。
  * [Razor Pages](https://docs.microsoft.com/ja-jp/aspnet/core/razor-pages)
    * a MVV-Model
    * Razor Pages is enabled in Startup.cs, and  put @page directive in .cshtml
    * define a PageModel class in .cshtml.cs
    * PageModel includes:
      * page handlers (a method. OnGet(), etc.), that is called for request (routed), instead of controller action method
      * properties (member variables), targets of model binding
    * page handerで return Page()とすると、.cshtmlが返る。 
  * Razor (cshtml)
    * syntax: https://docs.microsoft.com/ja-jp/aspnet/core/mvc/views/razor
    * 変数を参照
      * using @, refer C# variables
      * action method/page handler内から参照できる変数はそのまま参照できる？？？
      * "Model" refer:
        * argument of View() returned by action method, or Page() returned by page hander
        * If argment is omitted, Controller/PageModel？ (https://docs.microsoft.com/ja-jp/aspnet/core/mvc/views/)
      * <input asp-for="Customer.Name"> (CustomerはPageModelのproperty)
      * ViewData - action/handerからread/write, Razorからread
  * [HTML Helper](https://stephenwalther.com/archive/2009/03/03/chapter-6-understanding-html-helpers)
    * WebFormsのサーバーコントロールに相当する機能。イベントなどがあるわけではなく、単純にHTMLを生成するために使います
    *  in most cases, is just a method that returns a string.
    * ex. Html.ActionLink("About this Website", "About"), Html.DataGrid()
    * standard helpers, custom helpers
  * [Tag Helper](https://docs.microsoft.com/ja-jp/aspnet/core/mvc/views/tag-helpers/)
      *
  * [Layout](https://docs.microsoft.com/ja-jp/aspnet/core/mvc/views/layout)
      * Layout is .cshtml that represents common top page structure.　(Pages/Shared/_Layout.cshtml)
      * Page .cshtml specifies _Layout.cshtml by Layout property.
      * Layout .cshtml contains @RenderBody(), where Page cshtml (div, etc) is rendered.
      * If Layout .cshtml contains @RenderSection(), section defined in Page cshtml is rendered (if exists) 
      * Importing Shared Directives:  _ViewImports.cshtml
      * Running Code Before Each View/Page: _ViewStart.cshtml
      
* [Partial View](https://docs.microsoft.com/ja-jp/aspnet/core/mvc/views/partial)
      * 
  * Http Client https://docs.microsoft.com/ja-jp/aspnet/core/fundamentals/http-requests
  
　* viewの状態保持
      * Session変数 などで明示的に書く。
      * TempDataは、1つのHTTP要求と次のHTTP要求の間でデータを永続化する場合に使用できます。redirectに使うみたい。
* Model
  * Use Entity Framework
  * Scaffolding: scaffolding tool generates pages (V, C) for Create, Read, Update, and Delete (CRUD) operations for Model class.
  * IEnumerable, ToList

* Server
  * https://docs.microsoft.com/ja-jp/aspnet/core/fundamentals/servers
  * https://docs.microsoft.com/ja-jp/aspnet/core/host-and-deploy
  * デフォルトは、Kestrel is the default web server included in ASP.NET Core project templates.
  * IISは、in-process(IIS worker process内), out-of-process Modelがある。
    * Core 2.2からはin-processがIISのデフォルト。in-processでは複数アプリができないが通常はこちらでよさそう。
  * Kestrel単独 (開発用?) https://docs.microsoft.com/ja-jp/aspnet/core/fundamentals/servers/kestrel
    * Program.cs: WebHost.CreateDefaultBuilder(args)   [calls UseKestrel() behind the scenes.]
    * APP.proj: <AspNetCoreHostingModel>InProcess</AspNetCoreHostingModel>
  * IIS in-process (IIS HTTP Server is used instead of Kestrel server) https://docs.microsoft.com/ja-jp/aspnet/core/host-and-deploy/iis
    * Program.cs: WebHost.CreateDefaultBuilder(args).UseIIS
    * APP.proj: <AspNetCoreHostingModel>InProcess</AspNetCoreHostingModel>
  * IIS out-of-process (use Kestrel server)  https://docs.microsoft.com/ja-jp/aspnet/core/host-and-deploy/aspnet-core-module
    * Program.cs: WebHost.CreateDefaultBuilder(args).UseIISIntegration
    * APP.proj: <AspNetCoreHostingModel>OutOfProcess</AspNetCoreHostingModel>
  * Log
    * IIS Log : IIS管理コンソール-Site-ログ記録　にログ出力フォルダ設定
    
* Unit Test: https://docs.microsoft.com/ja-jp/aspnet/core/mvc/controllers/testing
             https://docs.microsoft.com/ja-jp/dotnet/core/testing/unit-testing-with-dotnet-test

* [Authentication](https://docs.microsoft.com/ja-jp/aspnet/core/security/authentication/identity?view=aspnetcore-2.2&tabs=visual-studio)
  * Identity : a membership system that adds login functionality to ASP.NET Core apps.
    * ユーザ情報を登録するModel Classとそれを操作(ユーザ登録、変更など)するユーティリティなど
    * ログインページなどのコード生成
  * Windows Authentication: https://docs.microsoft.com/ja-jp/aspnet/core/security/authentication/windowsauth
    * Integrated Windows Authentication (ASP.NET MVC ?)
      * https://docs.microsoft.com/ja-jp/aspnet/web-api/overview/security/integrated-windows-authentication
      * https://support.microsoft.com/en-us/help/323176/how-to-implement-windows-authentication-and-authorization-in-asp-net
    * AD group (role)などの属性をIdentityに取り込めるみたい。
    * 
    
* [Authorization](https://docs.microsoft.com/ja-jp/aspnet/core/security/authorization/introduction)
  * page, controller, folderなどに対して、user, role, all userなどを設定。コードで記述する。
  
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
  * using SQL
     * Raw SQL query : DBSet.FromSql(), or DBQuery.FromSql() https://docs.microsoft.com/en-us/ef/core/querying/raw-sql
       * query or non-query. result type must be type of dbset or dbquery
       * DBQuery is a class, that must be registered in context: https://stackoverflow.com/questions/35631903/raw-sql-query-without-dbset-entity-framework-core
     * Database.ExecuteSqlCommand() : non-query (no return)
     * using ADO
       * Database.GetDbConnection().CreateCommand() ...
       * type-less utility function : 
          * https://stackoverflow.com/questions/35631903/raw-sql-query-without-dbset-entity-framework-core
          * https://www.learnentityframeworkcore.com/raw-sql
           
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


