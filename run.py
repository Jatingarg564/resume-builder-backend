#!/usr/bin/env python
"""
Startup script for Render deployment.
Runs migrations, collects static files, then starts gunicorn.
"""
import os
import sys
import subprocess
import traceback

print("=== Starting Django Application ===", flush=True)
print(f"Current directory: {os.getcwd()}", flush=True)
print(f"DATABASE_URL is set: {'Yes' if os.getenv('DATABASE_URL') else 'No'}", flush=True)

# First, check if manage.py exists
if not os.path.exists("manage.py"):
    print("ERROR: manage.py not found!", flush=True)
    sys.exit(1)

print("\n=== Running database migrations ===", flush=True)

# Try importing django to check if it's installed
try:
    import django
    print(f"Django version: {django.VERSION}", flush=True)
except ImportError as e:
    print(f"ERROR: Django not installed: {e}", flush=True)
    sys.exit(1)

# Run migrations and capture ALL output
try:
    # Use shell=True to get better error output
    result = subprocess.run(
        f"{sys.executable} manage.py migrate --noinput",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=os.getcwd()
    )
    print(result.stdout, flush=True)

    if result.returncode != 0:
        print(f"\n=== MIGRATION FAILED (exit code {result.returncode}) ===", flush=True)
        sys.exit(1)

    print("\n=== Migrations OK ===", flush=True)
except Exception as e:
    print(f"\n=== MIGRATION EXCEPTION: {e} ===", flush=True)
    print(traceback.format_exc(), flush=True)
    sys.exit(1)

print("\n=== Collecting static files ===", flush=True)
subprocess.run(
    f"{sys.executable} manage.py collectstatic --noinput --clear",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

print("\n=== Starting Gunicorn ===", flush=True)
os.execvp("gunicorn", [
    "gunicorn",
    "core.wsgi:application",
    "--workers", "4",
    "--bind", f"0.0.0.0:{os.getenv('PORT', '8000')}"
])
