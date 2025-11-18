#!/bin/bash

# PhD Application Automator - One-Command Setup Script
# This script sets up both backend and frontend

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════╗"
echo "║  PhD Application Automator - Setup Script             ║"
echo "║  Version 1.0.0                                         ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}📁 Project root: $PROJECT_ROOT${NC}"
echo ""

# Step 1: Check Python version
echo -e "${BLUE}🔍 Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
echo ""

# Step 2: Check Node.js version (optional for now)
echo -e "${BLUE}🔍 Checking Node.js version...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
else
    echo -e "${YELLOW}⚠ Node.js not found (optional for frontend)${NC}"
fi
echo ""

# Step 3: Setup Backend
echo -e "${BLUE}🔧 Setting up backend...${NC}"
cd "$PROJECT_ROOT/backend"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating Python virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
echo -e "${YELLOW}This may take a few minutes...${NC}"
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Python dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi
echo ""

# Create necessary directories
echo -e "${BLUE}Creating necessary directories...${NC}"
mkdir -p logs uploads
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Initialize database
echo -e "${BLUE}🗄️  Initializing database...${NC}"
export FLASK_APP=app.py
python3 << END
from app import app, db
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
END

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database initialized${NC}"
else
    echo -e "${RED}❌ Database initialization failed${NC}"
    exit 1
fi
echo ""

# Step 4: Frontend Setup (optional)
echo -e "${BLUE}🌐 Setting up frontend...${NC}"
if [ -d "$PROJECT_ROOT/frontend" ] && command -v npm &> /dev/null; then
    cd "$PROJECT_ROOT/frontend"

    if [ -f "package.json" ]; then
        echo -e "${BLUE}Installing Node.js dependencies...${NC}"
        npm install

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Node.js dependencies installed${NC}"
        else
            echo -e "${YELLOW}⚠ Frontend setup had issues (you can set it up later)${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ Frontend not configured yet${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Skipping frontend setup (Node.js not found or frontend directory missing)${NC}"
fi
echo ""

# Step 5: Final instructions
cd "$PROJECT_ROOT"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ Setup completed successfully!                      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📝 Next steps:${NC}"
echo ""
echo "1️⃣  Configure your environment variables:"
echo "   ${YELLOW}Edit backend/.env and add your API keys${NC}"
echo "   - GEMINI_API_KEY (already set)"
echo "   - SMTP credentials for email sending"
echo ""
echo "2️⃣  Start the application:"
echo "   ${YELLOW}./scripts/start.sh${NC}"
echo ""
echo "3️⃣  Access the application:"
echo "   - Backend API: ${YELLOW}http://localhost:5000${NC}"
echo "   - Frontend: ${YELLOW}http://localhost:3000${NC} (if configured)"
echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo "   - README.md for full documentation"
echo "   - API documentation: http://localhost:5000/api"
echo ""
echo -e "${GREEN}Happy PhD hunting! 🎓🚀${NC}"
echo ""
