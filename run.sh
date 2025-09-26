#!/bin/bash
# Bug Bounty Hunter Pro - Robust Launch Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🎯 Bug Bounty Hunter Pro - Launcher"
echo "=================================="

# Function to check requirements
check_requirements() {
    echo "🔍 Checking requirements..."
    
    # Check if virtual environment exists
    if [ ! -d "bug_bounty_env" ]; then
        echo "❌ Virtual environment not found"
        echo "💡 Run: ./install.sh"
        return 1
    fi
    
    # Check critical files
    critical_files=("main.py" "main_dashboard.py" "scanner_engine.py" "config_manager.py")
    for file in "${critical_files[@]}"; do
        if [ ! -f "$file" ]; then
            echo "❌ Missing critical file: $file"
            return 1
        fi
    done
    
    # Check wordlists directory
    if [ ! -d "wordlists" ]; then
        echo "❌ Wordlists directory missing"
        echo "💡 Run: ./install.sh"
        return 1
    fi
    
    echo "✅ All requirements satisfied"
    return 0
}

# Function to launch application
launch_app() {
    echo "🚀 Launching Bug Bounty Hunter Pro..."
    
    # Activate virtual environment
    source bug_bounty_env/bin/activate
    
    # Set environment variables for better stability
    export QT_LOGGING_RULES="*.debug=false"
    
    # Launch with error handling
    if python3 launch_hunter.py "$@"; then
        echo "✅ Application closed normally"
    else
        echo "❌ Application encountered an error"
        echo "💡 Check the output above for details"
        echo "💡 Try: python3 quick_test.py"
    fi
}

# Main execution
main() {
    if check_requirements; then
        launch_app "$@"
    else
        echo ""
        echo "🔧 To fix issues, run:"
        echo "   ./install.sh"
        echo ""
        echo "🧪 To test the system:"
        echo "   python3 quick_test.py"
        exit 1
    fi
}

# Handle Ctrl+C gracefully
trap 'echo ""; echo "👋 Goodbye!"; exit 0' INT

# Run main function
main "$@"