#!/usr/bin/env python3
"""
Tool Integrations - GAU, FFF, GF integration for enhanced reconnaissance
"""

import os
import subprocess
import json
import tempfile
import shutil
from typing import List, Dict, Optional
from urllib.parse import urlparse, parse_qs
import requests
import time
import re

class ToolIntegrations:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="bughunter_")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BugHunter-Pro/1.0 (Educational Use Only)'
        })
        
    def __del__(self):
        """Cleanup temporary directory"""
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def check_tool_availability(self) -> Dict[str, bool]:
        """Check if required tools are available"""
        tools = {
            'gau': self._check_command('gau'),
            'fff': self._check_command('fff'),
            'gf': self._check_command('gf'),
            'curl': self._check_command('curl'),
            'wget': self._check_command('wget')
        }
        return tools
    
    def _check_command(self, command: str) -> bool:
        """Check if a command is available"""
        try:
            subprocess.run([command, '--help'], 
                         capture_output=True, 
                         timeout=5)
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            return False
    
    def install_missing_tools(self) -> Dict[str, str]:
        """Install missing tools (for educational environments)"""
        results = {}
        
        # GAU installation
        if not self._check_command('gau'):
            try:
                subprocess.run([
                    'go', 'install', 'github.com/lc/gau/v2/cmd/gau@latest'
                ], check=True, capture_output=True)
                results['gau'] = 'installed'
            except:
                results['gau'] = 'failed - install manually: go install github.com/lc/gau/v2/cmd/gau@latest'
        
        # FFF installation
        if not self._check_command('fff'):
            try:
                subprocess.run([
                    'go', 'install', 'github.com/tomnomnom/fff@latest'
                ], check=True, capture_output=True)
                results['fff'] = 'installed'
            except:
                results['fff'] = 'failed - install manually: go install github.com/tomnomnom/fff@latest'
        
        # GF installation
        if not self._check_command('gf'):
            try:
                subprocess.run([
                    'go', 'install', 'github.com/tomnomnom/gf@latest'
                ], check=True, capture_output=True)
                results['gf'] = 'installed'
            except:
                results['gf'] = 'failed - install manually: go install github.com/tomnomnom/gf@latest'
        
        return results
    
    def run_gau(self, target: str, include_subs: bool = True, 
                providers: List[str] = None) -> List[str]:
        """Run GAU (Get All URLs) against target"""
        if not self._check_command('gau'):
            raise Exception("GAU tool not available. Install with: go install github.com/lc/gau/v2/cmd/gau@latest")
        
        cmd = ['gau']
        
        if include_subs:
            cmd.append('-subs')
        
        if providers:
            cmd.extend(['-providers', ','.join(providers)])
        
        cmd.append(target)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                urls = [url.strip() for url in result.stdout.split('\n') if url.strip()]
                return urls
            else:
                raise Exception(f"GAU failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            raise Exception("GAU timed out after 5 minutes")
    
    def filter_js_urls(self, urls: List[str]) -> List[str]:
        """Filter URLs to find JavaScript files"""
        js_urls = []
        js_patterns = [
            r'\.js$',
            r'\.json$',
            r'\.jsx$',
            r'\.ts$',
            r'\.tsx$'
        ]
        
        for url in urls:
            # Remove query parameters for pattern matching
            base_url = url.split('?')[0]
            for pattern in js_patterns:
                if re.search(pattern, base_url, re.IGNORECASE):
                    js_urls.append(url)
                    break
        
        return js_urls
    
    def run_fff(self, urls: List[str], status_codes: List[int] = None, 
                output_dir: str = None) -> Dict[str, any]:
        """Run FFF (Fuzzing for Files) against URLs"""
        if not self._check_command('fff'):
            raise Exception("FFF tool not available. Install with: go install github.com/tomnomnom/fff@latest")
        
        if not urls:
            return {'error': 'No URLs provided'}
        
        # Create temporary file with URLs
        urls_file = os.path.join(self.temp_dir, 'urls.txt')
        with open(urls_file, 'w') as f:
            f.write('\n'.join(urls))
        
        # Set up output directory
        if not output_dir:
            output_dir = os.path.join(self.temp_dir, 'fff_output')
        
        os.makedirs(output_dir, exist_ok=True)
        
        cmd = ['fff']
        
        if status_codes:
            cmd.extend(['-s', ','.join(map(str, status_codes))])
        else:
            cmd.extend(['-s', '200'])
        
        cmd.extend(['-o', output_dir])
        
        try:
            # Run fff with URLs from file
            with open(urls_file, 'r') as f:
                result = subprocess.run(cmd, stdin=f, capture_output=True, 
                                      text=True, timeout=600)
            
            if result.returncode == 0:
                # Parse results
                results = self._parse_fff_output(output_dir)
                return {
                    'success': True,
                    'results': results,
                    'output_dir': output_dir
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'output_dir': output_dir
                }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'FFF timed out after 10 minutes',
                'output_dir': output_dir
            }
    
    def _parse_fff_output(self, output_dir: str) -> Dict[str, any]:
        """Parse FFF output directory"""
        results = {
            'files_found': 0,
            'responses': [],
            'errors': []
        }
        
        try:
            for filename in os.listdir(output_dir):
                filepath = os.path.join(output_dir, filename)
                if os.path.isfile(filepath):
                    results['files_found'] += 1
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            results['responses'].append({
                                'filename': filename,
                                'size': len(content),
                                'content_preview': content[:500] + '...' if len(content) > 500 else content
                            })
                    except Exception as e:
                        results['errors'].append(f"Error reading {filename}: {str(e)}")
        except Exception as e:
            results['errors'].append(f"Error parsing output directory: {str(e)}")
        
        return results
    
    def run_gf_secrets(self, content_dir: str) -> Dict[str, List[str]]:
        """Run GF patterns to find secrets"""
        if not self._check_command('gf'):
            raise Exception("GF tool not available. Install with: go install github.com/tomnomnom/gf@latest")
        
        secrets_found = {}
        
        try:
            # Get list of available GF patterns
            result = subprocess.run(['gf', '-list'], capture_output=True, text=True)
            if result.returncode != 0:
                return {'error': 'Failed to get GF patterns list'}
            
            patterns = result.stdout.strip().split('\n')
            secret_patterns = [p for p in patterns if 'secret' in p.lower() or 
                             'key' in p.lower() or 'token' in p.lower() or 
                             'password' in p.lower() or 'credential' in p.lower()]
            
            # Run each secret pattern
            for pattern in secret_patterns:
                try:
                    # Find all files in content directory
                    files_to_scan = []
                    for root, dirs, files in os.walk(content_dir):
                        for file in files:
                            files_to_scan.append(os.path.join(root, file))
                    
                    if files_to_scan:
                        # Run gf pattern on files
                        cmd = ['gf', pattern] + files_to_scan
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                        
                        if result.returncode == 0 and result.stdout.strip():
                            secrets_found[pattern] = result.stdout.strip().split('\n')
                
                except subprocess.TimeoutExpired:
                    secrets_found[pattern] = ['Timeout occurred']
                except Exception as e:
                    secrets_found[pattern] = [f'Error: {str(e)}']
        
        except Exception as e:
            return {'error': f'GF execution failed: {str(e)}'}
        
        return secrets_found
    
    def comprehensive_url_discovery(self, target: str) -> Dict[str, any]:
        """Comprehensive URL discovery using GAU + filtering"""
        results = {
            'target': target,
            'total_urls': 0,
            'js_urls': 0,
            'parameter_urls': 0,
            'endpoints_found': [],
            'parameters_found': set(),
            'errors': []
        }
        
        try:
            # Step 1: Run GAU
            print(f"🔍 Running GAU against {target}...")
            all_urls = self.run_gau(target, include_subs=True)
            results['total_urls'] = len(all_urls)
            
            # Step 2: Filter JavaScript URLs
            js_urls = self.filter_js_urls(all_urls)
            results['js_urls'] = len(js_urls)
            
            # Step 3: Find URLs with parameters
            param_urls = [url for url in all_urls if '?' in url]
            results['parameter_urls'] = len(param_urls)
            
            # Step 4: Extract parameters
            for url in param_urls:
                parsed = urlparse(url)
                if parsed.query:
                    params = parse_qs(parsed.query)
                    for param in params.keys():
                        results['parameters_found'].add(param)
            
            # Step 5: Identify interesting endpoints
            interesting_patterns = [
                'admin', 'login', 'upload', 'download', 'api', 'config',
                'backup', 'debug', 'test', 'dev', 'staging', 'internal'
            ]
            
            for url in all_urls:
                for pattern in interesting_patterns:
                    if pattern in url.lower():
                        results['endpoints_found'].append(url)
                        break
            
            results['parameters_found'] = list(results['parameters_found'])
            
        except Exception as e:
            results['errors'].append(f"URL discovery failed: {str(e)}")
        
        return results
    
    def automated_secrets_hunting(self, target: str) -> Dict[str, any]:
        """Automated secrets hunting workflow"""
        results = {
            'target': target,
            'urls_discovered': 0,
            'files_analyzed': 0,
            'secrets_found': {},
            'high_value_findings': [],
            'errors': []
        }
        
        try:
            # Step 1: URL Discovery
            print("🔍 Phase 1: URL Discovery...")
            discovery_results = self.comprehensive_url_discovery(target)
            results['urls_discovered'] = discovery_results['total_urls']
            
            if discovery_results['errors']:
                results['errors'].extend(discovery_results['errors'])
            
            # Step 2: Get JavaScript URLs for analysis
            all_urls = self.run_gau(target, include_subs=True)
            js_urls = self.filter_js_urls(all_urls)
            
            if js_urls:
                print(f"📁 Phase 2: Analyzing {len(js_urls)} JavaScript files...")
                
                # Step 3: Use FFF to fetch responses
                fff_results = self.run_fff(js_urls[:50])  # Limit to first 50 for performance
                
                if fff_results.get('success'):
                    results['files_analyzed'] = fff_results['results']['files_found']
                    
                    # Step 4: Run GF secrets scanning
                    print("🔐 Phase 3: Secrets scanning...")
                    secrets = self.run_gf_secrets(fff_results['output_dir'])
                    results['secrets_found'] = secrets
                    
                    # Step 5: Identify high-value findings
                    high_value_patterns = ['api_key', 'secret', 'token', 'password', 'credential']
                    for pattern, findings in secrets.items():
                        if any(hv in pattern.lower() for hv in high_value_patterns):
                            if findings and findings != ['Timeout occurred']:
                                results['high_value_findings'].extend(findings)
                
                else:
                    results['errors'].append(f"FFF analysis failed: {fff_results.get('error', 'Unknown error')}")
            
        except Exception as e:
            results['errors'].append(f"Automated secrets hunting failed: {str(e)}")
        
        return results
    
    def generate_custom_wordlist(self, target: str, discovered_params: List[str]) -> List[str]:
        """Generate custom wordlist based on discovered parameters and target"""
        from enhanced_wordlists import get_all_parameters, get_all_endpoints
        
        custom_wordlist = []
        
        # Add discovered parameters
        custom_wordlist.extend(discovered_params)
        
        # Add standard parameters
        custom_wordlist.extend(get_all_parameters())
        
        # Add endpoints
        custom_wordlist.extend(get_all_endpoints())
        
        # Add target-specific variations
        domain_parts = target.replace('http://', '').replace('https://', '').split('.')
        for part in domain_parts:
            if len(part) > 2:
                custom_wordlist.extend([
                    f"{part}_api",
                    f"{part}_admin",
                    f"{part}_config",
                    f"{part}_backup",
                    f"{part}_test"
                ])
        
        # Remove duplicates and return
        return list(set(custom_wordlist))

# Example usage and testing
if __name__ == "__main__":
    tools = ToolIntegrations()
    
    # Check tool availability
    available = tools.check_tool_availability()
    print("Tool Availability:")
    for tool, status in available.items():
        print(f"  {tool}: {'✅' if status else '❌'}")
    
    # Install missing tools (if in appropriate environment)
    if not all(available.values()):
        print("\n🔧 Installing missing tools...")
        install_results = tools.install_missing_tools()
        for tool, result in install_results.items():
            print(f"  {tool}: {result}")