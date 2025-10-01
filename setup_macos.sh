#!/bin/bash

# Bug Bounty Hunter Pro - macOS Setup Script
# This script sets up the application for macOS

set -e

echo "🍎 Bug Bounty Hunter Pro - macOS Setup"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on macOS
check_macos() {
    if [[ "$OSTYPE" != "darwin"* ]]; then
        print_error "This script is designed for macOS only."
        exit 1
    fi
    print_success "Running on macOS $(sw_vers -productVersion)"
}

# Check if Homebrew is installed
check_homebrew() {
    if ! command -v brew &> /dev/null; then
        print_warning "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        print_success "Homebrew is installed"
    fi
}

# Install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."

    # Update Homebrew
    brew update

    # Install Python 3.11 if not available
    if ! brew list python@3.11 &> /dev/null; then
        brew install python@3.11
    fi

    # Install Qt6
    brew install qt@6

    # Install other dependencies
    brew install \
        git \
        curl \
        wget \
        libffi \
        openssl \
        sqlite3 \
        xz \
        zlib

    print_success "System dependencies installed"
}

# Create virtual environment
setup_python_env() {
    print_status "Setting up Python virtual environment..."

    # Remove existing environment if it exists
    if [ -d "bug_bounty_env" ]; then
        rm -rf bug_bounty_env
    fi

    # Create new virtual environment with Python 3.11
    python3.11 -m venv bug_bounty_env

    # Activate virtual environment
    source bug_bounty_env/bin/activate

    # Upgrade pip
    pip install --upgrade pip

    print_success "Virtual environment created"

    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip install \
        PyQt6 \
        requests \
        beautifulsoup4 \
        lxml \
        bcrypt \
        PyJWT \
        cryptography \
        scapy \
        websockets \
        colorlog \
        jsonschema \
        flask \
        pytest \
        dnspython

    # Optional dependencies (install if available)
    pip install python-nmap || print_warning "python-nmap not available on macOS"
    pip install uro || print_warning "uro not available"

    print_success "Python dependencies installed"
}

# Create macOS application bundle
create_macos_app() {
    print_status "Creating macOS application bundle..."

    APP_NAME="Bug Bounty Hunter Pro"
    APP_DIR="$APP_NAME.app"
    CONTENTS_DIR="$APP_DIR/Contents"
    MACOS_DIR="$CONTENTS_DIR/MacOS"
    RESOURCES_DIR="$CONTENTS_DIR/Resources"

    # Create directory structure
    mkdir -p "$MACOS_DIR"
    mkdir -p "$RESOURCES_DIR"

    # Create Info.plist
    cat > "$CONTENTS_DIR/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>BugBountyHunterPro</string>
    <key>CFBundleIdentifier</key>
    <string>com.bugbountyhunter.pro</string>
    <key>CFBundleName</key>
    <string>Bug Bounty Hunter Pro</string>
    <key>CFBundleVersion</key>
    <string>2.0</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.12</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSSupportsAutomaticGraphicsSwitching</key>
    <true/>
</dict>
</plist>
EOF

    # Create launcher script
    cat > "$MACOS_DIR/BugBountyHunterPro" << 'EOF'
#!/bin/bash

# Bug Bounty Hunter Pro macOS Launcher
# Get the directory where the app bundle is located
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
cd "$APP_DIR"

# Set environment variables for Qt
export QT_QPA_PLATFORM_PLUGIN_PATH="$APP_DIR/bug_bounty_env/lib/python3.11/site-packages/PyQt6/Qt6/plugins"
export DYLD_LIBRARY_PATH="$APP_DIR/bug_bounty_env/lib:$DYLD_LIBRARY_PATH"

# Activate virtual environment
source bug_bounty_env/bin/activate

# Set Python path
export PYTHONPATH="$APP_DIR:$PYTHONPATH"

# Run the application
python3.11 main.py
EOF

    # Make launcher executable
    chmod +x "$MACOS_DIR/BugBountyHunterPro"

    # Copy icon if available
    if [ -f "assets/icon.png" ]; then
        cp "assets/icon.png" "$RESOURCES_DIR/"
        # Convert PNG to ICNS if sips is available
        if command -v sips &> /dev/null; then
            sips -s format icns "assets/icon.png" --out "$RESOURCES_DIR/icon.icns" 2>/dev/null || true
        fi
    fi

    print_success "macOS application bundle created at: $APP_DIR"
}

