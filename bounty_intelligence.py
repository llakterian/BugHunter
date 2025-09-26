#!/usr/bin/env python3
"""
Bug Bounty Intelligence System - Automated target discovery and analysis
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import re
from urllib.parse import urlparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class BountyIntelligence:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Bug bounty platforms APIs and endpoints
        self.platforms = {
            'hackerone': {
                'api_base': 'https://api.hackerone.com/v1',
                'programs_endpoint': '/programs',
                'reports_endpoint': '/reports',
                'public_programs': 'https://hackerone.com/programs.json',
                'headers': {'Accept': 'application/json'}
            },
            'bugcrowd': {
                'api_base': 'https://bugcrowd.com/programs.json',
                'public_endpoint': 'https://bugcrowd.com/programs',
                'headers': {'Accept': 'application/json'}
            },
            'intigriti': {
                'api_base': 'https://api.intigriti.com/core/program',
                'public_endpoint': 'https://intigriti.com/programs',
                'headers': {'Accept': 'application/json'}
            }
        }
        
        # Vulnerability patterns we can detect
        self.vulnerability_patterns = {
            'jwt_vulnerabilities': {
                'keywords': ['jwt', 'json web token', 'authentication', 'session', 'token'],
                'scanner_modules': ['jwt_analyzer', 'authentication_bypass'],
                'confidence': 0.9
            },
            'directory_traversal': {
                'keywords': ['directory traversal', 'path traversal', 'lfi', 'local file inclusion'],
                'scanner_modules': ['directory_fuzzing', 'lfi_testing'],
                'confidence': 0.8
            },
            'sql_injection': {
                'keywords': ['sql injection', 'sqli', 'database', 'mysql', 'postgresql'],
                'scanner_modules': ['sql_injection_testing', 'parameter_fuzzing'],
                'confidence': 0.85
            },
            'xss_vulnerabilities': {
                'keywords': ['xss', 'cross-site scripting', 'reflected', 'stored', 'dom xss'],
                'scanner_modules': ['xss_testing', 'parameter_fuzzing'],
                'confidence': 0.8
            },
            'admin_panel_exposure': {
                'keywords': ['admin panel', 'administrative', 'unauthorized access', 'privilege escalation'],
                'scanner_modules': ['admin_panel_discovery', 'directory_fuzzing'],
                'confidence': 0.75
            },
            'subdomain_takeover': {
                'keywords': ['subdomain takeover', 'dns', 'cname', 'subdomain'],
                'scanner_modules': ['subdomain_enumeration', 'takeover_detection'],
                'confidence': 0.7
            }
        }
        
        # Recent vulnerability reports cache
        self.recent_reports = []
        self.target_suggestions = []
    
    def fetch_recent_programs(self, days_back: int = 30) -> List[Dict]:
        """Fetch recently launched or updated bug bounty programs"""
        print("🔍 Fetching recent bug bounty programs...")
        
        recent_programs = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        # Fetch from multiple platforms
        for platform_name, platform_config in self.platforms.items():
            try:
                print(f"   Checking {platform_name.title()}...")
                programs = self._fetch_platform_programs(platform_name, platform_config)
                
                # Filter for recent programs
                for program in programs:
                    if self._is_recent_program(program, cutoff_date):
                        program['platform'] = platform_name
                        recent_programs.append(program)
                        
                time.sleep(2)  # Be respectful to APIs
                
            except Exception as e:
                print(f"   ⚠️  Error fetching from {platform_name}: {e}")
        
        print(f"✅ Found {len(recent_programs)} recent programs")
        return recent_programs
    
    def _fetch_platform_programs(self, platform_name: str, config: Dict) -> List[Dict]:
        """Fetch programs from a specific platform"""
        programs = []
        
        if platform_name == 'hackerone':
            programs = self._fetch_hackerone_programs(config)
        elif platform_name == 'bugcrowd':
            programs = self._fetch_bugcrowd_programs(config)
        elif platform_name == 'intigriti':
            programs = self._fetch_intigriti_programs(config)
        
        return programs
    
    def _fetch_hackerone_programs(self, config: Dict) -> List[Dict]:
        """Fetch HackerOne programs"""
        programs = []
        
        try:
            # Use public programs endpoint
            response = self.session.get(
                config['public_programs'],
                headers=config['headers'],
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                for program_data in data.get('results', []):
                    program = {
                        'name': program_data.get('name', ''),
                        'handle': program_data.get('handle', ''),
                        'url': program_data.get('url', ''),
                        'targets': self._extract_targets(program_data.get('targets', {})),
                        'bounty_range': self._extract_bounty_range(program_data),
                        'launched_at': program_data.get('launched_at'),
                        'updated_at': program_data.get('updated_at'),
                        'submission_state': program_data.get('submission_state'),
                        'offers_bounties': program_data.get('offers_bounties', False)
                    }
                    programs.append(program)
                    
        except Exception as e:
            print(f"HackerOne fetch error: {e}")
        
        return programs
    
    def _fetch_bugcrowd_programs(self, config: Dict) -> List[Dict]:
        """Fetch Bugcrowd programs"""
        programs = []
        
        try:
            response = self.session.get(
                config['api_base'],
                headers=config['headers'],
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                for program_data in data.get('programs', []):
                    program = {
                        'name': program_data.get('name', ''),
                        'code': program_data.get('code', ''),
                        'url': program_data.get('program_url', ''),
                        'targets': self._extract_bugcrowd_targets(program_data),
                        'bounty_range': program_data.get('max_payout', 'Unknown'),
                        'launched_at': program_data.get('launched_at'),
                        'updated_at': program_data.get('updated_at'),
                        'accepts_submissions': program_data.get('accepts_submissions', False)
                    }
                    programs.append(program)
                    
        except Exception as e:
            print(f"Bugcrowd fetch error: {e}")
        
        return programs
    
    def _fetch_intigriti_programs(self, config: Dict) -> List[Dict]:
        """Fetch Intigriti programs"""
        programs = []
        
        try:
            response = self.session.get(
                config['api_base'],
                headers=config['headers'],
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                for program_data in data:
                    program = {
                        'name': program_data.get('companyHandle', ''),
                        'handle': program_data.get('handle', ''),
                        'url': f"https://intigriti.com/programs/{program_data.get('companyHandle')}/{program_data.get('handle')}",
                        'targets': self._extract_intigriti_targets(program_data),
                        'bounty_range': program_data.get('maxBounty', 'Unknown'),
                        'launched_at': program_data.get('createdAt'),
                        'updated_at': program_data.get('updatedAt'),
                        'status': program_data.get('status')
                    }
                    programs.append(program)
                    
        except Exception as e:
            print(f"Intigriti fetch error: {e}")
        
        return programs
    
    def fetch_recent_vulnerability_reports(self, days_back: int = 7) -> List[Dict]:
        """Fetch recent vulnerability reports to identify trending vulnerabilities"""
        print("📊 Analyzing recent vulnerability reports...")
        
        reports = []
        
        # Fetch from public disclosure sources
        sources = [
            self._fetch_hacktivity_reports,
            self._fetch_cve_reports,
            self._fetch_security_advisories
        ]
        
        for source_func in sources:
            try:
                source_reports = source_func(days_back)
                reports.extend(source_reports)
                time.sleep(1)
            except Exception as e:
                print(f"   ⚠️  Error fetching reports: {e}")
        
        self.recent_reports = reports
        print(f"✅ Analyzed {len(reports)} recent vulnerability reports")
        return reports
    
    def _fetch_hacktivity_reports(self, days_back: int) -> List[Dict]:
        """Fetch recent HackerOne Hacktivity reports"""
        reports = []
        
        try:
            # HackerOne Hacktivity API (public reports)
            url = "https://hackerone.com/hacktivity.json"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                for report in data.get('reports', []):
                    if self._is_recent_report(report, days_back):
                        vulnerability_info = {
                            'title': report.get('title', ''),
                            'vulnerability_types': report.get('vulnerability_types', []),
                            'disclosed_at': report.get('disclosed_at'),
                            'bounty_amount': report.get('total_awarded_amount'),
                            'program': report.get('team', {}).get('handle', ''),
                            'platform': 'hackerone'
                        }
                        reports.append(vulnerability_info)
                        
        except Exception as e:
            print(f"Hacktivity fetch error: {e}")
        
        return reports
    
    def _fetch_cve_reports(self, days_back: int) -> List[Dict]:
        """Fetch recent CVE reports"""
        reports = []
        
        try:
            # NVD API for recent CVEs
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            url = f"https://services.nvd.nist.gov/rest/json/cves/2.0"
            params = {
                'pubStartDate': start_date.strftime('%Y-%m-%dT%H:%M:%S.000'),
                'pubEndDate': end_date.strftime('%Y-%m-%dT%H:%M:%S.000'),
                'resultsPerPage': 100
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                for cve in data.get('vulnerabilities', []):
                    cve_data = cve.get('cve', {})
                    vulnerability_info = {
                        'title': cve_data.get('id', ''),
                        'description': self._extract_cve_description(cve_data),
                        'severity': self._extract_cve_severity(cve_data),
                        'published_date': cve_data.get('published'),
                        'platform': 'nvd'
                    }
                    reports.append(vulnerability_info)
                    
        except Exception as e:
            print(f"CVE fetch error: {e}")
        
        return reports
    
    def _fetch_security_advisories(self, days_back: int) -> List[Dict]:
        """Fetch recent security advisories"""
        reports = []
        
        # This would fetch from various security advisory sources
        # For now, return empty list as a placeholder
        return reports
    
    def analyze_vulnerability_trends(self) -> Dict[str, float]:
        """Analyze recent vulnerability reports to identify trending vulnerability types"""
        print("📈 Analyzing vulnerability trends...")
        
        if not self.recent_reports:
            self.fetch_recent_vulnerability_reports()
        
        trend_scores = {}
        
        for pattern_name, pattern_config in self.vulnerability_patterns.items():
            score = 0
            keywords = pattern_config['keywords']
            
            for report in self.recent_reports:
                report_text = f"{report.get('title', '')} {report.get('description', '')}".lower()
                
                # Count keyword matches
                keyword_matches = sum(1 for keyword in keywords if keyword in report_text)
                
                if keyword_matches > 0:
                    # Weight by bounty amount if available
                    bounty_weight = 1
                    if report.get('bounty_amount'):
                        try:
                            bounty_weight = min(float(report['bounty_amount']) / 1000, 10)
                        except:
                            bounty_weight = 1
                    
                    score += keyword_matches * bounty_weight * pattern_config['confidence']
            
            trend_scores[pattern_name] = score
        
        # Normalize scores
        max_score = max(trend_scores.values()) if trend_scores.values() else 1
        normalized_scores = {k: v / max_score for k, v in trend_scores.items()}
        
        print("✅ Vulnerability trend analysis complete")
        return normalized_scores
    
    def suggest_targets(self, programs: List[Dict], trend_scores: Dict[str, float]) -> List[Dict]:
        """Suggest targets based on programs and vulnerability trends"""
        print("🎯 Generating target suggestions...")
        
        suggestions = []
        
        for program in programs:
            if not program.get('targets'):
                continue
            
            program_score = self._calculate_program_score(program, trend_scores)
            
            for target in program.get('targets', []):
                target_suggestion = {
                    'program_name': program.get('name', ''),
                    'program_handle': program.get('handle', ''),
                    'platform': program.get('platform', ''),
                    'target_url': target.get('asset_identifier', target.get('endpoint', '')),
                    'target_type': target.get('asset_type', 'web'),
                    'program_score': program_score,
                    'bounty_range': program.get('bounty_range', 'Unknown'),
                    'recommended_scans': self._recommend_scans(target, trend_scores),
                    'vulnerability_potential': self._assess_vulnerability_potential(target, trend_scores),
                    'program_url': program.get('url', ''),
                    'last_updated': program.get('updated_at', ''),
                    'accepts_submissions': program.get('submission_state') == 'open' or program.get('accepts_submissions', False)
                }
                
                # Only suggest if target accepts submissions and has decent score
                if target_suggestion['accepts_submissions'] and program_score > 0.3:
                    suggestions.append(target_suggestion)
        
        # Sort by score and potential
        suggestions.sort(key=lambda x: (x['program_score'] + x['vulnerability_potential']), reverse=True)
        
        self.target_suggestions = suggestions[:50]  # Top 50 suggestions
        print(f"✅ Generated {len(self.target_suggestions)} target suggestions")
        return self.target_suggestions
    
    def _calculate_program_score(self, program: Dict, trend_scores: Dict[str, float]) -> float:
        """Calculate a score for a bug bounty program"""
        score = 0
        
        # Base score for offering bounties
        if program.get('offers_bounties') or program.get('accepts_submissions'):
            score += 0.5
        
        # Score based on bounty range
        bounty_range = str(program.get('bounty_range', '')).lower()
        if 'critical' in bounty_range or any(x in bounty_range for x in ['10000', '20000', '50000']):
            score += 0.3
        elif any(x in bounty_range for x in ['5000', '1000']):
            score += 0.2
        
        # Score based on recent activity
        if program.get('updated_at'):
            try:
                updated_date = datetime.fromisoformat(program['updated_at'].replace('Z', '+00:00'))
                days_since_update = (datetime.now() - updated_date.replace(tzinfo=None)).days
                if days_since_update < 30:
                    score += 0.2
            except:
                pass
        
        # Score based on program maturity (newer programs might have more low-hanging fruit)
        if program.get('launched_at'):
            try:
                launch_date = datetime.fromisoformat(program['launched_at'].replace('Z', '+00:00'))
                days_since_launch = (datetime.now() - launch_date.replace(tzinfo=None)).days
                if days_since_launch < 90:  # New programs
                    score += 0.3
                elif days_since_launch < 365:  # Relatively new
                    score += 0.1
            except:
                pass
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _recommend_scans(self, target: Dict, trend_scores: Dict[str, float]) -> List[str]:
        """Recommend specific scans for a target based on trends"""
        recommendations = []
        
        target_url = target.get('asset_identifier', target.get('endpoint', ''))
        target_type = target.get('asset_type', 'web')
        
        # Always recommend basic scans
        recommendations.extend(['directory_fuzzing', 'subdomain_enumeration'])
        
        # Add trend-based recommendations
        sorted_trends = sorted(trend_scores.items(), key=lambda x: x[1], reverse=True)
        
        for trend_name, score in sorted_trends[:3]:  # Top 3 trending vulnerabilities
            if score > 0.5:  # Only if significantly trending
                pattern_config = self.vulnerability_patterns.get(trend_name, {})
                scanner_modules = pattern_config.get('scanner_modules', [])
                recommendations.extend(scanner_modules)
        
        # Target-specific recommendations
        if 'api' in target_url.lower():
            recommendations.extend(['parameter_fuzzing', 'jwt_analysis'])
        
        if target_type == 'web':
            recommendations.extend(['admin_panel_discovery', 'xss_testing'])
        
        return list(set(recommendations))  # Remove duplicates
    
    def _assess_vulnerability_potential(self, target: Dict, trend_scores: Dict[str, float]) -> float:
        """Assess the vulnerability potential of a target"""
        potential = 0
        
        target_url = target.get('asset_identifier', target.get('endpoint', ''))
        
        # Higher potential for certain domains/technologies
        high_potential_indicators = [
            'admin', 'api', 'test', 'dev', 'staging', 'beta',
            'internal', 'private', 'secure', 'auth', 'login'
        ]
        
        for indicator in high_potential_indicators:
            if indicator in target_url.lower():
                potential += 0.1
        
        # Technology-based potential
        if any(tech in target_url.lower() for tech in ['php', 'asp', 'jsp']):
            potential += 0.1
        
        # Subdomain potential
        parsed_url = urlparse(target_url if target_url.startswith('http') else f'http://{target_url}')
        if parsed_url.hostname and len(parsed_url.hostname.split('.')) > 2:
            potential += 0.1
        
        # Trend-based potential
        avg_trend_score = sum(trend_scores.values()) / len(trend_scores) if trend_scores else 0
        potential += avg_trend_score * 0.3
        
        return min(potential, 1.0)  # Cap at 1.0
    
    def auto_scan_suggestions(self, max_targets: int = 10) -> List[Dict]:
        """Get top targets for automated scanning"""
        if not self.target_suggestions:
            # Fetch fresh data
            programs = self.fetch_recent_programs()
            trends = self.analyze_vulnerability_trends()
            self.suggest_targets(programs, trends)
        
        # Return top targets suitable for automated scanning
        auto_scan_targets = []
        
        for suggestion in self.target_suggestions[:max_targets]:
            if suggestion['vulnerability_potential'] > 0.5 and suggestion['program_score'] > 0.4:
                auto_scan_targets.append({
                    'target_url': suggestion['target_url'],
                    'program_name': suggestion['program_name'],
                    'platform': suggestion['platform'],
                    'recommended_scans': suggestion['recommended_scans'],
                    'priority_score': suggestion['program_score'] + suggestion['vulnerability_potential'],
                    'bounty_range': suggestion['bounty_range']
                })
        
        return auto_scan_targets
    
    def generate_intelligence_report(self) -> Dict:
        """Generate a comprehensive intelligence report"""
        if not self.target_suggestions:
            programs = self.fetch_recent_programs()
            trends = self.analyze_vulnerability_trends()
            self.suggest_targets(programs, trends)
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_programs_analyzed': len([s['program_name'] for s in self.target_suggestions]),
                'total_targets_found': len(self.target_suggestions),
                'high_priority_targets': len([s for s in self.target_suggestions if s['vulnerability_potential'] > 0.7]),
                'trending_vulnerabilities': self.analyze_vulnerability_trends()
            },
            'top_targets': self.target_suggestions[:20],
            'auto_scan_ready': self.auto_scan_suggestions(),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if not self.target_suggestions:
            return ["Run intelligence gathering first to get recommendations"]
        
        # Analyze top targets
        top_targets = self.target_suggestions[:10]
        
        # Platform recommendations
        platforms = {}
        for target in top_targets:
            platform = target['platform']
            platforms[platform] = platforms.get(platform, 0) + 1
        
        top_platform = max(platforms.items(), key=lambda x: x[1])[0] if platforms else None
        if top_platform:
            recommendations.append(f"Focus on {top_platform.title()} programs - highest target concentration")
        
        # Vulnerability type recommendations
        all_scans = []
        for target in top_targets:
            all_scans.extend(target['recommended_scans'])
        
        scan_counts = {}
        for scan in all_scans:
            scan_counts[scan] = scan_counts.get(scan, 0) + 1
        
        top_scans = sorted(scan_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        for scan, count in top_scans:
            recommendations.append(f"Prioritize {scan.replace('_', ' ')} - appears in {count} target recommendations")
        
        # Timing recommendations
        new_programs = [t for t in top_targets if 'new' in str(t.get('last_updated', '')).lower()]
        if new_programs:
            recommendations.append(f"Target {len(new_programs)} recently launched programs for potential low-hanging fruit")
        
        return recommendations
    
    # Helper methods
    def _extract_targets(self, targets_data) -> List[Dict]:
        """Extract target information from program data"""
        targets = []
        
        if isinstance(targets_data, dict):
            for target_type, target_list in targets_data.items():
                if isinstance(target_list, list):
                    for target in target_list:
                        targets.append({
                            'asset_type': target_type,
                            'asset_identifier': target.get('asset_identifier', ''),
                            'eligible_for_bounty': target.get('eligible_for_bounty', False)
                        })
        
        return targets
    
    def _extract_bounty_range(self, program_data) -> str:
        """Extract bounty range from program data"""
        if program_data.get('offers_bounties'):
            return f"${program_data.get('min_bounty', 0)} - ${program_data.get('max_bounty', 'Unknown')}"
        return "No bounty"
    
    def _extract_bugcrowd_targets(self, program_data) -> List[Dict]:
        """Extract Bugcrowd target information"""
        targets = []
        target_groups = program_data.get('target_groups', [])
        
        for group in target_groups:
            for target in group.get('targets', []):
                targets.append({
                    'asset_type': target.get('category', 'web'),
                    'asset_identifier': target.get('name', ''),
                    'eligible_for_bounty': True
                })
        
        return targets
    
    def _extract_intigriti_targets(self, program_data) -> List[Dict]:
        """Extract Intigriti target information"""
        targets = []
        domains = program_data.get('domains', [])
        
        for domain in domains:
            targets.append({
                'asset_type': 'web',
                'asset_identifier': domain.get('endpoint', ''),
                'eligible_for_bounty': domain.get('bounty', False)
            })
        
        return targets
    
    def _is_recent_program(self, program: Dict, cutoff_date: datetime) -> bool:
        """Check if a program is recent"""
        date_fields = ['launched_at', 'updated_at', 'createdAt', 'updatedAt']
        
        for field in date_fields:
            if program.get(field):
                try:
                    program_date = datetime.fromisoformat(program[field].replace('Z', '+00:00'))
                    if program_date.replace(tzinfo=None) > cutoff_date:
                        return True
                except:
                    continue
        
        return False
    
    def _is_recent_report(self, report: Dict, days_back: int) -> bool:
        """Check if a vulnerability report is recent"""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        date_fields = ['disclosed_at', 'published_date', 'published']
        
        for field in date_fields:
            if report.get(field):
                try:
                    report_date = datetime.fromisoformat(report[field].replace('Z', '+00:00'))
                    return report_date.replace(tzinfo=None) > cutoff_date
                except:
                    continue
        
        return False
    
    def _extract_cve_description(self, cve_data: Dict) -> str:
        """Extract CVE description"""
        descriptions = cve_data.get('descriptions', [])
        for desc in descriptions:
            if desc.get('lang') == 'en':
                return desc.get('value', '')
        return ''
    
    def _extract_cve_severity(self, cve_data: Dict) -> str:
        """Extract CVE severity"""
        metrics = cve_data.get('metrics', {})
        cvss_v3 = metrics.get('cvssMetricV31', [])
        
        if cvss_v3:
            return cvss_v3[0].get('cvssData', {}).get('baseSeverity', 'Unknown')
        
        return 'Unknown'