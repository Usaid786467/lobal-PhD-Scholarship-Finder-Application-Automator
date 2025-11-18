#!/bin/bash

# PhD Application Automation System - Setup Script
# One-command setup for the entire application

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  PhD Application Automation System - Setup                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running from project root
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}✗ Error: Please run this script from the project root directory${NC}"
    exit 1
fi

echo -e "${YELLOW}[1/7] Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ Node.js is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}✗ npm is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ npm found${NC}"

echo ""
echo -e "${YELLOW}[2/7] Setting up Python virtual environment...${NC}"
cd backend

if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
source venv/bin/activate

echo ""
echo -e "${YELLOW}[3/7] Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

echo ""
echo -e "${YELLOW}[4/7] Setting up environment variables...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created from .env.example${NC}"
    echo -e "${YELLOW}⚠ Please edit backend/.env with your configuration${NC}"
else
    echo ".env already exists, skipping..."
fi

echo ""
echo -e "${YELLOW}[5/7] Initializing database...${NC}"
python3 -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all(); print('✓ Database initialized')"
echo -e "${GREEN}✓ Database tables created${NC}"

cd ..

echo ""
echo -e "${YELLOW}[6/7] Installing frontend dependencies...${NC}"
cd frontend

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Frontend .env created${NC}"
fi

npm install
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"

cd ..

echo ""
echo -e "${YELLOW}[7/7] Making scripts executable...${NC}"
chmod +x scripts/*.sh
echo -e "${GREEN}✓ Scripts are executable${NC}"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Setup Complete! ✨                                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your API keys and SMTP settings"
echo "2. Run: ./scripts/start.sh to start the application"
echo ""
echo "Documentation: See README.md for more information"
echo ""
