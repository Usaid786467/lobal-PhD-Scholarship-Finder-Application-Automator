#!/bin/bash

# PhD Application Automator - Start Script
# One-command start for backend and frontend

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║     🚀 PhD APPLICATION AUTOMATOR                            ║"
echo "║                                                              ║"
echo "║     Starting your PhD application automation system...      ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."

    if [ ! -z "$BACKEND_PID" ] && kill -0 $BACKEND_PID 2>/dev/null; then
        echo "   Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
    fi

    if [ ! -z "$FRONTEND_PID" ] && kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "   Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
    fi

    echo "✅ All services stopped"
    exit 0
}

# Register cleanup function
trap cleanup SIGINT SIGTERM

# Start backend
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STARTING BACKEND API"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd backend

# Activate virtual environment
if [ -d "venv" ]; then
    echo "📦 Activating Python virtual environment..."
    source venv/bin/activate || . venv/Scripts/activate
else
    echo "❌ Virtual environment not found!"
    echo "   Please run ./scripts/setup.sh first"
    exit 1
fi

# Start backend
echo "🔧 Starting Flask backend server..."
python app.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!

echo "   ✅ Backend started (PID: $BACKEND_PID)"
echo "   📝 Logs: logs/backend.log"
echo "   🌐 URL: http://localhost:5000"

cd ..

# Start frontend (if available)
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  STARTING FRONTEND"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    cd frontend

    echo "⚛️  Starting React development server..."
    npm start > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!

    echo "   ✅ Frontend started (PID: $FRONTEND_PID)"
    echo "   📝 Logs: logs/frontend.log"
    echo "   🌐 URL: http://localhost:3000"

    cd ..
else
    echo ""
    echo "⚠️  Frontend not available. Only backend is running."
fi

# Create logs directory
mkdir -p logs

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║     ✅ APPLICATION RUNNING                                  ║"
echo "║                                                              ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  Services:                                                   ║"
echo "║                                                              ║"
echo "║  🔧 Backend API:    http://localhost:5000                   ║"
echo "║  ⚛️  Frontend Web:   http://localhost:3000                   ║"
echo "║                                                              ║"
echo "║  📚 API Docs:       http://localhost:5000/api/docs          ║"
echo "║  ❤️  Health Check:   http://localhost:5000/api/health        ║"
echo "║                                                              ║"
echo "║  Press CTRL+C to stop all services                          ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Wait for processes
if [ ! -z "$FRONTEND_PID" ]; then
    wait $BACKEND_PID $FRONTEND_PID
else
    wait $BACKEND_PID
fi
