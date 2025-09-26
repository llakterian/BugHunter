#!/usr/bin/env python3
"""
Comprehensive Test Suite - Test all components of Bug Bounty Hunter Pro
"""

import unittest
import sys
import os
import tempfile
import json
import time
from unittest.mock import Mock, patch, MagicMock
import requests_mock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from auth_manager import AuthManager
from config_manager import ConfigManager
from jwt_analyzer import JWTAnalyzer
from scanner_engine import ScannerEngine
from exploit_generator import ExploitGenerator
from network_scanner import NetworkScanner
from advanced_scanner import AdvancedScanner

class TestAuthManager(unittest.TestCase):
    """Test authentication manager"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.users_file = os.path.join(self.temp_dir, 'test_users.json')
        self.auth_manager = AuthManager(self.users_file)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_create_user(self):
        """Test user creation"""
        result = self.auth_manager.create_user('testuser', 'testpass123', 'user', 'Test User')
        self.assertTrue(result)
        
        # Test duplicate user
        result = self.auth_manager.create_user('testuser', 'testpass123', 'user', 'Test User')
        self.assertFalse(result)
    
    def test_authenticate(self):
        """Test user authentication"""
        # Create user first
        self.auth_manager.create_user('testuser', 'testpass123', 'user', 'Test User')
        
        # Test correct credentials
        result = self.auth_manager.authenticate('testuser', 'testpass123')
        self.assertTrue(result)
        
        # Test wrong password
        result = self.auth_manager.authenticate('testuser', 'wrongpass')
        self.assertFalse(result)
        
        # Test non-existent user
        result = self.auth_manager.authenticate('nonexistent', 'password')
        self.assertFalse(result)
    
    def test_password_hashing(self):
        """Test password hashing"""
        password = 'testpassword123'
        hashed = self.auth_manager.hash_password(password)
        
        # Hash should be different from original
        self.assertNotEqual(password, hashed)
        
        # Verification should work
        self.assertTrue(self.auth_manager.verify_password(password, hashed))
        
        # Wrong password should fail
        self.assertFalse(self.auth_manager.verify_password('wrongpassword', hashed))

class TestConfigManager(unittest.TestCase):
    """Test configuration manager"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'test_config.json')
        self.config_manager = ConfigManager(self.config_file)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_get_set_config(self):
        """Test getting and setting configuration values"""
        # Test setting and getting
        self.config_manager.set('test.key', 'test_value')
        value = self.config_manager.get('test.key')
        self.assertEqual(value, 'test_value')
        
        # Test default value
        value = self.config_manager.get('nonexistent.key', 'default')
        self.assertEqual(value, 'default')
    
    def test_zap_config(self):
        """Test ZAP configuration"""
        zap_config = self.config_manager.get_zap_config()
        self.assertIsInstance(zap_config, dict)
        self.assertIn('host', zap_config)
        self.assertIn('port', zap_config)

class TestJWTAnalyzer(unittest.TestCase):
    """Test JWT analyzer"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'test_config.json')
        self.config_manager = ConfigManager(self.config_file)
        self.jwt_analyzer = JWTAnalyzer(self.config_manager)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_weak_secret_detection(self):
        """Test JWT weak secret detection"""
        import jwt
        
        # Create JWT with weak secret
        payload = {'user': 'test', 'role': 'user'}
        weak_secret = 'secret'
        token = jwt.encode(payload, weak_secret, algorithm='HS256')
        
        # Test weak secret detection
        found_secret = self.jwt_analyzer._test_weak_secrets(token, {'alg': 'HS256'})
        self.assertEqual(found_secret, weak_secret)
    
    def test_token_analysis(self):
        """Test comprehensive token analysis"""
        import jwt
        
        # Create test token
        payload = {
            'user': 'test',
            'role': 'user',
            'exp': int(time.time()) + 3600  # 1 hour from now
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        # Analyze token
        analysis = self.jwt_analyzer.analyze_token(token)
        
        self.assertTrue(analysis['decoded_successfully'])
        self.assertIsNotNone(analysis['header'])
        self.assertIsNotNone(analysis['payload'])
        self.assertIsInstance(analysis['vulnerabilities'], list)

class TestScannerEngine(unittest.TestCase):
    """Test scanner engine"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'test_config.json')
        self.config_manager = ConfigManager(self.config_file)
        self.scanner_engine = ScannerEngine(self.config_manager)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @requests_mock.Mocker()
    def test_directory_fuzzing(self, m):
        """Test directory fuzzing functionality"""
        # Mock HTTP responses
        m.get('http://example.com/admin', status_code=200, text='Admin Panel')
        m.get('http://example.com/test', status_code=404, text='Not Found')
        
        # Test directory fuzzing
        result = self.scanner_engine._test_directory('http://example.com', 'admin')
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 200)  # status code
        
        result = self.scanner_engine._test_directory('http://example.com', 'nonexistent')
        self.assertIsNone(result)
    
    def test_wordlist_loading(self):
        """Test wordlist loading"""
        directories = self.scanner_engine.wordlists['directories']
        self.assertIsInstance(directories, list)
        self.assertGreater(len(directories), 0)

