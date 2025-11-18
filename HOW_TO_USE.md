# 🎯 How to Use the PhD Application Automation System

## 🚀 Starting the Application

### Option 1: One-Command Start (Recommended)
```bash
./scripts/start.sh
```

This will automatically:
- Check if setup is complete
- Start the Flask backend on port 5000
- Start the React frontend on port 3000
- Display access URLs

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## 🌐 Accessing the Application

Once started, open your browser:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

---

## 📝 Step-by-Step Usage Guide

### 1. Create Your Account

1. Go to http://localhost:3000
2. Click "Register" (or go to http://localhost:3000/register)
3. Fill in:
   - Email address
   - Password
   - Your name
   - Research interests (e.g., "Deep Learning", "Manufacturing")
4. Click "Register"
5. You'll be automatically logged in

### 2. Discover Universities

1. Navigate to "University Search" from the sidebar
2. Use filters:
   - **Country**: Select from 20+ countries
   - **Research Area**: Filter by your interests
   - **Scholarship**: Show only funded positions
3. Click "Search"
4. Browse results:
   - View university details
   - Check scholarship information
   - See application deadlines
5. Click "Find Professors" for interesting universities

### 3. Find Professors

1. Navigate to "Professor Search"
2. Filter by:
   - **University**: Specific institution
   - **Department**: Engineering, Computer Science, etc.
   - **Accepting Students**: Only show available professors
   - **Minimum Match Score**: Filter by compatibility
3. Review professor cards:
   - **Name & Title**
   - **Research Interests**
   - **Match Score** (AI-calculated compatibility)
   - **Publications**
   - **Contact Information**
4. Select professors you're interested in

### 4. Generate AI-Powered Emails

1. Select multiple professors (checkbox selection)
2. Click "Generate Emails"
3. AI will create personalized emails for each professor:
   - Custom introduction
   - Mentions their specific research
   - Highlights your relevant background
   - Professional structure (200-300 words)
   - CV automatically attached
4. Wait for generation to complete

### 5. Review & Edit Email Drafts

1. Navigate to "Email Management"
2. View your email batches
3. Click on a batch to see all emails
4. For each email:
   - **Preview** the content
   - **Edit** if needed (subject or body)
   - **Delete** if not suitable
5. Make any necessary adjustments

### 6. Approve Email Batch

1. Once satisfied with all emails in a batch
2. Click "Approve Batch"
3. This marks emails as ready to send
4. You can still edit approved emails before sending

### 7. Send Emails

1. Select an approved batch
2. Click "Send Batch"
3. Emails will be sent via SMTP
4. Monitor sending progress:
   - **Sent count**: Successfully delivered
   - **Failed count**: Errors encountered
5. Check individual email status

### 8. Track Applications

1. Navigate to "Applications"
2. View all your applications:
   - **Status**: Draft, Sent, Delivered, Opened, Replied
   - **Professor & University**
   - **Match Score**
   - **Dates**: Applied, Opened, Replied
3. Update status manually as needed
4. Add notes for each application
5. Attach additional documents

### 9. Monitor Progress

1. Navigate to "Dashboard"
2. View statistics:
   - **Total Applications**: All applications created
   - **Sent**: Emails sent out
   - **Replies Received**: Responses from professors
   - **Response Rate**: Success percentage
3. Check recent activity
4. View upcoming deadlines
5. Use quick actions for common tasks

### 10. Analyze Results

1. Navigate to "Analytics"
2. View charts and insights:
   - **Response Rate Over Time**
   - **Applications by Country**
   - **Success Funnel**
   - **Best Performing Universities**
3. Export reports if needed

---

## 🛠️ CLI Commands (Advanced)

### Database Management
```bash
cd backend
source venv/bin/activate

# Initialize database
python cli/main.py db init

# Backup database
python cli/main.py db backup

# Export data to CSV
python cli/main.py db export --format csv
```

### Scraping Commands
```bash
# Discover universities in a country
python cli/main.py scrape universities --country USA

# Discover professors for a university
python cli/main.py scrape professors --university "MIT"

# Check scraping status
python cli/main.py scrape status
```

### Email Commands
```bash
# Generate 100 emails
python cli/main.py email generate --count 100

# Approve batch
python cli/main.py email approve --batch-id 1

# Send approved batch
python cli/main.py email send --batch-id 1

# View email statistics
python cli/main.py email stats
```

---

## ⚙️ Configuration

### Backend Configuration

Edit `backend/.env` file:

```env
# Your Email Settings (REQUIRED for sending)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
EMAIL_FROM=your-email@gmail.com

# Gemini AI (Already configured)
GEMINI_API_KEY=AIzaSyDoM23RVH_WZLsiNGxYpYlulLfEGb9XrNY

# Database (Default is fine for development)
DATABASE_URL=sqlite:///phd_applications.db

# Email Limits
DAILY_EMAIL_LIMIT=10000
HOURLY_EMAIL_LIMIT=500
```

### Gmail Setup (Recommended)

1. Go to https://myaccount.google.com/security
2. Enable 2-Factor Authentication
3. Generate an "App Password"
4. Use this password in `.env` file

### Frontend Configuration

Edit `frontend/.env.local` if needed:

```env
VITE_API_URL=http://localhost:5000
```

---

## 🛑 Stopping the Application

### If Started with `start.sh`:
Press `Ctrl+C` in the terminal

### If Started Manually:
Press `Ctrl+C` in both terminals (backend and frontend)

### Force Stop:
```bash
# Kill processes on ports
lsof -ti:5000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend (or 5173 for Vite)
```

---

## 🔄 Restarting the Application

```bash
# Simple restart
./scripts/start.sh

# Or manually restart each service
cd backend && source venv/bin/activate && python app.py &
cd frontend && npm run dev &
```

---

## 🧪 Running Tests

### Backend Tests:
```bash
cd backend
source venv/bin/activate
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Frontend Tests:
```bash
cd frontend
npm test
```

---

## 🐛 Troubleshooting

### Backend Won't Start

**Problem**: Port 5000 already in use
```bash
# Solution: Kill the process
lsof -ti:5000 | xargs kill -9
```

**Problem**: Database errors
```bash
# Solution: Reinitialize database
cd backend
rm phd_applications.db
./venv/bin/python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all()"
```

### Frontend Won't Start

**Problem**: Port 3000/5173 in use
```bash
# Solution: Kill the process
lsof -ti:3000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

**Problem**: Dependencies missing
```bash
# Solution: Reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Emails Not Sending

1. Check SMTP credentials in `backend/.env`
2. Verify Gmail app password (not regular password)
3. Check email quota limits
4. Review logs in `backend/logs/app.log`

### API Errors

1. Check backend is running: http://localhost:5000/health
2. Verify CORS settings in `backend/config.py`
3. Check JWT token hasn't expired
4. Review browser console for errors

---

## 📊 Database Location

- **Development**: `backend/phd_applications.db`
- **Backups**: Created when you run `python cli/main.py db backup`

---

## 📁 Important Files

### Configuration
- `backend/.env` - Backend environment variables
- `frontend/.env.local` - Frontend environment variables

### Data
- `backend/data/universities.json` - University seed data
- `backend/data/countries.json` - Country information
- `backend/data/research_areas.json` - Research taxonomies

### Database
- `backend/phd_applications.db` - SQLite database

### Logs
- `backend/logs/app.log` - Application logs

---

## 💡 Tips for Best Results

### 1. Email Sending
- Start with small batches (10-20 emails)
- Review and edit AI-generated emails
- Personalize when possible
- Respect daily limits
- Track response rates

### 2. University Discovery
- Use multiple search criteria
- Check scholarship requirements
- Note application deadlines
- Research program fit
- Contact departments directly

### 3. Professor Selection
- Focus on high match scores (70%+)
- Read their recent publications
- Check if accepting students
- Verify email addresses
- Research their lab website

### 4. Application Management
- Update status regularly
- Add notes for follow-ups
- Set reminders for deadlines
- Keep documents organized
- Track all communications

---

## 🚀 Deployment (Optional)

### Backend - Render.com (Free)
1. Push code to GitHub
2. Create Render account
3. Connect repository
4. Add environment variables
5. Deploy

### Frontend - Vercel (Free)
1. Push code to GitHub
2. Create Vercel account
3. Import project
4. Configure build settings
5. Deploy

### Database - ElephantSQL (Free)
1. Create account
2. Create database
3. Update DATABASE_URL in .env
4. Migrate database

---

## 📞 Getting Help

### Documentation
- **README.md**: Main documentation
- **COMPLETE_DEMONSTRATION.md**: Full feature list
- **API Docs**: Check backend code for endpoint details

### Logs
```bash
# View backend logs
tail -f backend/logs/app.log

# View frontend logs
# Check browser console
```

### Testing
```bash
# Test specific functionality
cd backend
pytest tests/test_<module>.py -v
```

---

## 🎓 Example Workflow

**Day 1**: Setup & Configuration
1. Run `./scripts/setup.sh`
2. Configure SMTP in `.env`
3. Test email sending
4. Create your account

**Day 2**: Discovery
1. Search universities in target countries
2. Find 50-100 professors
3. Review match scores
4. Select best matches

**Day 3**: Email Generation
1. Generate emails for selected professors
2. Review and edit drafts
3. Approve batches
4. Send first batch (10-20 emails)

**Day 4+**: Management
1. Track email status
2. Respond to replies
3. Update application status
4. Send more batches
5. Analyze results

---

## ✅ Daily Checklist

- [ ] Start application (`./scripts/start.sh`)
- [ ] Check for new replies
- [ ] Update application statuses
- [ ] Review pending email batches
- [ ] Send new emails (within limits)
- [ ] Backup database
- [ ] Monitor analytics
- [ ] Update notes and reminders

---

## 🎉 Success!

You're now ready to use the PhD Application Automation System!

**Remember**: Quality over quantity. Personalize emails, research programs carefully, and track your applications diligently.

**Good luck with your PhD applications! 🚀**

---

**Questions?**
- Check the comprehensive documentation
- Review the code comments
- Test with small batches first
- Monitor logs for issues
