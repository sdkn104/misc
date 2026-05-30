using Microsoft.AspNetCore.Server.IISIntegration;
using Microsoft.AspNetCore.Authorization;

var builder = WebApplication.CreateBuilder(args);

// IISのWindows認証を利用
builder.Services.AddAuthentication(IISDefaults.AuthenticationScheme);
builder.Services.AddAuthorization(options =>
{
    options.FallbackPolicy = new AuthorizationPolicyBuilder()
        .RequireAuthenticatedUser()
        .Build();
});

// YARPリバースプロキシの設定
builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();

// Windows認証ユーザー名を X-Auth-User ヘッダーに付加
app.Use(async (context, next) =>
{
    var userName = context.User.Identity?.Name ?? string.Empty;
    context.Request.Headers["X-Auth-User"] = userName;
    await next();
});

app.MapReverseProxy();

//app.MapGet("/", () => "Hello World!");

app.Run();