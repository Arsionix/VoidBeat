#!/bin/bash
cd VoidBeat  
export PORT=5000
unset PIP_USER

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment with system site packages..."
    python3 -m venv venv --system-site-packages
fi

# Activate
source venv/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

mkdir -p db static/music static/uploads

echo "Starting VoidBeat..."
python main.py