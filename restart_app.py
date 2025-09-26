#!/usr/bin/env python3
"""
Quick restart script to apply UI changes
"""

import subprocess
import sys
import os
import time

def restart_app():
    """Restart the Bug Bounty Hunter Pro application"""
    print("🔄 Restarting Bug Bounty Hunter Pro with improved UI...")
    
    # Kill any existing processes
    try:
        subprocess.run(["pkill", "-f", "main.py"], capture_output=True)
        time.sleep(1)
    except:
        pass
    
    # Start the application
    try:
        subprocess.run(["./run.sh"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")
        return False
    
    return True

if __name__ == "__main__":
    restart_app()