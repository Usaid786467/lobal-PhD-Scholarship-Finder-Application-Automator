# 🌍 Global PhD Scholarship Finder & Application Automator

An advanced AI-powered platform that discovers PhD opportunities worldwide, matches them with your research profile, and automates personalized outreach to professors with intelligent batch approval system.

## 🎯 Project Vision

This system revolutionizes PhD applications by:
- Discovering opportunities across 50+ countries
- Intelligent matching with your research interests
- Automated professor profile analysis
- Batch email management with approval workflow
- Complete application tracking
- Professional CV attachment system
- Multi-language support for international applications

## ✨ Key Features

### 🔍 1. Global University Discovery
- **195+ Countries Covered**: USA, UK, Canada, Australia, New Zealand, Germany, France, Netherlands, Switzerland, Sweden, Norway, Denmark, China (.cn domains), Hong Kong, Singapore, Japan, South Korea, Taiwan, Vietnam, Thailand, Malaysia, UAE, Saudi Arabia, Qatar, Turkey, Israel, and more
- **Scholarship-First Approach**: Prioritizes funded positions
- **No Ranking Bias**: Includes universities of all rankings
- **Real-time Web Scraping**: Live data from university websites
- **Department-Level Search**: Specific to Mechanical Engineering & Aerospace
- **Research Lab Discovery**: Finds specific research groups

### 🎓 2. Intelligent Matching Engine
- **Research Area Matching**: Deep Learning, ML in Manufacturing, Aerospace
- **Funding Availability**: Scholarship/Stipend detection
- **Application Deadline Tracking**: Automatic date extraction
- **Professor Specialization**: Matches with your research interests
- **Publication Analysis**: Checks professor's recent papers
- **Lab Capacity**: Determines if accepting students

### 👨‍🏫 3. Professor Profile Analyzer
- **Automated Profile Scraping**: Google Scholar, ResearchGate, University pages
- **Research Interest Extraction**: NLP-based analysis
- **Recent Publications**: Last 2 years focus
- **Student Availability**: Current openings detection
- **Contact Information**: Email extraction
- **H-index & Citations**: Academic impact metrics

### 📧 4. Smart Email System
- **Dynamic Template Generation**: Personalized per professor
- **Research Alignment**: Mentions specific shared interests
- **CV Auto-Attachment**: PDF format
- **Batch Approval Workflow**: Review before sending
- **Smart Scheduling**: Optimal sending times
- **Daily Quota Management**: 10,000+ emails/day capability
- **Bounce Detection**: Invalid email filtering
- **Follow-up Automation**: Smart reminder system

### 🖥️ 5. Professional Frontend (React)
- **Beautiful Dashboard**: Statistics & insights
- **University Explorer**: Interactive search & filters
- **Professor Database**: Detailed profiles with match scores
- **Email Management**: Draft, review, approve, send
- **Application Tracker**: Status monitoring
- **Calendar Integration**: Deadline management
- **Analytics Dashboard**: Success rate tracking
- **Document Manager**: CV versions & cover letters

### 🔧 6. Backend Control System
- **Python CLI Interface**: Terminal-based control
- **Database Management**: Easy backups & exports
- **API Rate Limiting**: Prevents blocking
- **Error Recovery**: Automatic retry mechanisms
- **Logging System**: Detailed activity logs
- **Configuration Manager**: Easy settings adjustment

## 🛠️ Technology Stack

### Backend
- **Framework**: Python 3.9+ with Flask/FastAPI
- **Database**: SQLite (development) / PostgreSQL (production) - 100% FREE
- **AI/ML**: 
  - Google Gemini AI (Free tier: 60 requests/minute)
  - HuggingFace Transformers (NLP)
  - spaCy (Text processing)
- **Web Scraping**:
  - BeautifulSoup4
  - Selenium (headless Chrome)
  - Scrapy (large-scale crawling)
  - Playwright (JavaScript-heavy sites)
- **Email**:
  - SMTP (Gmail/Outlook free tier)
  - Mailgun (Free: 5,000 emails/month)
  - SendGrid (Free: 100 emails/day)
- **Task Queue**: Celery + Redis (async processing)
- **Testing**: pytest, unittest, coverage

### Frontend
- **Framework**: React 18+ with Hooks
- **Styling**: 
  - TailwindCSS 3.4+
  - HeadlessUI (accessible components)
  - Heroicons
- **UI Libraries**:
  - Framer Motion (animations)
  - React Table (data grids)
  - Recharts (visualizations)
  - React-PDF (CV preview)
- **State Management**: 
  - React Context API
  - React Query (server state)
- **Routing**: React Router v6
- **Forms**: React Hook Form + Zod validation
- **Notifications**: React-Toastify

### DevOps & Tools
- **Version Control**: Git
- **CI/CD**: GitHub Actions (free)
- **Deployment**: 
  - Backend: Render.com (free tier)
  - Frontend: Vercel/Netlify (free)
  - Database: ElephantSQL (free PostgreSQL)
- **Monitoring**: 
  - Sentry (error tracking - free)
  - LogTail (log management - free)

