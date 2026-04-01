#!/usr/bin/env bash

# Organizer script for lab1

set -euo pipefail

ARCHIVE_DIR="archive"
CSV_FILE="grades.csv"
LOG_FILE="organizer.log"

# Ensure archive directory exists
if [[ ! -d "$ARCHIVE_DIR" ]]; then
    mkdir -p "$ARCHIVE_DIR"
fi

# Timestamp for filename/logging
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

if [[ ! -f "$CSV_FILE" ]]; then
    echo "Error: $CSV_FILE not found in $(pwd)." >&2
    exit 1
fi

ARCHIVED_NAME="grades_${TIMESTAMP}.csv"
ARCHIVED_PATH="$ARCHIVE_DIR/$ARCHIVED_NAME"

# Move grades.csv into archive with timestamped name
mv "$CSV_FILE" "$ARCHIVED_PATH"

# Create a fresh (empty) grades.csv for the next run
: > "$CSV_FILE"

# Log the archive operation
echo "${TIMESTAMP}	${CSV_FILE}	${ARCHIVED_PATH}" >> "$LOG_FILE"

echo "Archived $CSV_FILE -> $ARCHIVED_PATH"
