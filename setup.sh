#!/bin/bash

echo "========================================"
echo "  Crypto Price Tracker - Setup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.11+ first"
    exit 1
fi

echo "[1/5] Checking Python installation..."
python3 --version
echo ""

echo "[2/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created successfully"
else
    echo "Virtual environment already exists"
fi
echo ""

echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo ""

echo "[4/5] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo ""

echo "[5/5] Initializing database..."
python3 -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"
echo ""

echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python3 app.py"
echo "  3. Visit: http://localhost:5000"
echo ""
echo "For deployment instructions, see DEPLOYMENT.md"
echo ""
