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
print(f"PYTHONPATH: {sys.path}", flush=True)

try:
    print("\n=== Running database migrations ===", flush=True)
    result = subprocess.run(
        [sys.executable, "manage.py", "migrate", "--noinput"],
        capture_output=False,
        text=True,
        cwd=os.getcwd()
    )
    if result.returncode != 0:
        print(f"MIGRATION FAILED with code {result.returncode}", flush=True)
        sys.exit(1)
    print("Migrations completed successfully!", flush=True)
except Exception as e:
    print(f"MIGRATION ERROR: {e}", flush=True)
    print(traceback.format_exc(), flush=True)
    sys.exit(1)

print("\n=== Collecting static files ===", flush=True)
try:
    subprocess.run(
        [sys.executable, "manage.py", "collectstatic", "--noinput", "--clear"],
        capture_output=False,
        text=True,
        cwd=os.getcwd()
    )
except Exception as e:
    print(f"Collectstatic error (non-fatal): {e}", flush=True)

print("\n=== Starting Gunicorn ===", flush=True)
os.execvp("gunicorn", [
    "gunicorn",
    "core.wsgi:application",
    "--workers", "4",
    "--bind", f"0.0.0.0:{os.getenv('PORT', '8000')}"
])
