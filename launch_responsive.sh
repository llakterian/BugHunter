#!/bin/bash

# 🚀 Bug Bounty Hunter Pro - Responsive Launch Script
# Automatically sets up environment and launches the responsive GUI

echo "🛡️  Bug Bounty Hunter Pro - Enhanced Responsive Edition"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "enhanced_desktop_app.py" ]; then
    echo "❌ Error: enhanced_desktop_app.py not found!"
    echo "Please run this script from the BugHunter directory"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Python Version: $python_version"

# Check if virtual environment exists
if [ ! -d "bughunter-env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv bughunter-env
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        echo "💡 Try: sudo apt install python3-venv python3-full"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source bughunter-env/bin/activate

# Check if dependencies are installed
echo "📋 Checking dependencies..."
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installing Python dependencies..."
    pip install PyQt6 requests beautifulsoup4 lxml bcrypt PyJWT cryptography
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        echo "💡 Try running with --break-system-packages if needed"
        exit 1
    fi
fi

# Check screen resolution
echo "📺 Detecting screen resolution..."
if command -v xrandr &> /dev/null; then
    resolution=$(xrandr | grep '*' | awk '{print $1}' | head -1)
    echo "   Current Resolution: $resolution"
else
    echo "   Resolution detection not available"
fi

# Launch the application
echo "🚀 Launching Bug Bounty Hunter Pro..."
echo "   Features: Responsive GUI, Auto-sizing, Cross-platform"
echo "   Compatibility: 1366x768 to 3440x1440 screens"
echo ""

# Set display variable if not set (for some Linux environments)
if [ -z "$DISPLAY" ]; then
    export DISPLAY=:0
fi

# Launch with error handling
python3 enhanced_desktop_app.py

launch_result=$?

if [ $launch_result -eq 0 ]; then
    echo ""
    echo "✅ Application closed successfully"
else
    echo ""
    echo "❌ Application encountered an error (exit code: $launch_result)"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "   1. Make sure you have a GUI environment running"
    echo "   2. Check if X11 forwarding is enabled (for SSH)"
    echo "   3. Verify PyQt6 installation: python3 -c 'import PyQt6'"
    echo "   4. Try: export DISPLAY=:0"
fi

echo ""
echo "📚 For help and documentation:"
echo "   • README_ENHANCED.md - Complete feature guide"
echo "   • RESPONSIVE_IMPROVEMENTS.md - GUI improvements"
echo "   • QUICK_START.md - Getting started guide"
echo ""
echo "🌟 Thank you for using Bug Bounty Hunter Pro!"