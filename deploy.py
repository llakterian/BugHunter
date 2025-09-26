#!/usr/bin/env python3
"""
Deployment Script - Deploy Bug Bounty Hunter Pro for distribution
"""

import os
import sys
import subprocess
import shutil
import zipfile
import tarfile
from pathlib import Path
import json
import time

class BugBountyDeployer:
    def __init__(self):
        self.project_root = Path.cwd()
        self.version = "1.0.0"
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        
    def clean_build(self):
        """Clean previous builds"""
        print("🧹 Cleaning previous builds...")
        
        for directory in [self.build_dir, self.dist_dir]:
            if directory.exists():
                shutil.rmtree(directory)
            directory.mkdir(parents=True, exist_ok=True)
        
        print("✅ Build directories cleaned")
    
    def run_tests(self):
        """Run comprehensive tests before deployment"""
        print("🧪 Running tests before deployment...")
        
        try:
            result = subprocess.run([
                sys.executable, "test_suite.py"
            ], capture_output=True, text=True, check=True)
            
            print("✅ All tests passed")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            print(f"Output: {e.stdout}")
            print(f"Error: {e.stderr}")
            return False
    
    def create_source_package(self):
        """Create source code package"""
        print("📦 Creating source package...")
        
        source_files = [
            "main.py",
            "auth_manager.py",
            "login_window.py", 
            "main_dashboard.py",
            "config_manager.py",
            "zap_manager.py",
            "scanner_engine.py",
            "jwt_analyzer.py",
            "report_generator.py",
            "advanced_scanner.py",
            "exploit_generator.py",
            "network_scanner.py",
            "bug_bounty_finder.py",
            "test_suite.py",
            "install.sh",
            "build_package.py",
            "requirements.txt",
            "README.md",
            "USAGE_GUIDE.md"
        ]
        
        source_dirs = [
            "wordlists",
            "assets"
        ]
        
        # Create source package directory
        source_pkg_dir = self.build_dir / f"bug-bounty-hunter-pro-{self.version}-source"
        source_pkg_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy files
        for file in source_files:
            if Path(file).exists():
                shutil.copy2(file, source_pkg_dir / file)
        
        # Copy directories
        for directory in source_dirs:
            if Path(directory).exists():
                shutil.copytree(directory, source_pkg_dir / directory)
        
        # Create data directory structure
        (source_pkg_dir / "data").mkdir(exist_ok=True)
        (source_pkg_dir / "reports").mkdir(exist_ok=True)
        (source_pkg_dir / "logs").mkdir(exist_ok=True)
        (source_pkg_dir / "screenshots").mkdir(exist_ok=True)
        
        # Create archive
        archive_path = self.dist_dir / f"bug-bounty-hunter-pro-{self.version}-source.tar.gz"
        
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(source_pkg_dir, arcname=f"bug-bounty-hunter-pro-{self.version}")
        
        print(f"✅ Source package created: {archive_path}")
        return archive_path
    
    def create_binary_package(self):
        """Create binary package using PyInstaller"""
        print("🔨 Creating binary package...")
        
        try:
            # Activate virtual environment
            venv_python = self.project_root / "bug_bounty_env" / "bin" / "python"
            
            if not venv_python.exists():
                print("❌ Virtual environment not found. Run install.sh first.")
                return None
            
            # Install PyInstaller if not present
            subprocess.run([
                str(venv_python), "-m", "pip", "install", "pyinstaller"
            ], check=True, capture_output=True)
            
            # Create spec file
            spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['{self.project_root}'],
    binaries=[],
    datas=[
        ('wordlists', 'wordlists'),
        ('assets', 'assets'),
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
        'cryptography',
        'dns.resolver',
        'scapy'
    ],
    hookspath=[],
    hooksconfig={{}},
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
)
'''
            
            spec_file = self.project_root / "bug_bounty_hunter_pro.spec"
            with open(spec_file, 'w') as f:
                f.write(spec_content)
            
            # Build with PyInstaller
            subprocess.run([
                str(venv_python), "-m", "PyInstaller", 
                str(spec_file), "--clean", "--noconfirm"
            ], check=True)
            
            # Create binary package
            binary_pkg_dir = self.build_dir / f"bug-bounty-hunter-pro-{self.version}-linux-x64"
            binary_pkg_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy executable
            exe_path = self.project_root / "dist" / "bug-bounty-hunter-pro"
            if exe_path.exists():
                shutil.copy2(exe_path, binary_pkg_dir / "bug-bounty-hunter-pro")
                os.chmod(binary_pkg_dir / "bug-bounty-hunter-pro", 0o755)
            
            # Copy additional files
            additional_files = [
                "README.md",
                "USAGE_GUIDE.md",
                "bug_bounty_finder.py"
            ]
            
            for file in additional_files:
                if Path(file).exists():
                    shutil.copy2(file, binary_pkg_dir / file)
            
            # Copy directories
            for directory in ["wordlists", "assets"]:
                if Path(directory).exists():
                    shutil.copytree(directory, binary_pkg_dir / directory)
            
            # Create installer script
            installer_script = f'''#!/bin/bash
