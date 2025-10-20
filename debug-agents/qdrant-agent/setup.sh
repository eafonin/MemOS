#!/bin/bash
# Setup script for Qdrant debug agent
# Creates virtual environment and installs dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Qdrant Debug Agent Setup"
echo "=========================================="
echo ""

# Check if venv exists
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists at: venv/"
    read -p "Do you want to recreate it? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing venv..."
        rm -rf venv
    else
        echo "✓ Using existing venv"
        source venv/bin/activate
        echo "✓ Virtual environment activated"
        exit 0
    fi
fi

# Create venv
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate venv
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --quiet --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install --quiet -r requirements.txt
    echo "✓ Dependencies installed from requirements.txt"
else
    echo "⚠️  requirements.txt not found, installing manually..."
    pip install --quiet qdrant-client python-dotenv
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To run the agent scripts:"
echo "  source venv/bin/activate"
echo "  python scripts/qdrant_utils.py"
echo ""
echo "Or use the run.sh script:"
echo "  ./run.sh"
echo ""
