# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django REST API backend for a resume builder application with JWT authentication, resume versioning, AI-enhanced content, PDF generation, and job application tracking.

## Tech Stack

- Django 5.2
- Django REST Framework + SimpleJWT
- PostgreSQL (production) / SQLite (development)
- Gunicorn + WhiteNoise (production)
- Celery + Redis (async tasks, caching)
- OpenAI API (AI enhancements)

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Run all tests
python manage.py test

# Run specific test file
python manage.py test accounts.tests

# Run specific test class
python manage.py test accounts.tests.SignupTests

# Start Celery worker (development)
celery -A core worker --loglevel=info

# Collect static files
python manage.py collectstatic --noinput
```

## Environment Variables

Required (`.env` file):
- `SECRET_KEY` - Django secret key
- `DEBUG` - "True" for development
- `ALLOWED_HOSTS` - Comma-separated allowed hosts
- `DATABASE_URL` - PostgreSQL URL (optional, defaults to SQLite)

Optional:
- `REDIS_URL` - Redis URL for caching/Celery
- `CELERY_BROKER_URL` - Celery broker URL
- `JWT_ACCESS_LIFETIME_MINUTES` - Access token TTL (default: 60)
- `JWT_REFRESH_LIFETIME_DAYS` - Refresh token TTL (default: 7)
- `OPENAI_API_KEY` - For AI resume enhancements
- `EMAIL_HOST`, `DEFAULT_FROM_EMAIL` - For password reset emails
- `FRONTEND_URL` - Frontend base URL for password reset links

## Architecture

### Apps

**`core`** - Settings, URL routing, WSGI/ASGI
- `settings.py` - Django config with JWT, CORS, Celery, logging
- `urls.py` - Main routing: `/api/accounts/`, `/api/resumes/`, `/api/token/`
- `views.py` - Simple health check endpoint

**`accounts`** - Authentication & user management
- Custom `User` model (extends `AbstractUser`)
- `UserSettings` model for user preferences
- Views: Signup, Login, Profile, PasswordReset, ProfilePictureUpload

**`resumes`** - Resume management
- Models: `Resume`, `ResumeTemplate`, `ResumeVersion`, `Education`, `Experience`, `Skill`, `Project`, `CoverLetter`, `JobApplication`, `ResumeAnalytics`
- Service classes: `PDFGenerator` (HTML generation), `AIEnhancer` (OpenAI integration)
- Soft deletes via `is_deleted` flag on all models

### Key Patterns

- **Soft deletes**: Resume-related models use `is_deleted` boolean instead of hard deletes
- **Ordering**: Education, Experience, Project have `order` field for custom排序
- **Versioning**: `ResumeVersion` stores snapshots of resume state
- **Analytics**: `ResumeAnalytics` tracks views, downloads, shares per resume
- **Sharing**: Resumes can be shared publicly via `share_code` UUID

### API Authentication

All resume endpoints require JWT: `Authorization: Bearer <access_token>`

Token flow:
1. `POST /api/accounts/signup/` or `POST /api/token/` → get access/refresh tokens
2. Include access token in Authorization header
3. Refresh with `POST /api/token/refresh/` when expired

### Logging

Structured logging configured in `settings.py`:
- Root logger: INFO to console
- `accounts` logger: DEBUG level
- Use `logger = logging.getLogger('accounts')` in views
