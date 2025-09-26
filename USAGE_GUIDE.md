# Bug Bounty Hunter Pro - Usage Guide 🎯

## Quick Start

### 1. Installation
```bash
# Clone or download the project
git clone <repository-url>
cd bug-bounty-hunter-pro

# Run installation
chmod +x install.sh
./install.sh

# Test installation
./test_installation.py
```

### 2. First Launch
```bash
# Start the application
./run.sh

# Default login credentials:
# Username: admin
# Password: BugHunter2024!
```

## Complete Bug Bounty Workflow

### Step 1: Target Configuration
1. **Enter Target URL**: `https://example.com`
2. **Select Wordlist**: Choose from Default, Common, Extensive, or Custom
3. **Configure Threads**: Set number of concurrent threads (1-50)
4. **Set Timeout**: Request timeout in seconds (5-120)

### Step 2: Scan Options
Enable the scans you want to perform:
- ✅ **Directory Fuzzing** - Find hidden directories and files
- ✅ **Subdomain Enumeration** - Discover subdomains
- ✅ **JWT Analysis** - Analyze JWT tokens for vulnerabilities
- ✅ **Admin Panel Discovery** - Find admin interfaces
- ✅ **Bypass Redirects** - Ignore HTTP redirects

### Step 3: OWASP ZAP Integration (Optional)
1. **Start ZAP**: Click "Start ZAP" to launch ZAP daemon
2. **Connect**: Click "Connect ZAP" to establish connection
3. **Spider Scan**: Crawl the target website
4. **Active Scan**: Perform active vulnerability scanning

### Step 4: Start Bug Hunt
1. Click **"Start Bug Hunt"** button
2. Monitor progress in real-time
3. View results in the tabs:
   - **Results**: Discovered endpoints and directories
   - **Logs**: Detailed scanning logs
   - **Vulnerabilities**: Found security issues

### Step 5: Generate Report
1. Click **"Generate Report"** when scan completes
2. Choose format (HTML or JSON)
3. Professional report saved to `reports/` directory

## Vulnerability Types Detected

### 🔴 Critical Vulnerabilities
- **JWT Weak Secrets**: Weak signing secrets allowing token forgery
- **Admin Panel Exposure**: Unprotected administrative interfaces
- **Algorithm Confusion**: RS256/HS256 JWT vulnerabilities
- **None Algorithm**: JWT tokens accepting no signature

### 🟠 High Vulnerabilities
- **Sensitive Data Exposure**: Sensitive information in JWT payloads
- **JWK URL Manipulation**: Exploitable JWK URL parameters
- **Unprotected Endpoints**: Accessible admin/management endpoints

### 🟡 Medium Vulnerabilities
- **Expired Tokens**: JWT tokens past expiration
- **Missing Expiration**: JWT tokens without expiration
- **Information Disclosure**: Directory listings and exposed files

## Bug Bounty Site Finder

Find active bug bounty programs:

```bash
# Activate virtual environment
source bug_bounty_env/bin/activate

# Run bug bounty finder
python3 bug_bounty_finder.py
```

### Top Programs Found:
1. **Apple Security Bounty** - Up to $1,000,000+
2. **Google VRP** - Up to $31,337+
3. **Zoom** - Up to $50,000+
4. **Coinbase** - Up to $50,000+
5. **Shopify** - Up to $25,000+
6. **Discord** - Up to $25,000+

## Advanced Configuration

### Custom Wordlists
Replace files in `wordlists/` directory:
- `directories.txt` - Directory fuzzing wordlist
- `subdomains.txt` - Subdomain enumeration wordlist
- `jwt_secrets.txt` - JWT weak secrets wordlist

### Configuration File
Edit `data/config.json`:
```json
{
  "zap": {
    "host": "127.0.0.1",
    "port": 8080,
    "api_key": ""
  },
  "scanning": {
    "max_threads": 10,
    "timeout": 30,
    "user_agent": "BugBountyHunterPro/1.0"
  }
}
```

## Replicating Your Bug Bounty Success

This tool automates the exact workflow you described:

