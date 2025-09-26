"""
Bug Bounty Reporter - Professional report generation for bug bounty submissions
Generates comprehensive, professional reports with exploitation proofs
"""

import json
import time
import os
import base64
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal

class BugBountyReporter(QObject):
    report_generated = pyqtSignal(str, dict)  # report_path, report_data
    log_message = pyqtSignal(str, str)
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.reports_dir = "reports"
        self.ensure_reports_directory()
    
    def ensure_reports_directory(self):
        """Ensure reports directory exists"""
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(f"{self.reports_dir}/html", exist_ok=True)
        os.makedirs(f"{self.reports_dir}/json", exist_ok=True)
        os.makedirs(f"{self.reports_dir}/markdown", exist_ok=True)
    
    def generate_comprehensive_report(self, scan_data, vulnerabilities, exploitations, logins):
        """Generate comprehensive bug bounty report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_id = f"BBH_{timestamp}"
        
        # Compile all data
        report_data = {
            'report_metadata': {
                'report_id': report_id,
                'generated_at': datetime.now().isoformat(),
                'target_url': scan_data.get('target_url', 'Unknown'),
                'scan_duration': scan_data.get('scan_duration', 0),
                'scanner_version': '2.0.0-ADVANCED',
                'report_type': 'Professional Bug Bounty Submission'
            },
            'executive_summary': self._generate_executive_summary(vulnerabilities, exploitations, logins),
            'vulnerability_details': self._process_vulnerabilities(vulnerabilities),
            'exploitation_proofs': self._process_exploitations(exploitations),
            'credential_discoveries': self._process_login_successes(logins),
            'impact_assessment': self._generate_impact_assessment(vulnerabilities, exploitations),
            'remediation_roadmap': self._generate_remediation_roadmap(vulnerabilities),
            'technical_appendix': self._generate_technical_appendix(scan_data)
        }
        
        # Generate multiple report formats
        reports_generated = {}
        
        # JSON Report (for automation/integration)
        json_path = self._generate_json_report(report_data, report_id)
        reports_generated['json'] = json_path
        
        # HTML Report (for presentation)
        html_path = self._generate_html_report(report_data, report_id)
        reports_generated['html'] = html_path
        
        # Markdown Report (for GitHub/documentation)
        md_path = self._generate_markdown_report(report_data, report_id)
        reports_generated['markdown'] = md_path
        
        self.log_message.emit(f"📄 Comprehensive report generated: {report_id}", "success")
        self.report_generated.emit(report_id, reports_generated)
        
        return reports_generated
    
    def _generate_executive_summary(self, vulnerabilities, exploitations, logins):
        """Generate executive summary"""
        total_vulns = len(vulnerabilities)
        critical_vulns = len([v for v in vulnerabilities if v.get('severity') == 'Critical'])
        high_vulns = len([v for v in vulnerabilities if v.get('severity') == 'High'])
        successful_exploits = len([e for e in exploitations if e.get('exploitation_successful')])
        successful_logins = len(logins)
        
        risk_level = "CRITICAL" if critical_vulns > 0 else "HIGH" if high_vulns > 0 else "MEDIUM"
        
        return {
            'total_vulnerabilities': total_vulns,
            'critical_vulnerabilities': critical_vulns,
            'high_vulnerabilities': high_vulns,
            'successful_exploitations': successful_exploits,
            'credential_compromises': successful_logins,
            'overall_risk_level': risk_level,
            'key_findings': self._generate_key_findings(vulnerabilities, exploitations, logins),
            'business_impact': self._assess_business_impact(vulnerabilities, exploitations),
            'immediate_actions': self._generate_immediate_actions(critical_vulns, successful_exploits)
        }
    
    def _generate_key_findings(self, vulnerabilities, exploitations, logins):
        """Generate key findings summary"""
        findings = []
        
        # Critical vulnerabilities
        critical_vulns = [v for v in vulnerabilities if v.get('severity') == 'Critical']
        if critical_vulns:
            findings.append(f"🚨 {len(critical_vulns)} CRITICAL vulnerabilities discovered with immediate exploitation risk")
        
        # Successful exploitations
        successful_exploits = [e for e in exploitations if e.get('exploitation_successful')]
        if successful_exploits:
            findings.append(f"💥 {len(successful_exploits)} vulnerabilities successfully exploited with concrete proof")
        
        # Credential compromises
        if logins:
            findings.append(f"🔓 {len(logins)} admin/user accounts compromised with working credentials")
        
        # Data extraction
        data_extractions = sum(len(e.get('data_extracted', [])) for e in exploitations)
        if data_extractions:
            findings.append(f"📊 {data_extractions} sensitive data items successfully extracted")
        
        # Shell access
        shell_access = sum(len(e.get('shells_obtained', [])) for e in exploitations)
        if shell_access:
            findings.append(f"🐚 {shell_access} remote shell access points established")
        
        return findings
    
    def _assess_business_impact(self, vulnerabilities, exploitations):
        """Assess business impact"""
        impacts = []
        
        # Check for data breach potential
        sql_injections = [v for v in vulnerabilities if 'sql injection' in v.get('type', '').lower()]
        if sql_injections:
            impacts.append("💾 DATABASE COMPROMISE: Complete database access possible leading to data breach")
        
        # Check for system compromise
        rce_vulns = [v for v in vulnerabilities if any(term in v.get('type', '').lower() for term in ['rce', 'command injection'])]
        if rce_vulns:
            impacts.append("🖥️ SYSTEM COMPROMISE: Complete server takeover possible")
        
        # Check for admin access
        admin_vulns = [v for v in vulnerabilities if 'admin' in v.get('type', '').lower()]
        if admin_vulns:
            impacts.append("👑 ADMINISTRATIVE ACCESS: Complete application control achieved")
        
        # Check for user data exposure
        xss_vulns = [v for v in vulnerabilities if 'xss' in v.get('type', '').lower()]
        if xss_vulns:
            impacts.append("👥 USER COMPROMISE: User session hijacking and credential theft possible")
        
        return impacts
    
    def _generate_immediate_actions(self, critical_count, exploit_count):
        """Generate immediate action items"""
        actions = []
        
        if critical_count > 0:
            actions.append("🚨 IMMEDIATE: Patch all critical vulnerabilities within 24 hours")
        
        if exploit_count > 0:
            actions.append("🔒 URGENT: Implement emergency security controls to prevent active exploitation")
        
        actions.extend([
            "🛡️ Deploy Web Application Firewall (WAF) with strict rules",
            "📊 Implement security monitoring and alerting",
            "🔍 Conduct comprehensive security audit",
            "👨‍💻 Provide emergency security training to development team"
        ])
        
        return actions
    
    def _process_vulnerabilities(self, vulnerabilities):
        """Process and enhance vulnerability data"""
        processed = []
        
        for i, vuln in enumerate(vulnerabilities, 1):
            processed_vuln = {
                'id': f"VULN-{i:03d}",
                'title': vuln.get('type', 'Unknown Vulnerability'),
                'severity': vuln.get('severity', 'Unknown'),
                'url': vuln.get('url', ''),
                'description': vuln.get('description', ''),
                'impact': vuln.get('impact', ''),
                'cvss_score': self._calculate_cvss_score(vuln),
                'cwe_classification': self._get_cwe_classification(vuln.get('type', '')),
                'exploitation_difficulty': self._assess_exploitation_difficulty(vuln),
                'remediation_effort': self._assess_remediation_effort(vuln),
                'proof_of_concept': vuln.get('proof', ''),
                'technical_details': vuln.get('technical_details', {}),
                'references': self._get_vulnerability_references(vuln.get('type', ''))
            }
            processed.append(processed_vuln)
        
        return processed
    
    def _calculate_cvss_score(self, vulnerability):
        """Calculate CVSS score based on vulnerability details"""
        severity_scores = {
            'Critical': {'score': 9.5, 'vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H'},
            'High': {'score': 8.2, 'vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:L'},
            'Medium': {'score': 6.1, 'vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N'},
            'Low': {'score': 3.7, 'vector': 'CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N'}
        }
        
        return severity_scores.get(vulnerability.get('severity', 'Low'), severity_scores['Low'])
    
    def _get_cwe_classification(self, vuln_type):
        """Get CWE classification for vulnerability type"""
        cwe_mappings = {
            'sql injection': 'CWE-89: SQL Injection',
            'xss': 'CWE-79: Cross-site Scripting',
            'cross-site scripting': 'CWE-79: Cross-site Scripting',
            'command injection': 'CWE-78: OS Command Injection',
            'rce': 'CWE-78: OS Command Injection',
            'lfi': 'CWE-22: Path Traversal',
            'local file inclusion': 'CWE-22: Path Traversal',
            'admin panel exposed': 'CWE-200: Information Exposure',
            'jwt weak secret': 'CWE-326: Inadequate Encryption Strength',
            'open redirect': 'CWE-601: URL Redirection to Untrusted Site'
        }
        
        return cwe_mappings.get(vuln_type.lower(), 'CWE-Other: Security Vulnerability')
    
    def _assess_exploitation_difficulty(self, vulnerability):
        """Assess how difficult the vulnerability is to exploit"""
        vuln_type = vulnerability.get('type', '').lower()
        
        if any(term in vuln_type for term in ['sql injection', 'rce', 'command injection']):
            return 'Easy - Automated tools available'
        elif any(term in vuln_type for term in ['xss', 'lfi']):
            return 'Moderate - Requires some technical knowledge'
        else:
            return 'Variable - Depends on specific implementation'
    
    def _assess_remediation_effort(self, vulnerability):
        """Assess remediation effort required"""
        vuln_type = vulnerability.get('type', '').lower()
        
        if any(term in vuln_type for term in ['sql injection', 'xss']):
            return 'Medium - Code changes and testing required'
        elif any(term in vuln_type for term in ['rce', 'command injection']):
            return 'High - Significant architecture changes needed'
        elif 'admin panel' in vuln_type:
            return 'Low - Configuration changes only'
        else:
            return 'Medium - Standard security fixes'
    
    def _get_vulnerability_references(self, vuln_type):
        """Get relevant references for vulnerability type"""
        references = {
            'sql injection': [
                'https://owasp.org/www-community/attacks/SQL_Injection',
                'https://cwe.mitre.org/data/definitions/89.html',
                'https://portswigger.net/web-security/sql-injection'
            ],
            'xss': [
                'https://owasp.org/www-community/attacks/xss/',
                'https://cwe.mitre.org/data/definitions/79.html',
                'https://portswigger.net/web-security/cross-site-scripting'
            ],
            'command injection': [
                'https://owasp.org/www-community/attacks/Command_Injection',
                'https://cwe.mitre.org/data/definitions/78.html',
                'https://portswigger.net/web-security/os-command-injection'
            ]
        }
        
        return references.get(vuln_type.lower(), [
            'https://owasp.org/www-project-top-ten/',
            'https://cwe.mitre.org/'
        ])
    
    def _process_exploitations(self, exploitations):
        """Process exploitation data"""
        processed = []
        
        for i, exploit in enumerate(exploitations, 1):
            if exploit.get('exploitation_successful'):
                processed_exploit = {
                    'id': f"EXPLOIT-{i:03d}",
                    'vulnerability_type': exploit.get('vulnerability', {}).get('type', 'Unknown'),
                    'target_url': exploit.get('vulnerability', {}).get('url', ''),
                    'exploitation_method': self._describe_exploitation_method(exploit),
                    'data_extracted': len(exploit.get('data_extracted', [])),
                    'shells_obtained': len(exploit.get('shells_obtained', [])),
                    'proof_of_concept': exploit.get('proof_of_concept', []),
                    'impact_demonstration': self._generate_impact_demonstration(exploit),
                    'exploitation_timestamp': exploit.get('timestamp', ''),
                    'technical_details': exploit
                }
                processed.append(processed_exploit)
        
        return processed
    
    def _describe_exploitation_method(self, exploit):
        """Describe the exploitation method used"""
        vuln_type = exploit.get('vulnerability', {}).get('type', '').lower()
        
        if 'sql injection' in vuln_type:
            return "Automated SQL injection with union-based and time-based techniques"
        elif 'xss' in vuln_type:
            return "Cross-site scripting payload injection and execution"
        elif 'rce' in vuln_type or 'command injection' in vuln_type:
            return "Remote command execution via parameter manipulation"
        elif 'admin panel' in vuln_type:
            return "Credential brute force and administrative access"
        else:
            return "Custom exploitation technique based on vulnerability type"
    
    def _generate_impact_demonstration(self, exploit):
        """Generate impact demonstration text"""
        impacts = []
        
        if exploit.get('data_extracted'):
            impacts.append(f"✅ Successfully extracted {len(exploit['data_extracted'])} sensitive data items")
        
        if exploit.get('shells_obtained'):
            impacts.append(f"✅ Established {len(exploit['shells_obtained'])} remote shell connections")
        
        if exploit.get('proof_of_concept'):
            impacts.append(f"✅ Executed {len(exploit['proof_of_concept'])} proof-of-concept demonstrations")
        
        return impacts
    
    def _process_login_successes(self, logins):
        """Process successful login attempts"""
        processed = []
        
        for i, login in enumerate(logins, 1):
            processed_login = {
                'id': f"LOGIN-{i:03d}",
                'url': login.get('url', ''),
                'credentials': login.get('credentials', ''),
                'access_level': login.get('access_level', 'Unknown'),
                'timestamp': login.get('timestamp', ''),
                'session_data': login.get('session_data', {}),
                'impact': 'Complete administrative access to application',
                'risk_level': 'CRITICAL'
            }
            processed.append(processed_login)
        
        return processed
    
    def _generate_impact_assessment(self, vulnerabilities, exploitations):
        """Generate comprehensive impact assessment"""
        return {
            'confidentiality_impact': self._assess_confidentiality_impact(vulnerabilities, exploitations),
            'integrity_impact': self._assess_integrity_impact(vulnerabilities, exploitations),
            'availability_impact': self._assess_availability_impact(vulnerabilities, exploitations),
            'business_continuity_risk': self._assess_business_continuity_risk(vulnerabilities),
            'compliance_implications': self._assess_compliance_implications(vulnerabilities),
            'reputation_risk': self._assess_reputation_risk(vulnerabilities, exploitations)
        }
    
    def _assess_confidentiality_impact(self, vulnerabilities, exploitations):
        """Assess confidentiality impact"""
        sql_vulns = [v for v in vulnerabilities if 'sql injection' in v.get('type', '').lower()]
        lfi_vulns = [v for v in vulnerabilities if 'lfi' in v.get('type', '').lower()]
        
        if sql_vulns or lfi_vulns:
            return "HIGH - Complete database and file system access possible"
        else:
            return "MEDIUM - Limited data exposure possible"
    
    def _assess_integrity_impact(self, vulnerabilities, exploitations):
        """Assess integrity impact"""
        rce_vulns = [v for v in vulnerabilities if any(term in v.get('type', '').lower() for term in ['rce', 'command injection'])]
        sql_vulns = [v for v in vulnerabilities if 'sql injection' in v.get('type', '').lower()]
        
        if rce_vulns:
            return "HIGH - Complete system modification possible"
        elif sql_vulns:
            return "HIGH - Database modification possible"
        else:
            return "MEDIUM - Limited data modification possible"
    
    def _assess_availability_impact(self, vulnerabilities, exploitations):
        """Assess availability impact"""
        rce_vulns = [v for v in vulnerabilities if any(term in v.get('type', '').lower() for term in ['rce', 'command injection'])]
        
        if rce_vulns:
            return "HIGH - Complete system shutdown possible"
        else:
            return "LOW - Limited service disruption possible"
    
    def _assess_business_continuity_risk(self, vulnerabilities):
        """Assess business continuity risk"""
        critical_count = len([v for v in vulnerabilities if v.get('severity') == 'Critical'])
        
        if critical_count >= 3:
            return "SEVERE - Multiple critical vulnerabilities pose significant business risk"
        elif critical_count > 0:
            return "HIGH - Critical vulnerabilities require immediate attention"
        else:
            return "MODERATE - Vulnerabilities should be addressed in planned maintenance"
    
    def _assess_compliance_implications(self, vulnerabilities):
        """Assess compliance implications"""
        implications = []
        
        sql_vulns = [v for v in vulnerabilities if 'sql injection' in v.get('type', '').lower()]
        if sql_vulns:
            implications.append("PCI DSS: Data protection requirements violated")
            implications.append("GDPR: Personal data protection at risk")
        
        admin_vulns = [v for v in vulnerabilities if 'admin' in v.get('type', '').lower()]
        if admin_vulns:
            implications.append("SOX: Access control requirements not met")
        
        return implications if implications else ["No immediate compliance violations identified"]
    
    def _assess_reputation_risk(self, vulnerabilities, exploitations):
        """Assess reputation risk"""
        successful_exploits = [e for e in exploitations if e.get('exploitation_successful')]
        
        if successful_exploits:
            return "HIGH - Successful exploitation demonstrates real security breach potential"
        elif any(v.get('severity') == 'Critical' for v in vulnerabilities):
            return "MEDIUM - Critical vulnerabilities could lead to public security incidents"
        else:
            return "LOW - Standard security issues with limited public impact"
    
    def _generate_remediation_roadmap(self, vulnerabilities):
        """Generate remediation roadmap"""
        roadmap = {
            'immediate_actions': [],
            'short_term_goals': [],
            'long_term_strategy': []
        }
        
        # Immediate actions (0-7 days)
        critical_vulns = [v for v in vulnerabilities if v.get('severity') == 'Critical']
        if critical_vulns:
            roadmap['immediate_actions'].extend([
                "🚨 Patch all critical vulnerabilities within 24-48 hours",
                "🛡️ Deploy emergency WAF rules to block exploitation attempts",
                "📊 Implement emergency monitoring for attack attempts"
            ])
        
        # Short-term goals (1-4 weeks)
        roadmap['short_term_goals'].extend([
            "🔍 Conduct comprehensive code review",
            "🧪 Implement automated security testing",
            "👨‍💻 Provide security training to development team",
            "📋 Establish security incident response procedures"
        ])
        
        # Long-term strategy (1-6 months)
        roadmap['long_term_strategy'].extend([
            "🏗️ Implement secure development lifecycle (SDLC)",
            "🔄 Establish regular penetration testing schedule",
            "📊 Deploy comprehensive security monitoring solution",
            "🎓 Create ongoing security awareness program"
        ])
        
        return roadmap
    
    def _generate_technical_appendix(self, scan_data):
        """Generate technical appendix"""
        return {
            'scan_configuration': {
                'target_url': scan_data.get('target_url', 'Unknown'),
                'scan_duration': scan_data.get('scan_duration', 0),
                'threads_used': scan_data.get('threads', 10),
                'timeout_settings': scan_data.get('timeout', 30),
                'wordlists_used': scan_data.get('wordlists', {}),
                'scan_modules': [
                    'Directory Fuzzing',
                    'Subdomain Enumeration',
                    'Parameter Discovery',
                    'Admin Panel Detection',
                    'JWT Analysis',
                    'Vulnerability Validation',
                    'Automated Exploitation'
                ]
            },
            'methodology': [
                "1. Reconnaissance and target analysis",
                "2. Automated vulnerability discovery",
                "3. Manual verification and validation",
                "4. Exploitation and proof-of-concept development",
                "5. Impact assessment and documentation"
            ],
            'tools_used': [
                "Bug Bounty Hunter Pro v2.0",
                "Custom vulnerability validators",
                "Automated exploitation engine",
                "Professional report generator"
            ]
        }
    
    def _generate_json_report(self, report_data, report_id):
        """Generate JSON report"""
        json_path = f"{self.reports_dir}/json/{report_id}.json"
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        self.log_message.emit(f"📄 JSON report saved: {json_path}", "success")
        return json_path
    
    def _generate_html_report(self, report_data, report_id):
        """Generate HTML report"""
        html_path = f"{self.reports_dir}/html/{report_id}.html"
        
        html_content = self._create_html_template(report_data)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.log_message.emit(f"🌐 HTML report saved: {html_path}", "success")
        return html_path
    
    def _create_html_template(self, data):
        """Create HTML report template"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bug Bounty Report - {data['report_metadata']['report_id']}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; border-bottom: 3px solid #e74c3c; padding-bottom: 20px; margin-bottom: 30px; }}
        .title {{ color: #e74c3c; font-size: 2.5em; margin: 0; }}
        .subtitle {{ color: #666; font-size: 1.2em; margin: 10px 0; }}
        .section {{ margin: 30px 0; }}
        .section-title {{ color: #2c3e50; font-size: 1.8em; border-left: 5px solid #3498db; padding-left: 15px; margin-bottom: 20px; }}
        .vulnerability {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin: 15px 0; }}
        .critical {{ border-left: 5px solid #e74c3c; }}
        .high {{ border-left: 5px solid #f39c12; }}
        .medium {{ border-left: 5px solid #f1c40f; }}
        .low {{ border-left: 5px solid #27ae60; }}
        .vuln-title {{ font-size: 1.3em; font-weight: bold; margin-bottom: 10px; }}
        .vuln-details {{ margin: 10px 0; }}
        .code {{ background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 4px; padding: 10px; font-family: monospace; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .summary-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
        .summary-number {{ font-size: 2em; font-weight: bold; color: #e74c3c; }}
        .summary-label {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🎯 Bug Bounty Security Report</h1>
            <p class="subtitle">Professional Vulnerability Assessment & Exploitation Report</p>
            <p><strong>Report ID:</strong> {data['report_metadata']['report_id']}</p>
            <p><strong>Generated:</strong> {data['report_metadata']['generated_at']}</p>
            <p><strong>Target:</strong> {data['report_metadata']['target_url']}</p>
        </div>
        
        <div class="section">
            <h2 class="section-title">📊 Executive Summary</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-number">{data['executive_summary']['total_vulnerabilities']}</div>
                    <div class="summary-label">Total Vulnerabilities</div>
                </div>
                <div class="summary-card">
                    <div class="summary-number">{data['executive_summary']['critical_vulnerabilities']}</div>
                    <div class="summary-label">Critical Issues</div>
                </div>
                <div class="summary-card">
                    <div class="summary-number">{data['executive_summary']['successful_exploitations']}</div>
                    <div class="summary-label">Successful Exploits</div>
                </div>
                <div class="summary-card">
                    <div class="summary-number">{data['executive_summary']['credential_compromises']}</div>
                    <div class="summary-label">Compromised Accounts</div>
                </div>
            </div>
            
            <h3>🔍 Key Findings</h3>
            <ul>
                {''.join(f'<li>{finding}</li>' for finding in data['executive_summary']['key_findings'])}
            </ul>
            
            <h3>💼 Business Impact</h3>
            <ul>
                {''.join(f'<li>{impact}</li>' for impact in data['executive_summary']['business_impact'])}
            </ul>
        </div>
        
        <div class="section">
            <h2 class="section-title">🚨 Vulnerability Details</h2>
            {''.join(self._format_vulnerability_html(vuln) for vuln in data['vulnerability_details'])}
        </div>
        
        <div class="section">
            <h2 class="section-title">💥 Exploitation Proofs</h2>
            {''.join(self._format_exploitation_html(exploit) for exploit in data['exploitation_proofs'])}
        </div>
        
        <div class="section">
            <h2 class="section-title">🔧 Remediation Roadmap</h2>
            <h3>🚨 Immediate Actions (0-7 days)</h3>
            <ul>
                {''.join(f'<li>{action}</li>' for action in data['remediation_roadmap']['immediate_actions'])}
            </ul>
            
            <h3>📅 Short-term Goals (1-4 weeks)</h3>
            <ul>
                {''.join(f'<li>{goal}</li>' for goal in data['remediation_roadmap']['short_term_goals'])}
            </ul>
            
            <h3>🎯 Long-term Strategy (1-6 months)</h3>
            <ul>
                {''.join(f'<li>{strategy}</li>' for strategy in data['remediation_roadmap']['long_term_strategy'])}
            </ul>
        </div>
    </div>
</body>
</html>
        """
    
    def _format_vulnerability_html(self, vuln):
        """Format vulnerability for HTML"""
        severity_class = vuln['severity'].lower()
        return f"""
        <div class="vulnerability {severity_class}">
            <div class="vuln-title">{vuln['title']} - {vuln['severity']}</div>
            <div class="vuln-details"><strong>URL:</strong> {vuln['url']}</div>
            <div class="vuln-details"><strong>CVSS Score:</strong> {vuln['cvss_score']['score']}</div>
            <div class="vuln-details"><strong>CWE:</strong> {vuln['cwe_classification']}</div>
            <div class="vuln-details"><strong>Description:</strong> {vuln['description']}</div>
            <div class="vuln-details"><strong>Impact:</strong> {vuln['impact']}</div>
            {f'<div class="code">{vuln["proof_of_concept"]}</div>' if vuln.get('proof_of_concept') else ''}
        </div>
        """
    
    def _format_exploitation_html(self, exploit):
        """Format exploitation for HTML"""
        return f"""
        <div class="vulnerability critical">
            <div class="vuln-title">💥 {exploit['vulnerability_type']} - EXPLOITED</div>
            <div class="vuln-details"><strong>Target:</strong> {exploit['target_url']}</div>
            <div class="vuln-details"><strong>Method:</strong> {exploit['exploitation_method']}</div>
            <div class="vuln-details"><strong>Data Extracted:</strong> {exploit['data_extracted']} items</div>
            <div class="vuln-details"><strong>Shells Obtained:</strong> {exploit['shells_obtained']}</div>
            <div class="vuln-details"><strong>Impact:</strong></div>
            <ul>
                {''.join(f'<li>{impact}</li>' for impact in exploit['impact_demonstration'])}
            </ul>
        </div>
        """
    
    def _generate_markdown_report(self, report_data, report_id):
        """Generate Markdown report"""
        md_path = f"{self.reports_dir}/markdown/{report_id}.md"
        
        md_content = self._create_markdown_template(report_data)
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        self.log_message.emit(f"📝 Markdown report saved: {md_path}", "success")
        return md_path
    
    def _create_markdown_template(self, data):
        """Create Markdown report template"""
        return f"""# 🎯 Bug Bounty Security Report

**Report ID:** {data['report_metadata']['report_id']}  
**Generated:** {data['report_metadata']['generated_at']}  
**Target:** {data['report_metadata']['target_url']}  
**Scanner:** {data['report_metadata']['scanner_version']}

## 📊 Executive Summary

| Metric | Count |
|--------|-------|
| Total Vulnerabilities | {data['executive_summary']['total_vulnerabilities']} |
| Critical Issues | {data['executive_summary']['critical_vulnerabilities']} |
| Successful Exploits | {data['executive_summary']['successful_exploitations']} |
| Compromised Accounts | {data['executive_summary']['credential_compromises']} |

**Overall Risk Level:** {data['executive_summary']['overall_risk_level']}

### 🔍 Key Findings

{''.join(f'- {finding}\\n' for finding in data['executive_summary']['key_findings'])}

### 💼 Business Impact

{''.join(f'- {impact}\\n' for impact in data['executive_summary']['business_impact'])}

## 🚨 Vulnerability Details

{''.join(self._format_vulnerability_markdown(vuln) for vuln in data['vulnerability_details'])}

## 💥 Exploitation Proofs

{''.join(self._format_exploitation_markdown(exploit) for exploit in data['exploitation_proofs'])}

## 🔧 Remediation Roadmap

### 🚨 Immediate Actions (0-7 days)

{''.join(f'- {action}\\n' for action in data['remediation_roadmap']['immediate_actions'])}

### 📅 Short-term Goals (1-4 weeks)

{''.join(f'- {goal}\\n' for goal in data['remediation_roadmap']['short_term_goals'])}

### 🎯 Long-term Strategy (1-6 months)

{''.join(f'- {strategy}\\n' for strategy in data['remediation_roadmap']['long_term_strategy'])}

---

*Report generated by Bug Bounty Hunter Pro v2.0 - Advanced Security Testing Platform*
"""
    
    def _format_vulnerability_markdown(self, vuln):
        """Format vulnerability for Markdown"""
        return f"""
### {vuln['id']}: {vuln['title']} - {vuln['severity']}

**URL:** {vuln['url']}  
**CVSS Score:** {vuln['cvss_score']['score']}  
**CWE:** {vuln['cwe_classification']}  

**Description:** {vuln['description']}

**Impact:** {vuln['impact']}

{'**Proof of Concept:**\\n```\\n' + vuln['proof_of_concept'] + '\\n```\\n' if vuln.get('proof_of_concept') else ''}

---
"""
    
    def _format_exploitation_markdown(self, exploit):
        """Format exploitation for Markdown"""
        return f"""
### {exploit['id']}: 💥 {exploit['vulnerability_type']} - EXPLOITED

**Target:** {exploit['target_url']}  
**Method:** {exploit['exploitation_method']}  
**Data Extracted:** {exploit['data_extracted']} items  
**Shells Obtained:** {exploit['shells_obtained']}  

**Impact Demonstration:**
{''.join(f'- {impact}\\n' for impact in exploit['impact_demonstration'])}

---
"""