
Install
  * (Visual Studio Code)
  * (C# for Visual Studio Code)
  * .NET Core SDK 2.2 or later
  * When use IIS, Install the .NET Core Hosting Bundle, which includes
     * .NET Core Runtime
     * .NET Core Library
     * ASP.NET Core Module (a native IIS module for ASP.NET Core app)

Create project in folder .\MyWebApp
> dotnet new webapp -o MyWebApp

> (code -r MyWebApp  (open by vs code))

> cd MyWebApp

Specify hosting mode in Program.cs, APP.csproj
> 

Publish and Run (Kestrel model only)
> dotnet run [--configuration Debug]
    ---> start web app at http://localhost:5000

Publish (IIS in/out-of-process model)
 -- compile and move to publish folder bin\Release, etc.
> dotnet publish --configuration Release

Deploy (IIS in/out-of-process model)
> Move the contents of the bin/Release/{TARGET FRAMEWORK}/publish folder to the IIS site folder

IIS enable　https://docs.microsoft.com/ja-jp/aspnet/core/host-and-deploy/
> IISを有効化　（Win10の場合、 enable IIS Management Console and World Wide Web Services）

Create the IIS site (コントロールパネル　管理ツール　IIS管理コンソール)
> Create the IIS site (set site name, pysical path)
> Application Pool (set the .NET CLR version to No Managed Code)
> siteフォルダ(web.config)に、IIS_IUSRSグループにフルコントロール権限

ODP.NET
> dotnet add package Oracle.ManagedDataAccess.Core --version 2.19.31