# Bug Bounty Hunter Pro v{self.version} - Binary Installer

echo "🚀 Installing Bug Bounty Hunter Pro v{self.version}..."

# Create installation directory
INSTALL_DIR="$HOME/.local/share/bug-bounty-hunter-pro"
mkdir -p "$INSTALL_DIR"

# Copy files
cp -r * "$INSTALL_DIR/"

# Make executable
chmod +x "$INSTALL_DIR/bug-bounty-hunter-pro"

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
sudo ln -sf "$INSTALL_DIR/bug-bounty-hunter-pro" /usr/local/bin/bug-bounty-hunter-pro 2>/dev/null || true

echo "✅ Installation completed!"
echo "🎯 Run 'bug-bounty-hunter-pro' from terminal or find it in applications menu"
'''
            
            with open(binary_pkg_dir / "install.sh", 'w') as f:
                f.write(installer_script)
            
            os.chmod(binary_pkg_dir / "install.sh", 0o755)
            
            # Create archive
            archive_path = self.dist_dir / f"bug-bounty-hunter-pro-{self.version}-linux-x64.tar.gz"
            
            with tarfile.open(archive_path, "w:gz") as tar:
                tar.add(binary_pkg_dir, arcname=f"bug-bounty-hunter-pro-{self.version}")
            
            print(f"✅ Binary package created: {archive_path}")
            return archive_path
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Binary package creation failed: {e}")
            return None
    
    def create_deb_package(self):
        """Create Debian package"""
        print("📦 Creating Debian package...")
        
        try:
            deb_dir = self.build_dir / "debian-package"
            
            # Create directory structure
            dirs = [
                deb_dir / "DEBIAN",
                deb_dir / "usr" / "local" / "bin",
                deb_dir / "usr" / "share" / "applications",
                deb_dir / "usr" / "share" / "bug-bounty-hunter-pro",
                deb_dir / "usr" / "share" / "pixmaps",
                deb_dir / "usr" / "share" / "doc" / "bug-bounty-hunter-pro"
            ]
            
            for directory in dirs:
                directory.mkdir(parents=True, exist_ok=True)
            
            # Create control file
            control_content = f'''Package: bug-bounty-hunter-pro
Version: {self.version}
Section: utils
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.8), python3-pyqt6, default-jdk
Maintainer: Bug Bounty Hunter Pro Team <team@bugbountyhunterpro.com>
Description: Advanced Security Testing Platform
 A comprehensive bug bounty automation tool with GUI interface,
 OWASP ZAP integration, and advanced vulnerability detection.
 .
 Features include:
  - Directory and subdomain fuzzing
  - JWT vulnerability analysis
  - Admin panel discovery
  - SQL injection detection
  - XSS testing
  - Command injection testing
  - Professional reporting
Homepage: https://github.com/bugbountyhunterpro/bug-bounty-hunter-pro
'''
            
            with open(deb_dir / "DEBIAN" / "control", 'w') as f:
                f.write(control_content)
            
            # Copy executable
            exe_path = self.project_root / "dist" / "bug-bounty-hunter-pro"
            if exe_path.exists():
                shutil.copy2(exe_path, deb_dir / "usr" / "local" / "bin" / "bug-bounty-hunter-pro")
                os.chmod(deb_dir / "usr" / "local" / "bin" / "bug-bounty-hunter-pro", 0o755)
            
            # Copy assets and wordlists
            for directory in ["wordlists", "assets"]:
                if Path(directory).exists():
                    shutil.copytree(directory, deb_dir / "usr" / "share" / "bug-bounty-hunter-pro" / directory)
            
            # Copy documentation
            for doc in ["README.md", "USAGE_GUIDE.md"]:
                if Path(doc).exists():
                    shutil.copy2(doc, deb_dir / "usr" / "share" / "doc" / "bug-bounty-hunter-pro" / doc)
            
            # Create desktop file
            desktop_content = '''[Desktop Entry]
