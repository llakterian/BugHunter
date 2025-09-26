# Bug Bounty Hunter Pro 🎯

**Advanced Security Testing Platform for Professional Bug Bounty Hunters**

A comprehensive, GUI-based bug bounty automation tool designed specifically for Kali Linux. This application replicates and automates the entire bug bounty hunting workflow, from reconnaissance to vulnerability discovery and reporting.

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Kali%20Linux-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)

## 🚀 Features

### Core Functionality
- **🔐 Secure Authentication System** - Multi-user support with encrypted passwords
- **🕷️ OWASP ZAP Integration** - Full integration with ZAP for automated security scanning
- **🎯 Directory Fuzzing** - Advanced directory and file discovery
- **🌐 Subdomain Enumeration** - Comprehensive subdomain discovery
- **🔑 JWT Analysis** - Advanced JWT token vulnerability detection
- **👑 Admin Panel Discovery** - Automated admin interface detection
- **📊 Real-time Progress Updates** - Live scanning progress via WebSocket
- **📋 Comprehensive Reporting** - Professional HTML and JSON reports

### Advanced Security Features
- **Redirect Bypass** - Automatic HTTP redirect manipulation
- **Weak JWT Secret Detection** - Brute force JWT signing secrets
- **Algorithm Confusion Testing** - RS256/HS256 vulnerability detection
- **User Creation Endpoint Discovery** - Find unprotected user registration
- **Account Takeover Detection** - Identify ATO vulnerabilities

### User Interface
- **Modern GUI** - Professional PyQt6-based interface
- **Dark Theme** - Eye-friendly dark mode design
- **Multi-tab Interface** - Organized results, logs, and vulnerability views
- **Real-time Updates** - Live progress and status updates
- **Configurable Settings** - Customizable scan parameters

## 🛠️ Installation

### Prerequisites
- Kali Linux (recommended) or any Debian-based Linux distribution
- Python 3.8 or higher
- Java 8 or higher (for OWASP ZAP)
- Internet connection for downloading dependencies

### Quick Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/bug-bounty-hunter-pro.git
cd bug-bounty-hunter-pro
```

2. **Run the installation script:**
```bash
chmod +x install.sh
./install.sh
```

3. **Launch the application:**
```bash
./run.sh
```

### Manual Installation

If you prefer manual installation:

```bash
# Create virtual environment
python3 -m venv bug_bounty_env
source bug_bounty_env/bin/activate

# Install dependencies
pip install PyQt6 requests python-owasp-zap-v2.4 websockets bcrypt pyjwt cryptography

# Install OWASP ZAP (if not already installed)
sudo apt install zaproxy

# Create necessary directories
mkdir -p {data,reports,screenshots,logs,wordlists}

# Run the application
python3 main.py
```

## 🎮 Usage

### First Launch

1. **Start the application:**
```bash
./run.sh
```

2. **Login with default credentials:**
   - Username: `admin`
   - Password: `BugHunter2024!`

3. **Change default password** (recommended)

### Basic Workflow

1. **Configure Target:**
   - Enter target URL (e.g., `https://example.com`)
   - Select wordlist type
   - Configure threads and timeout

2. **Select Scan Options:**
   - ✅ Directory Fuzzing
   - ✅ Subdomain Enumeration  
   - ✅ JWT Analysis
   - ✅ Admin Panel Discovery
   - ✅ Bypass Redirects

3. **Start ZAP (Optional):**
   - Click "Start ZAP" to launch OWASP ZAP daemon
   - Click "Connect ZAP" to establish connection
   - Use "Spider Scan" and "Active Scan" for comprehensive testing

4. **Begin Bug Hunt:**
   - Click "Start Bug Hunt" to begin automated scanning
   - Monitor real-time progress in the interface
   - View results in the Results, Logs, and Vulnerabilities tabs

5. **Generate Report:**
   - Click "Generate Report" when scanning is complete
   - Choose HTML or JSON format
   - Professional report saved to `reports/` directory

### Bug Bounty Site Finder

Find active bug bounty programs:

```bash
source bug_bounty_env/bin/activate
python3 bug_bounty_finder.py
```

This will search and display the top 6 paying bug bounty programs currently active.

## 🔧 Configuration

### Application Settings

Configuration files are stored in `data/config.json`:

```json
{
  "zap": {
    "host": "127.0.0.1",
    "port": 8080,
    "api_key": "",
    "auto_start": true
  },
  "scanning": {
    "max_threads": 10,
    "timeout": 30,
    "user_agent": "BugBountyHunterPro/1.0"
  },
  "wordlists": {
    "directories": "wordlists/directories.txt",
    "subdomains": "wordlists/subdomains.txt",
    "jwt_secrets": "wordlists/jwt_secrets.txt"
  }
}
```

### Custom Wordlists

Replace default wordlists in the `wordlists/` directory:
- `directories.txt` - Directory fuzzing wordlist
- `subdomains.txt` - Subdomain enumeration wordlist  
- `jwt_secrets.txt` - JWT weak secrets wordlist

