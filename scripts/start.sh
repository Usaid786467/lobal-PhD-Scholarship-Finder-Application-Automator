#!/bin/bash

# PhD Application Automation System - Start Script
# One-command start for backend and frontend

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  PhD Application Automation System - Starting...             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if running from project root
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}✗ Error: Please run this script from the project root directory${NC}"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $(jobs -p) 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Check if setup was run
if [ ! -d "backend/venv" ]; then
    echo -e "${RED}✗ Backend not set up. Please run: ./scripts/setup.sh${NC}"
    exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
    echo -e "${RED}✗ Frontend not set up. Please run: ./scripts/setup.sh${NC}"
    exit 1
fi

# Start Backend
echo -e "${YELLOW}[1/2] Starting Flask backend...${NC}"
cd backend
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}✗ .env file not found. Please copy .env.example and configure it.${NC}"
    exit 1
fi

# Start Flask in background
python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✓ Backend started on http://localhost:5000${NC}"
else
    echo -e "${RED}✗ Backend failed to start${NC}"
    exit 1
fi

cd ..

# Start Frontend
echo -e "${YELLOW}[2/2] Starting React frontend...${NC}"
cd frontend

# Start Vite in background
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 3

if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}✓ Frontend started on http://localhost:3000${NC}"
else
    echo -e "${RED}✗ Frontend failed to start${NC}"
    kill $BACKEND_PID
    exit 1
fi

cd ..

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Application Running! 🚀                                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Access the application:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:5000"
echo "  API Docs: http://localhost:5000/api"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Keep script running
wait
