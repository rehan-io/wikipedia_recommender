#!/bin/sh

# Wait for the database to be ready
echo "Waiting for database..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "Database is ready"

# Create migrations
echo "Creating migrations..."
python manage.py makemigrations

# Apply migrations
echo "Applying migrations..."
python manage.py migrate



# Create a superuser if not exists
echo "Creating superuser..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')"

# Start server
echo "Starting server..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000