# Create desktop shortcut (alias)
create_desktop_shortcut() {
    print_status "Creating desktop shortcut..."

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    APP_PATH="$SCRIPT_DIR/Bug Bounty Hunter Pro.app"

    # Create alias on Desktop
    DESKTOP_SHORTCUT="$HOME/Desktop/Bug Bounty Hunter Pro"

    if [ -d "$APP_PATH" ]; then
        # Remove existing shortcut
        if [ -L "$DESKTOP_SHORTCUT" ] || [ -f "$DESKTOP_SHORTCUT" ]; then
            rm -f "$DESKTOP_SHORTCUT"
        fi

        # Create new alias
        ln -s "$APP_PATH" "$DESKTOP_SHORTCUT"
        print_success "Desktop shortcut created: $DESKTOP_SHORTCUT"
    else
        print_warning "App bundle not found, skipping desktop shortcut"
    fi
}

# Create run script for terminal use
create_run_script() {
    print_status "Creating run script..."

    cat > run_macos.sh << 'EOF'
#!/bin/bash
# Bug Bounty Hunter Pro - macOS Run Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Set environment variables for Qt
export QT_QPA_PLATFORM_PLUGIN_PATH="$SCRIPT_DIR/bug_bounty_env/lib/python3.11/site-packages/PyQt6/Qt6/plugins"
export DYLD_LIBRARY_PATH="$SCRIPT_DIR/bug_bounty_env/lib:$DYLD_LIBRARY_PATH"

# Activate virtual environment
source bug_bounty_env/bin/activate

# Set Python path
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Run the application
python3.11 main.py "$@"
EOF

    chmod +x run_macos.sh
    print_success "Run script created: run_macos.sh"
}

# Test the application
test_app() {
    print_status "Testing application..."

    source bug_bounty_env/bin/activate

    # Quick import test
    if python3.11 -c "import PyQt6.QtWidgets; print('PyQt6 OK')"; then
        print_success "PyQt6 is working"
    else
        print_error "PyQt6 not working properly"
        return 1
    fi

    # Test main imports
    if python3.11 -c "import auth_manager; import scanner_engine; print('Core imports OK')"; then
        print_success "Core modules import successfully"
    else
        print_error "Core modules failed to import"
        return 1
    fi

    print_success "Application test passed"
}

# Set permissions
set_permissions() {
    print_status "Setting file permissions..."

    chmod +x main.py
    chmod +x run_macos.sh
    chmod +x setup_macos.sh

    print_success "File permissions set"
}

# Main setup function
main() {
    echo
    print_status "Starting Bug Bounty Hunter Pro macOS setup..."
    echo

    check_macos
    check_homebrew
    install_system_deps
    setup_python_env
    create_macos_app
    create_desktop_shortcut
    create_run_script
    set_permissions
    test_app

    echo
    print_success "macOS setup completed successfully!"
    echo
    echo "🎉 Bug Bounty Hunter Pro is now ready for macOS!"
    echo
    echo "To run the application:"
    echo "  ./run_macos.sh"
    echo
    echo "Or double-click the app bundle:"
    echo "  Bug Bounty Hunter Pro.app"
    echo
    echo "Desktop shortcut created at:"
    echo "  ~/Desktop/Bug Bounty Hunter Pro"
    echo
    echo "Default login credentials:"
    echo "  Username: admin"
    echo "  Password: (run reset_admin.py to set new password)"
    echo
    print_warning "Remember to change the default password after first login!"
}

# Run main function
main "$@"