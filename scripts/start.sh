#!/bin/bash

# PhD Application Automator - Start Script
# Starts both backend and frontend servers

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "╔════════════════════════════════════════════════════════╗"
echo "║  PhD Application Automator - Starting Application     ║"
echo "║  Version 1.0.0                                         ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping all services...${NC}"

    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}✓ Backend stopped${NC}"
    fi

    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}✓ Frontend stopped${NC}"
    fi

    echo -e "${BLUE}👋 Goodbye!${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/backend/venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run ./scripts/setup.sh first${NC}"
    exit 1
fi

# Start Backend
echo -e "${BLUE}🚀 Starting backend server...${NC}"
cd "$PROJECT_ROOT/backend"
source venv/bin/activate
export FLASK_APP=app.py
python3 app.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Check if backend started successfully
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${GREEN}✓ Backend server started (PID: $BACKEND_PID)${NC}"
    echo -e "${BLUE}   URL: http://localhost:5000${NC}"
else
    echo -e "${RED}❌ Backend failed to start${NC}"
    echo -e "${YELLOW}Check logs/backend.log for errors${NC}"
    exit 1
fi
echo ""

# Start Frontend (if available)
if [ -d "$PROJECT_ROOT/frontend" ] && [ -f "$PROJECT_ROOT/frontend/package.json" ]; then
    echo -e "${BLUE}🌐 Starting frontend server...${NC}"
    cd "$PROJECT_ROOT/frontend"

    if command -v npm &> /dev/null; then
        npm start > ../logs/frontend.log 2>&1 &
        FRONTEND_PID=$!

        echo -e "${GREEN}✓ Frontend server starting (PID: $FRONTEND_PID)${NC}"
        echo -e "${BLUE}   URL: http://localhost:3000${NC}"
    else
        echo -e "${YELLOW}⚠ npm not found, skipping frontend${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Frontend not configured${NC}"
fi
echo ""

echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ Application is running!                            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📊 Services:${NC}"
echo "   - Backend API: ${GREEN}http://localhost:5000${NC}"
echo "   - API Docs: ${GREEN}http://localhost:5000/api${NC}"
echo "   - Health Check: ${GREEN}http://localhost:5000/health${NC}"
if [ ! -z "$FRONTEND_PID" ]; then
    echo "   - Frontend: ${GREEN}http://localhost:3000${NC}"
fi
echo ""
echo -e "${BLUE}📝 Logs:${NC}"
echo "   - Backend: ${YELLOW}logs/backend.log${NC}"
if [ ! -z "$FRONTEND_PID" ]; then
    echo "   - Frontend: ${YELLOW}logs/frontend.log${NC}"
fi
echo ""
echo -e "${RED}Press Ctrl+C to stop all services${NC}"
echo ""

# Wait for user to press Ctrl+C
while true; do
    sleep 1
done
