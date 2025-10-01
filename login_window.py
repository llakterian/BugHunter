"""
Login Window - Ultra Simple and Guaranteed Visible
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QPushButton, QFrame, QMessageBox,
                            QCheckBox, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPalette, QIcon

class LoginWindow(QWidget):
    login_successful = pyqtSignal(str)

    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.login_attempts = 0
        self.setup_ui()

    def setup_ui(self):
        """Setup the most basic, guaranteed-visible login interface"""
        # Set window properties
        self.setWindowTitle("Bug Bounty Hunter Pro - Login")
        self.setFixedSize(400, 350)

        # Main layout - very simple
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("Bug Bounty Hunter Pro")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Username
        username_label = QLabel("Username:")
        layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        layout.addWidget(self.username_input)

        # Password
        password_label = QLabel("Password:")
        layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter password")
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("LOGIN")
        self.login_button.setMinimumHeight(40)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        # Status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Hint
        hint_label = QLabel("Default: admin / Check console for password")
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint_label)

        self.setLayout(layout)

        # Connect Enter key
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

    def handle_login(self):
        """Handle login attempt with security best practices"""
        username = self.username_input.text().strip()
        password = self.password_input.text()

        # Input validation
        if not username or not password:
            self.show_status("Please enter both username and password", "error")
            return

        if len(username) < 3:
            self.show_status("Username must be at least 3 characters", "error")
            return

        if len(password) < 8:
            self.show_status("Password must be at least 8 characters", "error")
            return

        # Ethical use agreement (required for security testing tools)
        # Note: In production, consider adding explicit user agreement
        ethical_agreement = True  # Assuming user understands ethical use requirements

        if not ethical_agreement:
            self.show_status("Ethical use agreement required", "error")
            return

        # Rate limiting: disable multiple rapid attempts
        self.login_attempts += 1
        if self.login_attempts > 3:
            self.show_status("Too many login attempts. Please wait.", "error")
            QTimer.singleShot(30000, self.reset_login_attempts)  # 30 second cooldown
            return

        # Disable login button during authentication
        self.login_button.setEnabled(False)
        self.login_button.setText("Authenticating...")

        # Add slight delay for security (prevents brute force automation)
        QTimer.singleShot(800, lambda: self.authenticate_user(username, password))

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
            "success": "#42b883",
            "error": "#e41e3f",
            "info": "#1877f2",
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
        self.status_label.clear()
        self.login_button.setEnabled(True)
        self.login_button.setText("Login")
        self.login_attempts = 0

    def reset_login_attempts(self):
        """Reset login attempts after cooldown"""
        self.login_attempts = 0
        self.login_button.setEnabled(True)
        self.login_button.setText("Login")
        self.show_status("You can try logging in again", "info")

