# 🎯 Getting Started with PhD Application Automator

Welcome! This guide will help you get started with the PhD Application Automator in just a few steps.

## 🚀 Quick Start (5 Minutes)

### Step 1: Run Setup Script

```bash
# Navigate to the project directory
cd lobal-PhD-Scholarship-Finder-Application-Automator

# Run the setup script
./scripts/setup.sh
```

### Step 2: Start the Application

```bash
# Start both backend and frontend
./scripts/start.sh
```

### Step 3: Open in Browser

Open your browser and go to: **http://localhost:3000**

That's it! You're ready to start using the application.

---

## 📖 Detailed Walkthrough

### Creating Your Account

1. Navigate to **http://localhost:3000**
2. Click "Sign Up" or "Register"
3. Fill in your details:
   - Email address
   - Secure password (at least 8 characters with uppercase, lowercase, and numbers)
   - Full name
   - Research interests (e.g., "Deep Learning", "Manufacturing", "Aerospace")
   - Target countries (e.g., "USA", "UK", "Canada")
4. Click "Register"

You'll be automatically logged in!

### Using the Dashboard

After logging in, you'll see your dashboard with:
- **Statistics Cards**: Track your applications
- **Recent Applications**: Monitor your progress
- **Quick Actions**: Add universities, professors, create applications

### Adding Universities

#### Option 1: Manual Entry

```python
# Using Python
from app import app, db
from models import University

with app.app_context():
    uni = University(
        name="Stanford University",
        country="USA",
        city="Stanford",
        has_scholarship=True,
        scholarship_details="Full funding for all PhD students",
        research_areas=["AI", "ML", "Robotics"]
    )
    db.session.add(uni)
    db.session.commit()
```

#### Option 2: Via API

```bash
# Get your access token first by logging in
TOKEN="your-access-token"

curl -X POST http://localhost:5000/api/universities \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MIT",
    "country": "USA",
    "city": "Cambridge",
    "has_scholarship": true,
    "scholarship_details": "Full tuition + $40k stipend",
    "research_areas": ["AI", "Robotics", "Aerospace"]
  }'
```

### Adding Professors

```python
from app import app, db
from models import Professor

with app.app_context():
    prof = Professor(
        university_id=1,  # ID of the university
        name="Dr. Jane Smith",
        title="Professor",
        email="jsmith@university.edu",
        department="Mechanical Engineering",
        research_interests=["Deep Learning", "Computer Vision", "Manufacturing"],
        accepting_students=True,
        h_index=45
    )
    db.session.add(prof)
    db.session.commit()
```

### Generating AI-Powered Emails

The system uses **Google Gemini AI** to generate personalized emails!

```python
from services.ai.email_generator import get_email_generator

# Initialize generator
gen = get_email_generator()

# Generate personalized email
email = gen.generate_email(
    professor_name="Dr. Jane Smith",
    professor_interests=["Deep Learning", "Computer Vision"],
    university_name="Stanford University",
    department="Mechanical Engineering",
    user_background="Master's student in ME with focus on AI and manufacturing",
    user_interests=["Machine Learning", "Quality Control", "Predictive Maintenance"]
)

# Use the generated email
print("Subject:", email['subject'])
print("\nBody:\n", email['body'])
```

**Example Output:**

```
Subject: PhD Opportunity - Machine Learning in Manufacturing

Body:
Dear Professor Smith,

I am writing to express my strong interest in pursuing a PhD under your supervision at Stanford University. I was particularly impressed by your recent work in applying deep learning techniques to computer vision problems, which aligns closely with my research interests.

I am currently completing my Master's degree in Mechanical Engineering with a specialization in AI applications for manufacturing. My thesis focuses on using machine learning for quality control and predictive maintenance systems, which I believe complements your research in computer vision and deep learning.

I am especially interested in exploring how your computer vision techniques could be applied to manufacturing defect detection and process optimization. I believe this represents an exciting opportunity to bridge your foundational research with practical industrial applications.

I would be grateful for the opportunity to discuss potential PhD positions in your lab and available funding opportunities. I have attached my CV for your review.

Thank you for considering my application.

Best regards,
[Your Name]
```

### Calculating Match Scores

```python
from services.ai.matching_engine import get_matching_engine

matcher = get_matching_engine()

result = matcher.calculate_match_score(
    user_interests=["Deep Learning", "Manufacturing", "Quality Control"],
    professor_interests=["Machine Learning", "Computer Vision", "Industrial AI"]
)

print(f"Match Score: {result['score']}/100")
print(f"Reasons: {result['reasons']}")
print(f"Collaboration Areas: {result['collaboration_areas']}")
```

---

## 🔧 Configuration

### Email Settings (Optional)

To enable email sending, configure SMTP in `backend/.env`:

```env
# Gmail Example
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=True
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your-app-specific-password
EMAIL_FROM=your.email@gmail.com
```

**Get Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Generate a new app password
3. Copy it to `SMTP_PASSWORD`

