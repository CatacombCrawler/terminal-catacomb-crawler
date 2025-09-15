#!/bin/bash

# Terminal Dungeon Crawler Setup Script
echo "🏰 Setting up Terminal Dungeon Crawler development environment..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Check if virtual environment already exists
if [ -d "venv" ]; then
    echo "📦 Virtual environment already exists, skipping creation..."
else
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "🎮 To run the game:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "🔚 To deactivate virtual environment:"
echo "   deactivate"