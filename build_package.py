#!/usr/bin/env python3
"""
Package Builder - Create distributable package for Bug Bounty Hunter Pro
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔨 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def create_spec_file():
    """Create PyInstaller spec file"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('wordlists', 'wordlists'),
        ('assets', 'assets'),
        ('data', 'data'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'requests',
        'jwt',
        'bcrypt',
        'zapv2',
        'websockets',
        'cryptography'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='bug-bounty-hunter-pro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.png'
)
'''
    
    with open('bug_bounty_hunter_pro.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ PyInstaller spec file created")

def build_executable():
    """Build executable using PyInstaller"""
    print("🚀 Building executable package...")
    
    # Activate virtual environment
    venv_python = "./bug_bounty_env/bin/python"
    if not os.path.exists(venv_python):
        print("❌ Virtual environment not found. Please run install.sh first.")
        return False
    
    # Create spec file
    create_spec_file()
    
    # Build with PyInstaller
    build_cmd = f"{venv_python} -m PyInstaller bug_bounty_hunter_pro.spec --clean --noconfirm"
    
    if run_command(build_cmd, "Building executable"):
        print("✅ Executable built successfully")
        return True
    else:
        print("❌ Failed to build executable")
        return False

def create_installer():
    """Create installation package"""
    print("📦 Creating installation package...")
    
    # Create package directory
    package_dir = "bug-bounty-hunter-pro-package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    # Copy files to package
    files_to_copy = [
        ('dist/bug-bounty-hunter-pro', 'bug-bounty-hunter-pro'),
        ('wordlists', 'wordlists'),
        ('assets', 'assets'),
        ('install.sh', 'install.sh'),
        ('README.md', 'README.md'),
        ('requirements.txt', 'requirements.txt'),
        ('bug_bounty_finder.py', 'bug_bounty_finder.py')
    ]
    
    for src, dst in files_to_copy:
        src_path = Path(src)
        dst_path = Path(package_dir) / dst
        
        if src_path.exists():
            if src_path.is_dir():
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
            print(f"✅ Copied {src} to package")
        else:
            print(f"⚠️  Warning: {src} not found, skipping")
    
    # Create package installer script
    installer_script = f"""#!/bin/bash

# Bug Bounty Hunter Pro - Package Installer
echo "🚀 Installing Bug Bounty Hunter Pro..."

# Create installation directory
INSTALL_DIR="$HOME/.local/share/bug-bounty-hunter-pro"
mkdir -p "$INSTALL_DIR"

# Copy files
cp -r * "$INSTALL_DIR/"

# Make executable
chmod +x "$INSTALL_DIR/bug-bounty-hunter-pro"
chmod +x "$INSTALL_DIR/install.sh"

# Create desktop entry
DESKTOP_FILE="$HOME/.local/share/applications/bug-bounty-hunter-pro.desktop"
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Bug Bounty Hunter Pro
Comment=Advanced Security Testing Platform
Exec=$INSTALL_DIR/bug-bounty-hunter-pro
Icon=$INSTALL_DIR/assets/icon.png
Terminal=false
Categories=Security;Network;
StartupNotify=true
EOF

chmod +x "$DESKTOP_FILE"

# Create symlink for command line access
sudo ln -sf "$INSTALL_DIR/bug-bounty-hunter-pro" /usr/local/bin/bug-bounty-hunter-pro

echo "✅ Installation completed!"
echo "🎯 You can now run 'bug-bounty-hunter-pro' from terminal"
echo "📱 Or find it in your applications menu"
"""
    
    with open(f"{package_dir}/install_package.sh", 'w') as f:
        f.write(installer_script)
    
    os.chmod(f"{package_dir}/install_package.sh", 0o755)
    
    # Create archive
    archive_name = "bug-bounty-hunter-pro-v1.0-linux"
    shutil.make_archive(archive_name, 'tar', package_dir)
    
    print(f"✅ Package created: {archive_name}.tar")
    print(f"📦 Package directory: {package_dir}")
    
    return True

def create_deb_package():
    """Create Debian package"""
    print("📦 Creating Debian package...")
    
    deb_dir = "bug-bounty-hunter-pro-deb"
    if os.path.exists(deb_dir):
        shutil.rmtree(deb_dir)
    
    # Create directory structure
    dirs = [
        f"{deb_dir}/DEBIAN",
        f"{deb_dir}/usr/local/bin",
        f"{deb_dir}/usr/share/applications",
        f"{deb_dir}/usr/share/bug-bounty-hunter-pro",
        f"{deb_dir}/usr/share/pixmaps"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    # Create control file
    control_content = """Package: bug-bounty-hunter-pro
Version: 1.0
Section: utils
Priority: optional
Architecture: amd64
Depends: python3, python3-pyqt6, default-jdk
Maintainer: Bug Bounty Hunter Pro Team <team@bugbountyhunterpro.com>
Description: Advanced Security Testing Platform
 A comprehensive bug bounty automation tool with GUI interface,
 OWASP ZAP integration, and advanced vulnerability detection.
"""
    
    with open(f"{deb_dir}/DEBIAN/control", 'w') as f:
        f.write(control_content)
    
    # Copy executable and files
    if os.path.exists("dist/bug-bounty-hunter-pro"):
        shutil.copy2("dist/bug-bounty-hunter-pro", f"{deb_dir}/usr/local/bin/")
        
        # Copy assets
        if os.path.exists("assets"):
            shutil.copytree("assets", f"{deb_dir}/usr/share/bug-bounty-hunter-pro/assets")
        
        if os.path.exists("wordlists"):
            shutil.copytree("wordlists", f"{deb_dir}/usr/share/bug-bounty-hunter-pro/wordlists")
        
        # Create desktop file
        desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=Bug Bounty Hunter Pro
Comment=Advanced Security Testing Platform
Exec=/usr/local/bin/bug-bounty-hunter-pro
Icon=/usr/share/bug-bounty-hunter-pro/assets/icon.png
Terminal=false
Categories=Security;Network;
StartupNotify=true
"""
        
        with open(f"{deb_dir}/usr/share/applications/bug-bounty-hunter-pro.desktop", 'w') as f:
            f.write(desktop_content)
        
        # Build deb package
        if run_command(f"dpkg-deb --build {deb_dir}", "Building Debian package"):
            print("✅ Debian package created successfully")
            return True
    
    print("❌ Failed to create Debian package")
    return False

def main():
    """Main packaging function"""
    print("🚀 Bug Bounty Hunter Pro - Package Builder")
    print("=" * 50)
    
    # Check if virtual environment exists
    if not os.path.exists("bug_bounty_env"):
        print("❌ Virtual environment not found. Please run install.sh first.")
        sys.exit(1)
    
    # Build executable
    if not build_executable():
        print("❌ Failed to build executable")
        sys.exit(1)
    
    # Create installation package
    if not create_installer():
        print("❌ Failed to create installation package")
        sys.exit(1)
    
    # Create Debian package (optional)
    create_deb_package()
    
    print("\n🎉 Packaging completed successfully!")
    print("\nGenerated files:")
    print("📦 bug-bounty-hunter-pro-v1.0-linux.tar - Installation package")
    print("📱 bug-bounty-hunter-pro-deb.deb - Debian package")
    print("📁 dist/bug-bounty-hunter-pro - Standalone executable")
    
    print("\nTo distribute:")
    print("1. Share the .tar file for manual installation")
    print("2. Share the .deb file for Debian/Ubuntu systems")
    print("3. Use the executable directly from dist/ folder")

if __name__ == "__main__":
    main()