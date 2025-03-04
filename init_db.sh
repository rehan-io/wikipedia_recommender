#!/bin/bash

echo "Creating migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

echo "Database initialization completed."
