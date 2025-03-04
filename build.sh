#!/bin/bash
# Script to build Docker images with extended timeout

echo "Building Docker images with extended timeout..."
DOCKER_BUILDKIT=1 COMPOSE_HTTP_TIMEOUT=300 docker-compose build --no-cache

echo "Starting services..."
docker-compose up
