#!/bin/bash
set -euo pipefail

# Load environment from the mounted project root.
source /script/.env

# Check whether the target database already exists.
DB_EXISTS=$(
  psql \
    -U "$DB_USERNAME" \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -d postgres \
    -tAc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME';"
)

if [ "$DB_EXISTS" = "1" ]; then
  echo "The database already exists. Skipping database creation."
else
  echo "The database does not exist. Creating database..."
  psql \
    -U "$DB_USERNAME" \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -d postgres \
    -c "CREATE DATABASE \"$DB_NAME\";"
fi