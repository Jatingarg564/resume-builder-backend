# Resume Builder

A modern, full-stack resume building application with AI-powered content enhancement, job application tracking, and professional templates.

![Status](https://img.shields.io/badge/status-stable-success)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![React](https://img.shields.io/badge/react-19.2.4-61dafb)
![Tests](https://img.shields.io/badge/tests-65%20passing-green)

**Live Demo:** [Frontend](https://your-frontend.vercel.app) | [Backend API](https://resume-builder-backend-td5t.onrender.com/api)

---

## ✨ Features

### 📝 Resume Building
- **Multi-step wizard** for easy resume creation
- **Professional templates** (Classic & Modern)
- **Real-time editing** with auto-save
- **PDF export** with browser print integration
- **Version control** - create snapshots and restore previous versions

### 📊 Sections
- **Education** - Degree, institution, years
- **Experience** - Company, role, dates, descriptions
- **Skills** - Tag-based skill listing
- **Projects** - Title, description, tech stack, links

### 🎯 Job Tracking
- Track applications by company and position
- Status workflow: Applied → Interviewing → Offer/Rejected
- Add notes and job URLs
- Application timeline view

### 📄 Cover Letters
- Create multiple cover letters per resume
- Rich text content support
- Link to specific job applications

### 🔗 Sharing & Analytics
- Generate public share links
- Revoke access anytime
- Track views, downloads, and shares
- Per-resume analytics dashboard

### 🤖 AI Enhancement
- Enhance experience descriptions with OpenAI
- Generate professional summaries
- Improve bullet points for impact

### 🔐 Security
- JWT authentication with auto-refresh
- IDOR protection on all resources
- Soft deletes to prevent data loss
- Input validation and XSS prevention

---

## 🛠️ Tech Stack

| Backend | Frontend |
|---------|----------|
| Django 5.2 | React 19.2.4 |
| Django REST Framework | Vite 8 |
| SimpleJWT (Authentication) | Tailwind CSS 4 |
| PostgreSQL / SQLite | React Router 7 |
| Celery + Redis | Axios |
| Gunicorn + WhiteNoise | html2canvas + jsPDF |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (optional for development)

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/Jatingarg564/resume-builder-backend.git
cd resume-builder-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (see .env.example)
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Backend runs at `http://localhost:8000/api`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## 📚 Documentation

- [Complete Documentation](DOCUMENTATION.md) - Full API reference, database schema, architecture
- [API Tests](postman_collection.json) - Import into Postman for testing

### Key Documentation Sections
- [API Reference](DOCUMENTATION.md#api-reference) - All 40+ endpoints
- [Database Schema](DOCUMENTATION.md#database-schema) - 12 models explained
- [Authentication Flow](DOCUMENTATION.md#authentication-flow) - JWT token flow
- [Deployment Guide](DOCUMENTATION.md#deployment) - Render + Vercel setup

---

## 🧪 Testing

### Backend Tests (65 passing)

```bash
# Run all tests
python manage.py test

# Run specific app
python manage.py test accounts
python manage.py test resumes

# Verbose output
python manage.py test --verbosity=2
```

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

---

## 📦 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/accounts/signup/` | Create user |
| POST | `/api/accounts/login/` | Get JWT tokens |
| GET | `/api/accounts/profile/` | Get profile |
| PATCH | `/api/accounts/profile/` | Update profile |

### Resumes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/resumes/` | List resumes |
| POST | `/api/resumes/` | Create resume |
| GET | `/api/resumes/{id}/` | Get resume |
| PATCH | `/api/resumes/{id}/` | Update resume |
| DELETE | `/api/resumes/{id}/` | Soft delete |
| POST | `/api/resumes/{id}/share/` | Generate share link |
| GET | `/api/resumes/public/{uuid}/` | Public access |

### Sections (Education, Experience, Skills, Projects)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/resumes/{id}/{section}/` | Add item |
| PATCH | `/api/resumes/{section}/{id}/` | Update item |
| DELETE | `/api/resumes/{section}/{id}/` | Delete item |

[View all endpoints →](DOCUMENTATION.md#api-reference)

---

## 🏗️ Project Structure

```
resume-builder-backend/
├── core/                 # Django project settings
├── accounts/             # Authentication & user management
├── resumes/              # Resume CRUD & features
├── frontend/             # React application
│   ├── src/
│   │   ├── pages/        # Page components
│   │   ├── components/   # Reusable UI components
│   │   ├── context/      # React context providers
│   │   └── api/          # API client
│   └── package.json
├── DOCUMENTATION.md      # Full documentation
├── requirements.txt      # Python dependencies
└── manage.py             # Django management
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | - |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost` |
| `DATABASE_URL` | Database URL | SQLite |
| `VITE_API_URL` | Backend API URL | Render URL |

---

## 🌐 Deployment

### Backend (Render)
1. Connect GitHub repository
2. Set environment variables
3. Deploy with auto-deploy on push

### Frontend (Vercel)
1. Import project to Vercel
2. Set `VITE_API_URL` environment variable
3. Deploy

[Detailed deployment guide →](DOCUMENTATION.md#deployment)

---

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Run tests before submitting PR
- Write descriptive commit messages
- Add tests for new features

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Django REST Framework for the amazing API framework
- React team for the UI library
- OpenAI for AI enhancement capabilities
- All contributors who made this project possible

---

## 📞 Support

- **Documentation:** [DOCUMENTATION.md](DOCUMENTATION.md)
- **Issues:** [GitHub Issues](https://github.com/Jatingarg564/resume-builder-backend/issues)
- **API Status:** https://resume-builder-backend-td5t.onrender.com/api/health/

---

## 🎯 Roadmap

- [ ] Additional resume templates
- [ ] Resume scoring with AI
- [ ] Job board integration
- [ ] Email notifications for application updates
- [ ] Custom CSS themes
- [ ] Export to Word format

---

**Made with ❤️ by [Jatingarg564](https://github.com/Jatingarg564)**