## 📁 Project Structure
```
phd-application-automator/
│
├── backend/
│   ├── app.py                          # Main Flask/FastAPI application
│   ├── config.py                       # Configuration management
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Environment variables template
│   │
│   ├── models/                         # Database models
│   │   ├── __init__.py
│   │   ├── user.py                     # User authentication
│   │   ├── university.py               # University data
│   │   ├── professor.py                # Professor profiles
│   │   ├── application.py              # Application tracking
│   │   └── email.py                    # Email records
│   │
│   ├── routes/                         # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py                     # Authentication routes
│   │   ├── universities.py             # University search
│   │   ├── professors.py               # Professor management
│   │   ├── applications.py             # Application tracking
│   │   ├── emails.py                   # Email management
│   │   └── analytics.py                # Dashboard analytics
│   │
│   ├── services/                       # Business logic
│   │   ├── __init__.py
│   │   ├── scraper/
│   │   │   ├── __init__.py
│   │   │   ├── base_scraper.py         # Base scraper class
│   │   │   ├── university_scraper.py   # University website scraper
│   │   │   ├── professor_scraper.py    # Professor profile scraper
│   │   │   ├── scholarship_scraper.py  # Scholarship page scraper
│   │   │   └── china_scraper.py        # Special .cn domain handler
│   │   │
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── gemini_service.py       # Google Gemini AI
│   │   │   ├── matching_engine.py      # Research matching
│   │   │   ├── email_generator.py      # Email template generation
│   │   │   └── nlp_processor.py        # Text analysis
│   │   │
│   │   ├── email/
│   │   │   ├── __init__.py
│   │   │   ├── smtp_service.py         # Email sending
│   │   │   ├── template_engine.py      # Email templates
│   │   │   ├── batch_manager.py        # Batch processing
│   │   │   └── scheduler.py            # Sending scheduler
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── validators.py           # Input validation
│   │       ├── helpers.py              # Helper functions
│   │       └── logger.py               # Logging configuration
│   │
│   ├── tasks/                          # Celery async tasks
│   │   ├── __init__.py
│   │   ├── scraping_tasks.py
│   │   ├── email_tasks.py
│   │   └── analysis_tasks.py
│   │
│   ├── tests/                          # Test files
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_scraper.py
│   │   ├── test_email.py
│   │   └── test_matching.py
│   │
│   ├── cli/                            # Command-line interface
│   │   ├── __init__.py
│   │   ├── main.py                     # CLI entry point
│   │   ├── commands/
│   │   │   ├── scrape.py               # Scraping commands
│   │   │   ├── email.py                # Email commands
│   │   │   └── db.py                   # Database commands
│   │   └── utils.py
│   │
│   ├── migrations/                     # Database migrations
│   │   └── versions/
│   │
│   └── data/                           # Data files
│       ├── universities.json           # University list
│       ├── countries.json              # Country data
│       └── research_areas.json         # Research taxonomy
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── assets/
│   │
│   ├── src/
│   │   ├── App.js                      # Main app component
│   │   ├── index.js                    # Entry point
│   │   ├── index.css                   # Global styles
│   │   │
│   │   ├── components/                 # React components
│   │   │   ├── Layout/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   ├── Footer.jsx
│   │   │   │   └── Layout.jsx
│   │   │   │
│   │   │   ├── Auth/
│   │   │   │   ├── LoginForm.jsx
│   │   │   │   ├── RegisterForm.jsx
│   │   │   │   └── ProfileSetup.jsx
│   │   │   │
│   │   │   ├── Dashboard/
│   │   │   │   ├── StatsCards.jsx
│   │   │   │   ├── RecentActivity.jsx
│   │   │   │   ├── UpcomingDeadlines.jsx
│   │   │   │   └── QuickActions.jsx
│   │   │   │
│   │   │   ├── Universities/
│   │   │   │   ├── UniversityList.jsx
│   │   │   │   ├── UniversityCard.jsx
│   │   │   │   ├── UniversityDetail.jsx
│   │   │   │   └── SearchFilters.jsx
│   │   │   │
│   │   │   ├── Professors/
│   │   │   │   ├── ProfessorList.jsx
│   │   │   │   ├── ProfessorCard.jsx
│   │   │   │   ├── ProfessorDetail.jsx
│   │   │   │   └── MatchScore.jsx
│   │   │   │
│   │   │   ├── Emails/
│   │   │   │   ├── EmailDashboard.jsx
│   │   │   │   ├── EmailEditor.jsx
│   │   │   │   ├── EmailPreview.jsx
│   │   │   │   ├── BatchApproval.jsx
│   │   │   │   └── EmailHistory.jsx
│   │   │   │
│   │   │   ├── Applications/
│   │   │   │   ├── ApplicationList.jsx
│   │   │   │   ├── ApplicationCard.jsx
│   │   │   │   ├── StatusTracker.jsx
│   │   │   │   └── Timeline.jsx
│   │   │   │
│   │   │   ├── Analytics/
│   │   │   │   ├── AnalyticsDashboard.jsx
│   │   │   │   ├── Charts.jsx
│   │   │   │   ├── SuccessRate.jsx
│   │   │   │   └── Insights.jsx
│   │   │   │
│   │   │   ├── Documents/
│   │   │   │   ├── CVManager.jsx
│   │   │   │   ├── CVUpload.jsx
│   │   │   │   └── CVPreview.jsx
│   │   │   │
│   │   │   └── Common/
│   │   │       ├── Button.jsx
│   │   │       ├── Input.jsx
│   │   │       ├── Modal.jsx
│   │   │       ├── Loader.jsx
│   │   │       ├── Toast.jsx
│   │   │       └── Card.jsx
│   │   │
│   │   ├── pages/                      # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── UniversitySearch.jsx
│   │   │   ├── ProfessorSearch.jsx
│   │   │   ├── EmailManagement.jsx
│   │   │   ├── Applications.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── Settings.jsx
│   │   │   └── Profile.jsx
│   │   │
│   │   ├── hooks/                      # Custom React hooks
│   │   │   ├── useAuth.js
│   │   │   ├── useUniversities.js
│   │   │   ├── useProfessors.js
│   │   │   ├── useEmails.js
│   │   │   └── useAnalytics.js
│   │   │
│   │   ├── context/                    # React Context
│   │   │   ├── AuthContext.jsx
│   │   │   ├── ThemeContext.jsx
│   │   │   └── AppContext.jsx
│   │   │
│   │   ├── services/                   # API services
│   │   │   ├── api.js                  # Axios configuration
│   │   │   ├── authService.js
│   │   │   ├── universityService.js
│   │   │   ├── professorService.js
│   │   │   ├── emailService.js
│   │   │   └── analyticsService.js
│   │   │
│   │   ├── utils/                      # Utility functions
│   │   │   ├── constants.js
│   │   │   ├── formatters.js
│   │   │   ├── validators.js
│   │   │   └── helpers.js
│   │   │
│   │   └── styles/                     # Style files
│   │       └── custom.css
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── .env.example
│
├── docs/                               # Documentation
│   ├── API.md                          # API documentation
│   ├── SETUP.md                        # Setup guide
│   ├── DEPLOYMENT.md                   # Deployment guide
│   ├── CLI.md                          # CLI documentation
│   └── ARCHITECTURE.md                 # Architecture overview
│
├── scripts/                            # Utility scripts
│   ├── setup.sh                        # One-command setup
│   ├── start.sh                        # One-command start
│   ├── deploy.sh                       # Deployment script
│   └── test.sh                         # Run all tests
│
├── .gitignore
├── README.md
├── LICENSE
└── docker-compose.yml                  # Optional Docker setup
```

## 🚀 One-Command Setup & Run

### First Time Setup (Run Once):
```bash
# Clone and setup everything
./scripts/setup.sh
```

