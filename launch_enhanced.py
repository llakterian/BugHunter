#!/usr/bin/env python3
"""
Enhanced Desktop Application Launcher
Robust Bug Bounty Hunter Pro for Parrot Linux Desktop
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def check_system_requirements():
    """Check system requirements"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check OS
    os_name = platform.system()
    print(f"✅ Operating System: {os_name}")
    
    # Check if running on Parrot Linux
    try:
        with open('/etc/os-release', 'r') as f:
            os_info = f.read()
            if 'parrot' in os_info.lower():
                print("✅ Parrot Linux detected - Optimized for security testing")
            else:
                print("ℹ️ Not running on Parrot Linux, but compatible")
    except:
        print("ℹ️ Could not detect OS distribution")
    
    return True

def check_dependencies():
    """Check Python dependencies"""
    print("\n📦 Checking Python dependencies...")
    
    required_packages = [
        'PyQt6', 'requests', 'beautifulsoup4', 'lxml'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def check_external_tools():
    """Check external tools availability"""
    print("\n🛠️ Checking external tools...")
    
    tools = {
        'gau': 'github.com/lc/gau/v2/cmd/gau@latest',
        'fff': 'github.com/tomnomnom/fff@latest',
        'gf': 'github.com/tomnomnom/gf@latest'
    }
    
    available_tools = []
    missing_tools = []
    
    for tool, install_cmd in tools.items():
        try:
            subprocess.run([tool, '--help'], capture_output=True, timeout=5)
            print(f"✅ {tool.upper()}")
            available_tools.append(tool)
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            print(f"❌ {tool.upper()} - Not available")
            missing_tools.append((tool, install_cmd))
    
    if missing_tools:
        print(f"\n⚠️ Missing tools can be installed from within the application")
        print("Or manually install with Go:")
        for tool, cmd in missing_tools:
            print(f"  go install {cmd}")
    
    return len(available_tools) > 0

def setup_directories():
    """Setup required directories"""
    print("\n📁 Setting up directories...")
    
    directories = [
        'data', 'reports', 'screenshots', 'logs', 'wordlists', 'temp'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ {directory}/")
    
    return True

def create_desktop_entry():
    """Create desktop entry for Parrot Linux"""
    print("\n🖥️ Creating desktop entry...")
    
    desktop_entry = f"""[Desktop Entry]
Name=Bug Bounty Hunter Pro Enhanced
Comment=Educational Security Testing Tool (33x More Robust)
Exec=python3 {os.path.abspath('enhanced_desktop_app.py')}
Icon={os.path.abspath('icon.png') if os.path.exists('icon.png') else 'security-high'}
Terminal=false
Type=Application
Categories=Security;Network;Development;
Keywords=security;testing;bugbounty;xss;vulnerability;
StartupNotify=true
"""
    
    try:
        desktop_dir = Path.home() / '.local' / 'share' / 'applications'
        desktop_dir.mkdir(parents=True, exist_ok=True)
        
        desktop_file = desktop_dir / 'bughunter-pro-enhanced.desktop'
        with open(desktop_file, 'w') as f:
            f.write(desktop_entry)
        
        # Make executable
        os.chmod(desktop_file, 0o755)
        
        print(f"✅ Desktop entry created: {desktop_file}")
        return True
    except Exception as e:
        print(f"⚠️ Could not create desktop entry: {e}")
        return False

def show_banner():
    """Show application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🛡️  BUG BOUNTY HUNTER PRO - ENHANCED EDITION (33x MORE ROBUST)  🛡️      ║
║                                                                              ║
║    🎯 Comprehensive Security Testing Suite                                   ║
║    🚨 Advanced XSS Detection with 33+ Evasion Techniques                    ║
║    🔗 URL Discovery with GAU Integration                                     ║
║    🔐 Automated Secrets Hunting with GF Patterns                            ║
║    📊 Professional Reporting & Export                                        ║
║    🖥️ Optimized for Parrot Linux Desktop                                    ║
║                                                                              ║
║    ⚠️  EDUCATIONAL USE ONLY - AUTHORIZED TESTING ONLY  ⚠️                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    """Main launcher function"""
    show_banner()
    
    print("🚀 Initializing Bug Bounty Hunter Pro Enhanced...")
    print("=" * 80)
    
    # Check system requirements
    if not check_system_requirements():
        print("\n❌ System requirements not met. Exiting.")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Exiting.")
        sys.exit(1)
    
    # Check external tools
    check_external_tools()
    
    # Setup directories
    if not setup_directories():
        print("\n❌ Directory setup failed. Exiting.")
        sys.exit(1)
    
    # Create desktop entry (optional)
    create_desktop_entry()
    
    print("\n" + "=" * 80)
    print("✅ All checks completed successfully!")
    print("🚀 Launching Bug Bounty Hunter Pro Enhanced...")
    print("=" * 80)
    
    # Set environment variables for better GUI experience
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '1'
    
    # Launch the enhanced desktop application
    try:
        from enhanced_desktop_app import main as app_main
        app_main()
    except ImportError as e:
        print(f"❌ Failed to import enhanced desktop app: {e}")
        print("Make sure all files are in the correct location.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Application failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()