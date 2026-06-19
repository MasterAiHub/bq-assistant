#!/bin/bash
# Restore script for BQ Assistant

if [ -z "$1" ]; then
    echo "Usage: $0 <backup_timestamp>"
    exit 1
fi

TIMESTAMP=$1
BACKUP_DIR="./backups"
DB_FILE="./test.db"

echo "Restoring from backup $TIMESTAMP..."

# Restore database
if [ -f "$BACKUP_DIR/db_backup_$TIMESTAMP.sqlite" ]; then
    cp "$BACKUP_DIR/db_backup_$TIMESTAMP.sqlite" $DB_FILE
    echo "Database restored."
else
    echo "Backup file not found."
fi

# Restore logs
if [ -f "$BACKUP_DIR/logs_backup_$TIMESTAMP.tar.gz" ]; then
    tar -xzf "$BACKUP_DIR/logs_backup_$TIMESTAMP.tar.gz" -C .
    echo "Logs restored."
fi

echo "Restore completed successfully."
