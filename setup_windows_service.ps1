# NSFWBot Windows Service Setup Script
# This script sets up the bot as a Windows service using NSSM

param(
    [switch]$StartService,
    [switch]$RemoveService
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NSFWBot Windows Service Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if NSSM is installed
try {
    $nssm = Get-Command nssm -ErrorAction Stop
    Write-Host "✅ NSSM found at: $($nssm.Source)" -ForegroundColor Green
} catch {
    Write-Host "❌ NSSM not found in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 Please install NSSM first:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://nssm.cc/download" -ForegroundColor White
    Write-Host "2. Extract nssm.exe to a folder in your PATH" -ForegroundColor White
    Write-Host "3. Or add NSSM folder to your system PATH" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Get the current directory
$BotDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Bot Directory: $BotDir" -ForegroundColor White

# Check if Python is available
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
    Write-Host "Please ensure Python is installed and in your PATH" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if start_bot.py exists
$startBotPath = Join-Path $BotDir "start_bot.py"
if (-not (Test-Path $startBotPath)) {
    Write-Host "❌ start_bot.py not found in $BotDir" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Bot files found" -ForegroundColor Green
Write-Host ""

# Get Python executable path
$pythonExe = (Get-Command python).Source
Write-Host "Using Python: $pythonExe" -ForegroundColor White
Write-Host ""

if ($RemoveService) {
    Write-Host "Removing existing NSFWBot service..." -ForegroundColor Yellow
    & nssm stop NSFWBot 2>$null | Out-Null
    & nssm remove NSFWBot confirm 2>$null | Out-Null
    Write-Host "✅ Service removed" -ForegroundColor Green
    exit 0
}

# Remove existing service if it exists
Write-Host "Checking for existing service..." -ForegroundColor White
$nssmOutput = & nssm status NSFWBot 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Removing existing NSFWBot service..." -ForegroundColor Yellow
    & nssm stop NSFWBot 2>$null | Out-Null
    & nssm remove NSFWBot confirm 2>$null | Out-Null
}

Write-Host "Installing NSFWBot service..." -ForegroundColor White

# Install the service
$nssmResult = & nssm install NSFWBot $pythonExe "start_bot.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install service" -ForegroundColor Red
    exit 1
}

# Configure the service
& nssm set NSFWBot Application $pythonExe
& nssm set NSFWBot AppParameters "start_bot.py"
& nssm set NSFWBot AppDirectory $BotDir
& nssm set NSFWBot DisplayName "NSFWBot Telegram Bot"
& nssm set NSFWBot Description "NSFWBot - AI-powered Telegram bot with admin dashboard"

# Configure service behavior
& nssm set NSFWBot Start SERVICE_AUTO_START
& nssm set NSFWBot Type SERVICE_WIN32_OWN_PROCESS

# Configure restart behavior
& nssm set NSFWBot AppExit Default Restart
& nssm set NSFWBot AppRestartDelay 30000

# Configure logging
$logDir = Join-Path $BotDir "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

$stdoutLog = Join-Path $logDir "service_stdout.log"
$stderrLog = Join-Path $logDir "service_stderr.log"

& nssm set NSFWBot AppStdout $stdoutLog
& nssm set NSFWBot AppStderr $stderrLog

Write-Host "✅ Service installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Service Details:" -ForegroundColor White
Write-Host "- Service Name: NSFWBot" -ForegroundColor White
Write-Host "- Display Name: NSFWBot Telegram Bot" -ForegroundColor White
Write-Host "- Python: $pythonExe" -ForegroundColor White
Write-Host "- Working Directory: $BotDir" -ForegroundColor White
Write-Host "- Logs: $logDir" -ForegroundColor White
Write-Host ""

if ($StartService) {
    Write-Host "Starting NSFWBot service..." -ForegroundColor White
    $startResult = & nssm start NSFWBot
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Service started successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to start service" -ForegroundColor Red
        Write-Host "Check the logs for errors:" -ForegroundColor Yellow
        Write-Host "  $stderrLog" -ForegroundColor White
    }
} else {
    $startNow = Read-Host "Would you like to start the service now? (Y/N)"
    if ($startNow -eq 'Y' -or $startNow -eq 'y') {
        Write-Host ""
        Write-Host "Starting NSFWBot service..." -ForegroundColor White
        $startResult = & nssm start NSFWBot
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Service started successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to start service" -ForegroundColor Red
            Write-Host "Check the logs for errors" -ForegroundColor Yellow
        }
    } else {
        Write-Host ""
        Write-Host "Service installed but not started." -ForegroundColor Yellow
        Write-Host "To start manually: nssm start NSFWBot" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Service Management Commands:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Start:    nssm start NSFWBot" -ForegroundColor White
Write-Host "Stop:     nssm stop NSFWBot" -ForegroundColor White
Write-Host "Restart:  nssm restart NSFWBot" -ForegroundColor White
Write-Host "Status:   nssm status NSFWBot" -ForegroundColor White
Write-Host "Remove:   nssm remove NSFWBot confirm" -ForegroundColor White
Write-Host "Edit:     nssm edit NSFWBot" -ForegroundColor White
Write-Host ""
Write-Host "Logs:     $logDir" -ForegroundColor White
Write-Host "Health:   http://localhost:4656/health" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

if (-not $StartService) {
    Read-Host "Press Enter to exit"
}