#!/bin/bash

# Bug Bounty Hunter Pro - Installation Script for Kali Linux
# This script installs all dependencies and sets up the application

set -e

echo "🚀 Bug Bounty Hunter Pro - Installation Script"
echo "================================================"

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

# Check if running on Kali Linux or Parrot OS
check_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [[ "$ID" == "kali" ]]; then
            print_success "Running on Kali Linux"
        elif [[ "$ID" == "parrot" ]]; then
            print_success "Running on Parrot OS"
        else
            print_warning "Not running on Kali Linux or Parrot OS. Some features may not work as expected."
        fi
    fi
}

# Update system packages
update_system() {
    print_status "Updating system packages..."
    sudo apt update && sudo apt upgrade -y
    print_success "System packages updated"
}

# Install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."
    
    # Essential packages (PyQt6 will be installed via pip with its own Qt)
    sudo apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        build-essential \
        git \
        curl \
        wget \
        unzip \
        default-jdk \
        libgl1-mesa-dev \
        libglib2.0-dev \
        pkg-config
    
    print_success "System dependencies installed"
}

# Install OWASP ZAP
install_zap() {
    print_status "Installing OWASP ZAP..."
    
    if ! command -v zaproxy &> /dev/null; then
        # Download and install ZAP
        ZAP_VERSION="2.14.0"
        ZAP_URL="https://github.com/zaproxy/zaproxy/releases/download/v${ZAP_VERSION}/ZAP_${ZAP_VERSION}_Linux.tar.gz"
        
        cd /tmp
        wget -O zap.tar.gz "$ZAP_URL"
        tar -xzf zap.tar.gz
        sudo mv ZAP_${ZAP_VERSION} /opt/zaproxy
        sudo ln -sf /opt/zaproxy/zap.sh /usr/local/bin/zaproxy
        
        print_success "OWASP ZAP installed"
    else
        print_success "OWASP ZAP already installed"
    fi
}

# Create virtual environment and install Python dependencies
setup_python_env() {
    print_status "Setting up Python virtual environment..."
    
    # Create virtual environment
    python3 -m venv bug_bounty_env
    
    # Activate virtual environment
    source bug_bounty_env/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install Python dependencies
    pip install \
        PyQt6 \
        requests \
        python-owasp-zap-v2.4 \
        websockets \
        bcrypt \
        pyjwt \
        cryptography \
        pyinstaller \
        beautifulsoup4 \
        lxml \
        dnspython \
        python-nmap \
        scapy \
        colorlog \
        jsonschema \
        flask \
        uro \
        pytest \
        pytest-cov \
        black \
        flake8 \
        isort \
        mypy \
        pylint
    
    print_success "Python environment set up"
}

# Create application directories
create_directories() {
    print_status "Creating application directories..."
    
    mkdir -p data
    mkdir -p reports
    mkdir -p screenshots
    mkdir -p logs
    mkdir -p wordlists
    
    print_success "Application directories created"
}

# Set up desktop entry
create_desktop_entry() {
    print_status "Creating desktop entry..."
    
    DESKTOP_FILE="$HOME/.local/share/applications/bug-bounty-hunter-pro.desktop"
    CURRENT_DIR=$(pwd)
    
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Bug Bounty Hunter Pro
Comment=Advanced Security Testing Platform
Exec=$CURRENT_DIR/run.sh
Icon=$CURRENT_DIR/assets/icon.png
Terminal=false
Categories=Security;Network;
StartupNotify=true
EOF
    
    chmod +x "$DESKTOP_FILE"
    print_success "Desktop entry created"
}

# Create run script
create_run_script() {
    print_status "Creating run script..."
    
    cat > run.sh << 'EOF'
#!/bin/bash
# Bug Bounty Hunter Pro - Run Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
source bug_bounty_env/bin/activate

# Run the application
python3 main.py "$@"
EOF
    
    chmod +x run.sh
    print_success "Run script created"
}

# Create assets directory and icon
create_assets() {
    print_status "Creating application assets..."
    
    mkdir -p assets
    
    # Create a simple icon (you can replace this with a better one)
    cat > assets/icon.svg << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" fill="#2c3e50"/>
  <circle cx="32" cy="32" r="20" fill="#3498db"/>
  <text x="32" y="38" text-anchor="middle" fill="white" font-family="Arial" font-size="16" font-weight="bold">BB</text>
</svg>
EOF
    
    # Convert SVG to PNG if possible
    if command -v convert &> /dev/null; then
        convert assets/icon.svg assets/icon.png
    fi
    
    print_success "Application assets created"
}

# Set permissions
set_permissions() {
    print_status "Setting file permissions..."
    
    chmod +x main.py
    chmod +x bug_bounty_finder.py
    chmod +x run.sh
    
    print_success "File permissions set"
}

# Main installation function
main() {
    echo
    print_status "Starting Bug Bounty Hunter Pro installation..."
    echo
    
    check_os
    update_system
    install_system_deps
    install_zap
    setup_python_env
    create_directories
    create_run_script
    create_assets
    create_desktop_entry
    set_permissions
    
    echo
    print_success "Installation completed successfully!"
    echo
    echo "🎉 Bug Bounty Hunter Pro is now installed!"
    echo
    echo "To run the application:"
    echo "  ./run.sh"
    echo
    echo "Or double-click the desktop icon in your applications menu."
    echo
    echo "Default login credentials:"
    echo "  Username: admin"
    echo "  Password: BugHunter2024!"
    echo
    echo "For bug bounty site finder:"
    echo "  ./bug_bounty_env/bin/python3 bug_bounty_finder.py"
    echo
    print_warning "Remember to change the default password after first login!"
}

# Run main function
main "$@"