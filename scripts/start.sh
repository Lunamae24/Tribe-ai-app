#!/bin/bash
set -e

echo "Starting Tribe AI Application..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Run database migrations (if needed)
# alembic upgrade head

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