### Daily Usage (Every Time):
```bash
# Start both backend and frontend
./scripts/start.sh
```

That's it! Open http://localhost:3000 in your browser.

## 📖 Detailed Installation (Manual)

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git
- Chrome/Chromium (for web scraping)

### Step 1: Clone Repository
```bash
git clone <your-repo-url>
cd phd-application-automator
```

### Step 2: Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your details

# Initialize database
python cli/main.py db init
python cli/main.py db migrate

# Run tests
pytest tests/ -v

# Start backend server
python app.py
# Backend runs on http://localhost:5000
```

### Step 3: Frontend Setup (New Terminal)
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env.local
# Edit .env.local

# Start development server
npm start
# Frontend runs on http://localhost:3000
```

### Step 4: Start Background Workers (New Terminal)
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start Celery worker
celery -A tasks.celery worker --loglevel=info

# Start Celery beat (scheduler)
celery -A tasks.celery beat --loglevel=info
```

## 🎯 Configuration

### Backend Environment Variables (.env)
```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-here
DEBUG=True

# Database
DATABASE_URL=sqlite:///phd_applications.db
# For production: postgresql://user:password@localhost/dbname

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key-here

# Email Configuration (Gmail Example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=True
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
EMAIL_FROM=your-email@gmail.com

# Alternative: SendGrid
SENDGRID_API_KEY=your-sendgrid-key

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# Web Scraping
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
SCRAPING_DELAY=2  # seconds between requests
MAX_RETRIES=3

# Email Limits
DAILY_EMAIL_LIMIT=10000
HOURLY_EMAIL_LIMIT=500
BATCH_SIZE=50

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Frontend Environment Variables (.env.local)
```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_VERSION=1.0.0
REACT_APP_ENVIRONMENT=development
```

## 💻 CLI Usage

The backend includes a powerful CLI for terminal-based control:

### Database Management
```bash
# Initialize database
python cli/main.py db init

# Create migrations
python cli/main.py db migrate "description"

# Apply migrations
python cli/main.py db upgrade

# Backup database
python cli/main.py db backup

# Export data
python cli/main.py db export --format csv
```

### University Scraping
```bash
# Scrape all countries
python cli/main.py scrape universities --all

# Scrape specific country
python cli/main.py scrape universities --country USA

# Scrape multiple countries
python cli/main.py scrape universities --countries USA,UK,Canada,China

# Scrape with filters
python cli/main.py scrape universities --country China --domain .cn --field aerospace

# Resume failed scraping
python cli/main.py scrape resume
```

### Professor Discovery
```bash
# Find professors in specific university
python cli/main.py scrape professors --university "MIT"

# Find by research area
python cli/main.py scrape professors --research "deep learning manufacturing"

# Bulk professor discovery
python cli/main.py scrape professors --batch universities.csv
```

### Email Management
```bash
# Generate email drafts
python cli/main.py email generate --count 100

# Preview emails
python cli/main.py email preview --id 123

# Send test email
python cli/main.py email test --to your-email@gmail.com

# Approve batch
python cli/main.py email approve --batch-id 456

# Send approved emails
python cli/main.py email send --batch-id 456

# Check status
python cli/main.py email status

# View statistics
python cli/main.py email stats
```

### Analytics
```bash
# View dashboard stats
python cli/main.py analytics dashboard

# Generate report
python cli/main.py analytics report --period week

# Export analytics
python cli/main.py analytics export --format pdf
```

## 🌟 Usage Guide

### 1. Initial Setup
1. Register account at http://localhost:3000/register
2. Complete profile with your research interests
3. Upload your CV (PDF format)
4. Set preferences (countries, research areas, scholarship requirements)

### 2. Discover Opportunities
1. Navigate to "University Search"
2. Set filters:
   - Countries (select multiple)
   - Research areas (Deep Learning, ML, Aerospace, Manufacturing)
   - Scholarship availability
   - Application deadlines
3. Click "Start Search"
4. AI will discover universities and rank them by match score

### 3. Find Professors
1. Select interesting universities
2. Click "Find Professors"
3. AI analyzes:
   - Research interests
   - Recent publications
   - Student availability
   - Contact information
4. Review match scores and profiles

### 4. Generate Emails
1. Select professors (multiple selection)
2. Click "Generate Emails"
3. AI creates personalized emails:
   - Custom introduction
   - Research alignment
   - Your relevant experience
   - CV attachment
4. Review generated emails

### 5. Batch Approval Workflow
1. Navigate to "Email Management"
2. Review drafts in batches (50 emails per batch)
3. Edit if needed
4. Approve batch
5. Set sending schedule
6. Monitor sending progress

### 6. Track Applications
1. View "Applications" dashboard
2. Track status: Sent, Delivered, Opened, Replied
3. Set reminders for follow-ups
4. Update status manually
5. Add notes and feedback

### 7. Analytics
1. View success rates
2. Best performing universities
3. Response time analysis
4. Scholarship opportunities found
5. Geographic distribution

## 🎨 Frontend Features

### Beautiful Design
- **Modern UI**: Clean, professional interface
- **Glassmorphism**: Elegant glass-like effects
- **Smooth Animations**: Framer Motion powered
- **Responsive**: Perfect on all devices
- **Dark Mode**: Easy on the eyes
- **Professional Typography**: Inter & SF Pro fonts

### Key Pages

#### Dashboard
- Statistics cards (Opportunities, Applications, Responses, Success Rate)
- Recent activity feed
- Upcoming deadlines calendar
- Quick action buttons
- Interactive charts

#### University Search
- Advanced filters sidebar
- Grid/List view toggle
- Match score badges
- Quick preview cards
- Infinite scroll
- Export functionality

#### Professor Database
- Detailed profiles
- Research interest tags
- Publication list
- Match percentage
- Contact status
- Quick email button

#### Email Management
- Draft queue
- Batch approval interface
- Email preview
- Template editor
- Sending scheduler
- History log

#### Applications Tracker
- Kanban board view
- Status filters
- Timeline view
- Notes system
- Document attachments
- Follow-up reminders

#### Analytics Dashboard
- Success rate funnel
- Geographic heatmap
- Time-series charts
- Best performing metrics
- Export reports

## 🔐 Security Features

- **Authentication**: JWT-based with refresh tokens
- **Password Security**: Bcrypt hashing
- **Rate Limiting**: Prevents abuse
- **Input Validation**: Comprehensive sanitization
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Escaped outputs
- **CORS**: Configured properly
- **HTTPS**: Enforced in production
- **Data Encryption**: Sensitive data encrypted
- **Session Management**: Secure cookie handling

