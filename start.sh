#!/bin/bash
set -e

# Identify the Django project directory
PROJECT_DIR=$(find . -maxdepth 1 -type d -not -path "*/\.*" -not -path "./frontend" -not -path "./staticfiles" -not -path "." | head -1)
PROJECT_NAME=$(basename $PROJECT_DIR)

echo "Found Django project: $PROJECT_NAME"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn with project: $PROJECT_NAME.wsgi:application"
gunicorn $PROJECT_NAME.wsgi:application --bind 0.0.0.0:8000
