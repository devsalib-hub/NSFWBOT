#!/bin/bash
# Database backup script for NSFWBOT Docker container

# Configuration
CONTAINER_NAME="nsfwbot"
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="bot_database_backup_${DATE}.db"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "🔄 Starting database backup..."
echo "Container: $CONTAINER_NAME"
echo "Backup file: $BACKUP_FILE"

# Check if container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo "❌ Error: Container '$CONTAINER_NAME' is not running"
    exit 1
fi

# Create backup using SQLite .backup command
docker exec "$CONTAINER_NAME" sqlite3 /app/data/bot_database.db ".backup '/app/data/$BACKUP_FILE'"

# Copy backup to host
docker cp "$CONTAINER_NAME:/app/data/$BACKUP_FILE" "$BACKUP_DIR/$BACKUP_FILE"

# Remove backup from container
docker exec "$CONTAINER_NAME" rm "/app/data/$BACKUP_FILE"

# Verify backup file exists and has content
if [ -f "$BACKUP_DIR/$BACKUP_FILE" ] && [ -s "$BACKUP_DIR/$BACKUP_FILE" ]; then
    echo "✅ Backup completed successfully: $BACKUP_DIR/$BACKUP_FILE"
    
    # Show backup file size
    BACKUP_SIZE=$(stat -f%z "$BACKUP_DIR/$BACKUP_FILE" 2>/dev/null || stat -c%s "$BACKUP_DIR/$BACKUP_FILE" 2>/dev/null)
    echo "📊 Backup size: $BACKUP_SIZE bytes"
    
    # Optional: Remove old backups (keep last 7 days)
    find "$BACKUP_DIR" -name "bot_database_backup_*.db" -mtime +7 -delete 2>/dev/null
    echo "🧹 Cleaned up backups older than 7 days"
    
else
    echo "❌ Error: Backup failed or file is empty"
    exit 1
fi

echo "🎉 Database backup completed successfully!"