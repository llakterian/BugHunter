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
