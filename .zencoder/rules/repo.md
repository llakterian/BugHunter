---
description: Repository Information Overview
alwaysApply: true
---

# Bug Bounty Hunter Pro Information

## Summary
Bug Bounty Hunter Pro is an advanced security testing tool designed for ethical hackers and security professionals. It provides a GUI-based platform for automating bug bounty hunting tasks, vulnerability scanning, and security testing with OWASP ZAP integration.

## Structure
- **assets/**: Application icons and visual resources
- **data/**: Configuration files and user data storage
- **docker/**: Docker configuration for containerized deployment
- **docs/**: Project documentation
- **logs/**: Application logs
- **reports/**: Generated security reports
- **scripts/**: Utility scripts for development and testing
- **temp/**: Temporary files
- **wordlists/**: Security testing wordlists for various attack vectors
- **.github/**: GitHub workflows and CI/CD configuration

## Language & Runtime
**Language**: Python
**Version**: 3.8-3.12 (primary: 3.11)
**Build System**: PyInstaller
**Package Manager**: pip

## Dependencies
**Main Dependencies**:
- PyQt6: GUI framework for desktop application
- requests: HTTP client for web requests
- python-owasp-zap-v2.4: OWASP ZAP integration
- beautifulsoup4/lxml: Web scraping and parsing
- cryptography/PyJWT/bcrypt: Security and authentication
- dnspython/python-nmap/scapy: Network scanning tools

**Development Dependencies**:
- pytest/pytest-cov: Testing framework
- black/flake8/isort/mypy/pylint: Code quality tools
- sphinx/mkdocs: Documentation generation
- pre-commit: Git hooks for code quality

## Build & Installation
```bash
# Basic installation
./install.sh

# Development setup
pip install -r requirements-dev.txt

# Run application
./run.sh
```

## Docker
**Dockerfile**: Multi-stage build with Python 3.11
**Image**: bughunterpro/bug-bounty-hunter:latest
**Configuration**: Docker Compose with Redis, PostgreSQL, Nginx, and optional monitoring services

```bash
# Build and run with Docker
docker-compose up -d
```

## Testing
**Framework**: pytest with multiple plugins
**Test Location**: tests/ directory
**Configuration**: CI workflow in .github/workflows/ci.yml
**Run Command**:
```bash
# Quick test
python quick_test.py

# Full test suite
pytest tests/ -v --cov=.
```

## Main Components
- **main.py**: Application entry point with PyQt6 GUI
- **scanner_engine.py**: Core vulnerability scanning engine
- **main_dashboard.py**: Main application dashboard UI
- **tool_integrations.py**: Integration with external security tools
- **report_generator.py**: Security report generation
- **auth_manager.py**: User authentication and session management
- **config_manager.py**: Application configuration handling
- **nuclei_shodan_integration.py**: Mass CVE scanning with Shodan & Nuclei
- **lost_uncover.py**: Tool to uncover hidden elements on web pages
- **lost_fuzzer.py**: Quick DAST scanner using Nuclei for domains
- **recon_automation.py**: Automated reconnaissance with multiple sources
- **bug_hunting_workflow.py**: Complete workflow combining all bug hunting methods

## Enhanced Features (33X More Robust)
- **Mass CVE Scanning**: Shodan integration for large-scale vulnerability hunting
- **Hidden Element Discovery**: Bookmarklet-based tools to reveal client-side restrictions
- **Automated Recon**: Multi-source URL discovery (AlienVault, Wayback, URLScan, VirusTotal)
- **GF Pattern Filtering**: Advanced URL filtering with custom patterns and deduplication
- **LostFuzzer Integration**: Passive URL fuzzing and Nuclei DAST scanning
- **Complete Workflow Automation**: End-to-end bug hunting pipeline