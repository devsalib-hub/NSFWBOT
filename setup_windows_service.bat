@echo off
REM NSFWBot Windows Service Setup Script
REM This script sets up the bot as a Windows service using NSSM

echo ========================================
echo   NSFWBot Windows Service Setup
echo ========================================
echo.

REM Check if NSSM is installed
where nssm >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ NSSM not found in PATH
    echo.
    echo 📥 Please install NSSM first:
    echo 1. Download from: https://nssm.cc/download
    echo 2. Extract nssm.exe to a folder in your PATH
    echo 3. Or add NSSM folder to your system PATH
    echo.
    pause
    exit /b 1
)

echo ✅ NSSM found
echo.

REM Get the current directory
set "BOT_DIR=%~dp0"
set "BOT_DIR=%BOT_DIR:~0,-1%"

REM Check if Python is available
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found in PATH
    echo Please ensure Python is installed and in your PATH
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if start_bot.py exists
if not exist "%BOT_DIR%\start_bot.py" (
    echo ❌ start_bot.py not found in %BOT_DIR%
    pause
    exit /b 1
)

echo ✅ Bot files found
echo.

REM Get Python executable path
for /f "tokens=*" %%i in ('where python') do set PYTHON_EXE=%%i

echo Using Python: %PYTHON_EXE%
echo Bot Directory: %BOT_DIR%
echo.

REM Remove existing service if it exists
nssm stop NSFWBot >nul 2>nul
nssm remove NSFWBot confirm >nul 2>nul

echo Installing NSFWBot service...
echo.

REM Install the service
nssm install NSFWBot "%PYTHON_EXE%" "start_bot.py"

REM Configure the service
nssm set NSFWBot Application "%PYTHON_EXE%"
nssm set NSFWBot AppParameters "start_bot.py"
nssm set NSFWBot AppDirectory "%BOT_DIR%"
nssm set NSFWBot DisplayName "NSFWBot Telegram Bot"
nssm set NSFWBot Description "NSFWBot - AI-powered Telegram bot with admin dashboard"

REM Configure service behavior
nssm set NSFWBot Start SERVICE_AUTO_START
nssm set NSFWBot Type SERVICE_WIN32_OWN_PROCESS

REM Configure restart behavior
nssm set NSFWBot AppExit Default Restart
nssm set NSFWBot AppRestartDelay 30000

REM Configure logging
nssm set NSFWBot AppStdout "%BOT_DIR%\logs\service_stdout.log"
nssm set NSFWBot AppStderr "%BOT_DIR%\logs\service_stderr.log"

REM Create logs directory
if not exist "%BOT_DIR%\logs" mkdir "%BOT_DIR%\logs"

echo ✅ Service installed successfully!
echo.
echo Service Details:
echo - Service Name: NSFWBot
echo - Display Name: NSFWBot Telegram Bot
echo - Python: %PYTHON_EXE%
echo - Working Directory: %BOT_DIR%
echo - Logs: %BOT_DIR%\logs\
echo.

REM Ask user if they want to start the service now
echo Would you like to start the service now? (Y/N)
set /p START_SERVICE=

if /i "%START_SERVICE%"=="Y" (
    echo.
    echo Starting NSFWBot service...
    nssm start NSFWBot
    if %errorlevel% equ 0 (
        echo ✅ Service started successfully!
        echo.
        echo 🔍 Check service status: nssm status NSFWBot
        echo 📊 View logs: type "%BOT_DIR%\logs\service_stdout.log"
        echo 🛑 Stop service: nssm stop NSFWBot
        echo 🔄 Restart service: nssm restart NSFWBot
    ) else (
        echo ❌ Failed to start service
        echo Check the logs for errors
    )
) else (
    echo.
    echo Service installed but not started.
    echo To start manually: nssm start NSFWBot
)

echo.
echo ========================================
echo   Service Management Commands:
echo ========================================
echo Start:    nssm start NSFWBot
echo Stop:     nssm stop NSFWBot
echo Restart:  nssm restart NSFWBot
echo Status:   nssm status NSFWBot
echo Remove:   nssm remove NSFWBot confirm
echo Edit:     nssm edit NSFWBot
echo.
echo Logs:     %BOT_DIR%\logs\
echo ========================================

pause