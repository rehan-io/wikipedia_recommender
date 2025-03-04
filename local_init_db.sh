#!/bin/bash

# Activate virtual environment if needed
# source venv/bin/activate

# Create migrations
echo "Creating migrations..."
python manage.py makemigrations users

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

echo "Database initialization completed."
