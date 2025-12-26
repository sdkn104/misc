using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace AuthServer.Controllers
{
    /// <summary>
    /// Difyアプリケーションをホストするコントローラー
    /// </summary>
    [Authorize]
    [Route("difyApp")]
    [ApiController]
    public class DifyAppController : ControllerBase
    {
        private readonly IConfiguration _configuration;
        private readonly ILogger<DifyAppController> _logger;
        private readonly IHttpClientFactory _httpClientFactory;

        public DifyAppController(IConfiguration configuration, ILogger<DifyAppController> logger, IHttpClientFactory httpClientFactory)
        {
            _configuration = configuration;
            _logger = logger;
            _httpClientFactory = httpClientFactory;
        }

        /// <summary>
        /// Difyアプリをiframeで埋め込む
        /// </summary>
        [HttpGet("{*path}")]
        //[AllowAnonymous]
        public IActionResult Index(string path, [FromQuery] string message = "")
        {
            var userName = User?.Identity?.Name ?? "Anonymous";
            var clientIp = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "Unknown";
            var requestUrl = $"{HttpContext.Request.Scheme}://{HttpContext.Request.Host}{HttpContext.Request.Path}{HttpContext.Request.QueryString}";

            _logger.LogInformation("USER: {User} | {Message} | {IpAddress}\n",  userName, message, clientIp);

            // Get Dify base URL from configuration
            var difyBaseUrl = _configuration["Dify:BaseUrl"] ?? "http://dify.example.com";
            var difyAppUrl = $"{difyBaseUrl}/{path}";

            var html = GenerateHtmlWithIframe(difyAppUrl);
            return Content(html, "text/html; charset=utf-8");
        }

        private string GenerateHtmlWithIframe(string difyUrl)
        {
            return $@"
<!DOCTYPE html>
<html lang=""ja"">
<head>
    <meta charset=""UTF-8"">
    <meta name=""viewport"" content=""width=device-width, initial-scale=1.0"">
    <title>Dify Application</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background-color: #f5f5f5;
        }}
        .container {{
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        .header {{
            background-color: #fff;
            padding: 12px 20px;
            border-bottom: 1px solid #e0e0e0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .header h1 {{
            margin: 0;
            font-size: 18px;
            color: #333;
        }}
        .content {{
            flex: 1;
            overflow: hidden;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
    </style>
</head>
<body>
    <div class=""container"">
        <div class=""header"">
            <h1>Dify Application</h1>  [注意点:] 
        </div>
        <div class=""content"">
            <iframe src=""{difyUrl}"" title=""Dify Application""></iframe>
        </div>
    </div>
</body>
</html>";
        }
    }
}
