# 🚀 Quick Start Guide

Get the PhD Application Automator running in **5 minutes**!

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ installed (for frontend)
- Git installed

## Step 1: One-Command Setup (2 minutes)

```bash
# Make setup script executable and run it
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This script will:
- ✅ Check Python and Node.js versions
- ✅ Create Python virtual environment
- ✅ Install all backend dependencies
- ✅ Initialize the database
- ✅ Install frontend dependencies
- ✅ Create necessary directories

## Step 2: Configure Environment (1 minute)

The Gemini API key is already configured! But you can customize other settings:

```bash
# Edit backend/.env
nano backend/.env
```

**Optional settings:**
```env
# Email settings (for sending application emails)
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
EMAIL_FROM=your-email@gmail.com
```

**Note:** Gmail requires an "App Password" for SMTP. You can generate one at:
https://myaccount.google.com/apppasswords

## Step 3: Start the Application (1 minute)

```bash
# One command to start both backend and frontend!
./scripts/start.sh
```

This will start:
- 🔧 Backend API on **http://localhost:5000**
- 🌐 Frontend on **http://localhost:3000**

## Step 4: Access the Application

### Option 1: Use the Web Interface

Open your browser to: **http://localhost:3000**

1. **Register** a new account
2. Fill in your research interests
3. Start discovering opportunities!

### Option 2: Use the API Directly

```bash
# Health check
curl http://localhost:5000/health

# Register a user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your.email@example.com",
    "password": "YourSecurePassword123",
    "name": "Your Name",
    "research_interests": ["Deep Learning", "Aerospace", "Manufacturing"]
  }'
```

## Quick Feature Tour

### 1. **University Search**
```bash
# Search universities (requires authentication)
curl http://localhost:5000/api/universities \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. **Professor Discovery**
```bash
# Find professors
curl http://localhost:5000/api/professors \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. **AI-Powered Email Generation**

The system uses Google Gemini AI to generate personalized emails!

```python
from services.ai.email_generator import get_email_generator

generator = get_email_generator()

email = generator.generate_email(
    professor_name="Dr. Smith",
    professor_interests=["Deep Learning", "Computer Vision"],
    university_name="MIT",
    department="Mechanical Engineering",
    user_background="Master's student in ME with focus on AI",
    user_interests=["Machine Learning", "Manufacturing"]
)

print(email['subject'])
print(email['body'])
```

### 4. **Match Scoring**

AI calculates how well you match with each professor:

```python
from services.ai.matching_engine import get_matching_engine

matcher = get_matching_engine()

result = matcher.calculate_match_score(
    user_interests=["Deep Learning", "Manufacturing"],
    professor_interests=["Machine Learning", "Production Systems"]
)

print(f"Match Score: {result['score']}/100")
print(f"Reasons: {result['reasons']}")
```

## Troubleshooting

### Backend won't start

```bash
# Check logs
cat logs/backend.log

# Activate virtual environment manually
cd backend
source venv/bin/activate
python app.py
```

### Frontend won't start

```bash
# Check logs
cat logs/frontend.log

# Install dependencies manually
cd frontend
npm install
npm start
```

### Database errors

```bash
# Recreate database
cd backend
source venv/bin/activate
python << END
from app import app, db
with app.app_context():
    db.drop_all()
    db.create_all()
END
```

### Port already in use

```bash
# Find process using port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in backend/.env
PORT=5001
```

## Next Steps

1. **Read the full README.md** for comprehensive features
2. **Check API.md** in docs/ for API documentation
3. **Explore the dashboard** at http://localhost:3000
4. **Start adding universities and professors**
5. **Generate your first AI-powered email!**

## Common Tasks

### Create a new user via Python

```python
from models import db, User
from app import app

with app.app_context():
    user = User(
        email="test@example.com",
        password="SecurePassword123",
        name="Test User",
        research_interests=["AI", "ML"],
        target_countries=["USA", "UK", "Canada"]
    )
    db.session.add(user)
    db.session.commit()
    print(f"User created: {user.id}")
```

### Add a university manually

```python
from models import db, University
from app import app
from datetime import date

with app.app_context():
    uni = University(
        name="Massachusetts Institute of Technology",
        country="USA",
        city="Cambridge",
        website="https://mit.edu",
        has_scholarship=True,
        scholarship_details="Full tuition + stipend",
        research_areas=["AI", "Robotics", "Aerospace"],
        accepts_international=True
    )
    db.session.add(uni)
    db.session.commit()
    print(f"University added: {uni.id}")
```

### Test email generation

```bash
# Start Python shell in backend
cd backend
source venv/bin/activate
python

# Then in Python:
from services.ai.email_generator import get_email_generator

gen = get_email_generator()
email = gen.generate_email(
    professor_name="Dr. Jane Smith",
    professor_interests=["Deep Learning", "Computer Vision"],
    university_name="Stanford University",
    department="Computer Science",
    user_background="Master's in CS with focus on AI",
    user_interests=["Machine Learning", "Neural Networks"]
)

print("Subject:", email['subject'])
print("\nBody:\n", email['body'])
```

## Support

- **Issues:** Open an issue on GitHub
- **Questions:** Check the comprehensive README.md
- **API Docs:** http://localhost:5000/api

---

## 🎉 You're All Set!

Your PhD Application Automator is now running. Happy PhD hunting! 🎓🚀

**Remember:**
- Backend: http://localhost:5000
- Frontend: http://localhost:3000
- Logs: logs/ directory

To stop the application, press **Ctrl+C** in the terminal running start.sh.
