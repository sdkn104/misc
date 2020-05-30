
REM compile .exe with all required libraries (no need of .net runtime)

dotnet publish  --self-contained --runtime win-x64

pause