### 1. Subdomain Discovery (DuckDuckGo Dorking)
- **Automated**: Subdomain enumeration finds hidden subdomains
- **Manual Alternative**: Use Google/DuckDuckGo dorks manually

### 2. Login Endpoint Discovery
- **Automated**: Directory fuzzing discovers login endpoints
- **Detection**: Identifies different login vs user endpoints

### 3. Endpoint Fuzzing with Redirect Bypass
- **Automated**: Fuzzes endpoints and bypasses redirects
- **Burp Alternative**: Built-in redirect bypass functionality

### 4. User Management Endpoint Discovery
- **Automated**: Discovers admin and user management endpoints
- **Authentication Check**: Tests for missing authentication

### 5. User Creation Testing
- **Automated**: Tests user creation endpoints
- **Vulnerability Detection**: Identifies unprotected registration

### 6. JWT Analysis
- **Automated**: Extracts and analyzes JWT tokens
- **Weak Secret Detection**: Brute forces JWT signing secrets
- **Algorithm Confusion**: Tests for RS256/HS256 vulnerabilities

### 7. Admin Panel Access
- **Automated**: Discovers and tests admin panel access
- **Privilege Escalation**: Identifies unauthorized admin access

## Tips for Maximum Impact

### 1. Target Selection
- Choose targets with active bug bounty programs
- Focus on high-paying programs (use bug bounty finder)
- Read program scope and rules carefully

### 2. Scanning Strategy
- Start with subdomain enumeration
- Use comprehensive wordlists
- Enable all scan types for maximum coverage
- Use ZAP integration for additional coverage

### 3. Manual Verification
- Always manually verify automated findings
- Test edge cases and variations
- Document steps for reproduction

### 4. Reporting
- Use generated reports as starting point
- Add manual verification steps
- Include impact assessment
- Provide clear reproduction steps

## Troubleshooting

### Common Issues

**ZAP Connection Failed:**
```bash
# Install ZAP
sudo apt install zaproxy

# Start ZAP manually
zaproxy -daemon -port 8080
```

**Permission Denied:**
```bash
# Fix permissions
chmod +x install.sh run.sh main.py
```

**Missing Dependencies:**
```bash
# Reinstall dependencies
source bug_bounty_env/bin/activate
pip install -r requirements.txt
```

**GUI Not Starting:**
```bash
# Install Qt6 dependencies
sudo apt install python3-pyqt6 qt6-base-dev
```

### Performance Optimization

**Increase Threads:**
- More threads = faster scanning
- Be careful not to overwhelm target
- Start with 10 threads, increase gradually

**Timeout Settings:**
- Lower timeout = faster scanning
- Higher timeout = more reliable results
- Adjust based on target response time

**Wordlist Selection:**
- Default: Fast, basic coverage
- Common: Good balance of speed and coverage
- Extensive: Comprehensive but slower
- Custom: Use your own wordlists

## Legal and Ethical Guidelines

### ⚠️ Important Disclaimers

1. **Authorization Required**: Only test systems you own or have explicit permission to test
2. **Bug Bounty Programs**: Follow program rules and scope
3. **Responsible Disclosure**: Report vulnerabilities responsibly
4. **Rate Limiting**: Don't overwhelm target systems
5. **Legal Compliance**: Follow all applicable laws and regulations

### Best Practices

1. **Read Program Rules**: Understand scope, rules, and restrictions
2. **Start Small**: Begin with basic scans before intensive testing
3. **Document Everything**: Keep detailed records of your testing
4. **Respect Systems**: Don't cause damage or disruption
5. **Professional Communication**: Maintain professional communication with vendors

## Support and Community

### Getting Help
- 📖 Read this guide and README.md
- 🧪 Run `./test_installation.py` to verify setup
- 🐛 Report issues on GitHub
- 💬 Join community discussions

### Contributing
- Fork the repository
- Create feature branches
- Submit pull requests
- Share wordlists and improvements

---

**Happy Bug Hunting! 🎯**

*Remember: With great power comes great responsibility. Use this tool ethically and legally.*