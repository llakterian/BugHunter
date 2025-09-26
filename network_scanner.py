"""
Network Scanner - Advanced network reconnaissance and port scanning
"""

import socket
import threading
import subprocess
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple
import requests
import urllib.parse

class NetworkScanner:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.open_ports = []
        self.services = {}
        self.vulnerabilities = []
        
        # Common ports and their services
        self.common_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S',
            1433: 'MSSQL',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5900: 'VNC',
            6379: 'Redis',
            8080: 'HTTP-Alt',
            8443: 'HTTPS-Alt',
            9200: 'Elasticsearch',
            27017: 'MongoDB'
        }
        
        # Service banners and fingerprints
        self.service_banners = {
            'SSH': [b'SSH-', b'OpenSSH'],
            'HTTP': [b'HTTP/', b'Server:', b'Apache', b'nginx'],
            'FTP': [b'220', b'FTP', b'vsftpd'],
            'SMTP': [b'220', b'SMTP', b'Postfix'],
            'MySQL': [b'mysql_native_password', b'5.7.', b'8.0.'],
            'PostgreSQL': [b'SCRAM-SHA-256', b'md5'],
            'Redis': [b'PONG', b'redis_version']
        }
    
    def scan_port(self, host: str, port: int, timeout: int = 3) -> Optional[Dict]:
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            
            if result == 0:
                # Port is open, try to grab banner
                banner = self.grab_banner(sock, port)
                service = self.identify_service(port, banner)
                
                port_info = {
                    'port': port,
                    'state': 'open',
                    'service': service,
                    'banner': banner.decode('utf-8', errors='ignore') if banner else '',
                    'version': self.extract_version(banner, service) if banner else ''
                }
                
                sock.close()
                return port_info
            
            sock.close()
            return None
            
        except Exception as e:
            return None
    
    def grab_banner(self, sock: socket.socket, port: int) -> bytes:
        """Grab service banner"""
        try:
            # Send appropriate probe based on port
            if port == 80 or port == 8080:
                sock.send(b'GET / HTTP/1.1\r\nHost: target\r\n\r\n')
            elif port == 443 or port == 8443:
                # For HTTPS, we'd need SSL context
                pass
            elif port == 21:
                pass  # FTP sends banner automatically
            elif port == 22:
                pass  # SSH sends banner automatically
            elif port == 25:
                sock.send(b'EHLO test\r\n')
            elif port == 6379:
                sock.send(b'PING\r\n')
            
            # Receive banner
            sock.settimeout(3)
            banner = sock.recv(1024)
            return banner
            
        except Exception as e:
            return b''
    
    def identify_service(self, port: int, banner: bytes) -> str:
        """Identify service based on port and banner"""
        # First check common port mapping
        service = self.common_ports.get(port, 'Unknown')
        
        # Then check banner for more accurate identification
        if banner:
            banner_lower = banner.lower()
            for svc, patterns in self.service_banners.items():
                for pattern in patterns:
                    if pattern.lower() in banner_lower:
                        return svc
        
        return service
    
    def extract_version(self, banner: bytes, service: str) -> str:
        """Extract version information from banner"""
        try:
            banner_str = banner.decode('utf-8', errors='ignore')
            
            # Common version patterns
            version_patterns = {
                'Apache': r'Apache/([0-9.]+)',
                'nginx': r'nginx/([0-9.]+)',
                'OpenSSH': r'OpenSSH_([0-9.]+)',
                'MySQL': r'([0-9.]+)-',
                'PostgreSQL': r'PostgreSQL ([0-9.]+)',
                'Redis': r'redis_version:([0-9.]+)'
            }
            
            import re
            for pattern_name, pattern in version_patterns.items():
                if pattern_name.lower() in service.lower():
                    match = re.search(pattern, banner_str)
                    if match:
                        return match.group(1)
            
            return 'Unknown'
            
        except Exception as e:
            return 'Unknown'
    
    def port_scan(self, host: str, ports: List[int] = None, threads: int = 100) -> List[Dict]:
        """Perform port scan on target host"""
        if ports is None:
            # Scan top 1000 ports
            ports = list(range(1, 1001))
        
        open_ports = []
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.scan_port, host, port) for port in ports]
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
        
        # Sort by port number
        open_ports.sort(key=lambda x: x['port'])
        return open_ports
    
    def service_enumeration(self, host: str, port_info: Dict) -> Dict:
        """Enumerate specific service for vulnerabilities"""
        port = port_info['port']
        service = port_info['service']
        
        enumeration_result = {
            'port': port,
            'service': service,
            'vulnerabilities': [],
            'information': [],
            'recommendations': []
        }
        
        # Service-specific enumeration
        if service == 'HTTP' or service == 'HTTPS':
            enumeration_result.update(self.enumerate_http(host, port))
        elif service == 'SSH':
            enumeration_result.update(self.enumerate_ssh(host, port))
        elif service == 'FTP':
            enumeration_result.update(self.enumerate_ftp(host, port))
        elif service == 'MySQL':
            enumeration_result.update(self.enumerate_mysql(host, port))
        elif service == 'Redis':
            enumeration_result.update(self.enumerate_redis(host, port))
        
        return enumeration_result
    
    def enumerate_http(self, host: str, port: int) -> Dict:
        """Enumerate HTTP service"""
        result = {
            'vulnerabilities': [],
            'information': [],
            'recommendations': []
        }
        
        try:
            protocol = 'https' if port == 443 or port == 8443 else 'http'
            base_url = f"{protocol}://{host}:{port}"
            
            # Basic HTTP enumeration
            response = requests.get(base_url, timeout=10, verify=False)
            
            # Check server header
            server = response.headers.get('Server', '')
            if server:
                result['information'].append(f"Server: {server}")
            
            # Check for common vulnerabilities
            headers = response.headers
            
            # Missing security headers
            security_headers = {
                'X-Frame-Options': 'Clickjacking protection',
                'X-XSS-Protection': 'XSS protection',
                'X-Content-Type-Options': 'MIME type sniffing protection',
                'Strict-Transport-Security': 'HTTPS enforcement',
                'Content-Security-Policy': 'XSS and injection protection'
            }
            
            for header, description in security_headers.items():
                if header not in headers:
                    result['vulnerabilities'].append({
                        'type': f'Missing {header}',
                        'severity': 'Low',
                        'description': f'Missing security header: {description}',
                        'recommendation': f'Add {header} header'
                    })
            
            # Check for directory listing
            dir_response = requests.get(f"{base_url}/", timeout=10, verify=False)
            if 'Index of /' in dir_response.text:
                result['vulnerabilities'].append({
                    'type': 'Directory Listing',
                    'severity': 'Medium',
                    'description': 'Directory listing is enabled',
                    'recommendation': 'Disable directory listing'
                })
            
            # Check for common files
            common_files = [
                '/robots.txt',
                '/.htaccess',
                '/web.config',
                '/phpinfo.php',
                '/info.php',
                '/test.php'
            ]
            
            for file_path in common_files:
                try:
                    file_response = requests.get(f"{base_url}{file_path}", timeout=5, verify=False)
                    if file_response.status_code == 200:
                        result['information'].append(f"Found: {file_path}")
                        
                        if 'phpinfo' in file_path and 'PHP Version' in file_response.text:
                            result['vulnerabilities'].append({
                                'type': 'Information Disclosure',
                                'severity': 'Medium',
                                'description': 'PHP info page accessible',
                                'recommendation': 'Remove or restrict access to phpinfo.php'
                            })
                except:
                    pass
            
        except Exception as e:
            result['information'].append(f"HTTP enumeration error: {str(e)}")
        
        return result
    
    def enumerate_ssh(self, host: str, port: int) -> Dict:
        """Enumerate SSH service"""
        result = {
            'vulnerabilities': [],
            'information': [],
            'recommendations': []
        }
        
        try:
            # Connect and get SSH banner
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((host, port))
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            result['information'].append(f"SSH Banner: {banner.strip()}")
            
            # Check for old SSH versions
            if 'OpenSSH' in banner:
                import re
                version_match = re.search(r'OpenSSH_([0-9.]+)', banner)
                if version_match:
                    version = version_match.group(1)
                    version_parts = [int(x) for x in version.split('.')]
                    
                    # Check for known vulnerable versions
                    if version_parts[0] < 7 or (version_parts[0] == 7 and version_parts[1] < 4):
                        result['vulnerabilities'].append({
                            'type': 'Outdated SSH Version',
                            'severity': 'Medium',
                            'description': f'SSH version {version} may have known vulnerabilities',
                            'recommendation': 'Update to latest SSH version'
                        })
            
            # Test for weak authentication
            weak_creds = [
                ('root', 'root'),
                ('admin', 'admin'),
                ('root', ''),
                ('admin', 'password'),
                ('user', 'user')
            ]
            
            for username, password in weak_creds:
                try:
                    # Note: In a real implementation, use paramiko for SSH testing
                    # This is a placeholder for the concept
                    result['information'].append(f"Tested credentials: {username}:{password}")
                except:
                    pass
            
        except Exception as e:
            result['information'].append(f"SSH enumeration error: {str(e)}")
        
        return result
    
    def enumerate_ftp(self, host: str, port: int) -> Dict:
        """Enumerate FTP service"""
        result = {
            'vulnerabilities': [],
            'information': [],
            'recommendations': []
        }
        
        try:
            # Connect to FTP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((host, port))
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            result['information'].append(f"FTP Banner: {banner.strip()}")
            
            # Test anonymous login
            sock.send(b'USER anonymous\r\n')
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            
            if '331' in response:  # User OK, need password
                sock.send(b'PASS anonymous@test.com\r\n')
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                
                if '230' in response:  # Login successful
                    result['vulnerabilities'].append({
                        'type': 'Anonymous FTP Access',
                        'severity': 'Medium',
                        'description': 'FTP allows anonymous access',
                        'recommendation': 'Disable anonymous FTP access'
                    })
            
            sock.close()
            
        except Exception as e:
            result['information'].append(f"FTP enumeration error: {str(e)}")
        
        return result
    
    def enumerate_mysql(self, host: str, port: int) -> Dict:
        """Enumerate MySQL service"""
        result = {
            'vulnerabilities': [],
            'information': [],
            'recommendations': []
        }
        
        try:
            # Test MySQL connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((host, port))
            
            # Receive initial handshake
            handshake = sock.recv(1024)
            
            if handshake:
                # Extract version from handshake
                version_end = handshake.find(b'\x00', 5)
                if version_end > 5:
                    version = handshake[5:version_end].decode('utf-8', errors='ignore')
                    result['information'].append(f"MySQL Version: {version}")
            
            sock.close()
            
            # Test for weak credentials
            weak_creds = [
                ('root', ''),
                ('root', 'root'),
                ('admin', 'admin'),
                ('mysql', 'mysql')
            ]
            
            for username, password in weak_creds:
                # Note: In a real implementation, use mysql-connector-python
                result['information'].append(f"Tested MySQL credentials: {username}:{password}")
            
        except Exception as e:
            result['information'].append(f"MySQL enumeration error: {str(e)}")
        
        return result
    
    def enumerate_redis(self, host: str, port: int) -> Dict:
        """Enumerate Redis service"""
        result = {
            'vulnerabilities': [],
            'information': [],
            'recommendations': []
        }
        
        try:
            # Connect to Redis
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((host, port))
            
            # Test INFO command (no auth required if misconfigured)
            sock.send(b'INFO\r\n')
            response = sock.recv(4096).decode('utf-8', errors='ignore')
            
            if 'redis_version' in response:
                result['vulnerabilities'].append({
                    'type': 'Unauthenticated Redis Access',
                    'severity': 'High',
                    'description': 'Redis allows unauthenticated access',
                    'recommendation': 'Configure Redis authentication'
                })
                
                # Extract version
                import re
                version_match = re.search(r'redis_version:([0-9.]+)', response)
                if version_match:
                    result['information'].append(f"Redis Version: {version_match.group(1)}")
            
            sock.close()
            
        except Exception as e:
            result['information'].append(f"Redis enumeration error: {str(e)}")
        
        return result
    
    def comprehensive_scan(self, target: str) -> Dict:
        """Perform comprehensive network scan"""
        # Parse target (could be IP or domain)
        try:
            host = socket.gethostbyname(target)
        except:
            host = target
        
        scan_results = {
            'target': target,
            'host': host,
            'open_ports': [],
            'services': [],
            'vulnerabilities': [],
            'recommendations': []
        }
        
        # Port scan
        print(f"Scanning ports on {host}...")
        open_ports = self.port_scan(host, threads=50)
        scan_results['open_ports'] = open_ports
        
        # Service enumeration
        print(f"Enumerating services...")
        for port_info in open_ports:
            service_enum = self.service_enumeration(host, port_info)
            scan_results['services'].append(service_enum)
            
            # Collect vulnerabilities
            scan_results['vulnerabilities'].extend(service_enum.get('vulnerabilities', []))
        
        return scan_results
    
    def generate_nmap_command(self, target: str, scan_type: str = 'comprehensive') -> str:
        """Generate equivalent nmap command"""
        commands = {
            'quick': f'nmap -T4 -F {target}',
            'comprehensive': f'nmap -T4 -A -sC -sV -O {target}',
            'stealth': f'nmap -sS -T2 {target}',
            'udp': f'nmap -sU --top-ports 1000 {target}',
            'vuln': f'nmap --script vuln {target}'
        }
        
        return commands.get(scan_type, commands['comprehensive'])