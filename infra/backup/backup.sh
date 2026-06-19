#!/bin/bash
# Backup script for BQ Assistant

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
DB_FILE="./test.db"

mkdir -p $BACKUP_DIR

echo "Starting backup at $TIMESTAMP..."

# Backup database
if [ -f "$DB_FILE" ]; then
    cp $DB_FILE "$BACKUP_DIR/db_backup_$TIMESTAMP.sqlite"
    echo "Database backed up."
else
    echo "Database file not found."
fi

# Backup logs
tar -czf "$BACKUP_DIR/logs_backup_$TIMESTAMP.tar.gz" ./logs
echo "Logs backed up."

echo "Backup completed successfully."
