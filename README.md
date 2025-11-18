# PhD Application Automation System 🎓

A comprehensive AI-powered full-stack application for discovering global PhD opportunities and automating personalized email outreach to professors.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)

## 🌟 Overview

The PhD Application Automation System streamlines the PhD application process by discovering universities worldwide, finding professors, matching research interests with AI, and generating personalized emails automatically.

**Capabilities:**
- 🌍 Discover universities from 50+ countries
- 👨‍🏫 Find professors with research interests
- 🤖 AI-powered matching with Google Gemini
- ✉️ Generate personalized emails (10,000+ emails/day)
- 📊 Track applications and analyze success rates

## 🚀 Quick Start

### One-Command Setup
```bash
./scripts/setup.sh
```

### One-Command Start
```bash
./scripts/start.sh
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- npm

## 🛠️ Tech Stack

**Backend:** Flask, SQLAlchemy, Google Gemini AI, BeautifulSoup4, Celery
**Frontend:** React 18, Vite, Tailwind CSS, Framer Motion
**Database:** SQLite (dev) / PostgreSQL (prod)

## ⚙️ Configuration

Edit `backend/.env`:

```env
GEMINI_API_KEY=your-gemini-api-key
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

Get Gemini API key: https://makersuite.google.com/app/apikey

## 📁 Project Structure

```
├── backend/          # Flask API
│   ├── models/       # Database models
│   ├── routes/       # API endpoints
│   ├── services/     # Business logic
│   ├── tasks/        # Celery tasks
│   ├── cli/          # CLI commands
│   └── tests/        # Tests
├── frontend/         # React app
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── services/
└── scripts/          # Setup/start scripts
```

## 🔌 API Endpoints

- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `GET /api/universities/search` - Search universities
- `POST /api/universities/discover` - Scrape universities
- `GET /api/professors/search` - Search professors
- `POST /api/emails/generate` - Generate emails
- `POST /api/emails/batches/{id}/send` - Send batch
- `GET /api/analytics/dashboard` - Get analytics

## 💻 CLI Usage

```bash
cd backend && source venv/bin/activate

# Database
python cli/main.py db init
python cli/main.py db backup

# Scraping
python cli/main.py scrape universities --country USA --limit 50
python cli/main.py scrape professors --university "MIT" --limit 50

# Status
python cli/main.py status
```

## 🧪 Testing

```bash
./scripts/test.sh
```

Or manually:
```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

## 📖 Features

### Dashboard
- Overview statistics
- Application status
- Quick actions

### Universities
- Search by country/research area
- Filter by scholarships
- Discover new programs

### Professors
- Search by university/department
- AI match scores (0-100%)
- Bulk selection

### Email Management
- AI-generated personalized emails
- Batch review and editing
- Approve and send
- Track delivery status

### Applications
- Track all applications
- Update status
- View responses

### Analytics
- Response rates
- Timeline charts
- Success metrics

## 🚢 Deployment

**Backend:** Render.com, Railway
**Frontend:** Vercel, Netlify
**Database:** ElephantSQL (PostgreSQL)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push and open PR

## 📝 License

MIT License

## 🙏 Acknowledgments

- Google Gemini AI
- Open source community

---

**Built for aspiring PhD students worldwide** 🎓✨

For support: Open an issue on GitHub
