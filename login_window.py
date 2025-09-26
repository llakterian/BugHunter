"""
Login Window - Secure authentication interface
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QMessageBox,
                            QCheckBox, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPalette

class LoginWindow(QWidget):
    login_successful = pyqtSignal(str)
    
    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.setup_ui()
        self.setup_styling()
    
    def setup_ui(self):
        """Setup the login interface"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Add spacer at top
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Title and logo area
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Main title
        title_label = QLabel("Bug Bounty Hunter Pro")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        title_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Advanced Security Testing Platform")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 16))
        subtitle_label.setStyleSheet("color: #888888; margin-bottom: 30px;")
        title_layout.addWidget(subtitle_label)
        
        layout.addWidget(title_frame)
        
        # Login form container
        form_frame = QFrame()
        form_frame.setMaximumWidth(400)
        form_frame.setMinimumWidth(350)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
        # Username field
        username_label = QLabel("Username:")
        username_label.setFont(QFont("Arial", 14))
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFont(QFont("Arial", 14))
        self.username_input.setMinimumHeight(45)
        form_layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 14))
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Arial", 14))
        self.password_input.setMinimumHeight(45)
        form_layout.addWidget(self.password_input)
        
        # Remember me checkbox
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setFont(QFont("Arial", 10))
        form_layout.addWidget(self.remember_checkbox)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.login_button.setMinimumHeight(50)
        self.login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_button)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 10))
        form_layout.addWidget(self.status_label)
        
        # Default credentials info
        info_label = QLabel("Default: admin / BugHunter2024!")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setFont(QFont("Arial", 9))
        info_label.setStyleSheet("color: #666666; margin-top: 20px;")
        form_layout.addWidget(info_label)
        
        # Center the form
        form_container = QHBoxLayout()
        form_container.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        form_container.addWidget(form_frame)
        form_container.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        layout.addLayout(form_container)
        
        # Add spacer at bottom
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        self.setLayout(layout)
        
        # Connect Enter key to login
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
    
    def setup_styling(self):
        """Apply styling to the login window"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 10px;
                padding: 20px;
            }
            
            QLineEdit {
                background-color: #3d3d3d;
                border: 2px solid #555555;
                border-radius: 8px;
                padding: 10px;
                color: #ffffff;
            }
            
            QLineEdit:focus {
                border-color: #0078d4;
            }
            
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 8px;
                color: white;
                padding: 12px;
            }
            
            QPushButton:hover {
                background-color: #106ebe;
            }
            
            QPushButton:pressed {
                background-color: #005a9e;
            }
            
            QCheckBox {
                color: #cccccc;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            
            QCheckBox::indicator:unchecked {
                background-color: #3d3d3d;
                border: 2px solid #555555;
                border-radius: 3px;
            }
            
            QCheckBox::indicator:checked {
                background-color: #0078d4;
                border: 2px solid #0078d4;
                border-radius: 3px;
            }
        """)
    
    def handle_login(self):
        """Handle login attempt"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_status("Please enter both username and password", "error")
            return
        
        # Disable login button during authentication
        self.login_button.setEnabled(False)
        self.login_button.setText("Authenticating...")
        
        # Simulate authentication delay for security
        QTimer.singleShot(500, lambda: self.authenticate_user(username, password))
    
    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        if self.auth_manager.authenticate(username, password):
            self.show_status("Login successful!", "success")
            QTimer.singleShot(1000, lambda: self.login_successful.emit(username))
        else:
            self.show_status("Invalid username or password", "error")
            self.login_button.setEnabled(True)
            self.login_button.setText("Login")
            self.password_input.clear()
    
    def show_status(self, message, status_type="info"):
        """Show status message with appropriate styling"""
        colors = {
            "success": "#4CAF50",
            "error": "#f44336",
            "info": "#2196F3",
            "warning": "#ff9800"
        }
        
        color = colors.get(status_type, colors["info"])
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        
        # Clear status after 5 seconds
        QTimer.singleShot(5000, lambda: self.status_label.clear())
    
    def reset_form(self):
        """Reset the login form"""
        self.username_input.clear()
        self.password_input.clear()
        self.remember_checkbox.setChecked(False)
        self.status_label.clear()
        self.login_button.setEnabled(True)
        self.login_button.setText("Login")