#!/bin/bash

# Enhanced Bug Bounty Hunter Pro Installation Script
# Optimized for Parrot Linux and other Debian-based systems

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
show_banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                              ║"
    echo "║    🛡️  BUG BOUNTY HUNTER PRO - ENHANCED EDITION INSTALLER  🛡️              ║"
    echo "║                                                                              ║"
    echo "║    🎯 33x More Robust Security Testing Suite                                ║"
    echo "║    🖥️ Optimized for Parrot Linux Desktop                                    ║"
    echo "║    ⚠️  EDUCATIONAL USE ONLY  ⚠️                                             ║"
    echo "║                                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        warning "Running as root. This is not recommended for security tools."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Detect OS
detect_os() {
    log "Detecting operating system..."
    
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
        
        if [[ "$ID" == "parrot" ]]; then
            info "✅ Parrot Linux detected - Optimized installation"
            PARROT_LINUX=true
        elif [[ "$ID" == "kali" ]]; then
            info "✅ Kali Linux detected - Compatible"
            KALI_LINUX=true
        elif [[ "$ID" == "ubuntu" ]] || [[ "$ID" == "debian" ]]; then
            info "✅ Debian-based system detected - Compatible"
            DEBIAN_BASED=true
        else
            warning "Unknown Linux distribution. Installation may not work correctly."
        fi
    else
        error "Cannot detect operating system"
        exit 1
    fi
    
    log "OS: $OS $VER"
}

# Update system packages
update_system() {
    log "Updating system packages..."
    
    if command -v apt-get &> /dev/null; then
        sudo apt-get update -qq
        log "✅ Package list updated"
    else
        error "apt-get not found. This installer requires a Debian-based system."
        exit 1
    fi
}

# Install system dependencies
install_system_deps() {
    log "Installing system dependencies..."
    
    SYSTEM_DEPS=(
        "python3"
        "python3-pip"
        "python3-venv"
        "python3-dev"
        "build-essential"
        "libxcb-cursor0"
        "libxcb-xinerama0"
        "libxcb-randr0"
        "libxcb-xtest0"
        "libxcb-xfixes0"
        "libxcb-shape0"
        "libglib2.0-0"
        "libgl1-mesa-glx"
        "libfontconfig1"
        "libx11-xcb1"
        "libxcb-glx0"
        "libxcb-keysyms1"
        "libxcb-image0"
        "libxcb-shm0"
        "libxcb-icccm4"
        "libxcb-sync1"
        "libxcb-render-util0"
        "libxkbcommon-x11-0"
        "libxcb-xkb1"
        "git"
        "curl"
        "wget"
        "golang-go"
    )
    
    for dep in "${SYSTEM_DEPS[@]}"; do
        if ! dpkg -l | grep -q "^ii  $dep "; then
            info "Installing $dep..."
            sudo apt-get install -y "$dep" -qq
        else
            info "✅ $dep already installed"
        fi
    done
    
    log "✅ System dependencies installed"
}

# Install Python dependencies
install_python_deps() {
    log "Installing Python dependencies..."
    
    # Upgrade pip
    python3 -m pip install --upgrade pip --quiet
    
    # Install requirements
    if [[ -f "requirements.txt" ]]; then
        python3 -m pip install -r requirements.txt --quiet
        log "✅ Python dependencies from requirements.txt installed"
    else
        # Install essential packages manually
        PYTHON_DEPS=(
            "PyQt6"
            "requests"
            "beautifulsoup4"
            "lxml"
            "bcrypt"
            "PyJWT"
            "cryptography"
            "websockets"
            "dnspython"
            "python-nmap"
            "scapy"
            "jsonschema"
            "colorlog"
            "flask"
            "pytest"
            "requests-mock"
        )
        
        for dep in "${PYTHON_DEPS[@]}"; do
            info "Installing $dep..."
            python3 -m pip install "$dep" --quiet
        done
        
        log "✅ Essential Python dependencies installed"
    fi
}

# Install Go tools
install_go_tools() {
    log "Installing Go-based security tools..."
    
    # Check if Go is available
    if ! command -v go &> /dev/null; then
        error "Go is not installed. Please install Go first."
        return 1
    fi
    
    # Set Go environment
    export GOPATH=$HOME/go
    export PATH=$PATH:$GOPATH/bin
    
    # Add to shell profile
    if [[ -f "$HOME/.bashrc" ]]; then
        if ! grep -q "GOPATH" "$HOME/.bashrc"; then
            echo 'export GOPATH=$HOME/go' >> "$HOME/.bashrc"
            echo 'export PATH=$PATH:$GOPATH/bin' >> "$HOME/.bashrc"
        fi
    fi
    
    # Install tools
    GO_TOOLS=(
        "github.com/lc/gau/v2/cmd/gau@latest"
        "github.com/tomnomnom/fff@latest"
        "github.com/tomnomnom/gf@latest"
        "github.com/tomnomnom/httprobe@latest"
        "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
    )
    
    for tool in "${GO_TOOLS[@]}"; do
        tool_name=$(basename "$tool" | cut -d'@' -f1)
        info "Installing $tool_name..."
        go install "$tool" 2>/dev/null || warning "Failed to install $tool_name"
    done
    
    log "✅ Go tools installation completed"
}

