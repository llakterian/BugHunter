#!/usr/bin/env python3
"""
Bug Bounty Hunter Pro - Production Launcher
Robust launcher with error handling and diagnostics
"""

import sys
import os
import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

def check_environment():
    """Check if environment is ready"""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append("Python 3.8+ required")
    
    # Check critical files
    critical_files = [
        'main_dashboard.py',
        'scanner_engine.py', 
        'config_manager.py',
        'auth_manager.py'
    ]
    
    for file in critical_files:
        if not os.path.exists(file):
            issues.append(f"Missing critical file: {file}")
    
    # Check wordlists directory
    if not os.path.exists('wordlists'):
        issues.append("Wordlists directory missing")
    
    return issues

def main():
    """Main launcher function"""
    print("🎯 Bug Bounty Hunter Pro - Starting...")
    
    # Check environment
    issues = check_environment()
    if issues:
        print("❌ Environment issues found:")
        for issue in issues:
            print(f"   - {issue}")
        print("\nRun ./install.sh to fix these issues")
        return False
    
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("Bug Bounty Hunter Pro")
        app.setApplicationVersion("1.0.0")
        
        # Set application style
        app.setStyle('Fusion')
        
        # Import and create main components
        from config_manager import ConfigManager
        from auth_manager import AuthManager
        from login_window import LoginWindow
        
        print("✅ Components loaded successfully")
        
        # Initialize configuration
        config_manager = ConfigManager()
        config_manager.create_directories()
        
        # Initialize authentication
        auth_manager = AuthManager("data/users.json")
        
        # Create login window
        login_window = LoginWindow(auth_manager)
        
        # Create main dashboard (but don't show it yet)
        main_dashboard = None
        
        def on_login_successful(username):
            """Handle successful login"""
            nonlocal main_dashboard
            try:
                from main_dashboard import MainDashboard
                
                # Close login window
                login_window.close()
                
                # Create and show main dashboard
                main_dashboard = MainDashboard(config_manager)
                main_dashboard.current_user = username
                main_dashboard.show()
                
                print(f"✅ Welcome {username}! Main dashboard opened.")
                
            except Exception as e:
                print(f"❌ Error opening main dashboard: {e}")
                QMessageBox.critical(None, "Error", f"Failed to open main dashboard:\n{str(e)}")
                app.quit()
        
        # Connect login success signal
        login_window.login_successful.connect(on_login_successful)
        
        # Show login window
        login_window.show()
        
        print("🚀 Application launched successfully!")
        print("📋 Login with: admin / BugHunter2024!")
        
        # Start event loop
        return app.exec()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"💥 Startup error: {e}")
        print(f"Debug info: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)