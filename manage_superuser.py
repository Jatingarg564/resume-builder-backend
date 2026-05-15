"""
Temporary script to create a superuser on Render deployment.
Delete this file after the superuser is created.
"""
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    import django
    django.setup()

    from django.contrib.auth import get_user_model
    from django.db import connection

    # Check if database tables exist
    with connection.cursor() as cursor:
        tables = connection.introspection.table_names()
        if 'accounts_user' not in tables:
            print("Database tables not created yet. Run migrations first.")
            sys.exit(0)

    User = get_user_model()

    username = os.getenv('ADMIN_USERNAME', 'admin')
    email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    password = os.getenv('ADMIN_PASSWORD', 'Admin123!')

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f'Superuser "{username}" created successfully!')
    else:
        print(f'Superuser "{username}" already exists.')
