#!/bin/bash

# VaR Estimation Tool - Installation Script for macOS/Linux
# This script sets up the VaR Estimation Tool with all dependencies

set -e  # Exit on error

echo "================================================"
echo "VaR Estimation Tool - Installation (macOS/Linux)"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    echo "   Visit: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Using existing environment..."
    source venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created"
fi

echo ""
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "================================================"
echo "Installation complete!"
echo "================================================"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To launch the GUI application, run:"
echo "  python3 main.py"
echo ""
echo "To run integration tests, run:"
echo "  python3 integration_test.py"
echo ""
echo "To use the data reader interactively, run:"
echo "  python3 data_reader.py"
echo ""
echo "For more information, see README.md or QUICKSTART.md"
echo ""