class TestExploitGenerator(unittest.TestCase):
    """Test exploit generator"""
    
    def setUp(self):
        self.exploit_generator = ExploitGenerator()
    
    def test_jwt_exploit_generation(self):
        """Test JWT exploit generation"""
        vulnerability = {
            'type': 'JWT Weak Secret',
            'secret': 'secret',
            'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidGVzdCIsInJvbGUiOiJ1c2VyIn0.QjrvBbv8qOGCOKdPO6u2qOqKvLrCBvFwP8B8K8K8K8K',
            'url': 'http://example.com/api'
        }
        
        exploit = self.exploit_generator.generate_jwt_exploit(vulnerability)
        
        self.assertIsNotNone(exploit)
        self.assertEqual(exploit['vulnerability_type'], 'JWT Weak Secret')
        self.assertIn('steps', exploit)
        self.assertIn('code', exploit)
    
    def test_sql_injection_exploit(self):
        """Test SQL injection exploit generation"""
        vulnerability = {
            'type': 'SQL Injection',
            'severity': 'High',
            'url': 'http://example.com/search?q=test',
            'parameter': 'q',
            'payload': "' OR '1'='1"
        }
        
        exploit = self.exploit_generator.generate_sql_injection_exploit(vulnerability)
        
        self.assertIsNotNone(exploit)
        self.assertEqual(exploit['vulnerability_type'], 'SQL Injection')
        self.assertIn('steps', exploit)
        self.assertIn('code', exploit)

class TestNetworkScanner(unittest.TestCase):
    """Test network scanner"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'test_config.json')
        self.config_manager = ConfigManager(self.config_file)
        self.network_scanner = NetworkScanner(self.config_manager)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_service_identification(self):
        """Test service identification"""
        # Test HTTP banner
        http_banner = b'HTTP/1.1 200 OK\r\nServer: Apache/2.4.41'
        service = self.network_scanner.identify_service(80, http_banner)
        self.assertEqual(service, 'HTTP')
        
        # Test SSH banner
        ssh_banner = b'SSH-2.0-OpenSSH_7.4'
        service = self.network_scanner.identify_service(22, ssh_banner)
        self.assertEqual(service, 'SSH')
    
    def test_version_extraction(self):
        """Test version extraction from banners"""
        apache_banner = b'Server: Apache/2.4.41 (Ubuntu)'
        version = self.network_scanner.extract_version(apache_banner, 'Apache')
        self.assertEqual(version, '2.4.41')
        
        ssh_banner = b'SSH-2.0-OpenSSH_7.4'
        version = self.network_scanner.extract_version(ssh_banner, 'OpenSSH')
        self.assertEqual(version, '7.4')

class TestAdvancedScanner(unittest.TestCase):
    """Test advanced scanner"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'test_config.json')
        self.config_manager = ConfigManager(self.config_file)
        self.advanced_scanner = AdvancedScanner(self.config_manager)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @requests_mock.Mocker()
    def test_sql_injection_detection(self, m):
        """Test SQL injection detection"""
        # Mock response with SQL error
        m.get(requests_mock.ANY, text='mysql_fetch_array(): supplied argument is not a valid MySQL result')
        
        vulnerability = self.advanced_scanner._test_sql_injection(
            'http://example.com/search', 'q', "' OR '1'='1"
        )
        
        self.assertIsNotNone(vulnerability)
        self.assertEqual(vulnerability['type'], 'SQL Injection')
    
    @requests_mock.Mocker()
    def test_xss_detection(self, m):
        """Test XSS detection"""
        # Mock response with reflected payload
        payload = "<script>alert('XSS')</script>"
        m.get(requests_mock.ANY, text=f'Search results for: {payload}')
        
        vulnerability = self.advanced_scanner._test_xss(
            'http://example.com/search', 'q', payload
        )
        
        self.assertIsNotNone(vulnerability)
        self.assertEqual(vulnerability['type'], 'Reflected XSS')

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'test_config.json')
        self.config_manager = ConfigManager(self.config_file)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_full_workflow(self):
        """Test complete bug bounty workflow"""
        # Initialize components
        auth_manager = AuthManager(os.path.join(self.temp_dir, 'users.json'))
        scanner_engine = ScannerEngine(self.config_manager)
        jwt_analyzer = JWTAnalyzer(self.config_manager)
        exploit_generator = ExploitGenerator()
        
        # Test authentication
        auth_manager.create_user('testuser', 'testpass123', 'user', 'Test User')
        self.assertTrue(auth_manager.authenticate('testuser', 'testpass123'))
        
        # Test JWT analysis
        import jwt
        token = jwt.encode({'user': 'test'}, 'secret', algorithm='HS256')
        analysis = jwt_analyzer.analyze_token(token)
        self.assertTrue(analysis['decoded_successfully'])
        
        # Test exploit generation if vulnerabilities found
        if analysis['vulnerabilities']:
            for vuln in analysis['vulnerabilities']:
                if 'JWT' in vuln.get('type', ''):
                    exploit = exploit_generator.generate_jwt_exploit(vuln)
                    self.assertIsNotNone(exploit)

