using Serilog;

var builder = WebApplicationBuilder.CreateBuilder(args);

// Configure Serilog
var logPath = Path.Combine(AppContext.BaseDirectory, "logs", "access-.txt");
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .WriteTo.File(logPath, 
        outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss} [{Level:u3}] User:{User} | URL:{RequestPath}{QueryString} | Status:{StatusCode} | IP:{RemoteIpAddress} | {Message:lj}",
        rollingInterval: RollingInterval.Infinite,
        fileSizeLimitBytes: 52428800, // 50MB
        retainedFileCountLimit: null)
    .CreateLogger();

builder.Host.UseSerilog();

// Add services to the container
builder.Services.AddAuthentication(Microsoft.AspNetCore.Authentication.Negotiate.NegotiateDefaults.AuthenticationScheme)
    .AddNegotiate();

builder.Services.AddAuthorization();

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowSpecificOrigins", policy =>
    {
        // Configure allowed origins from appsettings.json
        var allowedOrigins = builder.Configuration.GetSection("Cors:AllowedOrigins").Get<string[]>() ?? new[] { "http://localhost:3000" };
        policy.WithOrigins(allowedOrigins)
            .AllowAnyMethod()
            .AllowAnyHeader();
    });
});

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Custom middleware to capture request/response details for logging
app.Use(async (context, next) =>
{
    var user = context.User?.Identity?.Name ?? "Anonymous";
    var remoteIp = context.Connection.RemoteIpAddress?.ToString() ?? "Unknown";
    var requestPath = context.Request.Path.Value ?? "/";
    var queryString = context.Request.QueryString.Value ?? "";
    var statusCode = "200";

    try
    {
        await next();
        statusCode = context.Response.StatusCode.ToString();
    }
    finally
    {
        // Log the request
        Log.Information("", null);
        var logger = context.RequestServices.GetRequiredService<ILogger<Program>>();
        logger.LogInformation("User:{User} | URL:{RequestPath}{QueryString} | Status:{StatusCode} | IP:{RemoteIp}",
            user, requestPath, queryString, statusCode, remoteIp);
    }
});

app.UseCors("AllowSpecificOrigins");
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

try
{
    app.Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Application terminated unexpectedly");
}
finally
{
    Log.CloseAndFlush();
}
