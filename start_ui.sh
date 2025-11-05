#!/bin/bash

# AI Coding Agent - UI Launcher
# This script starts both the backend API and frontend UI

echo "🤖 AI Coding Agent - Starting Web UI"
echo "===================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo "Please create a .env file with your OPENAI_API_KEY"
    echo ""
    echo "Example:"
    echo "OPENAI_API_KEY=sk-proj-your-key-here"
    echo "OPENAI_MODEL=gpt-4-turbo-preview"
    exit 1
fi

# Start backend
echo ""
echo -e "${BLUE}🚀 Starting Backend API...${NC}"
source venv/bin/activate
python -m api.main &
BACKEND_PID=$!

# Wait for backend to start
echo -e "${YELLOW}⏳ Waiting for backend to start...${NC}"
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend running on http://localhost:8000${NC}"
else
    echo -e "${RED}❌ Backend failed to start${NC}"
    kill $BACKEND_PID
    exit 1
fi

# Start frontend
echo ""
echo -e "${BLUE}🎨 Starting Frontend UI...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}✅ UI Started Successfully!${NC}"
echo ""
echo "===================================="
echo -e "${GREEN}🌐 Open your browser:${NC}"
echo -e "   ${BLUE}http://localhost:3000${NC}"
echo ""
echo -e "${YELLOW}📊 Backend API:${NC}"
echo -e "   ${BLUE}http://localhost:8000${NC}"
echo -e "   ${BLUE}http://localhost:8000/docs${NC} (API docs)"
echo ""
echo "===================================="
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both services${NC}"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait


