#!/bin/bash

# Bug Bounty Hunter Pro - GitHub Repository Setup Script
# This script initializes the GitHub repository with all necessary files and configurations

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Repository information
REPO_URL="https://github.com/llakterian/BugHunter.git"
REPO_NAME="BugHunter"
BRANCH_MAIN="main"
BRANCH_DEVELOP="develop"

echo -e "${BLUE}🎯 Bug Bounty Hunter Pro - GitHub Repository Setup${NC}"
echo "=================================================="

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

print_status "Git is available"

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -f "scanner_engine.py" ]; then
    print_error "This script must be run from the Bug Bounty Hunter Pro root directory"
    exit 1
fi

print_status "In correct directory"

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    print_info "Initializing Git repository..."
    git init
    print_status "Git repository initialized"
else
    print_info "Git repository already exists"
fi

# Create necessary directories
print_info "Creating directory structure..."
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p .github/PULL_REQUEST_TEMPLATE
mkdir -p docs
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/performance
mkdir -p docker/nginx
mkdir -p docker/postgres
mkdir -p docker/prometheus
mkdir -p docker/grafana/dashboards
mkdir -p docker/grafana/datasources
mkdir -p config
mkdir -p scripts

print_status "Directory structure created"

# Create GitHub issue templates
print_info "Creating GitHub issue templates..."

cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: 🐛 Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

## 🐛 Bug Description
A clear and concise description of what the bug is.

## 🔄 Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## ✅ Expected Behavior
A clear and concise description of what you expected to happen.

## ❌ Actual Behavior
A clear and concise description of what actually happened.

## 📸 Screenshots
If applicable, add screenshots to help explain your problem.

## 🖥️ Environment
- OS: [e.g. Ubuntu 20.04]
- Python Version: [e.g. 3.9.2]
- Application Version: [e.g. 2.0.0]
- Browser (if applicable): [e.g. Chrome 96]

## 📋 Additional Context
Add any other context about the problem here.

## 🔍 Possible Solution
If you have ideas on how to fix this, please describe them here.
EOF

cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: 💡 Feature Request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

## 💡 Feature Description
A clear and concise description of what you want to happen.

## 🎯 Problem Statement
Is your feature request related to a problem? Please describe.
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

## 💭 Proposed Solution
A clear and concise description of what you want to happen.

## 🔄 Alternative Solutions
A clear and concise description of any alternative solutions or features you've considered.

## 📋 Additional Context
Add any other context or screenshots about the feature request here.

## ✅ Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## 🎨 Mockups/Examples
If applicable, add mockups or examples to help explain your feature request.
EOF

cat > .github/ISSUE_TEMPLATE/security_report.md << 'EOF'
---
name: 🔒 Security Report
about: Report a security vulnerability (use private disclosure)
title: '[SECURITY] '
labels: 'security'
assignees: ''
---

## ⚠️ SECURITY NOTICE
**Please do not report security vulnerabilities in public issues.**

For security vulnerabilities, please:
1. Email security@bughunterpro.com
2. Use GitHub Security Advisory (private)
3. Include detailed information about the vulnerability
4. Allow time for responsible disclosure

## 🔒 For Non-Critical Security Improvements
If this is a general security improvement suggestion (not a vulnerability):

### Description
Describe the security improvement you're suggesting.

### Impact
What security benefit would this provide?

### Implementation
How could this be implemented?
EOF

print_status "GitHub issue templates created"

# Create pull request template
print_info "Creating pull request template..."

cat > .github/PULL_REQUEST_TEMPLATE/pull_request_template.md << 'EOF'
## 📋 Description
Brief description of changes made.

## 🔗 Related Issue
Closes #(issue number)

## 🧪 Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Security testing performed

## 📸 Screenshots (if applicable)
Include screenshots for UI changes.

## ✅ Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added for new functionality
- [ ] All tests pass
- [ ] Security implications considered
- [ ] Breaking changes documented

## 🔍 Security Considerations
Describe any security implications of the changes.

## 📝 Additional Notes
Any additional information for reviewers.

## 🎯 Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring
EOF

print_status "Pull request template created"

# Create basic documentation structure
print_info "Creating documentation structure..."

cat > docs/README.md << 'EOF'
# Bug Bounty Hunter Pro Documentation

Welcome to the Bug Bounty Hunter Pro documentation!

## 📚 Documentation Structure

- [Installation Guide](installation.md)
- [User Manual](user-manual.md)
- [Configuration Guide](configuration.md)
- [API Reference](api-reference.md)
- [Developer Guide](developer-guide.md)
- [Security Guide](security-guide.md)
- [Troubleshooting](troubleshooting.md)

## 🚀 Quick Links

- [Getting Started](installation.md#quick-start)
- [Basic Usage](user-manual.md#basic-usage)
- [Advanced Features](user-manual.md#advanced-features)
- [Contributing](../CONTRIBUTING.md)
- [Security Policy](../SECURITY.md)

## 📞 Support

- [GitHub Issues](https://github.com/llakterian/BugHunter/issues)
- [Discord Community](https://discord.gg/bughunter)
- Email: support@bughunterpro.com
EOF

print_status "Documentation structure created"

# Create Docker configuration files
print_info "Creating Docker configuration files..."

cat > docker/nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream bughunter {
        server bughunter:8080;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://bughunter;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /reports/ {
            alias /var/www/reports/;
            autoindex on;
        }

        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
EOF

cat > docker/postgres/init.sql << 'EOF'
-- Bug Bounty Hunter Pro Database Initialization

-- Create database schema
CREATE SCHEMA IF NOT EXISTS bughunter;

-- Create tables for future use
CREATE TABLE IF NOT EXISTS bughunter.scan_results (
    id SERIAL PRIMARY KEY,
    target_url VARCHAR(255) NOT NULL,
    scan_type VARCHAR(50) NOT NULL,
    vulnerability_type VARCHAR(100),
    severity VARCHAR(20),
    description TEXT,
    proof_of_concept TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bughunter.exploitation_results (
    id SERIAL PRIMARY KEY,
    scan_result_id INTEGER REFERENCES bughunter.scan_results(id),
    exploitation_successful BOOLEAN DEFAULT FALSE,
    data_extracted JSONB,
    shells_obtained JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_scan_results_target ON bughunter.scan_results(target_url);
CREATE INDEX IF NOT EXISTS idx_scan_results_type ON bughunter.scan_results(scan_type);
CREATE INDEX IF NOT EXISTS idx_scan_results_severity ON bughunter.scan_results(severity);
EOF

print_status "Docker configuration files created"

# Create environment file template
print_info "Creating environment configuration..."

cat > .env.example << 'EOF'
# Bug Bounty Hunter Pro Environment Configuration

# Application Settings
BBH_ENV=development
BBH_LOG_LEVEL=INFO
BBH_DEBUG=false

# Database Configuration
POSTGRES_PASSWORD=bughunter2024
REDIS_PASSWORD=bughunter2024

# Security Settings
JWT_SECRET_KEY=your-super-secret-jwt-key-here
ENCRYPTION_KEY=your-encryption-key-here

# External Services
DISCORD_WEBHOOK=https://discord.com/api/webhooks/your-webhook-here

# Monitoring
GRAFANA_PASSWORD=bughunter2024
VNC_PASSWORD=bughunter

# API Keys (for future integrations)
SHODAN_API_KEY=your-shodan-api-key
VIRUSTOTAL_API_KEY=your-virustotal-api-key
CENSYS_API_ID=your-censys-api-id
CENSYS_API_SECRET=your-censys-api-secret
EOF

print_status "Environment configuration created"

# Create development scripts
print_info "Creating development scripts..."

cat > scripts/dev-setup.sh << 'EOF'
#!/bin/bash
# Development environment setup script

echo "🚀 Setting up development environment..."

# Create virtual environment
python3 -m venv dev_env
source dev_env/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run initial tests
pytest tests/ -v

echo "✅ Development environment ready!"
EOF

chmod +x scripts/dev-setup.sh

cat > scripts/run-tests.sh << 'EOF'
#!/bin/bash
# Comprehensive test runner script

echo "🧪 Running comprehensive test suite..."

# Unit tests
echo "Running unit tests..."
pytest tests/unit/ -v --cov=. --cov-report=html

# Integration tests
echo "Running integration tests..."
pytest tests/integration/ -v

# Security tests
echo "Running security tests..."
bandit -r . -x tests/

# Code quality
echo "Running code quality checks..."
black --check .
flake8 .
mypy .

echo "✅ All tests completed!"
EOF

chmod +x scripts/run-tests.sh

print_status "Development scripts created"

# Add all files to git
print_info "Adding files to Git..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    print_info "No changes to commit"
else
    # Commit initial files
    print_info "Committing initial files..."
    git commit -m "🎯 Initial commit: Bug Bounty Hunter Pro v2.0

✨ Features:
- Advanced vulnerability discovery and validation
- Automated exploitation engine with proof-of-concept generation
- Professional bug bounty report generation
- Multi-platform support (Linux, Windows, macOS)
- Docker containerization with full stack
- Comprehensive CI/CD pipeline
- Security-focused development practices

🛡️ Security:
- Automated vulnerability validation
- Safe exploitation techniques
- Responsible disclosure guidelines
- Comprehensive security testing

📊 Reporting:
- HTML, JSON, and Markdown report formats
- CVSS scoring and CWE classification
- Business impact assessment
- Remediation roadmaps

🚀 Ready for professional bug bounty hunting!"

    print_status "Initial commit created"
fi

# Set up remote repository if provided
if [ ! -z "$REPO_URL" ]; then
    print_info "Setting up remote repository..."
    
    # Check if remote already exists
    if git remote get-url origin &> /dev/null; then
        print_info "Remote origin already exists"
    else
        git remote add origin "$REPO_URL"
        print_status "Remote origin added"
    fi
    
    # Create and switch to main branch
    git branch -M main
    
    # Create develop branch
    git checkout -b develop
    git checkout main
    
    print_status "Branch structure created"
    
    # Push to remote
    print_info "Pushing to remote repository..."
    echo -e "${YELLOW}Note: You may need to authenticate with GitHub${NC}"
    
    if git push -u origin main; then
        print_status "Pushed to main branch"
        
        if git push -u origin develop; then
            print_status "Pushed to develop branch"
        else
            print_warning "Failed to push develop branch"
        fi
    else
        print_warning "Failed to push to remote. You may need to:"
        echo "1. Create the repository on GitHub first"
        echo "2. Set up authentication (SSH keys or personal access token)"
        echo "3. Run: git push -u origin main"
    fi
fi

# Create GitHub repository using GitHub CLI (if available)
if command -v gh &> /dev/null; then
    print_info "GitHub CLI detected. You can create the repository with:"
    echo "gh repo create llakterian/BugHunter --public --description 'Advanced Bug Bounty Hunting Platform'"
else
    print_info "GitHub CLI not found. Create repository manually at:"
    echo "https://github.com/new"
fi

# Final instructions
echo ""
echo -e "${GREEN}🎉 Repository setup completed successfully!${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Create the repository on GitHub: https://github.com/new"
echo "2. Set repository name: BugHunter"
echo "3. Add description: Advanced Bug Bounty Hunting Platform"
echo "4. Make it public"
echo "5. Push your code: git push -u origin main"
echo ""
echo -e "${BLUE}🔧 Development:${NC}"
echo "- Run ./scripts/dev-setup.sh to set up development environment"
echo "- Run ./scripts/run-tests.sh to execute test suite"
echo "- Use docker-compose up to run the full stack"
echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo "- README.md: Main project documentation"
echo "- CONTRIBUTING.md: Contribution guidelines"
echo "- SECURITY.md: Security policy and reporting"
echo "- docs/: Detailed documentation"
echo ""
echo -e "${BLUE}🚀 Deployment:${NC}"
echo "- Docker: docker-compose up"
echo "- Local: ./run.sh"
echo "- CI/CD: Automated via GitHub Actions"
echo ""
echo -e "${GREEN}Happy Bug Hunting! 🎯${NC}"