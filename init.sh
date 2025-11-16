#!/bin/bash

# Load environment variables
source ./backend/.env

# Check if DB exists, create it if it doesn't
DB_LIST=$(psql -U $DB_USERNAME -h $DB_HOST -p $DB_PORT -lqt)
SEARCH_RESULT=$(echo $DB_LIST | grep $DB_NAME)
LENGTH=$(echo ${#SEARCH_RESULT})

if [ "$LENGTH" = "0" ]; then
    echo "The database does not exist. Creating database..."
    psql -U $DB_USERNAME -h $DB_HOST -p $DB_PORT -c "CREATE DATABASE \"$DB_NAME\";"
fi

# Set up backend by installing dependencies and initializing enemy data
cd ./backend

poetry install && poetry run python data/scripts/initialize_data.py --rebuild

# Install frontend dependencies and launch app
cd ../frontend

npm install

npm run start