## 🧪 Testing

### Backend Tests
```bash
cd backend

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_scraper.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run integration tests
pytest tests/integration/ -v
```

### Frontend Tests
```bash
cd frontend

# Run unit tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- Component.test.js
```

## 📊 Database Schema

### Users Table
- id, email, password_hash, name, created_at
- research_interests (JSON)
- target_countries (JSON)
- preferences (JSON)

### Universities Table
- id, name, country, website, ranking, created_at
- has_scholarship, application_deadline
- research_areas (JSON)
- contact_info (JSON)

### Professors Table
- id, university_id, name, email, department
- research_interests (JSON)
- publications (JSON)
- accepting_students, h_index

### Applications Table
- id, user_id, professor_id, university_id
- status, applied_date, last_updated
- email_sent, email_opened, responded
- notes, documents (JSON)

### Emails Table
- id, application_id, subject, body
- sent_at, opened_at, replied_at
- batch_id, status

### Analytics Table
- id, user_id, metric_name, value
- date, metadata (JSON)

## 🚀 Deployment

### Backend Deployment (Render.com - FREE)

1. **Prepare for Deployment**
```bash
# Create Procfile
web: gunicorn app:app

# Update requirements.txt
pip freeze > requirements.txt
```

2. **Deploy to Render**
- Push code to GitHub
- Connect repository to Render
- Select "Web Service"
- Set environment variables
- Deploy!

**Render.com Free Tier:**
- 750 hours/month
- Automatic HTTPS
- Custom domains
- Sleep after 15min inactivity

### Frontend Deployment (Vercel - FREE)

1. **Build for Production**
```bash
cd frontend
npm run build
```

2. **Deploy to Vercel**
- Install Vercel CLI: `npm i -g vercel`
- Run: `vercel`
- Follow prompts
- Done!

**Vercel Free Tier:**
- Unlimited deployments
- Automatic HTTPS
- CDN included
- Custom domains

### Database (ElephantSQL - FREE)

- Free PostgreSQL hosting
- 20MB storage
- 5 concurrent connections
- Perfect for development

### Update Environment Variables

**Backend (.env for production):**
```env
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@hostname/dbname
FRONTEND_URL=https://your-app.vercel.app
```

**Frontend (.env.production):**
```env
REACT_APP_API_URL=https://your-backend.onrender.com
```

## 🐛 Troubleshooting

### Common Issues

**1. Database Connection Error**
```bash
# Check if database file exists
ls backend/phd_applications.db

# Reinitialize if needed
cd backend
python cli/main.py db init
```

**2. Port Already in Use**
```bash
# Kill process on port 5000
# Linux/Mac:
lsof -ti:5000 | xargs kill -9

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**3. Scraping Blocked**
- Check your USER_AGENT in .env
- Increase SCRAPING_DELAY
- Use VPN if needed
- Check robots.txt compliance

**4. Email Not Sending**
- Verify SMTP credentials
- Enable "Less secure app access" (Gmail)
- Check daily limits
- Review logs: `tail -f backend/logs/app.log`

**5. Frontend Not Loading**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

## 📚 Advanced Features

### 1. Multi-Language Email Support
- Detects professor's country
- Generates emails in native language
- Professional translations
- Cultural customization

### 2. Intelligent Follow-up System
- Tracks non-responses
- Sends polite follow-ups
- Optimal timing (2 weeks)
- Limited to 2 follow-ups

### 3. Professor Publication Analyzer
- Scrapes Google Scholar
- Identifies recent work
- Matches with your interests
- Suggests collaboration points

### 4. Deadline Reminder System
- Email notifications
- Dashboard alerts
- Calendar integration
- Auto-priority sorting

### 5. Success Prediction ML Model
- Analyzes historical data
- Predicts response probability
- Recommends best professors
- Optimizes application strategy

### 6. Collaborative Features
- Share discovered opportunities
- Team application tracking
- Shared email templates
- Group analytics

## 🔄 Regular Maintenance

### Daily Tasks
```bash
# Check system status
python cli/main.py status

# View today's emails sent
python cli/main.py email stats --today

# Backup database
python cli/main.py db backup
```

### Weekly Tasks
```bash
# Update university database
python cli/main.py scrape universities --update

# Clean old logs
python cli/main.py logs clean --days 7

# Generate weekly report
python cli/main.py analytics report --period week
```

### Monthly Tasks
```bash
# Full database backup
python cli/main.py db backup --full

# Archive old applications
python cli/main.py applications archive --months 6

# Update research area taxonomy
python cli/main.py research update
```

## 🤝 Contributing

This is a personal project, but suggestions welcome!

1. Fork the repository
2. Create feature branch
3. Make changes
4. Write tests
5. Submit pull request

## 📄 License

MIT License - Feel free to modify and use!

## 👨‍💻 Author

**Your Name**
- Master's Student in Mechanical Engineering
- Research: Deep Learning & ML in Aerospace Manufacturing
- Specialization: Model Training, Manufacturing Optimization

## 🙏 Acknowledgments

- Google Gemini AI for intelligent processing
- Free tier providers (Render, Vercel, ElephantSQL)
- Open source community
- All the professors who respond to cold emails!

## 📞 Support & Contact

- GitHub Issues: [your-repo]/issues
- Email: your-email@example.com
- LinkedIn: your-profile

## 🎓 Research Interests

This system specifically targets opportunities in:
- Deep Learning in Manufacturing
- Machine Learning for Aerospace
- Computer Vision in Production
- Predictive Maintenance
- Quality Control Automation
- Digital Twin Technology
- Industry 4.0 Applications

## 🌍 Target Countries

**Priority Regions:**
- 🇺🇸 United States
- 🇨🇦 Canada
- 🇬🇧 United Kingdom
- 🇩🇪 Germany
- 🇳🇱 Netherlands
- 🇨🇭 Switzerland
- 🇸🇪 Sweden
- 🇳🇴 Norway
- 🇩🇰 Denmark
- 🇦🇺 Australia
- 🇳🇿 New Zealand
- 🇨🇳 China
- 🇭🇰 Hong Kong
- 🇸🇬 Singapore
- 🇯🇵 Japan
- 🇰🇷 South Korea
- 🇦🇪 UAE
- And 30+ more countries!

## 📈 Roadmap

**Version 1.0** (Current)
- ✅ Global university discovery
- ✅ Professor profile analysis
- ✅ Automated email system
- ✅ Batch approval workflow
- ✅ Application tracking

**Version 2.0** (Planned)
- 🔄 Machine learning match scoring
- 🔄 Interview scheduler
- 🔄 Video introduction creator
- 🔄 Mobile app (React Native)
- 🔄 Browser extension

**Version 3.0** (Future)
- 📅 AI interview preparation
- 📅 Recommendation letter manager
- 📅 Visa application tracker
- 📅 Housing finder
- 📅 Community forum

---

## 🚀 Quick Start Summary
```bash
# 1. Clone repository
git clone <repo-url> && cd phd-application-automator

