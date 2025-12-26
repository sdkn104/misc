using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace AuthServer.Controllers
{
    /// <summary>
    /// ログ記録API コントローラー
    /// </summary>
    [Authorize]
    [Route("api/log")]
    [ApiController]
    public class LogController : ControllerBase
    {
        private readonly ILogger<LogController> _logger;

        public LogController(ILogger<LogController> logger)
        {
            _logger = logger;
        }

        /// <summary>
        /// アクセスログを記録する
        /// </summary>
        /// <param name="name">ログの名前（呼び出し元が指定）</param>
        /// <param name="message">ログメッセージ</param>
        /// <returns>ログ記録の結果</returns>
        [HttpGet("{name}")]
        public IActionResult LogMessage(string name, [FromQuery] string message = "")
        {
            var userName = User?.Identity?.Name ?? "Anonymous";
            var clientIp = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "Unknown";
            var requestUrl = $"{HttpContext.Request.Path}{HttpContext.Request.QueryString}";

            try
            {
                _logger.LogInformation(
                    "USER: {User} | {LogName} | {Message} | {IpAddress}\n",
                    userName, name, message, clientIp);

                return Ok(new { status = "success", message = "Log recorded successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error recording log for {LogName}", name);
                return StatusCode(500, new { status = "error", message = "Failed to record log" });
            }
        }

        /// <summary>
        /// ログ記録API - POST版（JSONボディ対応）
        /// </summary>
        /// <param name="name">ログの名前</param>
        /// <param name="payload">ログペイロード</param>
        /// <returns>ログ記録の結果</returns>
        [HttpPost("{name}")]
        public IActionResult LogMessagePost(string name, [FromBody] LogPayload payload)
        {
            var userName = User?.Identity?.Name ?? "Anonymous";
            var clientIp = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "Unknown";

            try
            {
                _logger.LogInformation(
                    "USER: {User} | {LogName} | {Message} | Metadata:{Metadata} | {IpAddress}\n",
                    userName, name, payload.Message, payload.Metadata ?? "", clientIp);

                return Ok(new { status = "success", message = "Log recorded successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error recording log for {LogName}", name);
                return StatusCode(500, new { status = "error", message = "Failed to record log" });
            }
        }

        /// <summary>
        /// ログペイロードモデル
        /// </summary>
        public class LogPayload
        {
            public string Message { get; set; } = string.Empty;
            public string? Metadata { get; set; }
        }
    }
}