### Gemini AI (Already Configured)

The Gemini API key is already set in `backend/.env`. The system uses Google's Gemini AI for:
- Email generation
- Professor-applicant matching
- Research interest extraction
- Suggested research topics

---

## 📚 API Examples

### Authentication

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123",
    "name": "Test User",
    "research_interests": ["AI", "ML"]
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123"
  }'
```

### Universities

```bash
# List universities
curl http://localhost:5000/api/universities?country=USA \
  -H "Authorization: Bearer $TOKEN"

# Get specific university
curl http://localhost:5000/api/universities/1 \
  -H "Authorization: Bearer $TOKEN"

# Create university
curl -X POST http://localhost:5000/api/universities \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MIT",
    "country": "USA",
    "has_scholarship": true
  }'
```

### Applications

```bash
# Create application
curl -X POST http://localhost:5000/api/applications \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "professor_id": 1,
    "university_id": 1,
    "custom_message": "I am interested in your deep learning research..."
  }'

# List applications
curl http://localhost:5000/api/applications \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🎨 Frontend Features

The React frontend provides:

### Pages
- **Home** (`/`): Landing page with features
- **Login** (`/login`): User authentication
- **Register** (`/register`): Account creation
- **Dashboard** (`/dashboard`): Main application interface

### Components
- **Navbar**: Navigation with authentication
- **Statistics Cards**: Visual metrics
- **Application List**: Track all applications
- **Status Badges**: Color-coded application status

### Styling
- **Tailwind CSS**: Modern, responsive design
- **Custom Theme**: Professional blue color scheme
- **Mobile-Friendly**: Works on all devices

---

## 🐛 Troubleshooting

### Backend Issues

```bash
# Check backend logs
cat logs/backend.log

# Manually start backend
cd backend
source venv/bin/activate
python app.py
```

### Frontend Issues

```bash
# Check frontend logs
cat logs/frontend.log

# Manually start frontend
cd frontend
npm start
```

### Database Issues

```bash
# Recreate database
cd backend
source venv/bin/activate
python << 'END'
from app import app, db
with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database reset!")
END
```

### API Connection Issues

Make sure:
1. Backend is running on port 5000
2. Frontend `.env` has `REACT_APP_API_URL=http://localhost:5000`
3. No firewall blocking the ports

---

## 📖 Next Steps

1. **Read the Full README**: Comprehensive features and architecture
2. **API Documentation**: Check `docs/API.md`
3. **Quick Start Guide**: See `QUICKSTART.md`
4. **Explore the Code**: Well-documented and beginner-friendly

---

## 🎯 Common Use Cases

### 1. Find Matching Professors

```python
from models import Professor
from services.ai.matching_engine import get_matching_engine

matcher = get_matching_engine()
professors = Professor.query.all()

user_interests = ["Deep Learning", "Manufacturing"]

for prof in professors:
    match = matcher.calculate_match_score(
        user_interests,
        prof.research_interests
    )
    prof.match_score = match['score']
    prof.match_reasons = match['reasons']

# Sort by match score
sorted_profs = sorted(professors, key=lambda x: x.match_score or 0, reverse=True)

# Top 10 matches
for prof in sorted_profs[:10]:
    print(f"{prof.name}: {prof.match_score}/100")
```

### 2. Batch Email Generation

```python
from services.ai.email_generator import get_email_generator

gen = get_email_generator()

professors = [
    {"name": "Dr. Smith", "interests": ["AI", "ML"]},
    {"name": "Dr. Johnson", "interests": ["Robotics", "Vision"]},
    # ... more professors
]

for prof in professors:
    email = gen.generate_email(
        professor_name=prof['name'],
        professor_interests=prof['interests'],
        # ... other params
    )

    print(f"Email for {prof['name']}:")
    print(email['body'])
    print("\n" + "="*50 + "\n")
```

### 3. Track Application Status

```python
from models import Application, User
from app import app

with app.app_context():
    user = User.query.filter_by(email="your@email.com").first()
    apps = Application.query.filter_by(user_id=user.id).all()

    stats = {
        'total': len(apps),
        'sent': sum(1 for a in apps if a.status == 'sent'),
        'replied': sum(1 for a in apps if a.status == 'replied'),
    }

    print(f"Total Applications: {stats['total']}")
    print(f"Sent: {stats['sent']}")
    print(f"Replies: {stats['replied']}")
    print(f"Response Rate: {stats['replied']/stats['sent']*100:.1f}%")
```

---

## 🙏 Support

- **Issues**: Create an issue on GitHub
- **Documentation**: Full README.md
- **API Docs**: docs/API.md

---

## 🎓 Happy PhD Hunting!

You're all set to automate your PhD applications with AI-powered personalization!

**Key Features to Explore:**
- AI email generation with Gemini
- Professor-applicant matching
- Application tracking
- Batch email management
- Analytics dashboard

Good luck with your applications! 🚀
