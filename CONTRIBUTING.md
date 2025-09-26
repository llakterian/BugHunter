# Contributing to Bug Bounty Hunter Pro

🎉 **Thank you for your interest in contributing to Bug Bounty Hunter Pro!** 

We welcome contributions from the security community, developers, and researchers worldwide. This guide will help you get started with contributing to our project.

## 🌟 Ways to Contribute

### 🐛 Bug Reports
- Report bugs and issues
- Provide detailed reproduction steps
- Include system information and logs
- Suggest potential fixes

### 💡 Feature Requests
- Propose new vulnerability detection modules
- Suggest UI/UX improvements
- Request new exploitation techniques
- Recommend reporting enhancements

### 🔧 Code Contributions
- Fix bugs and issues
- Implement new features
- Improve performance
- Enhance security measures
- Add test coverage

### 📚 Documentation
- Improve existing documentation
- Write tutorials and guides
- Translate documentation
- Create video tutorials

### 🧪 Testing
- Test new features and releases
- Perform security testing
- Validate on different platforms
- Provide feedback on usability

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git version control
- Basic understanding of security testing
- Familiarity with PyQt6 (for UI contributions)

### Development Environment Setup

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/yourusername/BugHunter.git
cd BugHunter

# 3. Add upstream remote
git remote add upstream https://github.com/llakterian/BugHunter.git

# 4. Create development environment
python3 -m venv dev_env
source dev_env/bin/activate  # On Windows: dev_env\Scripts\activate

# 5. Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 6. Install pre-commit hooks
pre-commit install

# 7. Run tests to ensure everything works
python3 -m pytest tests/
```

### Development Dependencies
```bash
# Install additional development tools
pip install pytest pytest-cov black flake8 mypy pre-commit
```

## 📋 Development Guidelines

### Code Style
We follow PEP 8 with some modifications:

```python
# Use Black for code formatting
black --line-length 100 your_file.py

# Use flake8 for linting
flake8 --max-line-length 100 your_file.py

# Use mypy for type checking
mypy your_file.py
```

### Coding Standards
- **Line Length:** Maximum 100 characters
- **Indentation:** 4 spaces (no tabs)
- **Naming:** snake_case for functions/variables, PascalCase for classes
- **Docstrings:** Use Google-style docstrings
- **Type Hints:** Include type hints for all functions
- **Comments:** Write clear, concise comments for complex logic

### Example Code Structure
```python
"""
Module docstring describing the purpose and functionality.
"""

import os
import sys
from typing import Dict, List, Optional

from PyQt6.QtCore import QObject, pyqtSignal


class VulnerabilityScanner(QObject):
    """
    A class for scanning vulnerabilities in web applications.
    
    Attributes:
        target_url: The URL to scan for vulnerabilities.
        scan_results: Dictionary containing scan results.
    """
    
    scan_completed = pyqtSignal(dict)
    
    def __init__(self, target_url: str) -> None:
        """
        Initialize the vulnerability scanner.
        
        Args:
            target_url: The target URL to scan.
        """
        super().__init__()
        self.target_url = target_url
        self.scan_results: Dict[str, List[str]] = {}
    
    def scan_for_sql_injection(self, parameters: List[str]) -> Optional[Dict[str, str]]:
        """
        Scan for SQL injection vulnerabilities.
        
        Args:
            parameters: List of parameters to test.
            
        Returns:
            Dictionary containing vulnerability details if found, None otherwise.
        """
        # Implementation here
        pass
```

## 🔄 Contribution Workflow

### 1. Issue Creation
Before starting work, create or find an existing issue:

```markdown
**Issue Type:** [Bug Report/Feature Request/Enhancement]
**Priority:** [High/Medium/Low]
**Component:** [Scanner Engine/UI/Reporting/etc.]

**Description:**
Clear description of the issue or feature request.

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Additional Context:**
Any additional information, screenshots, or examples.
```

### 2. Branch Creation
Create a feature branch for your work:

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/vulnerability-scanner-enhancement
# or
git checkout -b bugfix/fix-sql-injection-detection
# or
git checkout -b docs/update-installation-guide
```

### 3. Development Process
- Write code following our coding standards
- Add comprehensive tests for new functionality
- Update documentation as needed
- Ensure all tests pass
- Run security checks

```bash
# Run tests
python3 -m pytest tests/ -v

# Run with coverage
python3 -m pytest tests/ --cov=. --cov-report=html

# Run security checks
bandit -r . -x tests/

# Run type checking
mypy .

# Format code
black .
```

### 4. Commit Guidelines
Follow conventional commit format:

```bash
# Format: type(scope): description
git commit -m "feat(scanner): add advanced SQL injection detection"
git commit -m "fix(ui): resolve responsive design issue on mobile"
git commit -m "docs(readme): update installation instructions"
git commit -m "test(scanner): add unit tests for XSS detection"
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `style`: Code style changes
- `chore`: Maintenance tasks

### 5. Pull Request Process

#### Before Submitting
- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Security checks pass
- [ ] No merge conflicts

#### Pull Request Template
```markdown
## 📋 Description
Brief description of changes made.

## 🔗 Related Issue
Closes #123

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

## 🔍 Security Considerations
Describe any security implications of the changes.

## 📝 Additional Notes
Any additional information for reviewers.
```

## 🧪 Testing Guidelines

### Test Structure
```
tests/
├── unit/
│   ├── test_scanner_engine.py
│   ├── test_vulnerability_validator.py
│   └── test_exploitation_engine.py
├── integration/
│   ├── test_full_scan_workflow.py
│   └── test_report_generation.py
├── fixtures/
│   ├── sample_responses.json
│   └── test_wordlists.txt
└── conftest.py
```

### Writing Tests
```python
import pytest
from unittest.mock import Mock, patch

from scanner_engine import ScannerEngine


class TestScannerEngine:
    """Test cases for the ScannerEngine class."""
    
    @pytest.fixture
    def scanner_engine(self):
        """Create a ScannerEngine instance for testing."""
        config_manager = Mock()
        return ScannerEngine(config_manager)
    
    def test_sql_injection_detection(self, scanner_engine):
        """Test SQL injection detection functionality."""
        # Arrange
        test_url = "https://example.com/test"
        expected_vulnerability = {
            'type': 'SQL Injection',
            'severity': 'Critical',
            'url': test_url
        }
        
        # Act
        with patch('requests.get') as mock_get:
            mock_get.return_value.text = "mysql_fetch_array() error"
            result = scanner_engine.detect_sql_injection(test_url)
        
        # Assert
        assert result is not None
        assert result['type'] == expected_vulnerability['type']
        assert result['severity'] == expected_vulnerability['severity']
    
    @pytest.mark.integration
    def test_full_scan_workflow(self, scanner_engine):
        """Test the complete scanning workflow."""
        # Integration test implementation
        pass
```

### Test Categories
- **Unit Tests:** Test individual functions and methods
- **Integration Tests:** Test component interactions
- **Security Tests:** Test security-related functionality
- **Performance Tests:** Test performance and scalability
- **UI Tests:** Test user interface components

## 📚 Documentation Standards

### Code Documentation
```python
def scan_for_vulnerabilities(
    self, 
    target_url: str, 
    scan_types: List[str], 
    timeout: int = 30
) -> Dict[str, List[Dict[str, str]]]:
    """
    Scan a target URL for various types of vulnerabilities.
    
    This method performs comprehensive vulnerability scanning including
    SQL injection, XSS, and other common web application vulnerabilities.
    
    Args:
        target_url: The URL to scan for vulnerabilities.
        scan_types: List of vulnerability types to scan for.
            Valid types: ['sql_injection', 'xss', 'lfi', 'rce']
        timeout: Request timeout in seconds. Defaults to 30.
    
    Returns:
        Dictionary mapping vulnerability types to lists of found vulnerabilities.
        Each vulnerability is represented as a dictionary with keys:
        - 'type': Vulnerability type
        - 'severity': Severity level (Critical/High/Medium/Low)
        - 'url': Affected URL
        - 'description': Detailed description
        - 'proof': Proof of concept
    
    Raises:
        ValueError: If target_url is invalid or scan_types is empty.
        ConnectionError: If unable to connect to target.
        
    Example:
        >>> scanner = VulnerabilityScanner()
        >>> results = scanner.scan_for_vulnerabilities(
        ...     "https://example.com",
        ...     ["sql_injection", "xss"]
        ... )
        >>> print(results['sql_injection'])
        [{'type': 'SQL Injection', 'severity': 'Critical', ...}]
    """
