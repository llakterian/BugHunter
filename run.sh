#!/bin/bash
# Bug Bounty Hunter Pro - Run Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
source bug_bounty_env/bin/activate

# Run the application
python3 main.py "$@"