Version=1.0
Type=Application
Name=Bug Bounty Hunter Pro
Comment=Advanced Security Testing Platform
Exec=/usr/local/bin/bug-bounty-hunter-pro
Icon=/usr/share/bug-bounty-hunter-pro/assets/icon.png
Terminal=false
Categories=Security;Network;
StartupNotify=true
'''
            
            with open(deb_dir / "usr" / "share" / "applications" / "bug-bounty-hunter-pro.desktop", 'w') as f:
                f.write(desktop_content)
            
            # Build deb package
            deb_file = self.dist_dir / f"bug-bounty-hunter-pro_{self.version}_amd64.deb"
            
            subprocess.run([
                "dpkg-deb", "--build", str(deb_dir), str(deb_file)
            ], check=True)
            
            print(f"✅ Debian package created: {deb_file}")
            return deb_file
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Debian package creation failed: {e}")
            return None
        except FileNotFoundError:
            print("⚠️  dpkg-deb not found. Skipping Debian package creation.")
            return None
    
    def create_docker_image(self):
        """Create Docker image"""
        print("🐳 Creating Docker image...")
        
        dockerfile_content = f'''
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    default-jdk \\
    wget \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Install OWASP ZAP
RUN wget -q https://github.com/zaproxy/zaproxy/releases/download/v2.14.0/ZAP_2.14.0_Linux.tar.gz \\
    && tar -xzf ZAP_2.14.0_Linux.tar.gz \\
    && mv ZAP_2.14.0 /opt/zaproxy \\
    && ln -s /opt/zaproxy/zap.sh /usr/local/bin/zaproxy \\
    && rm ZAP_2.14.0_Linux.tar.gz

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p data reports logs screenshots

# Set permissions
RUN chmod +x main.py bug_bounty_finder.py

# Expose port for web interface (if needed)
EXPOSE 8080

# Set environment variables
ENV PYTHONPATH=/app
ENV DISPLAY=:0

# Run the application
CMD ["python3", "main.py"]
'''
        
        dockerfile_path = self.project_root / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        # Create .dockerignore
        dockerignore_content = '''
.git
.gitignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.DS_Store
.vscode
.idea
*.swp
*.swo
*~
build/
dist/
*.egg-info/
bug_bounty_env/
'''
        
        with open(self.project_root / ".dockerignore", 'w') as f:
            f.write(dockerignore_content)
        
        print("✅ Docker files created")
        print("To build Docker image:")
        print(f"  docker build -t bug-bounty-hunter-pro:{self.version} .")
        print("To run Docker container:")
        print(f"  docker run -it --rm bug-bounty-hunter-pro:{self.version}")
    
    def generate_checksums(self, files):
        """Generate checksums for distribution files"""
        print("🔐 Generating checksums...")
        
        checksums_file = self.dist_dir / "checksums.txt"
        
        with open(checksums_file, 'w') as f:
            f.write(f"# Bug Bounty Hunter Pro v{self.version} - Checksums\n")
            f.write(f"# Generated on {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n\n")
            
            for file_path in files:
                if file_path and file_path.exists():
                    # Calculate SHA256
                    import hashlib
                    sha256_hash = hashlib.sha256()
                    
                    with open(file_path, "rb") as f_hash:
                        for byte_block in iter(lambda: f_hash.read(4096), b""):
                            sha256_hash.update(byte_block)
                    
                    checksum = sha256_hash.hexdigest()
                    f.write(f"{checksum}  {file_path.name}\n")
        
        print(f"✅ Checksums generated: {checksums_file}")
    
    def create_release_notes(self):
        """Create release notes"""
        print("📝 Creating release notes...")
        
        release_notes = f'''# Bug Bounty Hunter Pro v{self.version} - Release Notes

## 🚀 Features

### Core Functionality
- **Secure Authentication System** - Multi-user support with encrypted passwords
- **OWASP ZAP Integration** - Full integration with ZAP for automated security scanning
- **Directory Fuzzing** - Advanced directory and file discovery
- **Subdomain Enumeration** - Comprehensive subdomain discovery
- **JWT Analysis** - Advanced JWT token vulnerability detection
- **Admin Panel Discovery** - Automated admin interface detection
- **Real-time Progress Updates** - Live scanning progress via WebSocket
- **Comprehensive Reporting** - Professional HTML and JSON reports

### Advanced Security Features
- **Redirect Bypass** - Automatic HTTP redirect manipulation
- **Weak JWT Secret Detection** - Brute force JWT signing secrets
- **Algorithm Confusion Testing** - RS256/HS256 vulnerability detection
- **SQL Injection Testing** - Automated SQL injection detection
- **XSS Testing** - Cross-site scripting vulnerability detection
- **Command Injection Testing** - OS command injection detection
- **LFI Testing** - Local file inclusion vulnerability detection

