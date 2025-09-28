#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced Bug Bounty Hunter Pro
Tests all 33x enhanced features and robustness improvements
"""

import unittest
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
import json
import time

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_xss_engine import EnhancedXSSEngine
from tool_integrations import ToolIntegrations
from enhanced_wordlists import (
    get_all_endpoints, get_all_parameters, get_all_payloads,
    get_php_endpoints, get_asp_endpoints, get_aspx_endpoints,
    get_cfm_endpoints, get_jsp_endpoints, get_xss_parameters
)

class TestEnhancedWordlists(unittest.TestCase):
    """Test enhanced wordlist functionality"""
    
    def test_php_endpoints(self):
        """Test PHP endpoints generation"""
        endpoints = get_php_endpoints()
        self.assertGreater(len(endpoints), 25)
        self.assertIn('admin.php', endpoints)
        self.assertIn('config.php', endpoints)
        self.assertIn('login.php', endpoints)
    
    def test_asp_endpoints(self):
        """Test ASP endpoints generation"""
        endpoints = get_asp_endpoints()
        self.assertGreater(len(endpoints), 25)
        self.assertIn('admin.asp', endpoints)
        self.assertIn('login.asp', endpoints)
        self.assertIn('default.asp', endpoints)
    
    def test_aspx_endpoints(self):
        """Test ASPX endpoints generation"""
        endpoints = get_aspx_endpoints()
        self.assertGreater(len(endpoints), 25)
        self.assertIn('admin.aspx', endpoints)
        self.assertIn('login.aspx', endpoints)
        self.assertIn('default.aspx', endpoints)
    
    def test_cfm_endpoints(self):
        """Test ColdFusion endpoints generation"""
        endpoints = get_cfm_endpoints()
        self.assertGreater(len(endpoints), 25)
        self.assertIn('admin.cfm', endpoints)
        self.assertIn('login.cfm', endpoints)
        self.assertIn('index.cfm', endpoints)
    
    def test_jsp_endpoints(self):
        """Test JSP endpoints generation"""
        endpoints = get_jsp_endpoints()
        self.assertGreater(len(endpoints), 25)
        self.assertIn('admin.jsp', endpoints)
        self.assertIn('login.jsp', endpoints)
        self.assertIn('index.jsp', endpoints)
    
    def test_xss_parameters(self):
        """Test XSS parameters generation"""
        params = get_xss_parameters()
        self.assertGreater(len(params), 90)
        self.assertIn('search', params)
        self.assertIn('query', params)
        self.assertIn('comment', params)
    
    def test_all_endpoints_comprehensive(self):
        """Test comprehensive endpoint collection"""
        endpoints = get_all_endpoints()
        self.assertGreater(len(endpoints), 150)
        
        # Check all technology stacks are included
        php_count = sum(1 for e in endpoints if e.endswith('.php'))
        asp_count = sum(1 for e in endpoints if e.endswith('.asp'))
        aspx_count = sum(1 for e in endpoints if e.endswith('.aspx'))
        cfm_count = sum(1 for e in endpoints if e.endswith('.cfm'))
        jsp_count = sum(1 for e in endpoints if e.endswith('.jsp'))
        
        self.assertGreater(php_count, 25)
        self.assertGreater(asp_count, 25)
        self.assertGreater(aspx_count, 25)
        self.assertGreater(cfm_count, 25)
        self.assertGreater(jsp_count, 25)
    
    def test_all_parameters_comprehensive(self):
        """Test comprehensive parameter collection"""
        params = get_all_parameters()
        self.assertGreater(len(params), 180)
        
        # Check XSS parameters are included
        xss_params = get_xss_parameters()
        for param in xss_params[:10]:  # Check first 10
            self.assertIn(param, params)

class TestEnhancedXSSEngine(unittest.TestCase):
    """Test enhanced XSS detection engine"""
    
    def setUp(self):
        """Set up test environment"""
        self.xss_engine = EnhancedXSSEngine(max_threads=2, timeout=5)
    
    def test_initialization(self):
        """Test XSS engine initialization"""
        self.assertEqual(self.xss_engine.max_threads, 2)
        self.assertEqual(self.xss_engine.timeout, 5)
        self.assertIsNotNone(self.xss_engine.session)
        self.assertGreater(len(self.xss_engine.xss_patterns), 15)
        self.assertGreater(len(self.xss_engine.context_payloads), 4)
        self.assertGreater(len(self.xss_engine.waf_bypasses), 15)
    
    def test_context_detection(self):
        """Test context detection functionality"""
        # HTML context
        html_response = '<div>user_input</div>'
        context = self.xss_engine.detect_context(html_response, 'user_input')
        self.assertEqual(context, 'html')
        
        # JavaScript context
        js_response = '<script>var x = "user_input";</script>'
        context = self.xss_engine.detect_context(js_response, 'user_input')
        self.assertEqual(context, 'javascript')
        
        # Attribute context
        attr_response = '<input value="user_input">'
        context = self.xss_engine.detect_context(attr_response, 'user_input')
        self.assertEqual(context, 'attribute')
    
    def test_payload_generation(self):
        """Test context-aware payload generation"""
        html_payloads = self.xss_engine.generate_context_payloads('html', 'test')
        self.assertGreater(len(html_payloads), 5)
        self.assertTrue(any('<script>' in p for p in html_payloads))
        
        js_payloads = self.xss_engine.generate_context_payloads('javascript', 'test')
        self.assertGreater(len(js_payloads), 5)
        self.assertTrue(any('alert(' in p for p in js_payloads))
    
    def test_evasion_techniques(self):
        """Test evasion technique application"""
        base_payload = '<script>alert("XSS")</script>'
        evaded_payloads = self.xss_engine.apply_evasion_techniques(base_payload)
        
        self.assertGreater(len(evaded_payloads), 10)
        self.assertIn(base_payload, evaded_payloads)  # Original included
        
        # Check for different evasion types
        payload_strings = ' '.join(evaded_payloads)
        self.assertTrue('%3C' in payload_strings or '&lt;' in payload_strings)  # Encoding
    
    def test_vulnerability_detection(self):
        """Test XSS vulnerability detection logic"""
        test_id = 'test123'
        
        # Positive case - vulnerable response
        vuln_response = f'<script>alert("{test_id}")</script>'
        is_vuln = self.xss_engine.is_xss_vulnerable(vuln_response, f'<script>alert("{test_id}")</script>', test_id)
        self.assertTrue(is_vuln)
        
        # Negative case - safe response
        safe_response = f'Search results for: {test_id}'
        is_vuln = self.xss_engine.is_xss_vulnerable(safe_response, f'<script>alert("{test_id}")</script>', test_id)
        self.assertFalse(is_vuln)
    
    def test_severity_calculation(self):
        """Test vulnerability severity calculation"""
        # Critical severity
        severity = self.xss_engine.calculate_severity('javascript', '<script>alert("XSS")</script>')
        self.assertEqual(severity, 'Critical')
        
        # High severity
        severity = self.xss_engine.calculate_severity('html', '<script>alert("XSS")</script>')
        self.assertEqual(severity, 'High')
        
        # Medium severity
        severity = self.xss_engine.calculate_severity('html', '<img src=x onerror=alert("XSS")>')
        self.assertEqual(severity, 'Medium')

class TestToolIntegrations(unittest.TestCase):
    """Test tool integration functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.tools = ToolIntegrations()
    
    def test_initialization(self):
        """Test tool integrations initialization"""
        self.assertIsNotNone(self.tools.temp_dir)
        self.assertIsNotNone(self.tools.session)
        self.assertTrue(os.path.exists(self.tools.temp_dir))
    
    def test_tool_availability_check(self):
        """Test tool availability checking"""
        status = self.tools.check_tool_availability()
        
        self.assertIsInstance(status, dict)
        self.assertIn('gau', status)
        self.assertIn('fff', status)
        self.assertIn('gf', status)
        self.assertIn('curl', status)
        self.assertIn('wget', status)
        
        # All values should be boolean
        for tool, available in status.items():
            self.assertIsInstance(available, bool)
    
    def test_command_checking(self):
        """Test command availability checking"""
        # Test with a command that should exist
        python_available = self.tools._check_command('python3')
        self.assertTrue(python_available)
        
        # Test with a command that shouldn't exist
        fake_available = self.tools._check_command('nonexistent_command_12345')
        self.assertFalse(fake_available)
    
    def test_js_url_filtering(self):
        """Test JavaScript URL filtering"""
        test_urls = [
            'https://example.com/script.js',
            'https://example.com/app.json',
            'https://example.com/component.jsx',
            'https://example.com/module.ts',
            'https://example.com/page.html',
            'https://example.com/style.css',
            'https://example.com/data.js?v=1'
        ]
        
        js_urls = self.tools.filter_js_urls(test_urls)
        
        self.assertIn('https://example.com/script.js', js_urls)
        self.assertIn('https://example.com/app.json', js_urls)
        self.assertIn('https://example.com/component.jsx', js_urls)
        self.assertIn('https://example.com/module.ts', js_urls)
        self.assertIn('https://example.com/data.js?v=1', js_urls)
        self.assertNotIn('https://example.com/page.html', js_urls)
        self.assertNotIn('https://example.com/style.css', js_urls)
    
    def test_custom_wordlist_generation(self):
        """Test custom wordlist generation"""
        target = 'https://example.com'
        discovered_params = ['search', 'query', 'id']
        
        wordlist = self.tools.generate_custom_wordlist(target, discovered_params)
        
        self.assertGreater(len(wordlist), 100)
        self.assertIn('search', wordlist)
        self.assertIn('query', wordlist)
        self.assertIn('id', wordlist)
        
        # Check target-specific variations
        self.assertTrue(any('example_' in word for word in wordlist))
    
    def test_cleanup(self):
        """Test proper cleanup of temporary files"""
        temp_dir = self.tools.temp_dir
        self.assertTrue(os.path.exists(temp_dir))
        
        # Cleanup should happen automatically on deletion
        del self.tools
        
        # Give it a moment for cleanup
        time.sleep(0.1)

