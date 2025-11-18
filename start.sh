#!/bin/bash

# Task Manager - Start Script
# This script helps you start the backend and frontend together

echo "🚀 Starting Task Manager..."
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the task_manager root directory"
    exit 1
fi

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Check if backend is already running
if check_port 5000; then
    echo -e "${YELLOW}⚠️  Backend is already running on port 5000${NC}"
else
    echo -e "${BLUE}📦 Starting Backend API...${NC}"
    cd backend
    if [ -d "myenv" ]; then
        source myenv/bin/activate
    elif [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "❌ Error: No virtual environment found in backend/"
        exit 1
    fi
    python app.py &
    BACKEND_PID=$!
    cd ..
    echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
    sleep 2
fi

# Check if frontend is already running
if check_port 5173; then
    echo -e "${YELLOW}⚠️  Frontend is already running on port 5173${NC}"
else
    echo -e "${BLUE}🎨 Starting Frontend...${NC}"
    cd frontend
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing dependencies..."
        npm install
    fi
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Task Manager is running!${NC}"
echo ""
echo "📍 Backend API: http://127.0.0.1:5000"
echo "📍 Frontend:    http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
