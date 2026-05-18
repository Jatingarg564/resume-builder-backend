# Resume Builder - Complete Documentation

## Project Overview

Resume Builder is a full-stack web application that allows users to create, manage, and share professional resumes. It features a Django REST API backend and a React frontend with real-time editing, multiple templates, and AI-enhanced content suggestions.

---

## Table of Contents

1. [Tech Stack](#tech-stack)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Database Schema](#database-schema)
5. [API Reference](#api-reference)
6. [Authentication Flow](#authentication-flow)
7. [Resume Workflow](#resume-workflow)
8. [Security](#security)
9. [Deployment](#deployment)
10. [Testing](#testing)
11. [Development Setup](#development-setup)

---

## Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 5.2 | Web framework |
| Django REST Framework | 3.x | API framework |
| Django SimpleJWT | 5.x | JWT authentication |
| PostgreSQL | 15+ | Production database |
| SQLite | 3.x | Development database |
| Gunicorn | 21.x | WSGI server |
| WhiteNoise | 6.x | Static file serving |
| Celery | 5.x | Async tasks |
| Redis | 7.x | Caching & message broker |
| OpenAI API | - | AI content enhancement |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.2.4 | UI framework |
| Vite | 8.x | Build tool |
| Tailwind CSS | 4.x | Styling |
| React Router | 7.x | Routing |
| Axios | 1.x | HTTP client |
| html2canvas | 1.x | Canvas generation |
| jsPDF | 2.x | PDF generation |

---

## Architecture

### Project Structure

```
resume_builder_backend/
├── core/                    # Main Django project
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Root URL routing
│   ├── views.py             # Health check endpoint
│   ├── wsgi.py              # WSGI entry point
│   └── asgi.py              # ASGI entry point
├── accounts/                # Authentication app
│   ├── models.py            # User, UserSettings models
│   ├── views.py             # Auth views
│   ├── serializers.py       # User serializers
│   ├── urls.py              # Auth routes
│   └── tests.py             # Auth tests (14 tests)
├── resumes/                 # Resume management app
│   ├── models.py            # Resume, sections, analytics models
│   ├── views.py             # Resume CRUD, sharing, AI views
│   ├── serializers.py       # Resume serializers
│   ├── urls.py              # Resume routes
│   └── tests.py             # Resume tests (51 tests)
├── frontend/                # React frontend
│   ├── src/
│   │   ├── pages/           # Page components
│   │   ├── components/      # Reusable components
│   │   ├── context/         # React context providers
│   │   ├── api/             # API client
│   │   └── test/            # Test setup
│   └── package.json
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
```

### Request Flow

```
User → React Frontend → Axios (with JWT) → Django API → Database
                              ↓
                         Redis Cache (optional)
                              ↓
                         Celery Worker (async tasks)
```

---

## Features

### 1. Authentication System
- **Signup**: Create account with username, email, password
- **Login**: JWT token-based authentication
- **Profile Management**: Update name, email, profile picture
- **User Settings**: Theme preference, notifications, default template
- **Password Reset**: Email-based password recovery
- **Token Refresh**: Automatic token refresh on expiry

### 2. Resume Management
- **Create/Edit**: Multi-step wizard for resume creation
- **Templates**: Classic and Modern templates
- **Sections**:
  - Education (degree, institution, years)
  - Experience (company, role, dates, description)
  - Skills (name/tags)
  - Projects (title, description, tech stack, link)
- **Soft Delete**: Resumes marked as deleted, not removed
- **Versioning**: Create snapshots and restore previous versions

### 3. Cover Letters
- Create multiple cover letters per resume
- Rich text content support
- Link to specific job applications

### 4. Job Application Tracking
- Track applications by company, position, status
- Status workflow: Applied → Interviewing → Offer/Rejected
- Notes and job URL storage
- Application timeline

### 5. Resume Sharing
- Generate public share links (UUID-based)
- Revoke access anytime
- View analytics on shared resumes

### 6. Analytics
- Track views, downloads, shares
- Last viewed timestamp
- Per-resume analytics dashboard

### 7. AI Enhancement (Optional)
- Enhance experience descriptions
- Generate professional summaries
- Requires OpenAI API key

### 8. PDF Export
- Browser-based print-to-PDF
- A4 page sizing
- Preserves styling

---

## Database Schema

### Core Models

#### User (accounts/models.py)
```python
User(AbstractUser):
    - profile_picture: ImageField (nullable)
```

#### UserSettings (accounts/models.py)
```python
UserSettings:
    - user: OneToOne(User)
    - theme_preference: CharField (light/dark/system)
    - email_notifications: BooleanField
    - default_resume_template: CharField (nullable)
    - auto_save: BooleanField
```

#### Resume (resumes/models.py)
```python
Resume:
    - user: ForeignKey(User)
    - title: CharField(100)
    - template: ForeignKey(ResumeTemplate, nullable)
    - share_code: UUIDField (nullable, unique)
    - version: IntegerField (default: 1)
    - is_deleted: BooleanField (default: False)
    - created_at: DateTimeField
```

#### ResumeTemplate (resumes/models.py)
```python
ResumeTemplate:
    - name: CharField(100)
    - template_code: CharField(50, unique)
    - description: TextField
    - is_premium: BooleanField
    - thumbnail_url: URLField
    - is_active: BooleanField
```

#### ResumeVersion (resumes/models.py)
```python
ResumeVersion:
    - resume: ForeignKey(Resume)
    - version_number: IntegerField
    - snapshot_data: JSONField
    - created_at: DateTimeField
```

#### Education (resumes/models.py)
```python
Education:
    - resume: ForeignKey(Resume)
    - degree: CharField(100)
    - institution: CharField(150)
    - start_year: IntegerField
    - end_year: IntegerField (nullable)
    - order: IntegerField (default: 0)
    - is_deleted: BooleanField (default: False)
```

#### Experience (resumes/models.py)
```python
Experience:
    - resume: ForeignKey(Resume)
    - company: CharField(150)
    - role: CharField(100)
    - start_date: DateField
    - end_date: DateField (nullable)
    - description: TextField
    - order: IntegerField (default: 0)
    - is_deleted: BooleanField (default: False)
```

#### Skill (resumes/models.py)
```python
Skill:
    - resume: ForeignKey(Resume)
    - name: CharField(100)
    - is_deleted: BooleanField (default: False)
```

#### Project (resumes/models.py)
```python
Project:
    - resume: ForeignKey(Resume)
    - title: CharField(150)
    - description: TextField
    - tech_stack: CharField(200)
    - project_link: URLField (nullable)
    - order: IntegerField (default: 0)
    - is_deleted: BooleanField (default: False)
```

#### CoverLetter (resumes/models.py)
```python
CoverLetter:
    - resume: ForeignKey(Resume)
    - title: CharField(150)
    - content: TextField
    - created_at: DateTimeField
    - updated_at: DateTimeField
    - is_deleted: BooleanField (default: False)
```

#### JobApplication (resumes/models.py)
```python
JobApplication:
    - resume: ForeignKey(Resume)
    - company: CharField(150)
    - position: CharField(150)
    - applied_date: DateField
    - status: CharField (applied/interviewing/offer/rejected/withdrawn)
    - job_url: URLField (nullable)
    - notes: TextField (nullable)
    - created_at: DateTimeField
    - updated_at: DateTimeField
```

#### ResumeAnalytics (resumes/models.py)
```python
ResumeAnalytics:
    - resume: OneToOne(Resume)
    - views: IntegerField (default: 0)
    - downloads: IntegerField (default: 0)
    - shares: IntegerField (default: 0)
    - last_viewed_at: DateTimeField (nullable)
```

---

## API Reference

### Base URL
```
Development: http://localhost:8000/api
Production: https://resume-builder-backend-td5t.onrender.com/api
```

### Authentication Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/accounts/signup/` | Create new user | No |
| POST | `/accounts/login/` | Login, get tokens | No |
| GET | `/accounts/profile/` | Get user profile | Yes |
| PATCH | `/accounts/profile/` | Update profile | Yes |
| GET | `/accounts/settings/` | Get user settings | Yes |
| PATCH | `/accounts/settings/` | Update settings | Yes |
| POST | `/token/refresh/` | Refresh access token | No |

### Resume Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/resumes/` | List user's resumes | Yes |
| POST | `/resumes/` | Create new resume | Yes |
| GET | `/resumes/{id}/` | Get resume details | Yes |
| PATCH | `/resumes/{id}/` | Update resume | Yes |
| DELETE | `/resumes/{id}/` | Soft delete resume | Yes |
| POST | `/resumes/{id}/share/` | Generate share link | Yes |
| POST | `/resumes/{id}/share/revoke/` | Revoke share link | Yes |
| GET | `/resumes/public/{uuid}/` | Get public resume | No |
| POST | `/resumes/{id}/template/` | Set template | Yes |
| GET | `/resumes/{id}/pdf/` | Generate PDF | Yes |
| GET | `/resumes/templates/` | List templates | No |

### Education Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/resumes/{id}/education/` | Add education | Yes |
| PATCH | `/resumes/education/{id}/` | Update education | Yes |
| DELETE | `/resumes/education/{id}/` | Soft delete | Yes |

### Experience Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/resumes/{id}/experience/` | Add experience | Yes |
| PATCH | `/resumes/experience/{id}/` | Update experience | Yes |
| DELETE | `/resumes/experience/{id}/` | Soft delete | Yes |

### Skill Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/resumes/{id}/skills/` | Add skill | Yes |
| PATCH | `/resumes/skills/{id}/` | Update skill | Yes |
| DELETE | `/resumes/skills/{id}/` | Soft delete | Yes |

### Project Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/resumes/{id}/projects/` | Add project | Yes |
| PATCH | `/resumes/projects/{id}/` | Update project | Yes |
| DELETE | `/resumes/projects/{id}/` | Soft delete | Yes |

### Cover Letter Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/resumes/{id}/cover-letters/` | List cover letters | Yes |
| POST | `/resumes/{id}/cover-letters/` | Create cover letter | Yes |
| GET | `/resumes/cover-letters/{id}/` | Get cover letter | Yes |
| PATCH | `/resumes/cover-letters/{id}/` | Update cover letter | Yes |
| DELETE | `/resumes/cover-letters/{id}/` | Soft delete | Yes |

### Job Application Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/resumes/{id}/jobs/` | List applications | Yes |
| POST | `/resumes/{id}/jobs/` | Create application | Yes |
| GET | `/resumes/jobs/{id}/` | Get application | Yes |
| PATCH | `/resumes/jobs/{id}/` | Update application | Yes |
| DELETE | `/resumes/jobs/{id}/` | Delete application | Yes |

### Versioning Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/resumes/{id}/versions/` | List versions | Yes |
| POST | `/resumes/{id}/versions/create/` | Create version | Yes |
| POST | `/resumes/{id}/versions/{n}/restore/` | Restore version | Yes |

### Analytics Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/resumes/{id}/analytics/` | Get analytics | Yes |
| POST | `/resumes/{id}/analytics/view/` | Increment views | No |

### AI Enhancement Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/resumes/{id}/ai/enhance/` | Enhance description | Yes |
| GET | `/resumes/{id}/ai/summary/` | Generate summary | Yes |

---

## Authentication Flow

### 1. Signup
```javascript
POST /api/accounts/signup/
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}

Response (201):
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

### 2. Login
```javascript
POST /api/accounts/login/
{
  "username": "johndoe",
  "password": "SecurePass123!"
}

Response (200):
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. Token Refresh
```javascript
POST /api/token/refresh/
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Response (200):
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 4. Authenticated Request
```javascript
GET /api/resumes/
Headers:
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Resume Workflow

### Creating a Resume

1. **Step 1: Basic Info**
   - Enter resume title
   - POST `/api/resumes/` → Returns resume ID

2. **Step 2: Education**
   - Add education entries
   - POST `/api/resumes/{id}/education/` for each entry

3. **Step 3: Experience**
   - Add work experience
   - POST `/api/resumes/{id}/experience/` for each entry

4. **Step 4: Skills**
   - Add skills
   - POST `/api/resumes/{id}/skills/` for each skill

5. **Step 5: Projects**
   - Add projects
   - POST `/api/resumes/{id}/projects/` for each project

### Editing a Resume

1. Load existing resume: GET `/api/resumes/{id}/`
2. Modify sections via PATCH requests
3. Auto-save on each change

### Sharing a Resume

1. Generate link: POST `/api/resumes/{id}/share/`
2. Share URL: `https://app.com/share/{uuid}/`
3. Revoke: POST `/api/resumes/{id}/share/revoke/`

### Creating a Version

1. Create snapshot: POST `/api/resumes/{id}/versions/create/`
2. Resume version increments
3. Restore: POST `/api/resumes/{id}/versions/{n}/restore/`

---

## Security

### Authentication
- JWT tokens with configurable expiry (default: 60 min access, 7 days refresh)
- Tokens stored in localStorage on frontend
- Automatic refresh on 401 responses

### Authorization
- All resume endpoints check `user=request.user`
- IDOR protection via ownership verification
- Soft deletes prevent accidental data loss

### Input Validation
- Year ranges: 1900-2100
- Date validation: end_date >= start_date
- Email format validation
- XSS prevention via Django's escaping

### CORS
- Configured allowed origins
- Credentials support for auth cookies

### Known Limitations
- Duplicate emails allowed (username is unique)
- Profile pictures require authentication

---

## Deployment

### Backend (Render)

```yaml
# render.yaml
services:
  - type: web
    name: resume-builder-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn core.wsgi
    envVars:
      - SECRET_KEY
      - DEBUG=False
      - ALLOWED_HOSTS=resume-builder-backend-td5t.onrender.com
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://...
```

### Frontend (Vercel)

```json
// vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "env": {
    "VITE_API_URL": "https://resume-builder-backend-td5t.onrender.com/api"
  }
}
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | - | Django secret key |
| `DEBUG` | Yes | "True" | Debug mode |
| `ALLOWED_HOSTS` | Yes | - | Comma-separated hosts |
| `DATABASE_URL` | No | SQLite | PostgreSQL URL |
| `REDIS_URL` | No | - | Redis for Celery |
| `CELERY_BROKER_URL` | No | - | Celery broker |
| `JWT_ACCESS_LIFETIME_MINUTES` | No | 60 | Access token TTL |
| `JWT_REFRESH_LIFETIME_DAYS` | No | 7 | Refresh token TTL |
| `OPENAI_API_KEY` | No | - | AI features |
| `FRONTEND_URL` | No | - | Password reset links |

---

## Testing

### Backend Tests

```bash
# Run all tests
python manage.py test

# Run specific app
python manage.py test accounts
python manage.py test resumes

# Run specific test class
python manage.py test accounts.tests.SignupTests

# Verbose output
python manage.py test --verbosity=2
```

### Test Coverage

| App | Tests | Coverage |
|-----|-------|----------|
| accounts | 14 | Auth, Profile, Settings |
| resumes | 51 | CRUD, Sharing, Versioning, Analytics |
| **Total** | **65** | **All passing** |

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Watch mode
npm run test:watch

# Coverage report
npm run test:coverage
```

### Postman Collection

Import `postman_collection.json` for API testing:
- 33 pre-configured requests
- Auto-token management
- Test assertions included

---

## Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (optional for dev)

### Backend Setup

```bash
# Clone repository
cd resume_builder_backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit VITE_API_URL

# Run development server
npm run dev
```

### Common Commands

```bash
# Backend
python manage.py migrate          # Apply migrations
python manage.py makemigrations   # Create migrations
python manage.py createsuperuser  # Create admin user
python manage.py shell            # Django shell
python manage.py test             # Run tests

# Frontend
npm run dev        # Start dev server
npm run build      # Production build
npm run preview    # Preview build
npm test           # Run tests
```

---

## Troubleshooting

### Common Issues

**1. CORS Errors**
```
Solution: Add frontend URL to CORS_ALLOWED_ORIGINS in settings.py
```

**2. JWT Token Expired**
```
Solution: Frontend automatically refreshes. Check token refresh endpoint.
```

**3. Database Migration Errors**
```bash
python manage.py migrate --run-syncdb
```

**4. Static Files Not Loading**
```bash
python manage.py collectstatic --noinput
```

**5. Celery Worker Not Starting**
```bash
celery -A core worker --loglevel=info
# Ensure Redis is running
```

---

## API Response Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | GET, PATCH |
| 201 | Created | POST |
| 204 | Deleted | DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Unexpected error |

---

## Version History

### Phase 1: Core Features
- User authentication
- Resume CRUD
- Basic sections (Education, Experience, Skills, Projects)

### Phase 2: Enhanced Features
- Resume templates
- Public sharing
- PDF generation
- Soft deletes

### Phase 3: Advanced Features
- Cover letters
- Job application tracking
- Resume versioning
- Analytics
- AI enhancement

---

## Contributing

1. Create feature branch
2. Make changes
3. Run tests: `python manage.py test`
4. Commit with descriptive message
5. Create pull request

### Code Style
- Backend: PEP 8
- Frontend: ESLint + Prettier
- Commit format: `feat: add feature X` or `fix: resolve issue Y`

---

## License

MIT License - See LICENSE file for details

---

## Support

For issues or questions:
- GitHub Issues: [Repository Issues]
- Email: [Developer Email]
- Documentation: This file
