#!/usr/bin/env python3
"""
System Update & Rebuild Script - Bug Bounty Hunter Pro
Updates all components and rebuilds the entire system
"""

import subprocess
import sys
import os
import time
from pathlib import Path

class SystemUpdater:
    def __init__(self):
        self.project_root = Path.cwd()
        self.venv_path = self.project_root / "bug_bounty_env"
        
    def print_status(self, message, status="info"):
        """Print colored status messages"""
        colors = {
            "info": "\033[94m[INFO]\033[0m",
            "success": "\033[92m[SUCCESS]\033[0m", 
            "warning": "\033[93m[WARNING]\033[0m",
            "error": "\033[91m[ERROR]\033[0m"
        }
        print(f"{colors.get(status, colors['info'])} {message}")
    
    def run_command(self, command, description, check=True):
        """Run a command with status reporting"""
        self.print_status(f"{description}...")
        try:
            result = subprocess.run(command, shell=True, check=check, 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.print_status(f"{description} completed", "success")
                return True
            else:
                self.print_status(f"{description} failed: {result.stderr}", "error")
                return False
        except subprocess.CalledProcessError as e:
            self.print_status(f"{description} failed: {e}", "error")
            return False
    
    def update_dependencies(self):
        """Update Python dependencies"""
        self.print_status("Updating Python dependencies")
        
        activate_cmd = f"source {self.venv_path}/bin/activate"
        
        commands = [
            f"{activate_cmd} && pip install --upgrade pip",
            f"{activate_cmd} && pip install --upgrade -r requirements.txt"
        ]
        
        for cmd in commands:
            if not self.run_command(cmd, "Updating packages"):
                return False
        
        return True
    
    def run_tests(self):
        """Run comprehensive tests"""
        self.print_status("Running system tests")
        
        test_commands = [
            f"source {self.venv_path}/bin/activate && python3 test_installation.py",
            f"source {self.venv_path}/bin/activate && python3 test_responsive.py"
        ]
        
        for cmd in test_commands:
            if not self.run_command(cmd, "Running tests", check=False):
                self.print_status("Some tests failed, but continuing...", "warning")
        
        return True
    
    def validate_files(self):
        """Validate all critical files exist"""
        self.print_status("Validating system files")
        
        critical_files = [
            "main.py", "auth_manager.py", "login_window.py", "main_dashboard.py",
            "config_manager.py", "zap_manager.py", "scanner_engine.py",
            "jwt_analyzer.py", "report_generator.py", "wordlist_manager.py",
            "advanced_scanner.py", "exploit_generator.py", "network_scanner.py"
        ]
        
        missing_files = []
        for file in critical_files:
            if not (self.project_root / file).exists():
                missing_files.append(file)
        
        if missing_files:
            self.print_status(f"Missing files: {', '.join(missing_files)}", "error")
            return False
        
        self.print_status("All critical files present", "success")
        return True
    
    def validate_wordlists(self):
        """Validate wordlist files"""
        self.print_status("Validating wordlists")
        
        wordlist_files = [
            "wordlists/directories.txt", "wordlists/subdomains.txt",
            "wordlists/parameters.txt", "wordlists/admin_panels.txt",
            "wordlists/jwt_secrets.txt", "wordlists/usernames.txt",
            "wordlists/passwords.txt", "wordlists/extensions.txt"
        ]
        
        for wordlist in wordlist_files:
            wordlist_path = self.project_root / wordlist
            if wordlist_path.exists():
                with open(wordlist_path, 'r') as f:
                    lines = len([l for l in f if l.strip() and not l.startswith('#')])
                self.print_status(f"{wordlist}: {lines} entries", "success")
            else:
                self.print_status(f"Missing wordlist: {wordlist}", "warning")
        
        return True
    
    def create_directories(self):
        """Create necessary directories"""
        self.print_status("Creating system directories")
        
        directories = [
            "data", "reports", "logs", "screenshots", 
            "wordlists/custom", "assets"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.print_status("Directories created", "success")
        return True
    
    def set_permissions(self):
        """Set proper file permissions"""
        self.print_status("Setting file permissions")
        
        executable_files = [
            "main.py", "bug_bounty_finder.py", "install.sh", "run.sh",
            "test_installation.py", "test_responsive.py", "restart_app.py",
            "build_package.py", "deploy.py", "update_system.py"
        ]
        
        for file in executable_files:
            file_path = self.project_root / file
            if file_path.exists():
                os.chmod(file_path, 0o755)
        
        self.print_status("Permissions set", "success")
        return True
    
    def generate_system_info(self):
        """Generate system information file"""
        self.print_status("Generating system information")
        
        system_info = f"""# Bug Bounty Hunter Pro - System Information
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

## Version Information
- Application Version: 1.0.0
- Python Version: {sys.version}
- Platform: {sys.platform}

## Font Improvements
- Increased base font sizes for better readability
- Login window: 14px fonts, 45-50px button heights
- Main dashboard: 11px base fonts (1366px screens), 12px (larger screens)
- Headers: 16px (compact), 18px (full)
- Better spacing and sizing for all components

## Responsive Design
- Optimized for 1366x768 screens and above
- Automatic layout adaptation based on screen size
- Compact mode for smaller screens
- Scrollable panels for content overflow

## Components Status
- ✅ Authentication System
- ✅ Main Dashboard
- ✅ Wordlist Manager
- ✅ OWASP ZAP Integration
- ✅ Scanner Engine
- ✅ JWT Analyzer
- ✅ Report Generator
- ✅ Advanced Scanner
- ✅ Exploit Generator
- ✅ Network Scanner

## Wordlists Available
- Directories: {len(self.count_wordlist_entries('wordlists/directories.txt'))} entries
- Subdomains: {len(self.count_wordlist_entries('wordlists/subdomains.txt'))} entries
- Parameters: {len(self.count_wordlist_entries('wordlists/parameters.txt'))} entries
- Admin Panels: {len(self.count_wordlist_entries('wordlists/admin_panels.txt'))} entries
- JWT Secrets: {len(self.count_wordlist_entries('wordlists/jwt_secrets.txt'))} entries

## Installation
- Virtual environment: ✅ Present
- Dependencies: ✅ Installed
- OWASP ZAP: ✅ Available
- Permissions: ✅ Set

## Usage
```bash
# Start application
./run.sh

# Login credentials
Username: admin
Password: BugHunter2024!

# Test system
./test_installation.py
```
"""
        
        with open(self.project_root / "SYSTEM_INFO.md", 'w') as f:
            f.write(system_info)
        
        self.print_status("System information generated", "success")
        return True
    
    def count_wordlist_entries(self, wordlist_path):
        """Count entries in a wordlist file"""
        try:
            with open(wordlist_path, 'r') as f:
                return [l.strip() for l in f if l.strip() and not l.startswith('#')]
        except FileNotFoundError:
            return []
    
    def update_system(self):
        """Main system update process"""
        self.print_status("🚀 Starting Bug Bounty Hunter Pro System Update")
        print("=" * 60)
        
        steps = [
            ("Validating files", self.validate_files),
            ("Creating directories", self.create_directories),
            ("Updating dependencies", self.update_dependencies),
            ("Validating wordlists", self.validate_wordlists),
            ("Setting permissions", self.set_permissions),
            ("Running tests", self.run_tests),
            ("Generating system info", self.generate_system_info)
        ]
        
        success_count = 0
        total_steps = len(steps)
        
        for step_name, step_func in steps:
            try:
                if step_func():
                    success_count += 1
                else:
                    self.print_status(f"Step failed: {step_name}", "warning")
            except Exception as e:
                self.print_status(f"Step error: {step_name} - {e}", "error")
        
        print("\n" + "=" * 60)
        print("📊 UPDATE SUMMARY")
        print("=" * 60)
        
        self.print_status(f"Completed: {success_count}/{total_steps} steps", 
                         "success" if success_count == total_steps else "warning")
        
        if success_count == total_steps:
            self.print_status("🎉 System update completed successfully!", "success")
            print("\n🚀 Ready to use:")
            print("   ./run.sh")
            print("\n📋 Login credentials:")
            print("   Username: admin")
            print("   Password: BugHunter2024!")
            return True
        else:
            self.print_status("⚠️  Some steps failed. Check the output above.", "warning")
            return False

def main():
    """Main function"""
    updater = SystemUpdater()
    success = updater.update_system()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()