## 📊 Vulnerability Detection

The application detects various vulnerability types:

### Critical Vulnerabilities
- **JWT Weak Secrets** - Weak signing secrets allowing token forgery
- **Admin Panel Exposure** - Unprotected administrative interfaces
- **Algorithm Confusion** - RS256/HS256 JWT vulnerabilities
- **None Algorithm** - JWT tokens accepting no signature

### High Vulnerabilities  
- **Sensitive Data Exposure** - Sensitive information in JWT payloads
- **JWK URL Manipulation** - Exploitable JWK URL parameters
- **Unprotected Endpoints** - Accessible admin/management endpoints

### Medium/Low Vulnerabilities
- **Expired Tokens** - JWT tokens past expiration
- **Missing Expiration** - JWT tokens without expiration
- **Information Disclosure** - Directory listings and exposed files

## 📁 Project Structure

```
bug-bounty-hunter-pro/
├── main.py                 # Main application entry point
├── auth_manager.py         # User authentication system
├── login_window.py         # Login interface
├── main_dashboard.py       # Main application dashboard
├── config_manager.py       # Configuration management
├── zap_manager.py          # OWASP ZAP integration
├── scanner_engine.py       # Core scanning engine
├── jwt_analyzer.py         # JWT vulnerability analysis
├── report_generator.py     # Report generation
├── bug_bounty_finder.py    # Bug bounty program finder
├── install.sh              # Installation script
├── run.sh                  # Application launcher
├── wordlists/              # Fuzzing wordlists
│   ├── directories.txt
│   ├── subdomains.txt
│   └── jwt_secrets.txt
├── data/                   # Application data
│   ├── config.json
│   └── users.json
├── reports/                # Generated reports
├── logs/                   # Application logs
└── assets/                 # Application assets
    └── icon.png
```

## 🔒 Security Features

### Authentication
- **Bcrypt Password Hashing** - Secure password storage
- **Session Management** - Secure user sessions
- **Role-based Access** - Admin and user roles
- **Account Lockout** - Protection against brute force

### Network Security
- **Request Rate Limiting** - Respectful scanning rates
- **User Agent Rotation** - Avoid detection
- **Proxy Support** - Route traffic through ZAP proxy
- **SSL/TLS Support** - Secure HTTPS connections

## 🎯 Bug Bounty Workflow Automation

This tool automates the complete bug bounty workflow described in your scenario:

1. **🔍 Reconnaissance** - Subdomain enumeration and directory discovery
2. **🎯 Target Identification** - Find login endpoints and admin panels  
3. **🔨 Fuzzing** - Directory and parameter fuzzing with redirect bypass
4. **👤 User Creation** - Discover unprotected user registration endpoints
5. **🔐 JWT Analysis** - Detect weak JWT secrets and algorithm confusion
6. **👑 Privilege Escalation** - Identify admin panel access vulnerabilities
7. **📋 Reporting** - Generate professional vulnerability reports

## 🐛 Bug Bounty Programs Finder

The included `bug_bounty_finder.py` script searches for active bug bounty programs:

### Top Paying Programs (as of 2024):
1. **Apple Security Bounty** - Up to $1,000,000+
2. **Google VRP** - Up to $31,337+  
3. **Zoom** - Up to $50,000+
4. **Coinbase** - Up to $50,000+
5. **Shopify** - Up to $25,000+
6. **Discord** - Up to $25,000+

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**IMPORTANT:** This tool is designed for authorized security testing only. Users are responsible for:

- Obtaining proper authorization before testing any systems
- Complying with all applicable laws and regulations
- Following responsible disclosure practices
- Respecting bug bounty program terms and conditions

**The developers are not responsible for any misuse of this tool.**

## 🆘 Support

### Getting Help
- 📖 Check the documentation in this README
- 🐛 Report bugs via GitHub Issues
- 💬 Join our community discussions
- 📧 Contact: support@bugbountyhunterpro.com

### Common Issues

**ZAP Connection Failed:**
```bash
# Ensure ZAP is installed and running
sudo apt install zaproxy
zaproxy -daemon -port 8080
```

**Permission Denied:**
```bash
# Fix file permissions
chmod +x install.sh run.sh
```

**Python Dependencies:**
```bash
# Reinstall in virtual environment
source bug_bounty_env/bin/activate
pip install --upgrade -r requirements.txt
```

## 🚀 Roadmap

### Version 1.1 (Coming Soon)
- [ ] Advanced payload generation
- [ ] Custom vulnerability checks
- [ ] API endpoint discovery
- [ ] Mobile app testing support

### Version 1.2 (Future)
- [ ] Machine learning vulnerability detection
- [ ] Automated exploit generation
- [ ] Cloud deployment support
- [ ] Team collaboration features

---

**Made with ❤️ for the bug bounty community**

*Happy Hunting! 🎯*