# 2. Run setup script
./scripts/setup.sh

# 3. Start application
./scripts/start.sh

# 4. Open browser
# http://localhost:3000
```

**That's it! You're ready to automate your PhD applications! 🎓**

---

**Note**: Always follow university guidelines and respect email etiquette. This tool is designed to help you reach more opportunities efficiently, not to spam professors. Quality over quantity!

Good luck with your PhD applications! 🍀
```

---

## 🎯 COMPLETE CLAUDE CODE PROMPT

Now, here's the **comprehensive prompt** for Claude Code:
```
I need you to build a COMPLETE AI-Powered PhD Application Automation System. This is a large-scale project that will help me apply to PhD programs worldwide.

=== PROJECT OVERVIEW ===

Create a full-stack web application that:
1. Discovers PhD opportunities globally (195+ countries)
2. Scrapes university websites and professor profiles
3. Matches opportunities with my research interests
4. Generates personalized emails using AI
5. Manages batch email approval and sending (10,000+ emails/day)
6. Tracks applications and analyzes success rates
7. Provides beautiful React-based frontend
8. Includes Python CLI for backend control

=== MY PROFILE ===

**Education**: Master's student in Mechanical Engineering
**Research Focus**: 
- Deep Learning in Manufacturing
- Machine Learning in Aerospace Industry
- Computer Vision for Quality Control
- Predictive Maintenance
- Industry 4.0 Applications
- Model Training & Optimization

**Target Degree**: PhD in Mechanical Engineering / Aerospace / AI

**Must-Have Requirements**:
- Scholarship/Funding available
- Research alignment with my interests
- English-taught programs
- Accepting international students

=== CORE REQUIREMENTS ===

### 1. GLOBAL UNIVERSITY DISCOVERY ENGINE

**Countries to Cover** (ALL regions):
- North America: USA, Canada, Mexico
- Europe: UK, Germany, France, Netherlands, Switzerland, Sweden, Norway, Denmark, Finland, Belgium, Austria, Italy, Spain, Portugal, Ireland, Poland, Czech Republic
- Asia-Pacific: China (.cn domains), Hong Kong, Singapore, Japan, South Korea, Taiwan, Thailand, Malaysia, Vietnam, India, Australia, New Zealand
- Middle East: UAE, Saudi Arabia, Qatar, Israel, Turkey
- Others: Brazil, South Africa, Argentina

**Search Criteria**:
- Find universities with Mechanical Engineering / Aerospace departments
- Identify PhD programs with funding
- Extract scholarship information
- Detect application deadlines
- No ranking bias (include ALL universities offering scholarships)
- Special handling for .cn domains (Chinese universities)

**Data to Extract**:
- University name, location, website
- Department/School information
- Research labs and groups
- Scholarship details and amounts
- Application deadlines and requirements
- Contact information
- Program duration and structure

### 2. PROFESSOR PROFILE ANALYZER

**Profile Sources**:
- University faculty pages
- Google Scholar
- ResearchGate
- LinkedIn
- Personal websites

**Information to Extract**:
- Full name and title
- Email address (primary focus)
- Department and position
- Research interests and areas
- Recent publications (last 2 years)
- Current PhD students
- Lab website and openings
- H-index and citations
- Grants and funding

**Analysis Features**:
- Research interest matching (AI-powered)
- Calculate compatibility score (0-100%)
- Identify shared research areas
- Find recent relevant publications
- Detect if accepting new students

### 3. INTELLIGENT EMAIL SYSTEM

**Email Generation** (using Gemini AI):
- Personalized for each professor
- Mention specific research interests
- Reference professor's recent work
- Highlight my relevant experience
- Professional and concise (200-300 words)
- Include CV attachment automatically
- Multiple templates for variety
- Multi-language support (detect professor's country)

**Email Components**:
```
Subject: PhD Opportunity - Deep Learning in Aerospace Manufacturing

Dear Professor [Name],

[PERSONALIZED INTRO - mention their specific research]

[MY BACKGROUND - relevant experience]

[RESEARCH ALIGNMENT - shared interests]

[SPECIFIC INTEREST - why their lab]

[CV ATTACHMENT]

