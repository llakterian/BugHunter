# Bug Bounty Hunter Pro

## 🚀 Advanced Security Testing Platform (33X More Robust)

A comprehensive GUI-based security testing tool designed for ethical bug bounty hunters and security professionals.

## ✨ Features

- **Mass CVE Scanning** - Shodan integration for large-scale vulnerability hunting
- **Hidden Element Discovery** - Bookmarklet-based tools to reveal client-side restrictions
- **Automated Recon** - Multi-source URL discovery (AlienVault, Wayback, URLScan, VirusTotal)
- **GF Pattern Filtering** - Advanced URL filtering with custom patterns and deduplication
- **LostFuzzer Integration** - Passive URL fuzzing and Nuclei DAST scanning
- **Complete Workflow Automation** - End-to-end bug hunting pipeline

## 🛠 Installation

### Quick Install (Recommended)
```bash
git clone <repository>
cd bug-bounty-hunter-pro
./install.sh
```

### Manual Installation
```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv qt6-base-dev

# Create virtual environment
python3 -m venv bug_bounty_env
source bug_bounty_env/bin/activate

# Install Python dependencies
pip install PyQt6 requests python-owasp-zap-v2.4 beautifulsoup4 lxml bcrypt pyjwt cryptography

# Install OWASP ZAP (optional but recommended)
# Download from: https://www.zaproxy.org/download/
```

## 🚀 Running the Application

### GUI Mode (Desktop Environment)
```bash
# From the application directory
./run.sh

# Or double-click the desktop icon after installation
```

### Headless Mode (Servers/SSH)
```bash
# Set offscreen rendering
QT_QPA_PLATFORM=offscreen ./run.sh
```

### First Run Credentials
On first run, the application generates random admin credentials. Check the console output for:
- Username: admin
- Password: [randomly generated 16-character password]

**⚠️ IMPORTANT:** Save these credentials and change the password after first login!

## 🔧 Troubleshooting

### "Cannot find login page" or "App doesn't show"
- Ensure you have a desktop environment installed
- Check if DISPLAY environment variable is set: `echo $DISPLAY`
- For headless servers, use: `QT_QPA_PLATFORM=offscreen ./run.sh`

### Permission Issues
```bash
chmod +x run.sh
chmod +x install.sh
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf bug_bounty_env
python3 -m venv bug_bounty_env
source bug_bounty_env/bin/activate
pip install -r requirements.txt
```

### Desktop Icon Not Working
```bash
# Refresh desktop database
update-desktop-database ~/.local/share/applications/

# Or manually create desktop entry
cp /path/to/app/assets/icon.png ~/.icons/
sudo cp ~/.local/share/applications/bug-bounty-hunter-pro.desktop /usr/share/applications/
```

## 📋 System Requirements

- **OS**: Linux (Kali Linux, Parrot OS, Ubuntu recommended)
- **Python**: 3.8-3.12
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Display**: X11/Wayland for GUI mode

## 🔐 Security Features

- **Secure Authentication**: bcrypt password hashing
- **Session Management**: Automatic logout on inactivity
- **Rate Limiting**: Brute force protection on login
- **Ethical Use Enforcement**: Required agreement to ethical guidelines
- **Input Validation**: Comprehensive form validation

## 📖 Usage

1. **Login** with admin credentials (shown on first run)
2. **Navigate** through the tabbed interface
3. **Configure** your scanning parameters
4. **Run** automated scans and manual tests
5. **Generate** comprehensive reports

## 🆘 Support

- Check the logs in the `logs/` directory for errors
- Run `./test_app.py` to verify component functionality
- Ensure all dependencies are properly installed

## ⚖️ Legal & Ethical Notice

This tool is intended **only for authorized bug bounty hunting and security testing**. Unauthorized use for malicious purposes is strictly prohibited and may be illegal. By using this tool, you agree to:

- Only test systems you own or have explicit permission to test
- Comply with all applicable laws and regulations
- Respect the terms of service of target platforms
- Report findings responsibly through proper channels

## 📄 License

This project is licensed under appropriate terms. See LICENSE file for details.