def run_performance_tests():
    """Run performance tests"""
    print("\n" + "="*50)
    print("PERFORMANCE TESTS")
    print("="*50)
    
    # Test scanner performance
    temp_dir = tempfile.mkdtemp()
    config_file = os.path.join(temp_dir, 'test_config.json')
    config_manager = ConfigManager(config_file)
    scanner_engine = ScannerEngine(config_manager)
    
    # Time wordlist loading
    start_time = time.time()
    directories = scanner_engine.wordlists['directories']
    load_time = time.time() - start_time
    
    print(f"✅ Wordlist loading: {load_time:.3f}s ({len(directories)} entries)")
    
    # Test JWT analysis performance
    jwt_analyzer = JWTAnalyzer(config_manager)
    
    import jwt
    token = jwt.encode({'user': 'test', 'role': 'user'}, 'secret', algorithm='HS256')
    
    start_time = time.time()
    analysis = jwt_analyzer.analyze_token(token)
    analysis_time = time.time() - start_time
    
    print(f"✅ JWT analysis: {analysis_time:.3f}s")
    
    # Test exploit generation performance
    exploit_generator = ExploitGenerator()
    
    vulnerability = {
        'type': 'JWT Weak Secret',
        'secret': 'secret',
        'token': token,
        'url': 'http://example.com'
    }
    
    start_time = time.time()
    exploit = exploit_generator.generate_jwt_exploit(vulnerability)
    exploit_time = time.time() - start_time
    
    print(f"✅ Exploit generation: {exploit_time:.3f}s")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)

def run_security_tests():
    """Run security-focused tests"""
    print("\n" + "="*50)
    print("SECURITY TESTS")
    print("="*50)
    
    temp_dir = tempfile.mkdtemp()
    
    # Test password security
    auth_manager = AuthManager(os.path.join(temp_dir, 'users.json'))
    
    # Test password hashing
    password = 'testpassword123'
    hash1 = auth_manager.hash_password(password)
    hash2 = auth_manager.hash_password(password)
    
    # Hashes should be different (salt)
    if hash1 != hash2:
        print("✅ Password hashing uses salt")
    else:
        print("❌ Password hashing may not use salt")
    
    # Test hash verification
    if auth_manager.verify_password(password, hash1):
        print("✅ Password verification works")
    else:
        print("❌ Password verification failed")
    
    # Test JWT security
    jwt_analyzer = JWTAnalyzer(ConfigManager(os.path.join(temp_dir, 'config.json')))
    
    # Test none algorithm detection
    import jwt
    payload = {'user': 'test', 'admin': True}
    none_token = jwt.encode(payload, '', algorithm='none')
    
    analysis = jwt_analyzer.analyze_token(none_token)
    none_vuln_found = any('none' in vuln.get('type', '').lower() for vuln in analysis['vulnerabilities'])
    
    if none_vuln_found:
        print("✅ None algorithm vulnerability detected")
    else:
        print("⚠️  None algorithm vulnerability not detected")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)

def main():
    """Main test runner"""
    print("🧪 Bug Bounty Hunter Pro - Comprehensive Test Suite")
    print("=" * 60)
    
    # Run unit tests
    print("\nRunning unit tests...")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestAuthManager,
        TestConfigManager,
        TestJWTAnalyzer,
        TestScannerEngine,
        TestExploitGenerator,
        TestNetworkScanner,
        TestAdvancedScanner,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Run performance tests
    run_performance_tests()
    
    # Run security tests
    run_security_tests()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    
    if failures == 0 and errors == 0:
        print("\n🎉 All tests passed! The application is ready for use.")
        return True
    else:
        print(f"\n⚠️  {failures + errors} tests failed. Please review the issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)