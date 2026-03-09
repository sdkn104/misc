# Start Edge Extension HTTPS Server
Write-Host 'Starting Edge Extension HTTPS Server...' -ForegroundColor Cyan
Write-Host "Server Port: 8443"
Write-Host "Serving from: D:\NoSync\misc\Comp\EdgeExtension\output"

python "D:\NoSync\misc\Comp\EdgeExtension\server\https_server.py"
