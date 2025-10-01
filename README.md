# 🐛 BugHunter Pro - Advanced Security Testing Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt-6.0+-green.svg)](https://pypi.org/project/PyQt6/)

A comprehensive, professional-grade vulnerability scanner and bug bounty hunting platform built with Python and PyQt6. Designed for ethical security researchers and bug bounty hunters.

## ✨ Key Features

### 🔍 Advanced Vulnerability Detection
- **Real-World Scanning**: Discovers actual input fields from live websites (not hardcoded examples)
- **Multi-Engine Detection**: Combines manual testing with professional tools
- **Comprehensive Coverage**:
  - SQL Injection (error-based, time-based, boolean-based)
  - Cross-Site Scripting (XSS) with context-aware detection
  - Command Injection
  - Directory Traversal
  - File Inclusion vulnerabilities
  - IDOR (Insecure Direct Object References)
  - Known vulnerable site patterns

### 🛠️ Professional Tool Integration
- **Nuclei**: Template-based vulnerability scanning
- **Lost Fuzzer**: Advanced fuzzing capabilities
- **OWASP ZAP**: Integrated web application scanner
- **Custom Wordlists**: Extensive payload collections

### 🎯 Bug Bounty Focused
- **Automated Reconnaissance**: Subdomain enumeration and target discovery
- **Intelligence Dashboard**: Track bounties and vulnerabilities
- **Report Generation**: Professional vulnerability reports
- **Bounty Monitoring**: Real-time program updates

### 🖥️ Modern Desktop Application
- **Cross-Platform**: Windows, macOS, Linux support
- **Intuitive GUI**: User-friendly interface with real-time progress
- **Multi-Threading**: Concurrent scanning for efficiency
- **Secure Authentication**: Encrypted user management

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- 4GB RAM minimum (8GB recommended)
- Internet connection for scanning

### Installation

#### On Linux (Parrot OS, Kali Linux, Ubuntu)
```bash
git clone https://github.com/llakterian/BugHunter.git
cd BugHunter
chmod +x install.sh
./install.sh
./run.sh
```

#### On macOS
```bash
git clone https://github.com/llakterian/BugHunter.git
cd BugHunter
chmod +x setup_macos.sh
./setup_macos.sh
```

#### On Windows
1. Download and extract the repository
2. Run `setup_windows.bat` as Administrator
3. Double-click `run.bat` to launch

### First Run
- Default login: `admin` / `BugHunter2024!`
- **Important**: Change the default password immediately!

## 📖 Usage Guide

### Basic Scanning
1. Launch the application
2. Enter target URL (e.g., `http://testaspnet.vulnweb.com`)
3. Select scan types (SQLi, XSS, etc.)
4. Click "Start Scan"
5. View results in real-time

### Advanced Features
- **Custom Wordlists**: Import your own payloads
- **Proxy Configuration**: Route through Burp/ZAP
- **Report Export**: Generate detailed vulnerability reports
- **API Integration**: Connect with external tools

## 🏗️ Architecture

```
BugHunter/
├── Core Engine
│   ├── scanner_engine.py     # Main scanning logic
│   ├── vulnerability_validator.py # Detection validation
│   └── tool_integrations.py  # External tool management
├── GUI Components
│   ├── main.py              # Application entry point
│   ├── main_dashboard.py    # Main interface
│   └── login_window.py      # Authentication
├── Tool Integrations
│   ├── nuclei_shodan_integration.py
│   ├── lost_fuzzer.py
│   └── zap_manager.py
├── Data Management
│   ├── wordlist_manager.py
│   ├── auth_manager.py
│   └── config_manager.py
└── Assets & Config
    ├── assets/              # Icons and resources
    ├── wordlists/           # Payload collections
    └── data/                # Application data
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Configure proxy
export HTTP_PROXY=http://127.0.0.1:8080
export HTTPS_PROXY=http://127.0.0.1:8080
```

### Custom Wordlists
Place your wordlists in the `wordlists/` directory:
- `sqli_payloads.txt` - SQL injection payloads
- `xss_payloads.txt` - XSS test cases
- `lfi_payloads.txt` - File inclusion tests

## 🛡️ Security & Ethics

### ⚠️ Important Security Notice
This application is designed for **authorized security testing only**. It is a desktop application that requires local installation and cannot be run from web browsers or GitHub Pages.

- **Never scan without permission**
- **Respect scope limitations**
- **Follow bug bounty program rules**
- **Report vulnerabilities responsibly**

### 🔒 Application Security
- Encrypted user credentials
- Secure session management
- No external data transmission without user consent
- Local-only execution (cannot run in browsers)

## 📊 Performance

### System Requirements
- **Minimum**: 4GB RAM, Dual-core CPU
- **Recommended**: 8GB RAM, Quad-core CPU
- **Storage**: 2GB free space

### Scanning Performance
- **Basic Scan**: ~30 seconds per target
- **Full Scan**: 5-15 minutes depending on target complexity
- **Concurrent Threads**: Configurable (default: 5)

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Follow our coding standards

### Development Setup
```bash
git clone https://github.com/llakterian/BugHunter.git
cd BugHunter
python -m venv dev_env
source dev_env/bin/activate  # On Windows: dev_env\Scripts\activate
pip install -r requirements-dev.txt
python main.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OWASP for vulnerability research
- Nuclei project for scanning templates
- PyQt6 community for the GUI framework
- Security researchers worldwide

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/llakterian/BugHunter/issues)
- **Discussions**: [GitHub Discussions](https://github.com/llakterian/BugHunter/discussions)
- **Documentation**: [Wiki](https://github.com/llakterian/BugHunter/wiki)

---

**Remember**: With great power comes great responsibility. Use this tool ethically and legally! 🔒