```

### README Updates
When adding new features, update relevant documentation:
- Installation instructions
- Usage examples
- Configuration options
- API documentation

## 🔒 Security Considerations

### Security Review Process
All contributions undergo security review:

1. **Automated Security Scanning**
   - Static analysis with Bandit
   - Dependency vulnerability scanning
   - Code quality checks

2. **Manual Security Review**
   - Code review by security team
   - Threat modeling for new features
   - Penetration testing for security features

### Security Guidelines
- Never hardcode credentials or secrets
- Validate and sanitize all inputs
- Use parameterized queries for database operations
- Implement proper error handling
- Follow principle of least privilege
- Use secure communication protocols

### Reporting Security Issues
If you discover security vulnerabilities during development:
1. **DO NOT** create a public issue
2. Email security@bughunterpro.com immediately
3. Include detailed information about the vulnerability
4. Wait for security team response before proceeding

## 🏆 Recognition

### Contributor Recognition
We recognize contributors in several ways:

- **GitHub Contributors Page:** Automatic recognition for merged PRs
- **Release Notes:** Major contributors mentioned in release notes
- **Hall of Fame:** Top contributors featured on our website
- **Swag:** Bug Bounty Hunter Pro merchandise for significant contributions
- **Conference Mentions:** Recognition at security conferences

### Contribution Levels
- **🥉 Bronze:** 1-5 merged PRs
- **🥈 Silver:** 6-15 merged PRs or significant feature contribution
- **🥇 Gold:** 16+ merged PRs or major architectural contribution
- **💎 Diamond:** Long-term maintainer or exceptional contribution

## 📞 Getting Help

### Communication Channels
- **Discord:** [Join our developer community](https://discord.gg/bughunter-dev)
- **GitHub Discussions:** [Ask questions and discuss ideas](https://github.com/llakterian/BugHunter/discussions)
- **Email:** developers@bughunterpro.com
- **Weekly Office Hours:** Fridays 2-3 PM UTC on Discord

### Mentorship Program
New contributors can request mentorship:
- Pair programming sessions
- Code review guidance
- Architecture discussions
- Career advice in security field

## 📅 Release Process

### Release Schedule
- **Major Releases:** Quarterly (March, June, September, December)
- **Minor Releases:** Monthly
- **Patch Releases:** As needed for critical fixes

### Release Criteria
- All tests pass
- Security review completed
- Documentation updated
- Performance benchmarks met
- Community feedback incorporated

## 🎯 Roadmap Participation

### Feature Planning
Contributors can participate in feature planning:
- Quarterly planning meetings
- Feature request discussions
- Architecture decision records (ADRs)
- Community voting on priorities

### Special Interest Groups (SIGs)
Join specialized groups:
- **SIG-Security:** Security feature development
- **SIG-UI/UX:** User interface improvements
- **SIG-Performance:** Performance optimization
- **SIG-Documentation:** Documentation improvements

## 📜 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Experience level
- Gender identity and expression
- Sexual orientation
- Disability
- Personal appearance
- Body size
- Race
- Ethnicity
- Age
- Religion
- Nationality

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior
- Harassment or discriminatory language
- Personal attacks or trolling
- Public or private harassment
- Publishing others' private information
- Other conduct inappropriate in a professional setting

### Enforcement
Code of conduct violations should be reported to conduct@bughunterpro.com. All reports will be reviewed and investigated promptly and fairly.

## 📋 Contributor License Agreement

By contributing to Bug Bounty Hunter Pro, you agree that:

1. Your contributions are your original work
2. You have the right to submit the contributions
3. Your contributions are licensed under the MIT License
4. You grant us the right to use your contributions
5. You understand this is a security testing tool for authorized use only

## 🎉 Thank You!

Thank you for contributing to Bug Bounty Hunter Pro! Your contributions help make the security community stronger and more effective.

**Happy Contributing! 🚀**

---

*This contributing guide is a living document and will be updated as our project evolves. Please check back regularly for updates.*