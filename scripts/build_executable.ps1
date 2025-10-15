param(
    [switch]$SkipClean
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path -Path (Join-Path $scriptDir '..')

Push-Location $projectRoot

try {
    $pyInstallerInstalled = $true
    try {
        python -m PyInstaller --version | Out-Null
    } catch {
        $pyInstallerInstalled = $false
    }

    if (-not $pyInstallerInstalled) {
        Write-Host 'PyInstaller not found. Installing...' -ForegroundColor Yellow
        python -m pip install --upgrade pip | Out-Null
        python -m pip install pyinstaller | Out-Null
    }

    if (-not $SkipClean) {
        Write-Host 'Cleaning previous build artifacts...' -ForegroundColor Cyan
        Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
    }

    Write-Host 'Building NSFWBot executable...' -ForegroundColor Cyan
    python -m PyInstaller --noconfirm --clean NSFWBot.spec

    $exePath = Join-Path $projectRoot 'dist\NSFWBot.exe'
    if (Test-Path $exePath) {
        Write-Host "Build completed successfully.`nExecutable: $exePath" -ForegroundColor Green
    } else {
        Write-Host 'PyInstaller finished but no executable was created. Check the log output for errors.' -ForegroundColor Red
        exit 1
    }
}
finally {
    Pop-Location
}