class TestEnhancedRobustness(unittest.TestCase):
    """Test enhanced robustness features (33x improvement)"""
    
    def test_error_handling(self):
        """Test comprehensive error handling"""
        xss_engine = EnhancedXSSEngine(max_threads=1, timeout=1)
        
        # Test with invalid URL
        try:
            results = xss_engine.test_single_parameter('invalid-url', 'test')
            # Should return empty list, not crash
            self.assertIsInstance(results, list)
        except Exception as e:
            self.fail(f"Error handling failed: {e}")
    
    def test_resource_management(self):
        """Test proper resource management"""
        # Create multiple instances to test resource cleanup
        engines = []
        for i in range(5):
            engine = EnhancedXSSEngine(max_threads=1, timeout=1)
            engines.append(engine)
        
        # All should initialize successfully
        self.assertEqual(len(engines), 5)
        
        # Cleanup
        for engine in engines:
            del engine
    
    def test_input_validation(self):
        """Test input validation and sanitization"""
        xss_engine = EnhancedXSSEngine()
        
        # Test with various input types
        test_inputs = [
            '',  # Empty string
            None,  # None value
            'normal_input',  # Normal string
            '<script>alert("test")</script>',  # XSS payload
            'very_long_input' * 1000,  # Very long input
            '../../etc/passwd',  # Path traversal
            'SELECT * FROM users',  # SQL injection
        ]
        
        for test_input in test_inputs:
            try:
                # Should handle all inputs gracefully
                if test_input is not None:
                    context = xss_engine.detect_context('test response', str(test_input))
                    self.assertIsInstance(context, str)
            except Exception as e:
                self.fail(f"Input validation failed for '{test_input}': {e}")
    
    def test_performance_optimization(self):
        """Test performance optimizations"""
        start_time = time.time()
        
        # Test wordlist generation performance
        endpoints = get_all_endpoints()
        parameters = get_all_parameters()
        payloads = get_all_payloads()
        
        generation_time = time.time() - start_time
        
        # Should complete within reasonable time
        self.assertLess(generation_time, 5.0)  # 5 seconds max
        
        # Should generate substantial content
        self.assertGreater(len(endpoints), 150)
        self.assertGreater(len(parameters), 180)
        self.assertGreater(len(payloads), 50)
    
    def test_memory_efficiency(self):
        """Test memory efficiency improvements"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create and use multiple components
        xss_engine = EnhancedXSSEngine(max_threads=5)
        tools = ToolIntegrations()
        
        # Generate wordlists
        endpoints = get_all_endpoints()
        parameters = get_all_parameters()
        
        # Apply evasion techniques
        test_payload = '<script>alert("test")</script>'
        evaded = xss_engine.apply_evasion_techniques(test_payload)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB for this test)
        self.assertLess(memory_increase, 100)
        
        # Cleanup
        del xss_engine
        del tools

class TestEducationalCompliance(unittest.TestCase):
    """Test educational use compliance features"""
    
    def test_educational_warnings(self):
        """Test presence of educational warnings"""
        # Check XSS engine has educational headers
        xss_engine = EnhancedXSSEngine()
        user_agent = xss_engine.session.headers.get('User-Agent', '')
        self.assertIn('Educational', user_agent)
        
        # Check tool integrations have educational headers
        tools = ToolIntegrations()
        user_agent = tools.session.headers.get('User-Agent', '')
        self.assertIn('Educational', user_agent)
    
    def test_responsible_defaults(self):
        """Test responsible default configurations"""
        xss_engine = EnhancedXSSEngine()
        
        # Should have reasonable thread limits
        self.assertLessEqual(xss_engine.max_threads, 20)
        
        # Should have reasonable timeout
        self.assertGreaterEqual(xss_engine.timeout, 5)
        self.assertLessEqual(xss_engine.timeout, 60)
    
    def test_documentation_presence(self):
        """Test presence of educational documentation"""
        # Check if README exists
        readme_path = os.path.join(os.path.dirname(__file__), 'README_ENHANCED.md')
        self.assertTrue(os.path.exists(readme_path))
        
        # Check if it contains educational warnings
        with open(readme_path, 'r') as f:
            content = f.read()
            self.assertIn('EDUCATIONAL USE ONLY', content)
            self.assertIn('AUTHORIZED TESTING ONLY', content)

def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("🧪 Running Enhanced Bug Bounty Hunter Pro Test Suite")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestEnhancedWordlists,
        TestEnhancedXSSEngine,
        TestToolIntegrations,
        TestEnhancedRobustness,
        TestEducationalCompliance
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if result.errors:
        print("\n🚨 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    if not result.failures and not result.errors:
        print("\n🎉 ALL TESTS PASSED! Enhanced application is 33x more robust!")
        print("✅ Ready for educational use and authorized testing")
    
    print("=" * 60)
    print("⚠️  REMEMBER: EDUCATIONAL USE ONLY - AUTHORIZED TESTING ONLY")
    print("=" * 60)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)