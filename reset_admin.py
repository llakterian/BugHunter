#!/usr/bin/env python3
"""
Admin Password Reset Utility
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth_manager import AuthManager

def reset_admin_password():
    """Reset admin password and display new credentials"""
    auth_manager = AuthManager()

    # Generate a new random password
    new_password = auth_manager.generate_random_password()

    # Reset admin password (if admin exists)
    if "admin" in auth_manager.users:
        auth_manager.users["admin"]["password_hash"] = auth_manager.hash_password(new_password)
        auth_manager.save_users()

        print("=" * 60)
        print("🔐 ADMIN PASSWORD RESET")
        print("=" * 60)
        print(f"Username: admin")
        print(f"New Password: {new_password}")
        print("=" * 60)
        print("⚠️  IMPORTANT: Save these credentials and change the password after login!")
        print("=" * 60)
    else:
        print("❌ Admin user not found!")

if __name__ == "__main__":
    reset_admin_password()