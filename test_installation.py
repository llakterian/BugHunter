#!/usr/bin/env python3
"""
Test Installation - Verify Bug Bounty Hunter Pro installation
"""

import sys
import os
import importlib
import subprocess
from pathlib import Path

def test_python_version():
    """Test Python version"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n📦 Testing dependencies...")
    
    required_modules = [
        'PyQt6',
        'requests', 
        'jwt',
        'bcrypt',
        'cryptography',
        'websockets'
    ]
    
    all_good = True
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module} - OK")
        except ImportError:
            print(f"❌ {module} - Missing")
            all_good = False
    
    return all_good

def test_files():
    """Test required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'main.py',
        'auth_manager.py',
        'login_window.py',
        'main_dashboard.py',
        'config_manager.py',
        'zap_manager.py',
        'scanner_engine.py',
        'jwt_analyzer.py',
        'report_generator.py',
        'bug_bounty_finder.py'
    ]
    
    required_dirs = [
        'wordlists',
        'data'
    ]
    
    all_good = True
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} - OK")
        else:
            print(f"❌ {file} - Missing")
            all_good = False
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✅ {directory}/ - OK")
        else:
            print(f"❌ {directory}/ - Missing")
            all_good = False
    
    return all_good

def test_zap_installation():
    """Test OWASP ZAP installation"""
    print("\n🕷️ Testing OWASP ZAP...")
    
    try:
        result = subprocess.run(['zaproxy', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ OWASP ZAP - OK")
            return True
        else:
            print("❌ OWASP ZAP - Not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ OWASP ZAP - Not installed or not in PATH")
        return False

def test_virtual_environment():
    """Test virtual environment"""
    print("\n🔧 Testing virtual environment...")
    
    if Path('bug_bounty_env').exists():
        print("✅ Virtual environment - OK")
        
        # Test if we can activate it
        venv_python = Path('bug_bounty_env/bin/python')
        if venv_python.exists():
            print("✅ Virtual environment Python - OK")
            return True
        else:
            print("❌ Virtual environment Python - Missing")
            return False
    else:
        print("❌ Virtual environment - Missing")
        return False

def test_wordlists():
    """Test wordlists"""
    print("\n📝 Testing wordlists...")
    
    wordlist_files = [
        'wordlists/directories.txt',
        'wordlists/subdomains.txt', 
        'wordlists/jwt_secrets.txt'
    ]
    
    all_good = True
    
    for wordlist in wordlist_files:
        if Path(wordlist).exists():
            with open(wordlist, 'r') as f:
                lines = len(f.readlines())
            print(f"✅ {wordlist} - OK ({lines} entries)")
        else:
            print(f"❌ {wordlist} - Missing")
            all_good = False
    
    return all_good

def test_permissions():
    """Test file permissions"""
    print("\n🔐 Testing permissions...")
    
    executable_files = [
        'main.py',
        'bug_bounty_finder.py',
        'install.sh',
        'build_package.py'
    ]
    
    all_good = True
    
    for file in executable_files:
        if Path(file).exists():
            if os.access(file, os.X_OK):
                print(f"✅ {file} - Executable")
            else:
                print(f"⚠️  {file} - Not executable (may need chmod +x)")
        else:
            print(f"❌ {file} - Missing")
            all_good = False
    
    return all_good

def run_basic_import_test():
    """Test basic imports"""
    print("\n🧪 Testing basic imports...")
    
    try:
        # Test main modules
        from auth_manager import AuthManager
        from config_manager import ConfigManager
        from jwt_analyzer import JWTAnalyzer
        
        print("✅ Core modules import - OK")
        
        # Test basic functionality
        config = ConfigManager()
        auth = AuthManager()
        jwt_analyzer = JWTAnalyzer(config)
        
        print("✅ Basic initialization - OK")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Bug Bounty Hunter Pro - Installation Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("File Structure", test_files),
        ("Virtual Environment", test_virtual_environment),
        ("Wordlists", test_wordlists),
        ("Permissions", test_permissions),
        ("Basic Imports", run_basic_import_test),
        ("OWASP ZAP", test_zap_installation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} - Error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Installation is ready.")
        print("\nTo start the application:")
        print("  ./run.sh")
        return True
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the installation.")
        print("\nTo fix issues:")
        print("  ./install.sh")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)