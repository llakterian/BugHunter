"""
Authentication Manager - Secure user authentication system
"""

import json
import os
import bcrypt
import hashlib
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class AuthManager:
    def __init__(self, users_file="data/users.json"):
        self.users_file = users_file
        self.current_user = None
        self.session_timeout = timedelta(hours=8)
        self.ensure_data_directory()
        self.load_users()
        self.create_default_admin()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
    
    def load_users(self):
        """Load users from file"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            else:
                self.users = {}
        except Exception as e:
            print(f"Error loading users: {e}")
            self.users = {}
    
    def save_users(self):
        """Save users to file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def generate_random_password(self, length=16):
        """Generate a secure random password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def create_default_admin(self):
        """Create default admin user if no users exist"""
        if not self.users:
            # Generate secure random password
            admin_password = self.generate_random_password()
            self.create_user("admin", admin_password, "admin", "Default Administrator")
            print("=" * 60)
            print("🔐 DEFAULT ADMIN ACCOUNT CREATED")
            print("=" * 60)
            print(f"Username: admin")
            print(f"Password: {admin_password}")
            print("=" * 60)
            print("⚠️  IMPORTANT: Please save these credentials and change the password after first login!")
            print("=" * 60)
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_user(self, username: str, password: str, role: str = "user", full_name: str = "") -> bool:
        """Create a new user"""
        if username in self.users:
            return False
        
        self.users[username] = {
            "password_hash": self.hash_password(password),
            "role": role,
            "full_name": full_name,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "active": True
        }
        self.save_users()
        return True
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials"""
        if username not in self.users:
            return False
        
        user = self.users[username]
        if not user.get("active", True):
            return False
        
        if self.verify_password(password, user["password_hash"]):
            # Update last login
            user["last_login"] = datetime.now().isoformat()
            self.current_user = username
            self.save_users()
            return True
        
        return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self) -> Optional[str]:
        """Get current logged in user"""
        return self.current_user
    
    def get_user_info(self, username: str = None) -> Optional[Dict[str, Any]]:
        """Get user information"""
        if username is None:
            username = self.current_user
        
        if username and username in self.users:
            user_info = self.users[username].copy()
            # Remove sensitive information
            user_info.pop("password_hash", None)
            return user_info
        
        return None
    
    def is_admin(self, username: str = None) -> bool:
        """Check if user has admin privileges"""
        if username is None:
            username = self.current_user
        
        user_info = self.get_user_info(username)
        return user_info and user_info.get("role") == "admin"
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        if username not in self.users:
            return False
        
        user = self.users[username]
        if not self.verify_password(old_password, user["password_hash"]):
            return False
        
        user["password_hash"] = self.hash_password(new_password)
        self.save_users()
        return True
    
    def get_all_users(self) -> Dict[str, Dict[str, Any]]:
        """Get all users (admin only)"""
        if not self.is_admin():
            return {}
        
        users_info = {}
        for username, user_data in self.users.items():
            user_info = user_data.copy()
            user_info.pop("password_hash", None)
            users_info[username] = user_info
        
        return users_info