[PROFESSIONAL CLOSING]
```

**Batch Management**:
- Generate 100+ emails at once
- Group into batches of 50
- Preview all emails before sending
- Approve/reject individual emails
- Edit emails before approval
- Schedule sending times
- Respect daily limits (10,000/day)
- Track sending status

**Smart Sending**:
- Optimal time detection (9 AM - 5 PM professor's timezone)
- Avoid weekends and holidays
- Stagger sending (not all at once)
- Retry failed sends
- Bounce detection
- Blacklist management

### 4. WEB SCRAPING SYSTEM

**Technologies**:
- BeautifulSoup4 (static content)
- Selenium (dynamic content)
- Scrapy (large-scale crawling)
- Playwright (JavaScript-heavy sites)

**Features**:
- Respect robots.txt
- Rate limiting (2-5 seconds between requests)
- User-agent rotation
- Error handling and retry logic
- CAPTCHA detection (alert user)
- Proxy support (optional)
- Progress tracking
- Resume interrupted scraping

**Special Handlers**:
- Chinese websites (.cn domains) - handle character encoding
- JavaScript-rendered content
- PDF extraction (scholarship documents)
- Multi-page navigation
- Login-protected pages (for user's university portals)

### 5. PROFESSIONAL FRONTEND (React)

**Design Requirements**:
- Modern, clean, professional appearance
- Inspired by: Stripe, Linear, Notion interfaces
- Color scheme: Blue/Purple gradients, clean whites
- Typography: Inter font family
- Glassmorphism effects
- Smooth animations (Framer Motion)
- Responsive (mobile, tablet, desktop)
- Dark mode support

**Pages to Build**:

1. **Landing/Login Page**
   - Beautiful hero section
   - Feature highlights
   - Login/Register forms
   - Password reset

2. **Dashboard** (main page after login)
   - Statistics cards:
     * Total opportunities found
     * Applications sent
     * Responses received
     * Success rate percentage
   - Recent activity feed
   - Upcoming deadlines calendar
   - Quick action buttons
   - Interactive charts (Recharts)

3. **University Search**
   - Advanced filter sidebar:
     * Countries (multi-select)
     * Research areas (checkboxes)
     * Scholarship availability
     * Application deadlines
     * University ranking range
   - Search results grid/list toggle
   - University cards with:
     * Logo/Image
     * Name and location
     * Match score badge
     * Quick info
     * "View Details" button
   - Pagination/Infinite scroll
   - Export to CSV/Excel
   - Save favorites

4. **University Detail Page**
   - Full university information
   - Department details
   - Research labs list
   - Professor list with photos
   - Scholarship information
   - Application requirements
   - Important dates
   - Contact information
   - "Find Professors" button

5. **Professor Database**
   - Filterable professor list
   - Professor cards with:
     * Photo
     * Name and title
     * Research interests (tags)
     * Match percentage
     * Recent publications
     * Contact status
   - Sort by: Match score, H-index, Recent activity
   - Bulk selection for emails
   - Professor detail modal

6. **Email Management Dashboard**
   - Tabs: Drafts, Pending Approval, Scheduled, Sent, Failed
   - Email draft list
   - Preview pane
   - Edit functionality
   - Batch approval interface:
     * Select all/none
     * Review in batches of 50
     * Approve/reject individual
     * Edit before approval
   - Scheduling interface
   - Sending progress bar
   - Email history with filters

7. **Email Editor**
   - Rich text editor
   - Template selection
   - Variable insertion (professor name, university, etc.)
   - CV attachment upload
   - Preview mode
   - Save as template
   - Send test email

8. **Application Tracker**
   - Kanban board view (Sent, Delivered, Opened, Replied, Rejected)
   - List view with filters
   - Status indicators
   - Timeline view
   - Application details:
     * Professor and university
     * Email content
     * Sending date
     * Open/Reply dates
     * Notes section
     * Attached documents
   - Follow-up reminders
   - Manual status update

9. **Analytics Dashboard**
   - Response rate over time (line chart)
   - Applications by country (bar chart)
   - Success rate funnel
   - Best performing universities
   - Optimal sending times
   - Email open rates
   - Average response time
   - Export report (PDF/CSV)

10. **Profile Settings**
    - Personal information
    - Research interests editor
    - CV upload/update
    - Target countries selection
    - Email preferences
    - Notification settings
    - Account settings

11. **Document Manager**
    - CV versions list
    - Cover letter templates
    - Research proposal
    - Publication list
    - Upload/Download
    - Preview PDF files

**UI Components Library**:
- Reusable Button component
- Input fields with validation
- Select dropdowns (react-select)
- Modal dialogs
- Toast notifications
- Loading spinners and skeletons
- Empty states
- Error boundaries
- Tooltips
- Progress bars
- Badge components
- Card components
- Table components

### 6. BACKEND (Python Flask/FastAPI)

**Architecture**:
- RESTful API design
- JWT authentication
- SQLAlchemy ORM
- Celery for async tasks
- Redis for caching and queue
- Comprehensive error handling
- Request validation
- API rate limiting

**API Endpoints**:

**Authentication**:
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- POST /api/auth/refresh-token
- POST /api/auth/forgot-password
- POST /api/auth/reset-password

**Universities**:
- GET /api/universities/search
- GET /api/universities/:id
- POST /api/universities/discover (trigger scraping)
- GET /api/universities/:id/professors
- GET /api/universities/favorites
- POST /api/universities/:id/favorite

**Professors**:
- GET /api/professors/search
- GET /api/professors/:id
- POST /api/professors/discover
- GET /api/professors/:id/publications
- PUT /api/professors/:id/notes

**Emails**:
- POST /api/emails/generate (batch generation)
- GET /api/emails/drafts
- PUT /api/emails/:id
- POST /api/emails/batch/approve
- POST /api/emails/batch/send
- GET /api/emails/history
- GET /api/emails/:id/status

**Applications**:
- GET /api/applications
- GET /api/applications/:id
- PUT /api/applications/:id/status
- POST /api/applications/:id/note
- GET /api/applications/stats

**Analytics**:
- GET /api/analytics/dashboard
- GET /api/analytics/response-rate
- GET /api/analytics/by-country
- GET /api/analytics/success-funnel
- GET /api/analytics/export

**User**:
- GET /api/user/profile
- PUT /api/user/profile
- POST /api/user/cv-upload
- GET /api/user/preferences
- PUT /api/user/preferences

**System**:
- GET /api/system/status
- GET /api/system/stats
- POST /api/system/test-email

**Async Tasks** (Celery):
- University scraping (long-running)
- Professor discovery (batch processing)
- Email generation (AI-powered, slow)
- Email sending (scheduled)
- Analytics calculation (heavy computation)

### 7. CLI INTERFACE (Python)

**Command Structure**:
```bash
python cli/main.py [command] [subcommand] [options]
```

**Commands**:

**Database**:
```bash
python cli/main.py db init                # Initialize database
python cli/main.py db migrate "msg"       # Create migration
python cli/main.py db upgrade             # Apply migrations
python cli/main.py db backup              # Backup database
python cli/main.py db export --format csv # Export data
python cli/main.py db stats               # Database statistics
```

**Scraping**:
```bash
python cli/main.py scrape universities --all
python cli/main.py scrape universities --country USA
python cli/main.py scrape universities --countries USA,UK,China
python cli/main.py scrape professors --university "MIT"
python cli/main.py scrape professors --batch universities.csv
python cli/main.py scrape resume          # Resume failed scraping
python cli/main.py scrape status          # Check scraping progress
```

**Emails**:
```bash
python cli/main.py email generate --count 100
python cli/main.py email preview --id 123
python cli/main.py email test --to email@example.com
python cli/main.py email approve --batch-id 456
python cli/main.py email send --batch-id 456
python cli/main.py email status
python cli/main.py email stats --today
python cli/main.py email pause            # Pause sending
python cli/main.py email resume           # Resume sending
```

**Analytics**:
```bash
python cli/main.py analytics dashboard
python cli/main.py analytics report --period week
python cli/main.py analytics export --format pdf
```

**System**:
```bash
python cli/main.py status                 # System status
python cli/main.py logs --tail 100        # View logs
python cli/main.py logs clean --days 7    # Clean old logs
python cli/main.py config show            # Show configuration
python cli/main.py config set KEY=VALUE   # Update config
```

### 8. DATABASE DESIGN

**Tables**:

**users**:
- id (PRIMARY KEY)
- email (UNIQUE)
- password_hash
- name
- created_at
- last_login
- research_interests (JSON)
- target_countries (JSON)
- preferences (JSON)
- cv_path
- is_active
- is_verified

**universities**:
- id (PRIMARY KEY)
- name
- country
- city
- website
- domain
- ranking (nullable)
- has_scholarship
- scholarship_details (TEXT)
- application_deadline (DATE)
- research_areas (JSON)
- contact_email
- phone
- address
- logo_url
- created_at
- updated_at
- last_scraped

**professors**:
- id (PRIMARY KEY)
- university_id (FOREIGN KEY)
- name
- title
- email (INDEXED)
- department
- research_interests (JSON)
- publications (JSON)
- h_index
- citations
- accepting_students (BOOLEAN)
- lab_website
- profile_url
- google_scholar_url
- created_at
- updated_at
- last_contacted

**applications**:
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- professor_id (FOREIGN KEY)
- university_id (FOREIGN KEY)
- status (ENUM: draft, sent, delivered, opened, replied, rejected)
- applied_date
- opened_date
- replied_date
- response_content (TEXT)
- notes (TEXT)
- documents (JSON)
- follow_up_date
- match_score
- created_at
- updated_at

**emails**:
- id (PRIMARY KEY)
- application_id (FOREIGN KEY)
- batch_id
- subject
- body (TEXT)
- template_id
- status (ENUM: draft, pending, approved, scheduled, sending, sent, failed, bounced)
- scheduled_time
- sent_at
- opened_at
- replied_at
- error_message
- retry_count
- created_at

**email_batches**:
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- name
- total_count
- approved_count
- sent_count
- status
- created_at
- approved_at
- completed_at

**analytics**:
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- metric_name
- metric_value
- date
- metadata (JSON)

**scraping_jobs**:
- id (PRIMARY KEY)
- job_type (ENUM: universities, professors)
- status (ENUM: pending, running, completed, failed)
- parameters (JSON)
- progress
- results_count
- started_at
- completed_at
- error_message

### 9. AI INTEGRATION (Gemini API)

**Use Cases**:

1. **University Analysis**:
   - Extract scholarship information from web pages
   - Identify research areas
   - Summarize department strengths
   - Detect application requirements

2. **Professor Matching**:
   - Analyze research interests
   - Calculate compatibility score
   - Find shared research topics
   - Suggest collaboration points

3. **Email Generation**:
   - Create personalized introduction
   - Mention specific research work
   - Highlight relevant experience
   - Professional tone and structure
   - Appropriate length (200-300 words)

4. **Content Extraction**:
   - Parse professor publications
   - Extract contact information
   - Identify lab openings
   - Detect student requirements

**Prompts** (examples):

**University Analysis**:
```
Analyze this university's webpage and extract:
1. Available scholarships for international PhD students
2. Research areas in Mechanical Engineering / Aerospace
3. Application deadlines and requirements
4. Contact information for admissions

