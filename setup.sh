#!/bin/bash

# PubMed Paper Fetcher Setup Script
# This script automates the installation and setup process

set -e  # Exit on any error

echo "🚀 PubMed Paper Fetcher Setup"
echo "=============================="

# Check if Python 3.10+ is installed
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version is compatible"
else
    echo "❌ Python $python_version found, but Python 3.10+ is required"
    echo "Please install Python 3.10 or higher and try again"
    exit 1
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "📦 Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo "✅ Poetry installed successfully"
    
    # Add Poetry to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
else
    echo "✅ Poetry is already installed"
fi

# Install dependencies
echo "📚 Installing dependencies..."
poetry install

# Verify installation
echo "🔍 Verifying installation..."
poetry run get-papers-list --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Installation verified successfully"
else
    echo "❌ Installation verification failed"
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📖 Next steps:"
echo "1. Start the web server: poetry run python run_web_server.py"
echo "2. Open your browser: http://localhost:3000"
echo "3. Or use the CLI: poetry run get-papers-list 'clinical trial'"
echo ""
echo "📚 For more information, see README.md" 