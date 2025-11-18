#!/bin/bash

# PhD Application Automator - Setup Script
# One-command setup for the entire system

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║     🎓 PhD APPLICATION AUTOMATOR - SETUP                    ║"
echo "║                                                              ║"
echo "║     Setting up your PhD application automation system...    ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check Node.js version
echo "📌 Checking Node.js version..."
node --version
if [ $? -ne 0 ]; then
    echo "⚠️  Node.js is not installed. Frontend will not be set up."
    echo "   Install Node.js 18+ from https://nodejs.org"
    SKIP_FRONTEND=true
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  BACKEND SETUP"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Backend setup
cd backend

echo "1️⃣  Creating Python virtual environment..."
python3 -m venv venv

echo "2️⃣  Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

echo "3️⃣  Upgrading pip..."
pip install --upgrade pip

echo "4️⃣  Installing Python dependencies..."
echo "   (This may take a few minutes...)"
pip install -r requirements.txt

echo "5️⃣  Creating environment configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "   ✅ Created .env file"
    echo ""
    echo "   ⚠️  IMPORTANT: Edit backend/.env file with your configuration:"
    echo "      - GEMINI_API_KEY (Already set to: AIzaSyDoM23RVH_WZLsiNGxYpYlulLfEGb9XrNY)"
    echo "      - SMTP credentials (for sending emails)"
    echo "      - Other settings as needed"
    echo ""
else
    echo "   ℹ️  .env file already exists"
fi

echo "6️⃣  Creating necessary directories..."
mkdir -p logs
mkdir -p uploads
mkdir -p data

echo "7️⃣  Initializing database..."
python3 << EOF
from models import init_db
from config import Config

print("   Creating database tables...")
init_db(Config.SQLALCHEMY_DATABASE_URI, echo=False)
print("   ✅ Database initialized successfully")
EOF

cd ..

# Frontend setup
if [ "$SKIP_FRONTEND" != "true" ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  FRONTEND SETUP"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
        cd frontend

        echo "1️⃣  Installing Node.js dependencies..."
        echo "   (This may take a few minutes...)"
        npm install

        echo "2️⃣  Creating frontend environment configuration..."
        if [ ! -f .env.local ]; then
            cat > .env.local << 'ENVFILE'
REACT_APP_API_URL=http://localhost:5000
REACT_APP_VERSION=1.0.0
REACT_APP_ENVIRONMENT=development
ENVFILE
            echo "   ✅ Created .env.local file"
        else
            echo "   ℹ️  .env.local file already exists"
        fi

        cd ..
    else
        echo "⚠️  Frontend directory not found or incomplete. Skipping frontend setup."
    fi
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║     ✅ SETUP COMPLETE!                                      ║"
echo "║                                                              ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  Next Steps:                                                 ║"
echo "║                                                              ║"
echo "║  1. Edit backend/.env with your API keys and settings       ║"
echo "║                                                              ║"
echo "║  2. Run the application:                                     ║"
echo "║     ./scripts/start.sh                                       ║"
echo "║                                                              ║"
echo "║  3. Open your browser to:                                    ║"
echo "║     http://localhost:3000 (Frontend)                         ║"
echo "║     http://localhost:5000 (Backend API)                      ║"
echo "║                                                              ║"
echo "║  For help: Read README.md                                    ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
