@echo off
REM Edge Extension Deployment Setup
REM Run this batch file to start the deployment process

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Edge Extension Deployment Setup
echo ========================================
echo.

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

REM Run the PowerShell script
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%deploy_extension.ps1"

if errorlevel 1 (
    echo.
    echo Error occurred during setup
    pause
    exit /b 1
) else (
    echo.
    echo Setup completed successfully
    pause
)