Webpage content: [CONTENT]
```

**Email Generation**:
```
Generate a professional email to Professor [NAME] expressing interest in their PhD program.

Professor's research: [RESEARCH INTERESTS]
Recent publications: [PUBLICATIONS]

My background:
- Master's in Mechanical Engineering
- Research: Deep Learning in Manufacturing, ML in Aerospace
- Experience: [BRIEF SUMMARY]

Requirements:
- 200-300 words
- Professional tone
- Mention specific research alignment
- Include request for funding information
- End with clear call-to-action
```

### 10. TESTING REQUIREMENTS

**Backend Tests** (pytest):
- Unit tests for all services
- API endpoint tests
- Database model tests
- Scraping tests (mock responses)
- Email generation tests
- Authentication tests
- Integration tests

**Test After Each Major Feature**:
```python
# Test checklist after each feature:
✅ Unit tests pass
✅ Integration tests pass
✅ API returns correct responses
✅ Database queries work
✅ Error handling works
✅ Logging is correct
```

**Frontend Tests** (Jest + React Testing Library):
- Component rendering tests
- User interaction tests
- API integration tests
- Form validation tests
- Routing tests

**Critical Tests**:
1. Authentication flow
2. University search and filtering
3. Professor profile loading
4. Email generation and preview
5. Batch approval workflow
6. Email sending process
7. Application tracking
8. Analytics calculation

### 11. DEPLOYMENT

**Development**:
- Backend: http://localhost:5000
- Frontend: http://localhost:3000
- Database: SQLite (local file)
- Redis: localhost:6379

**Production** (All FREE):

**Backend** - Render.com:
- Free tier: 750 hours/month
- Auto-deploy from GitHub
- Environment variables
- Automatic HTTPS

**Frontend** - Vercel:
- Unlimited deployments
- CDN included
- Custom domains
- Automatic HTTPS

**Database** - ElephantSQL:
- Free PostgreSQL
- 20MB storage
- Perfect for starting

**Redis** - Redis Labs:
- Free 30MB
- Enough for job queue

**Email** - Multiple options:
- Gmail (free, limited)
- SendGrid (free 100/day)
- Mailgun (free 5000/month)

### 12. ONE-COMMAND SETUP

Create scripts for easy setup:

**scripts/setup.sh**:
```bash
#!/bin/bash
echo "🚀 Setting up PhD Application Automator..."

# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
cp .env.example .env
echo "⚙️ Please edit backend/.env with your API keys"
python cli/main.py db init
python cli/main.py db migrate

# Frontend setup
cd ../frontend
npm install
cp .env.example .env.local
echo "⚙️ Please edit frontend/.env.local with API URL"

echo "✅ Setup complete!"
echo "📝 Next steps:"
echo "  1. Edit backend/.env with your API keys"
echo "  2. Edit frontend/.env.local with API URL"
echo "  3. Run ./scripts/start.sh to start the application"
```

**scripts/start.sh**:
```bash
#!/bin/bash
echo "🚀 Starting PhD Application Automator..."

