Documents
--------

* [doc](https://docs.microsoft.com/ja-jp/aspnet/web-forms/)
* [ASP.NET Web Forms Pages](https://docs.microsoft.com/en-us/previous-versions/fddycb06(v=vs.140))  --- no longer updating this content regularly

Detail
------

* ファイル構成
  * XXX.aspx
  * XXX.aspx.cs -- VS solution explorerでは、aspxを右クリックしてコード表示で開く
  
* Server Control [ref](https://docs.microsoft.com/ja-jp/aspnet/web-forms/overview/getting-started/getting-started-with-aspnet-45-web-forms/ui_and_navigation)
  * Web server controls are similar to HTML buttons and input elements. However, they are processed on the server, allowing you to use server code to set their properties. These controls also raise events that you can handle in server code.
  * ```<asp:xxxx ID="xxxxx" runat="server">```
  
* Server Code [ref](https://docs.microsoft.com/ja-jp/aspnet/web-forms/overview/getting-started/getting-started-with-aspnet-45-web-forms/ui_and_navigation)
  *  the page is a page with server code directly in the page, which is called a single-file page, or whether it is a page with code in a separate class file, which is called a code-behind page.
  
* Master Page [ref](https://docs.microsoft.com/ja-jp/aspnet/web-forms/overview/getting-started/getting-started-with-aspnet-45-web-forms/ui_and_navigation)
  *　master pages allow you to create a consistent layout for the pages in your application.

* Routng [ref](https://docs.microsoft.com/ja-jp/aspnet/web-forms/overview/getting-started/getting-started-with-aspnet-45-web-forms/url-routing)
  * A route is a URL pattern that is mapped to a handler. The handler can be a physical file, such as an .aspx file or a class that processes the request. To define a route, you create an instance of the Route class by specifying the URL pattern, the handler, and optionally a name for the route, in Global.asax.cs
  * default routing
    * http://xxxx/folder1/folder2/xxx.aspx or xxx   --> folder1/folder2/xxx.aspx file (folder structure in Visual Studio)
    
* [.aspx syntax](https://docs.microsoft.com/en-us/previous-versions/k33801s3(v=vs.140))

* page to page
  * get query string and form data
    * HttpRequest.Param
    * Request.QueryString("UserName")
    * Request.Form("LastName")
    * https://www.ipa.go.jp/security/awareness/vendor/programmingv1/a05_01_main.html
  * response
    * Response.Redirect("default2.aspx 
    * https://www.codeproject.com/Articles/37539/Redirect-and-POST-in-ASP-NET
    * Server.Transfer
* runat=server

  
