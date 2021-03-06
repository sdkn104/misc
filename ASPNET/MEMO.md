# Links

* [ASP.NET 入門の書(MVC)](https://qiita.com/Kei18/items/1a9b936216bd2458ec08)
* ？[最新の ASPNET Web アプリケーション電子ブック](https://docs.microsoft.com/ja-jp/dotnet/standard/modern-web-apps-azure-architecture/)
* 〇[ASP.NET Web Forms vs ASP.NET MVC](https://techinfoofmicrosofttech.osscons.jp/index.php?ASP.NET%20Web%20Forms%20vs%20ASP.NET%20MVC)

* https://codezine.jp/article/detail/9604

* ASP.NET MVC 開発を始める前に理解しておきたいこと https://qiita.com/kazuhisam3/items/f056819172d2b6d36a8c

# 公式
* ASP.NET: https://dotnet.microsoft.com/apps/aspnet
* ASP.NET Web Forms: https://dotnet.microsoft.com/apps/aspnet/web-forms
* ASP.NET MVC: https://dotnet.microsoft.com/apps/aspnet/mvc
* ASP.NET Core: https://docs.microsoft.com/ja-jp/aspnet/core/?view=aspnetcore-2.2

# ASP.NET
* .NETプラットフォーム：.NET Framework (Windowsのみ), .NET Core (クロスプラットフォーム)
* ASP.NET: ASP.NET v1-5 (on .NET Framework only, v6からCoreに統合/吸収?),  ASP.NET Core (on .NET Framework? or.NET Core)
* template/view engine： Web Forms (ASP.NET v1-5 only), MVC, Web Pages

# ASP.NET　overview
https://docs.microsoft.com/ja-jp/aspnet/overview#websites-and-web-applications
ASP.NET (not Core) offers three frameworks for creating web applications: Web Forms, ASP.NET MVC, and ASP.NET Web Pages.
ASP.NET (not Core) offers other frameworks --- Web API, etc.

called ASP.NET 4.x ??

* Web Forms (ASP.NET 3, 4)

* MVC
 C: Controllers/XXController.cs
 V: Views/XX/Index.cshtml  (Razor view engine)

 Razor view engine : v3～

* .NET version
   * https://qiita.com/nskydiving/items/3af8bab5a0a63ccb9893
   * https://devblogs.microsoft.com/visualstudio-jpn/net-framework-201510/
   * https://dotnet.microsoft.com/platform/support/policy
   * 1-3.5はサポート切れ。3.5SP1はサポート中。
   * 2016 年 1 月 12 日以降は .NET Framework 4.0 ～ 4.5.1 はサポートされなくなり
   * Win10は4.6以上のみ

* ASP.NET version
   * https://dotnet.microsoft.com/platform/support/policy/aspnet
   * ASP.NET (not Core) is made up components that ship in both the .NET Framework and as external packages that ship outside of the .NET Framework.
   * External pckg: ASP.NET MVC, ASP.NET Web Pages, ASP.NET Web API and ASP.NET SignalR, etc
   * MVC4 was retired in 2019/7
   * Web Forms: ASP.NET Coreはサポートしない


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
  * Intro
    * Define ControllerクラスControllerNameController in Controllers/ControllerNameController.cs
    * HTTP requestに対し、Controllerクラスのメソッド（アクションメソッド）が起動する。
    * アクションメソッドは、response (html, json, etc)を返す。
  * Routing: urlに対してControllerクラスのメソッド（アクションメソッド）を対応づける。
    * default routing: URL /{contname}/{actname}/5  ---> call method {actname} of controller class {contname}Controller with arg 5
    * actionに属性（[HttpGet("/products")]など）を付加してルーティングを指定可。
  * [Model binding](https://docs.microsoft.com/ja-jp/aspnet/core/mvc/models/model-binding)
    * bindig client request data (form values, route data, query string parameters, HTTP headers) to objects:
      * args of action method, args of Razor Pages handler method, 
      * Public properties of a controller or PageModel class, if specified by attributes of the property
    * binding is specified by attributes in class definition, etc.
   
  * Model validation
    * validation by decorating your model object with data annotation validation attributes. 
    * The validation attributes are checked on the client side before values are posted to the server, 
      as well as on the server before the controller action is called.
    * action method内では、if (ModelState.IsValid)　で結果を取得、また、rendered view内にvalicatin logicが埋め込まれる(jquery validation)。
     
* View
  * MVC
    * action method名と同じ名前の.cshtmlを作成する。
    * Views/ControllerName/ActionName.cshtml
    * reurun View()とすると同名.cshtmlが返る。
  * Razor (cshtml)
    * syntax: https://docs.microsoft.com/ja-jp/aspnet/core/mvc/views/razor
    * 変数を参照
      * using @, refer C# variables
      * [Passing data to views](https://docs.microsoft.com/ja-jp/aspnet/core/mvc/views/overview#passing-data-to-views)
        * viewmodel (both Razor and Razor Pages)
          * @model ModelClassName   in .cshtml,  Model class is defined typically in Models(or ViewModels)/ModelClassName.cs, or it can be PageModel.
          * action method return View(instanceOfModelClass), page handler return Page()
          * refer the instance of the model by variable Model in .cshtml
        * ViewData dictionary : ViewData["key"] = xxx in action/hander, refered by ViewData["key"] in cshtml
        * ViewData Atribute
          * put [ViewData] attribute to Properties on controllers or Razor Page models
          * the property PropName can be refered by Model.PropName in .cshtml
        * ViewBag : ViewBag.keyname = xxx in action method, refered by ViewBag.keyname in cshtml
  * [Razor Pages](https://docs.microsoft.com/ja-jp/aspnet/core/razor-pages)
    * a MVVM
    * Razor Pages is enabled in Startup.cs, and  put @page directive in <PageName>.cshtml
      * Startup.ConfigureServices(services) { services.addMvc(); }
      * Startup.Configure(app) { app.useMvc(); }
    * files : Pages/.../PageName.cshtml, Pages/.../PageName.cshtml.cs  (no Controllers/, View/)
    * default routing: Pages/Folder/PageName.cshtml   -->   Url: /Folder/PageName 
    * define a PageModel class (<PageName>Model) in PageName.cshtml.cs
    * PageModel includes:
      * page handlers (a method. OnGet(), etc.), that is called for request (routed), instead of controller action method
         * OnGet(), OnPost(), OnGetAsync(), OnPostAsync()
      * properties (member variables), targets of model binding
    * page handerで return Page()とすると、.cshtmlが返る。 
  * [HTML Helper](https://stephenwalther.com/archive/2009/03/03/chapter-6-understanding-html-helpers)
    * WebFormsのサーバーコントロールに相当する機能。イベントなどがあるわけではなく、単純にHTMLを生成するために使います
    *  in most cases, is just a method that returns a string.
    * ex. Html.ActionLink("About this Website", "About"), Html.DataGrid()
    * standard helpers, custom helpers
  * [Tag Helper](https://docs.microsoft.com/ja-jp/aspnet/core/mvc/views/tag-helpers/)
      *
  * [Layout](https://docs.microsoft.com/ja-jp/aspnet/core/mvc/views/layout)
      * Layout is .cshtml that represents common top page structure.　(Pages/Shared/_Layout.cshtml)
      * Page .cshtml specifies _Layout.cshtml by Layout property. ( ex. @{ Layout = "_Layout"; } )
      * Layout .cshtml contains @RenderBody(), where Page cshtml (div, etc) is rendered.
      * If Layout .cshtml contains @RenderSection(), section defined in Page cshtml is rendered (if exists) 
      * _ViewImports.cshtml : Importing Shared Directives (@model, @using, etc)
      * _ViewStart.cshtml : executed at the top of every View/Page 
      
  * [Partial View](https://docs.microsoft.com/ja-jp/aspnet/core/mvc/views/partial)
    * A partial view is a Razor markup file (.cshtml) that renders HTML output within another markup file's rendered output.
    * A patilal view is not whole html (<html></html>), unlike html frame.
    * .cshtmlは通常のフォルダに格納。名前は_で始まるのが普通。
    * 親のcshtmlから呼び出す。
      * '<partial name="/Pages/Folder/_PartialName.cshtml" />'
      * '@await Html.PartialAsync("/Pages/Folder/_PartialName.cshtml")'
  * [View Component](https://docs.microsoft.com/ja-jp/aspnet/core/mvc/views/view-components)
    * View components are similar to partial views, but they're much more powerful. Can have parameters and business logic.
    * cshtmlから呼び出し。
      * `@await Component.InvokeAsync("PriorityList", new { maxPriority = 4, isDone = true })`
      * `<vc:[view-component-name] parameter1="parameter1 value"  parameter2="parameter2 value"> </vc:[view-component-name]>`

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
  * (Integrated) Windows Authentication: 
      * https://docs.microsoft.com/ja-jp/aspnet/core/security/authentication/windowsauth
      * https://docs.microsoft.com/en-us/iis/configuration/system.webServer/security/authentication/windowsAuthentication/
      * https://docs.microsoft.com/ja-jp/aspnet/web-api/overview/security/integrated-windows-authentication
      * https://support.microsoft.com/en-us/help/323176/how-to-implement-windows-authentication-and-authorization-in-asp-net
    * Integrated Windows authentication enables users to log in with their Windows credentials, using Kerberos or NTLM. The client sends credentials in the Authorization header. 
      * client -> IIS -> AD server
    * Requirements
      * use IIS running on a network that is using Microsoft Active Directory service domain identities
         * or other Windows accounts to identify users. (ユーザ認証がADでなくてもよい??)
      * Kerberos or NTLM support in the client browser. (IE is default supported)
      * Client computers and Web servers are in the same domain. (MUST??)
      * Intra-net environment (no proxy between client and server, etc)    
    * AD group (role)などの属性をIdentityに取り込めるみたい。
    
* [Authorization](https://docs.microsoft.com/ja-jp/aspnet/core/security/authorization/introduction)
  * page, controller, folderなどに対して、user, role, all userなどを設定。コードで記述する。
  * Authorization convention for RazorPage
    * 
  * Simple Authorization
    * put [Authorize]/[AllowAnonymous] atribute on controller/action/PageModel to allow authenticated/all users to access.
  * Role based Authorization
    * put [Authorize(Roles = "ROLL NAME")] attribute.
    * Role = Administrator, PowerUser, Manager, etc. 
    * Policyを登録しPolicy内でroleのチェックをすることも可。
  * Claim based
    * Claim(key-valueセット)をIdentityに登録しておき、keyとvalueの条件で判断する(特定のキーが存在するか、年齢が20歳以上かなど)。
    * Startup.csにポリシーとして判断方法を設定し、controller/action/(PageMdel?)に[Authorize(Policy = "POLICY NAME")]を付加。
  * Policy based
    * Startup.csに登録し、[Authorize(Policy = "POLICY NAME")]で呼び出す。
 
* Main, Host, Startup, Services, middleware
  * Host: The host is an object that encapsulates all of the app's resources
    * Program.Main() { CreateWebHostBuilder(args).Build().Run(); }
  * Startup
    * Startup class is called from Host.
  * Services (DI)
    * Startup.ConfigureServices(services) { servces.addMVC(); services.addDbContext().. }
  * middleware (called in request handling pipeline)
    * Startup.Configuire(app) { app.UseStaticFiles(); .. app.UseAuthentication(); ... }
 
# Razor Class Library (RCL)
* https://docs.microsoft.com/ja-jp/aspnet/core/razor-pages/ui-class
* reference: In app.csproj, <ItemGroup><PackageReference Include="xxxx"/>
* list install folders: ```[dotnet] nuget locals all --list```
* nuget, github, ...
    
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
    * Connection Pooling: https://www.oracle.com/technetwork/jp/articles/chapter5-2-085301-ja.html#p01a
  * ODT：Oracle Developer Tools for Visual Studio. GUI操作でOracleアプリケーション開発を行うためのVisual Studio 2005のアドインツール。開発環境（Visual Studio 2005）上で動作
    * ODTを使ったVisual StudioからのPL/SQL開発 https://www.atmarkit.co.jp/ait/articles/0705/07/news083_4.html

  * ODE.NET：Oracleデータベース上で.NETストアド・プロシージャを実行するための機能。Oracleデータベース・サーバ上で動作

  * Oracle Providers for ASP.NET: Microsoft ASP.NETのコントロールおよびサービスと直接統合され、Webサイトの状態管理機能が提供されます。
    * https://docs.oracle.com/cd/E57425_01/121/ASPNT/IntroOverview.htm
    * ASP.NETアプリケーションは、様々なタイプのアプリケーション状態をOracleデータベースに格納できます。


