#!/bin/bash
set -o errexit

echo "=== Starting Django Application ==="

echo "Running database migrations..."
python manage.py migrate --noinput 2>&1 | tee /tmp/migrate.log

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear 2>&1 | tee /tmp/collectstatic.log

echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application --workers 4 --bind 0.0.0.0:$PORT