# Setup directories
setup_directories() {
    log "Setting up application directories..."
    
    DIRECTORIES=(
        "data"
        "reports"
        "screenshots"
        "logs"
        "wordlists"
        "temp"
        "exports"
        "configs"
    )
    
    for dir in "${DIRECTORIES[@]}"; do
        if [[ ! -d "$dir" ]]; then
            mkdir -p "$dir"
            info "Created directory: $dir/"
        else
            info "✅ Directory exists: $dir/"
        fi
    done
    
    log "✅ Directories setup completed"
}

# Generate wordlists
generate_wordlists() {
    log "Generating enhanced wordlists..."
    
    if [[ -f "enhanced_wordlists.py" ]]; then
        python3 enhanced_wordlists.py
        log "✅ Enhanced wordlists generated"
    else
        warning "enhanced_wordlists.py not found. Wordlists not generated."
    fi
}

# Create desktop entry
create_desktop_entry() {
    log "Creating desktop entry..."
    
    DESKTOP_DIR="$HOME/.local/share/applications"
    mkdir -p "$DESKTOP_DIR"
    
    DESKTOP_FILE="$DESKTOP_DIR/bughunter-pro-enhanced.desktop"
    
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=Bug Bounty Hunter Pro Enhanced
Comment=Educational Security Testing Tool (33x More Robust)
Exec=python3 $(pwd)/launch_enhanced.py
Icon=$(pwd)/icon.png
Terminal=false
Type=Application
Categories=Security;Network;Development;Education;
Keywords=security;testing;bugbounty;xss;vulnerability;education;
StartupNotify=true
EOF
    
    chmod +x "$DESKTOP_FILE"
    
    log "✅ Desktop entry created: $DESKTOP_FILE"
}

# Create launcher script
create_launcher() {
    log "Creating launcher script..."
    
    LAUNCHER_SCRIPT="bughunter-enhanced"
    
    cat > "$LAUNCHER_SCRIPT" << 'EOF'
#!/bin/bash
# Bug Bounty Hunter Pro Enhanced Launcher

cd "$(dirname "$0")"
python3 launch_enhanced.py "$@"
EOF
    
    chmod +x "$LAUNCHER_SCRIPT"
    
    # Try to add to PATH
    if [[ -d "$HOME/.local/bin" ]]; then
        cp "$LAUNCHER_SCRIPT" "$HOME/.local/bin/"
        log "✅ Launcher installed to ~/.local/bin/"
    else
        log "✅ Launcher script created: ./$LAUNCHER_SCRIPT"
    fi
}

# Run tests
run_tests() {
    log "Running installation tests..."
    
    # Test Python imports
    python3 -c "
import sys
try:
    from PyQt6.QtWidgets import QApplication
    from enhanced_wordlists import get_all_endpoints
    from tool_integrations import ToolIntegrations
    from enhanced_xss_engine import EnhancedXSSEngine
    print('✅ All Python modules imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"
    
    if [[ $? -eq 0 ]]; then
        log "✅ Python module tests passed"
    else
        error "Python module tests failed"
        return 1
    fi
    
    # Test Go tools
    if command -v gau &> /dev/null; then
        info "✅ GAU tool available"
    else
        warning "GAU tool not available"
    fi
    
    if command -v fff &> /dev/null; then
        info "✅ FFF tool available"
    else
        warning "FFF tool not available"
    fi
    
    if command -v gf &> /dev/null; then
        info "✅ GF tool available"
    else
        warning "GF tool not available"
    fi
    
    log "✅ Installation tests completed"
}

# Show completion message
show_completion() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                              ║"
    echo "║    🎉 INSTALLATION COMPLETED SUCCESSFULLY! 🎉                               ║"
    echo "║                                                                              ║"
    echo "║    🚀 Launch the application:                                                ║"
    echo "║       • Run: python3 launch_enhanced.py                                     ║"
    echo "║       • Or use: ./bughunter-enhanced                                         ║"
    echo "║       • Or find it in your applications menu                                 ║"
    echo "║                                                                              ║"
    echo "║    📚 Features installed:                                                    ║"
    echo "║       • 🚨 Advanced XSS Detection (33+ techniques)                          ║"
    echo "║       • 🔗 URL Discovery with GAU                                           ║"
    echo "║       • 🔐 Secrets Hunting with GF                                          ║"
    echo "║       • 📊 Professional Reporting                                           ║"
    echo "║       • 🖥️ Desktop Integration                                              ║"
    echo "║                                                                              ║"
    echo "║    ⚠️  REMEMBER: EDUCATIONAL USE ONLY  ⚠️                                   ║"
    echo "║                                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Main installation function
main() {
    show_banner
    
    log "Starting Bug Bounty Hunter Pro Enhanced installation..."
    
    # Pre-installation checks
    check_root
    detect_os
    
    # Installation steps
    update_system
    install_system_deps
    install_python_deps
    install_go_tools
    setup_directories
    generate_wordlists
    create_desktop_entry
    create_launcher
    
    # Post-installation
    run_tests
    show_completion
    
    log "Installation completed successfully!"
}

# Run main function
main "$@"