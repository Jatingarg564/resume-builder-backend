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

print("\n=== Running database migrations ===", flush=True)
try:
    result = subprocess.run(
        [sys.executable, "manage.py", "migrate", "--noinput"],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    # Print stdout and stderr so we can see what happened
    if result.stdout:
        print(result.stdout, flush=True)
    if result.stderr:
        print(result.stderr, flush=True)

    if result.returncode != 0:
        print(f"\nMIGRATION FAILED with code {result.returncode}", flush=True)
        sys.exit(1)
    print("\nMigrations completed successfully!", flush=True)
except Exception as e:
    print(f"\nMIGRATION ERROR: {e}", flush=True)
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
