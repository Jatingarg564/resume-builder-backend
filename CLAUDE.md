# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django REST API backend for a resume builder application. It provides authentication via JWT and APIs for managing resumes with education, experience, skills, and projects.

## Tech Stack

- Django 5.2
- Django REST Framework
- SimpleJWT for authentication
- PostgreSQL (via dj-database-url) / SQLite for development
- Gunicorn for production
- Celery for async tasks

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

# Run tests
python manage.py test
```

## Environment Variables

Required environment variables (add to `.env` file):
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to "True" for development
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DATABASE_URL` - PostgreSQL connection string (optional, defaults to SQLite)

## Architecture

### Django Apps

- **`core`** - Project settings and URL configuration
  - `settings.py` - Django settings with JWT, database, and environment config
  - `urls.py` - Main URL routing

- **`accounts`** - User authentication
  - Custom `User` model extending `AbstractUser`
  - Views: Signup, Login, Profile
  - All endpoints under `/api/accounts/`

- **`resumes`** - Resume management
  - Models: `Resume`, `Education`, `Experience`, `Skill`, `Project`
  - All endpoints under `/api/resumes/`

### API Endpoints

**Authentication:**
- `POST /api/accounts/signup/` - User registration
- `POST /api/accounts/login/` - User login
- `GET /api/accounts/profile/` - Get user profile (requires auth)
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

**Resumes:**
- `GET /api/resumes/` - List user's resumes
- `POST /api/resumes/` - Create a new resume
- `GET /api/resumes/<id>/` - Get resume details
- `POST /api/resumes/<id>/education/` - Add education
- `PATCH/DELETE /api/resumes/education/<id>/` - Update/delete education
- `POST /api/resumes/<id>/experience/` - Add experience
- `PATCH/DELETE /api/resumes/experience/<id>/` - Update/delete experience
- `POST /api/resumes/<id>/skills/` - Add skill
- `DELETE /api/resumes/skills/<id>/` - Delete skill
- `POST /api/resumes/<id>/projects/` - Add project

All resume operations require JWT authentication (`Authorization: Bearer <token>`).