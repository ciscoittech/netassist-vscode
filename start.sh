#!/bin/bash

# NetAssist VS Code Extension Startup Script
# Starts the sanitization server and provides setup guidance

set -e

echo "🚀 NetAssist - AI Network Engineer VS Code Extension"
echo "====================================================="

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the vscode-extension directory"
    exit 1
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check Node.js for extension development
if command -v node &> /dev/null; then
    echo "✅ Node.js found: $(node --version)"
else
    echo "⚠️  Node.js not found (needed for extension development)"
fi

# Setup sanitization server
echo ""
echo "🔧 Setting up sanitization server..."
cd sanitization-server

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Test sanitization
echo ""
echo "🧪 Testing sanitization functionality..."
if python simple_test.py > /dev/null 2>&1; then
    echo "✅ Sanitization tests passed"
else
    echo "❌ Sanitization tests failed"
    echo "Running detailed test..."
    python simple_test.py
    exit 1
fi

# Start sanitization server
echo ""
echo "🌐 Starting sanitization server on http://localhost:8000"
echo "📊 Health check: http://localhost:8000/api/health"
echo "📝 API docs: http://localhost:8000/docs"
echo ""
echo "🔴 Press Ctrl+C to stop the server"
echo ""

# Check if port 8000 is already in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8000 is already in use"
    echo "Checking if it's our sanitization server..."

    if curl -s http://localhost:8000/api/health | grep -q "healthy"; then
        echo "✅ NetAssist sanitization server is already running"
        echo "🎯 Ready for VS Code extension use!"
        exit 0
    else
        echo "❌ Port 8000 is occupied by another service"
        echo "Please stop the other service or change the port in configuration"
        exit 1
    fi
fi

# Start the server
python main.py