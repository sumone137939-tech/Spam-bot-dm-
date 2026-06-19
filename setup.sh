#!/bin/bash

echo "======================================"
echo "🤖 ABHINAV DM BOT - Setup Script"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "For Termux, run: pkg install python"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your bot tokens"
echo "2. Run: python dm_bot_ultrafast.py"
echo ""
