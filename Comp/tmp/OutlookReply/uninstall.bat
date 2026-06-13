@echo off
setlocal enabledelayedexpansion

set "TASK_NAME=OutlookReplyMonitor"
set "INSTALL_DIR=%APPDATA%\OutlookReplyMonitor"

echo ============================================
echo  OutlookReplyMonitor Uninstaller
echo ============================================
echo.

rem -- 1. Stop and remove scheduled task --
schtasks /query /tn "%TASK_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo Stopping task...
    schtasks /end    /tn "%TASK_NAME%"    >nul 2>&1
    schtasks /delete /tn "%TASK_NAME%" /f
    echo Task removed: %TASK_NAME%
) else (
    echo Task not found (skipped): %TASK_NAME%
)
echo.

rem -- 2. Remove install directory --
if exist "%INSTALL_DIR%" (
    set /p "DEL_DIR=Delete %INSTALL_DIR% (includes log file)? (y/n): "
    if /i "!DEL_DIR!"=="y" (
        rmdir /s /q "%INSTALL_DIR%"
        echo Deleted: %INSTALL_DIR%
    ) else (
        echo Directory kept: %INSTALL_DIR%
    )
) else (
    echo Directory not found (skipped): %INSTALL_DIR%
)
echo.

echo Uninstallation complete.
echo.
pause
