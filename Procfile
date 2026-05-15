release: python manage.py migrate && python manage_superuser.py
web: gunicorn core.wsgi:application --workers 4 --bind 0.0.0.0:$PORT
