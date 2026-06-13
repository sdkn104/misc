# ============================================================
# build.ps1 - PyInstaller で exe をビルドする
# 実行: powershell -ExecutionPolicy Bypass -File build.ps1
# ============================================================

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "依存ライブラリを確認中..."
pip install pywin32 requests pyinstaller --quiet
if ($LASTEXITCODE -ne 0) { Write-Host "pip install 失敗" -ForegroundColor Red; exit 1 }

Write-Host "PyInstaller でビルド中..." -ForegroundColor Cyan
pyinstaller `
    --onefile `
    --noconsole `
    --name outlook_reply_monitor `
    --hidden-import win32com.client `
    --hidden-import win32timezone `
    outlook_reply_monitor.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "ビルド成功: dist\outlook_reply_monitor.exe" -ForegroundColor Green
} else {
    Write-Host "ビルド失敗" -ForegroundColor Red
    exit 1
}
