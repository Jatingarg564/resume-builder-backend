#!/usr/bin/env python
"""
Startup script for Render deployment.
Runs migrations, collects static files, then starts gunicorn.
"""
import os
import sys
import subprocess

print("=== Starting Django Application ===")
print(f"Current directory: {os.getcwd()}")
print(f"DATABASE_URL is set: {'Yes' if os.getenv('DATABASE_URL') else 'No'}")

print("\n=== Running database migrations ===")
result = subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"],
                       capture_output=False, text=True)
if result.returncode != 0:
    print(f"Migration failed with code {result.returncode}")
    sys.exit(1)

print("\n=== Collecting static files ===")
subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput", "--clear"],
               capture_output=False, text=True)

print("\n=== Starting Gunicorn ===")
os.execvp("gunicorn", [
    "gunicorn",
    "core.wsgi:application",
    "--workers", "4",
    "--bind", f"0.0.0.0:{os.getenv('PORT', '8000')}"
])
