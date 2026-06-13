@echo off
setlocal enabledelayedexpansion

set "TASK_NAME=OutlookReplyMonitor"
set "INSTALL_DIR=%APPDATA%\OutlookReplyMonitor"
set "EXE_NAME=outlook_reply_monitor.exe"
set "INSTALL_EXE=%INSTALL_DIR%\%EXE_NAME%"
set "SOURCE_EXE=%~dp0dist\%EXE_NAME%"

echo ============================================
echo  OutlookReplyMonitor Installer
echo ============================================
echo.

rem -- 1. Check source exe --
if not exist "%SOURCE_EXE%" (
    echo ERROR: %SOURCE_EXE% not found.
    echo Please run build.ps1 first.
    echo.
    pause
    exit /b 1
)

rem -- 2. Create install dir and copy exe --
echo Install dir: %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
copy /y "%SOURCE_EXE%" "%INSTALL_EXE%" >nul
if errorlevel 1 (
    echo ERROR: Failed to copy exe.
    pause
    exit /b 1
)
echo Copied: %INSTALL_EXE%
echo.

rem -- 3. Remove existing task --
schtasks /query /tn "%TASK_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo Removing existing task...
    schtasks /end    /tn "%TASK_NAME%"    >nul 2>&1
    schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1
    echo Done.
    echo.
)

rem -- 4. Register scheduled task (run at logon, current user) --
echo Registering scheduled task...
schtasks /create /tn "%TASK_NAME%" /tr "\"%INSTALL_EXE%\"" /sc ONLOGON /rl LIMITED /f
if errorlevel 1 (
    echo ERROR: Failed to register task.
    pause
    exit /b 1
)
echo.
echo Task registered: %TASK_NAME%
echo   Trigger : At logon
echo   User    : %USERDOMAIN%\%USERNAME%
echo   Log     : %INSTALL_DIR%\monitor.log

rem -- 5. Start now? --
echo.
set /p "START_NOW=Start now? (y/n): "
if /i "!START_NOW!"=="y" (
    schtasks /run /tn "%TASK_NAME%"
    echo Started.
)

echo.
echo Installation complete. Will auto-start at next logon.
echo.
pause
