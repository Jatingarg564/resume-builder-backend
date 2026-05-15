#!/bin/bash
set -o errexit

echo "=== Starting Django Application ==="
echo "Current directory: $(pwd)"
echo "DATABASE_URL is set: $([ -n "$DATABASE_URL" ] && echo 'Yes' || echo 'No')"

echo ""
echo "=== Running database migrations ==="
python manage.py migrate --noinput 2>&1

echo ""
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput --clear 2>&1

echo ""
echo "=== Starting Gunicorn ==="
exec gunicorn core.wsgi:application --workers 4 --bind 0.0.0.0:$PORT
