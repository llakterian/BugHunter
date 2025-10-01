#!/usr/bin/env python3
"""
Simple test script to verify Bug Bounty Hunter Pro components
"""

def test_imports():
    """Test all major imports"""
    try:
        from auth_manager import AuthManager
        from config_manager import ConfigManager
        from nuclei_shodan_integration import NucleiShodanIntegration
        from lost_uncover import LostUncover
        from recon_automation import ReconAutomation
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_auth_manager():
    """Test authentication manager"""
    try:
        from auth_manager import AuthManager
        am = AuthManager()
        # Try to authenticate existing user first
        auth_success = am.authenticate("testuser", "testpass123")
        if auth_success:
            print("✅ Auth manager working correctly (existing user)")
            return True

        # If that fails, try creating a new user
        import uuid
        test_username = f"testuser_{uuid.uuid4().hex[:8]}"
        success = am.create_user(test_username, "testpass123", "user", "Test User")
        if success:
            # Test authentication
            auth_success = am.authenticate(test_username, "testpass123")
            if auth_success:
                print("✅ Auth manager working correctly (new user)")
                return True
        print("❌ Auth manager test failed")
        return False
    except Exception as e:
        print(f"❌ Auth manager error: {e}")
        return False

def test_config_manager():
    """Test configuration manager"""
    try:
        from config_manager import ConfigManager
        cm = ConfigManager()
        # Test config operations
        cm.set("test.key", "test_value")
        value = cm.get("test.key")
        if value == "test_value":
            print("✅ Config manager working correctly")
            return True
        print("❌ Config manager test failed")
        return False
    except Exception as e:
        print(f"❌ Config manager error: {e}")
        return False

def test_enhanced_modules():
    """Test enhanced modules"""
    try:
        from nuclei_shodan_integration import NucleiShodanIntegration
        from lost_uncover import LostUncover
        from recon_automation import ReconAutomation

        # Test NucleiShodanIntegration
        nsi = NucleiShodanIntegration()
        # Just test instantiation

        # Test LostUncover
        lu = LostUncover()
        bookmarklet = lu.get_bookmarklet()
        if "javascript:" in bookmarklet:
            print("✅ LostUncover working")
        else:
            print("❌ LostUncover test failed")
            return False

        # Test ReconAutomation
        ra = ReconAutomation()
        # Test domain extraction
        domain = ra._extract_domain("https://example.com/path")
        if domain == "example.com":
            print("✅ ReconAutomation working")
        else:
            print("❌ ReconAutomation test failed")
            return False

        print("✅ All enhanced modules working correctly")
        return True
    except Exception as e:
        print(f"❌ Enhanced modules error: {e}")
        return False

def main():
    print("🧪 Bug Bounty Hunter Pro - Component Tests")
    print("=" * 50)

    tests = [
        ("Imports", test_imports),
        ("Auth Manager", test_auth_manager),
        ("Config Manager", test_config_manager),
        ("Enhanced Modules", test_enhanced_modules)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 All tests passed! The app is ready.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

    return passed == total

if __name__ == "__main__":
    main()