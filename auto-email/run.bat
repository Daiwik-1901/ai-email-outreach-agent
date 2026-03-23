@echo off
REM Start the FastAPI backend and Streamlit frontend

echo.
echo ========================================
echo AI Email Outreach Agent - Startup Script
echo ========================================
echo.

REM Check if virtual environment is activated
if not exist ".venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo Starting FastAPI server on http://localhost:8000...
echo Starting Streamlit UI on http://localhost:8501...
echo.
echo Press Ctrl+C in either terminal to stop.
echo.

REM Start FastAPI server in the background
start "" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for FastAPI to start
timeout /t 2 /nobreak

REM Start Streamlit
echo Launching Streamlit...
streamlit run streamlit_app.py

pause
