#!/usr/bin/env python3
"""
Bug Bounty Hunter Pro - Ultra-Advanced Security Testing Tool (33X More Robust)
Author: Kiro AI Assistant
Description: Professional bug bounty automation tool with mass CVE scanning, hidden element discovery, automated recon, LostFuzzer DAST scanning, and complete workflow automation
"""

import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont

from auth_manager import AuthManager
from login_window import LoginWindow
from main_dashboard import MainDashboard
from config_manager import ConfigManager

class BugBountyHunterPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bug Bounty Hunter Pro v2.0 - 33X More Robust")
        
        # Get screen dimensions for responsive sizing
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        # Calculate responsive window size (80% of screen)
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        # Set minimum size based on screen size
        min_width = min(1000, int(screen_width * 0.6))
        min_height = min(700, int(screen_height * 0.6))
        
        # Position window in center
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.setGeometry(x, y, window_width, window_height)
        self.setMinimumSize(min_width, min_height)
        
        # Initialize managers
        self.config_manager = ConfigManager()
        self.auth_manager = AuthManager()
        
        # Setup UI
        self.setup_ui()
        self.setup_styling()
        
        # Show login window first
        self.show_login()
    
    def setup_ui(self):
        """Initialize the main UI components"""
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        # Initialize windows
        self.login_window = LoginWindow(self.auth_manager)
        self.main_dashboard = MainDashboard(self.config_manager)
        
        # Add windows to stack
        self.central_widget.addWidget(self.login_window)
        self.central_widget.addWidget(self.main_dashboard)
        
        # Connect signals
        self.login_window.login_successful.connect(self.show_dashboard)
        self.main_dashboard.logout_requested.connect(self.show_login)
    
    def setup_styling(self):
        """Apply modern dark theme styling"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
    
    def show_login(self):
        """Show the login window"""
        self.central_widget.setCurrentWidget(self.login_window)
        self.setWindowTitle("Bug Bounty Hunter Pro - Login")
    
    def show_dashboard(self, username):
        """Show the main dashboard after successful login"""
        self.main_dashboard.set_user(username)
        self.central_widget.setCurrentWidget(self.main_dashboard)
        self.setWindowTitle(f"Bug Bounty Hunter Pro - {username}")

def main():
    print("🚀 Starting Bug Bounty Hunter Pro...")
    app = QApplication(sys.argv)
    app.setApplicationName("Bug Bounty Hunter Pro")
    app.setApplicationVersion("1.0")

    # Set application icon if available
    if os.path.exists("assets/icon.png"):
        app.setWindowIcon(QIcon("assets/icon.png"))
        print("✅ Application icon loaded")

    print("🔧 Creating main window...")
    window = BugBountyHunterPro()
    print("✅ Main window created")

    print("📱 Showing login window...")
    window.show()
    print("✅ Application started successfully")

    print("💡 If you don't see the login window, the app may be running in headless mode")
    print("💡 Try running with a display or check if DISPLAY environment variable is set")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()