#!/bin/bash
set -e

echo "Deploying Tribe AI Application..."

# Pull latest code
git pull origin main

# Build Docker images
docker-compose build

# Stop old containers
docker-compose down

# Start new containers
docker-compose up -d

# Check health
sleep 10
curl -f http://localhost:8000/health || exit 1

echo "Deployment successful!"
