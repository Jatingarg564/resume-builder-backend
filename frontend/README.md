# Resume Builder Frontend

A modern React frontend for a resume builder application with Django REST API backend.

## Features

- **Authentication**: JWT-based login/signup with automatic token refresh
- **Dashboard**: View and manage your resumes
- **Resume Builder**: Multi-step form to create resumes with:
  - Basic Info
  - Education
  - Experience
  - Skills
  - Projects
- **Templates**: Browse and select from professional resume templates
- **Pricing**: View subscription plans (Free, Pro, Premium)
- **Profile**: Manage your account settings

## Tech Stack

- **React 18** with Vite
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Axios** for API calls with interceptors
- **Context API** for state management

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Django backend running at `http://127.0.0.1:8000`

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Production Build

```bash
npm run build
```

Output will be in the `dist/` folder.

## API Integration

The frontend integrates with these backend endpoints:

**Authentication:**
- `POST /api/accounts/signup/` - User registration
- `POST /api/accounts/login/` - User login
- `GET /api/accounts/profile/` - Get user profile
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

**Resumes:**
- `GET /api/resumes/` - List user's resumes
- `POST /api/resumes/` - Create resume
- `GET /api/resumes/{id}/` - Get resume details
- `POST /api/resumes/{id}/education/` - Add education
- `PATCH/DELETE /api/resumes/education/{id}/` - Update/delete education
- `POST /api/resumes/{id}/experience/` - Add experience
- `PATCH/DELETE /api/resumes/experience/{id}/` - Update/delete experience
- `POST /api/resumes/{id}/skills/` - Add skills
- `DELETE /api/resumes/skills/{id}/` - Delete skill
- `POST /api/resumes/{id}/projects/` - Add project
- `GET /api/resumes/templates/` - List templates

## Environment Variables

Create a `.env` file in the frontend directory:

```
VITE_API_URL=http://127.0.0.1:8000/api
```

## Project Structure

```
src/
├── api/           # API service layer
├── components/    # Reusable UI components
├── context/       # React context (Auth, Resume state)
├── pages/         # Page components
└── App.jsx        # Main app with routing
```

## Backend Requirements

The frontend expects the Django backend to be running with CORS enabled. Install `django-cors-headers` on the backend:

```bash
pip install django-cors-headers
```

Add to `core/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

## License

MIT