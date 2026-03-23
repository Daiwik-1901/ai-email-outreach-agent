#!/bin/bash
# Start the FastAPI backend and Streamlit frontend

echo ""
echo "========================================"
echo "AI Email Outreach Agent - Startup Script"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: python -m venv .venv"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

echo "Starting FastAPI server on http://localhost:8000..."
echo "Starting Streamlit UI on http://localhost:8501..."
echo ""
echo "Press Ctrl+C in either terminal to stop."
echo ""

# Start FastAPI server in the background
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Wait a moment for FastAPI to start
sleep 2

# Start Streamlit (foreground)
streamlit run streamlit_app.py

# Clean up on exit
kill $FASTAPI_PID 2>/dev/null
