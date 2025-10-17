@echo off
echo ========================================
echo   Crypto Price Tracker - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 from python.org
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version
echo.

echo [2/5] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created successfully
) else (
    echo Virtual environment already exists
)
echo.

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [4/5] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
echo.

echo [5/5] Initializing database...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run the app: python app.py
echo   3. Visit: http://localhost:5000
echo.
echo For deployment instructions, see DEPLOYMENT.md
echo.
pause
