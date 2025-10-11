# Database backup script for NSFWBOT Docker container (Windows PowerShell)

param(
    [string]$ContainerName = "nsfwbot",
    [string]$BackupDir = "./backups"
)

# Configuration
$Date = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupFile = "bot_database_backup_$Date.db"

# Create backup directory if it doesn't exist
if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

Write-Host "🔄 Starting database backup..." -ForegroundColor Cyan
Write-Host "Container: $ContainerName" -ForegroundColor White
Write-Host "Backup file: $BackupFile" -ForegroundColor White

# Check if container is running
$containerRunning = docker ps --format "table {{.Names}}" | Select-String $ContainerName
if (-not $containerRunning) {
    Write-Host "❌ Error: Container '$ContainerName' is not running" -ForegroundColor Red
    exit 1
}

try {
    # Create backup using SQLite .backup command
    Write-Host "📝 Creating database backup..." -ForegroundColor Yellow
    docker exec $ContainerName sqlite3 /app/data/bot_database.db ".backup '/app/data/$BackupFile'"
    
    # Copy backup to host
    Write-Host "📥 Copying backup to host..." -ForegroundColor Yellow
    docker cp "${ContainerName}:/app/data/$BackupFile" "$BackupDir/$BackupFile"
    
    # Remove backup from container
    docker exec $ContainerName rm "/app/data/$BackupFile"
    
    # Verify backup file exists and has content
    $backupPath = Join-Path $BackupDir $BackupFile
    if ((Test-Path $backupPath) -and ((Get-Item $backupPath).Length -gt 0)) {
        Write-Host "✅ Backup completed successfully: $backupPath" -ForegroundColor Green
        
        # Show backup file size
        $backupSize = (Get-Item $backupPath).Length
        Write-Host "📊 Backup size: $backupSize bytes" -ForegroundColor White
        
        # Optional: Remove old backups (keep last 7 days)
        $cutoffDate = (Get-Date).AddDays(-7)
        Get-ChildItem -Path $BackupDir -Name "bot_database_backup_*.db" | 
            Where-Object { (Get-Item (Join-Path $BackupDir $_)).LastWriteTime -lt $cutoffDate } |
            ForEach-Object { 
                Remove-Item (Join-Path $BackupDir $_) -Force
                Write-Host "🗑️ Removed old backup: $_" -ForegroundColor Gray
            }
        
        Write-Host "🧹 Cleaned up backups older than 7 days" -ForegroundColor White
        
    } else {
        Write-Host "❌ Error: Backup failed or file is empty" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "🎉 Database backup completed successfully!" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error during backup: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}