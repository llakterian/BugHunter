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
