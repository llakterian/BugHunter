#!/bin/bash
# Bug Bounty Hunter Pro - Build Standalone Executable

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Building Bug Bounty Hunter Pro standalone executable..."

# Activate virtual environment
source bug_bounty_env/bin/activate

# Build with PyInstaller
pyinstaller --onefile \
    --windowed \
    --name "Bug Bounty Hunter Pro" \
    --icon assets/icon.png \
    --add-data "assets:assets" \
    --add-data "wordlists:wordlists" \
    --add-data "data:data" \
    --hidden-import PyQt6.QtCore \
    --hidden-import PyQt6.QtWidgets \
    --hidden-import PyQt6.QtGui \
    --hidden-import requests \
    --hidden-import beautifulsoup4 \
    --hidden-import lxml \
    --hidden-import cryptography \
    --hidden-import bcrypt \
    --hidden-import jwt \
    --hidden-import python_nmap \
    --hidden-import scapy \
    --hidden-import websockets \
    main.py

echo "✅ Build completed! Executable created at: dist/Bug Bounty Hunter Pro"
echo "🎯 To run: ./dist/Bug\ Bounty\ Hunter\ Pro"