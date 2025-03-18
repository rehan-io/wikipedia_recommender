FROM python:3.10-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

# Install system dependencies with Alpine's package manager
RUN apk add --no-cache \
    postgresql-client \
    postgresql-dev \
    build-base \
    jpeg-dev \
    zlib-dev \
    libffi-dev 

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt



# Copy application code
COPY . .

# Create an entrypoint script
RUN echo '#!/bin/sh' > /app/entrypoint.sh && \
    echo 'set -e' >> /app/entrypoint.sh && \
    echo 'echo "Waiting for database..."' >> /app/entrypoint.sh && \
    echo 'while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT; do sleep 1; done' >> /app/entrypoint.sh && \
    echo 'echo "Database is ready"' >> /app/entrypoint.sh && \
    echo 'python manage.py makemigrations' >> /app/entrypoint.sh && \
    echo 'python manage.py migrate' >> /app/entrypoint.sh && \
    echo 'python manage.py collectstatic --no-input' >> /app/entrypoint.sh && \
    echo 'python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username=\"admin\").exists() or User.objects.create_superuser(\"admin\", \"admin@example.com\", \"adminpassword\")"' >> /app/entrypoint.sh && \
    echo 'gunicorn config.wsgi:application --bind 0.0.0.0:8000' >> /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
