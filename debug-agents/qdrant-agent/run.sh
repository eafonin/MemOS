#!/bin/bash
# Run Qdrant debug agent scripts with automatic venv activation
# Usage: ./run.sh [script arguments]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Please run setup.sh first:"
    echo "  ./setup.sh"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Load environment variables
if [ -f "config.env" ]; then
    source config.env
fi

# Run the script
python scripts/qdrant_utils.py "$@"
