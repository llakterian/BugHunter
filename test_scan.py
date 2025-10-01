#!/usr/bin/env python3
"""
Test script to run the vulnerability scanner on test sites
"""

import sys
import signal
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from scanner_engine import ScannerEngine
from config_manager import ConfigManager

class TestScanner:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.config = ConfigManager()
        self.scanner = ScannerEngine(self.config)

        # Connect signals
        self.scanner.log_message.connect(self.on_log_message)
        self.scanner.vulnerability_found.connect(self.on_vulnerability_found)
        # self.scanner.scan_completed.connect(self.on_scan_completed)  # Not implemented

    def on_log_message(self, message, level):
        print(f"[{level.upper()}] {message}")

    def on_vulnerability_found(self, severity, vuln_type, url, description, impact):
        print("🚨 VULNERABILITY FOUND!")
        print(f"   Severity: {severity}")
        print(f"   Type: {vuln_type}")
        print(f"   URL: {url}")
        print(f"   Description: {description}")
        print(f"   Impact: {impact}")
        print("-" * 50)

    def on_scan_progress(self, current, total, status):
        print(f"📊 Progress: {current}/{total} - {status}")

    def on_scan_completed(self, results):
        print("✅ Scan completed!")
        print(f"Results: {results}")
        self.app.quit()

    def test_scan(self, target_url):
        print(f"🎯 Starting scan on: {target_url}")
        print("=" * 60)

        # Set scan configuration
        scan_config = {
            'target_url': target_url,
            'scan_types': ['sql_injection', 'xss', 'command_injection', 'directory_traversal', 'file_inclusion'],
            'max_threads': 3,
            'timeout': 10,
            'user_agent': 'BugHunter-Test/1.0',
            'proxies': None
        }

        # Start the scan
        self.scanner.start_scan(scan_config)

        # Set up timer to quit if scan takes too long (for testing)
        QTimer.singleShot(300000, self.app.quit)  # 5 minutes timeout

        # Run the event loop
        self.app.exec()

if __name__ == "__main__":
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n🛑 Scan interrupted by user")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Test sites
    test_sites = [
        "http://testaspnet.vulnweb.com",
        # "http://testphp.vulnweb.com",  # Uncomment to test more sites
    ]

    scanner = TestScanner()

    for site in test_sites:
        print(f"\n🌐 Testing site: {site}")
        scanner.test_scan(site)