# Start backend
cd backend
source venv/bin/activate &
python app.py &
BACKEND_PID=$!

# Start Celery
celery -A tasks.celery worker --loglevel=info &
CELERY_PID=$!

# Start frontend
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "✅ Application started!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:5000"
echo "📊 Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $CELERY_PID $FRONTEND_PID; exit" INT
wait
```

Make scripts executable:
```bash
chmod +x scripts/setup.sh scripts/start.sh
```

### 13. SPECIAL REQUIREMENTS

**Beginner-Friendly**:
- Comprehensive comments in code
- Clear variable names
- Modular structure (easy to understand)
- Detailed error messages
- Step-by-step documentation
- Video tutorial links in README
- Troubleshooting guide

**Easy Modification**:
- Configuration files for easy changes
- Template system for emails
- Pluggable scraper modules
- Customizable frontend themes
- Environment variables for all settings

**Professional Quality**:
- Production-ready code
- Security best practices
- Performance optimization
- Error handling everywhere
- Comprehensive logging
- Code documentation

**Scalability**:
- Async processing (Celery)
- Database indexing
- Caching strategy (Redis)
- Pagination for large datasets
- Batch processing
- Rate limiting

### 14. ADVANCED FEATURES

**Nice-to-Have** (if time permits):

1. **Deadline Calendar Integration**:
   - Google Calendar sync
   - iCal export
   - Reminder notifications

2. **Mobile App** (React Native):
   - View opportunities
   - Approve emails
   - Track applications

3. **Browser Extension**:
   - Save professors while browsing
   - Quick email generation
   - LinkedIn integration

4. **AI Interview Prep**:
   - Generate common interview questions
   - Research area deep-dive
   - Professor's work summary

5. **Recommendation Letter Tracker**:
   - Request tracking
   - Reminder system
   - Upload portal

6. **Visa Application Helper**:
   - Document checklist
   - Timeline planner
   - Country requirements

7. **Housing Finder**:
   - Near-campus housing
   - Student accommodation
   - Budget calculator

8. **Community Forum**:
   - Connect with other applicants
   - Share experiences
   - Ask questions

9. **Success Stories**:
   - Track successful applications
   - Share strategies
   - Inspire others

10. **Machine Learning Enhancements**:
    - Predict response probability
    - Optimize email content
    - Best time to send analysis
    - Success pattern recognition

=== DEVELOPMENT WORKFLOW ===

**Phase 1: Foundation** (Week 1)
1. ✅ Setup project structure
2. ✅ Initialize database
3. ✅ Create authentication system
4. ✅ Basic Flask API
5. ✅ React app skeleton
6. ✅ Test: User can register and login

**Phase 2: Scraping** (Week 2)
1. ✅ Build university scraper
2. ✅ Build professor scraper
3. ✅ Gemini AI integration
4. ✅ Data storage
5. ✅ Test: Can discover 100+ universities

**Phase 3: Matching** (Week 3)
1. ✅ Matching algorithm
2. ✅ Scoring system
3. ✅ Search functionality
4. ✅ Filtering system
5. ✅ Test: Can match and rank opportunities

**Phase 4: Email System** (Week 4)
1. ✅ Email generation (AI)
2. ✅ Template system
3. ✅ SMTP integration
4. ✅ Batch management
5. ✅ Scheduling
6. ✅ Test: Can generate and send 100 emails

**Phase 5: Frontend** (Week 5-6)
1. ✅ All pages created
2. ✅ Beautiful UI
3. ✅ Responsive design
4. ✅ Animations
5. ✅ Test: All features work from UI

**Phase 6: Polish** (Week 7)
1. ✅ Bug fixes
2. ✅ Performance optimization
3. ✅ Error handling
4. ✅ Documentation
5. ✅ Deployment

=== CRITICAL SUCCESS CRITERIA ===

The system must:
- ✅ Discover 1000+ universities in first run
- ✅ Find 5000+ professors with contact info
- ✅ Generate personalized emails in < 5 seconds each
- ✅ Support sending 10,000 emails/day
- ✅ Have beautiful, professional UI
- ✅ Work with ONE command: `./scripts/start.sh`
- ✅ Be easy for beginners to understand
- ✅ Be easy to modify and extend
- ✅ Handle errors gracefully
- ✅ Have comprehensive documentation

=== DELIVERABLES ===

Please create:
1. ✅ Complete backend (Python Flask)
2. ✅ Complete frontend (React)
3. ✅ CLI interface
4. ✅ Database with migrations
5. ✅ All API endpoints
6. ✅ Scraping system
7. ✅ Email system
8. ✅ Authentication system
9. ✅ Testing suite
10. ✅ Setup scripts
11. ✅ Documentation (README, API docs, etc.)
12. ✅ Deployment configurations

=== CODING STANDARDS ===

**Python**:
- PEP 8 compliant
- Type hints
- Docstrings for all functions
- Clear variable names
- Modular design
- Error handling with try-except
- Logging for all important events

**JavaScript/React**:
- ES6+ features
- Functional components with hooks
- Clear prop-types or TypeScript
- Component composition
- Custom hooks for logic
- Clean code structure

**Comments**:
- Explain WHY, not WHAT
- Comment complex algorithms
- Add TODOs for future improvements
- Section dividers in large files

=== API KEYS PROVIDED ===

Gemini AI: AIzaSyDoM23RVH_WZLsiNGxYpYlulLfEGb9XrNY

Please add placeholders in .env.example for:
- SMTP credentials
- Database URL
- Secret keys
- Other API keys

=== FINAL CHECKLIST ===

Before completion, ensure:
- [ ] All files created
- [ ] No syntax errors
- [ ] All tests pass
- [ ] setup.sh works
- [ ] start.sh works
- [ ] Database initializes correctly
- [ ] Frontend builds without errors
- [ ] Backend runs on port 5000
- [ ] Frontend runs on port 3000
- [ ] Authentication works
- [ ] University search works
- [ ] Professor search works
- [ ] Email generation works
- [ ] Email sending works
- [ ] All pages render correctly
- [ ] Mobile responsive
- [ ] Error messages are helpful
- [ ] Logging is comprehensive
- [ ] README is complete
- [ ] .env.example files exist
- [ ] Deployment docs included

=== START BUILDING ===

Please build this complete system following best practices. This is a real project that will be used for PhD applications, so quality and reliability are critical.

Make it beautiful, make it functional, make it beginner-friendly!

Let's help me get into a great PhD program! 🎓🚀