### Network Security
- **Port Scanning** - Comprehensive port and service discovery
- **Service Enumeration** - Detailed service fingerprinting
- **SSL/TLS Analysis** - Certificate and cipher analysis
- **Network Reconnaissance** - Advanced network mapping

## 📦 Installation Options

### Source Installation
```bash
tar -xzf bug-bounty-hunter-pro-{self.version}-source.tar.gz
cd bug-bounty-hunter-pro-{self.version}
chmod +x install.sh
./install.sh
```

### Binary Installation (Linux x64)
```bash
tar -xzf bug-bounty-hunter-pro-{self.version}-linux-x64.tar.gz
cd bug-bounty-hunter-pro-{self.version}
chmod +x install.sh
./install.sh
```

### Debian Package
```bash
sudo dpkg -i bug-bounty-hunter-pro_{self.version}_amd64.deb
sudo apt-get install -f  # Fix dependencies if needed
```

## 🎯 Usage

1. **Start the application:**
   ```bash
   bug-bounty-hunter-pro
   # or
   ./run.sh
   ```

2. **Login with default credentials:**
   - Username: `admin`
   - Password: `BugHunter2024!`

3. **Configure target and start scanning**

## 🔧 System Requirements

- **Operating System:** Linux (Kali Linux recommended)
- **Python:** 3.8 or higher
- **Java:** 8 or higher (for OWASP ZAP)
- **Memory:** 4GB RAM minimum, 8GB recommended
- **Storage:** 2GB free space

## 🐛 Bug Fixes

- Fixed JWT algorithm confusion detection
- Improved error handling in network scanner
- Enhanced SSL/TLS certificate validation
- Optimized memory usage during large scans

## 🔒 Security Improvements

- Enhanced password hashing with bcrypt
- Improved session management
- Added CSRF protection
- Strengthened input validation

## 📚 Documentation

- Comprehensive README.md
- Detailed USAGE_GUIDE.md
- Inline code documentation
- Example configurations

## 🤝 Contributing

We welcome contributions! Please see our GitHub repository for contribution guidelines.

## 📞 Support

- **Documentation:** README.md and USAGE_GUIDE.md
- **Issues:** Report bugs on GitHub
- **Community:** Join our discussions

## ⚠️ Legal Notice

This tool is for authorized security testing only. Users must obtain proper authorization before testing any systems and comply with all applicable laws and regulations.

---

**Happy Bug Hunting! 🎯**
'''
        
        release_notes_file = self.dist_dir / f"RELEASE_NOTES_v{self.version}.md"
        with open(release_notes_file, 'w') as f:
            f.write(release_notes)
        
        print(f"✅ Release notes created: {release_notes_file}")
    
    def deploy(self):
        """Main deployment function"""
        print(f"🚀 Deploying Bug Bounty Hunter Pro v{self.version}")
        print("=" * 60)
        
        # Clean previous builds
        self.clean_build()
        
        # Run tests
        if not self.run_tests():
            print("❌ Deployment aborted due to test failures")
            return False
        
        # Create packages
        created_files = []
        
        # Source package
        source_pkg = self.create_source_package()
        if source_pkg:
            created_files.append(source_pkg)
        
        # Binary package
        binary_pkg = self.create_binary_package()
        if binary_pkg:
            created_files.append(binary_pkg)
        
        # Debian package
        deb_pkg = self.create_deb_package()
        if deb_pkg:
            created_files.append(deb_pkg)
        
        # Docker files
        self.create_docker_image()
        
        # Generate checksums
        self.generate_checksums(created_files)
        
        # Create release notes
        self.create_release_notes()
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        print(f"\nVersion: {self.version}")
        print(f"Build Directory: {self.build_dir}")
        print(f"Distribution Directory: {self.dist_dir}")
        
        print("\n📦 Created Packages:")
        for file_path in created_files:
            if file_path and file_path.exists():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"  - {file_path.name} ({size_mb:.1f} MB)")
        
        print("\n🐳 Docker:")
        print("  - Dockerfile created")
        print("  - .dockerignore created")
        
        print("\n📋 Additional Files:")
        print(f"  - checksums.txt")
        print(f"  - RELEASE_NOTES_v{self.version}.md")
        
        print("\n🚀 Ready for Distribution!")
        
        return True

def main():
    """Main function"""
    deployer = BugBountyDeployer()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--version":
            print(f"Bug Bounty Hunter Pro Deployer v{deployer.version}")
            return
        elif sys.argv[1] == "--help":
            print("Bug Bounty Hunter Pro Deployment Script")
            print("\nUsage:")
            print("  python3 deploy.py           # Full deployment")
            print("  python3 deploy.py --version # Show version")
            print("  python3 deploy.py --help    # Show help")
            return
    
    success = deployer.deploy()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()