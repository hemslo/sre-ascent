#!/bin/bash

# Create the virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Setup completed. Virtual environment is ready and dependencies are installed."

# Run the app
echo "Running sre-ascent-dev.py..."
python3 sre-ascent-dev.py
