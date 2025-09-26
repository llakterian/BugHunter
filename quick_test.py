#!/usr/bin/env python3
"""
Quick Test Script - Verify Bug Bounty Hunter Pro is working
"""

import sys
import os
import requests
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

def test_dependencies():
    """Test if all dependencies are available"""
    print("🔍 Testing dependencies...")
    
    try:
        import requests
        import jwt
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QObject, pyqtSignal
        print("✅ All dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def test_wordlists():
    """Test if wordlists are available"""
    print("📝 Testing wordlists...")
    
    wordlist_files = [
        'wordlists/directories.txt',
        'wordlists/subdomains.txt', 
        'wordlists/parameters.txt',
        'wordlists/admin_panels.txt',
        'wordlists/jwt_secrets.txt'
    ]
    
    all_good = True
    for wordlist in wordlist_files:
        if os.path.exists(wordlist):
            with open(wordlist, 'r') as f:
                lines = len(f.readlines())
            print(f"✅ {wordlist}: {lines} entries")
        else:
            print(f"❌ Missing: {wordlist}")
            all_good = False
    
    return all_good

def test_connectivity():
    """Test internet connectivity"""
    print("🌐 Testing connectivity...")
    
    try:
        response = requests.get('https://httpbin.org/status/200', timeout=10)
        if response.status_code == 200:
            print("✅ Internet connectivity OK")
            return True
        else:
            print(f"⚠️ Unexpected status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connectivity issue: {e}")
        return False

def test_gui():
    """Test GUI components"""
    print("🖥️ Testing GUI...")
    
    try:
        app = QApplication(sys.argv)
        
        # Import main components
        from config_manager import ConfigManager
        from scanner_engine import ScannerEngine
        from main_dashboard import MainDashboard
        
        config_manager = ConfigManager()
        scanner = ScannerEngine(config_manager)
        
        print("✅ GUI components loaded successfully")
        
        # Quick test of scanner
        if hasattr(scanner, 'wordlists') and scanner.wordlists:
            print("✅ Scanner engine initialized with wordlists")
        else:
            print("⚠️ Scanner wordlists not loaded")
        
        app.quit()
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎯 Bug Bounty Hunter Pro - Quick Test")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Wordlists", test_wordlists), 
        ("Connectivity", test_connectivity),
        ("GUI Components", test_gui)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for bug hunting!")
        print("\n🚀 Launch the application:")
        print("   ./run.sh")
        return True
    else:
        print("⚠️ Some tests failed. Check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)