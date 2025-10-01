"""
Lost Uncover - Advanced Tool to Uncover Hidden Elements on Web Pages
33X Enhanced: Automated analysis, comprehensive detection, security assessment
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, urljoin
import time

class LostUncover:
    def __init__(self):
        self.unhide_script = """
javascript:(function(){
document.querySelectorAll('[disabled],[readonly]').forEach(el=>{
    el.removeAttribute('disabled');
    el.removeAttribute('readonly');
});
document.querySelectorAll('[style*="display: none"]').forEach(el=>{
    el.style.display='block';
});
document.querySelectorAll('[style*="pointer-events: none"]').forEach(el=>{
    el.style.pointerEvents='auto';
    el.style.opacity='1';
});
alert('Disabled, readonly, and hidden elements are now active!');
})();
        """.strip()

    def get_bookmarklet(self):
        """Return the bookmarklet JavaScript code."""
        return self.unhide_script

    def generate_test_html(self):
        """Generate test HTML page to test the bookmarklet."""
        test_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Bookmarklet Test Page</title>
  <style>
    body {
      background-color: black;
      color: #00ff88;
      font-family: monospace;
      padding: 20px;
    }
    input, button {
      font-family: monospace;
      margin-top: 5px;
      margin-bottom: 20px;
      padding: 5px;
    }
    .hidden {
      display: none;
    }
    .grayed {
      pointer-events: none;
      opacity: 0.4;
    }
  </style>
</head>
<body>
  <h1>Bookmarklet Test Page</h1>

  <h2>Disabled Input</h2>
  <label>Email (Disabled):<br>
    <input type="text" value="you@nowhere.com123" disabled>
  </label>

  <h2>Readonly Input</h2>
  <label>Username (Readonly):<br>
    <input type="text" value="readonly_user123" readonly>
  </label>

  <h2>Hidden Button</h2>
  <button class="hidden" id="secret-btn">Secret Admin Button</button>

  <h2>Grayed-Out Section</h2>
  <div class="grayed">Premium Content</div>
</body>
</html>
        """
        return test_html.strip()

    def save_test_page(self, filename="test_page.html"):
        """Save the test HTML page to a file."""
        html_content = self.generate_test_html()
        with open(filename, 'w') as f:
            f.write(html_content)
        return filename

    def analyze_page_for_hidden_elements(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Automated analysis of web page for hidden elements and security issues
        33X Enhanced: Comprehensive detection, security assessment, vulnerability correlation
        """
        logging.info(f"Analyzing {url} for hidden elements")

        results = {
            "url": url,
            "analysis_time": time.time(),
            "hidden_elements": [],
            "disabled_elements": [],
            "readonly_elements": [],
            "security_findings": [],
            "potential_vulnerabilities": [],
            "recommendations": []
        }

        try:
            # Fetch the page
            response = requests.get(url, headers=headers, timeout=30, verify=False)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Analyze for hidden elements
            results["hidden_elements"] = self._find_hidden_elements(soup)
            results["disabled_elements"] = self._find_disabled_elements(soup)
            results["readonly_elements"] = self._find_readonly_elements(soup)

            # Security analysis
            results["security_findings"] = self._analyze_security_issues(soup, url)
            results["potential_vulnerabilities"] = self._identify_vulnerabilities(soup, url)

            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(results)

        except Exception as e:
            logging.error(f"Error analyzing {url}: {e}")
            results["error"] = str(e)

        return results

    def _find_hidden_elements(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Find elements that are hidden via CSS or attributes"""
        hidden_elements = []

        # CSS display: none
        for element in soup.find_all(style=re.compile(r'display\s*:\s*none', re.I)):
            hidden_elements.append({
                "type": "css_display_none",
                "tag": element.name,
                "id": element.get('id'),
                "class": element.get('class'),
                "text_preview": element.get_text(strip=True)[:100],
                "severity": "medium"
            })

        # CSS visibility: hidden
        for element in soup.find_all(style=re.compile(r'visibility\s*:\s*hidden', re.I)):
            hidden_elements.append({
                "type": "css_visibility_hidden",
                "tag": element.name,
                "id": element.get('id'),
                "class": element.get('class'),
                "text_preview": element.get_text(strip=True)[:100],
                "severity": "low"
            })

        # Hidden attribute
        for element in soup.find_all(attrs={'hidden': True}):
            hidden_elements.append({
                "type": "hidden_attribute",
                "tag": element.name,
                "id": element.get('id'),
                "class": element.get('class'),
                "text_preview": element.get_text(strip=True)[:100],
                "severity": "medium"
            })

        # Zero opacity
        for element in soup.find_all(style=re.compile(r'opacity\s*:\s*0', re.I)):
            hidden_elements.append({
                "type": "zero_opacity",
                "tag": element.name,
                "id": element.get('id'),
                "class": element.get('class'),
                "text_preview": element.get_text(strip=True)[:100],
                "severity": "low"
            })

        return hidden_elements

    def _find_disabled_elements(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Find disabled form elements"""
        disabled_elements = []

        for element in soup.find_all(attrs={'disabled': True}):
            disabled_elements.append({
                "tag": element.name,
                "type": element.get('type', 'unknown'),
                "id": element.get('id'),
                "name": element.get('name'),
                "value": element.get('value'),
                "severity": "info"
            })

        return disabled_elements

    def _find_readonly_elements(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Find readonly form elements"""
        readonly_elements = []

        for element in soup.find_all(attrs={'readonly': True}):
            readonly_elements.append({
                "tag": element.name,
                "type": element.get('type', 'unknown'),
                "id": element.get('id'),
                "name": element.get('name'),
                "value": element.get('value'),
                "severity": "info"
            })

        return readonly_elements

    def _analyze_security_issues(self, soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
        """Analyze page for security-related findings"""
        issues = []

        # Check for exposed admin panels or debug endpoints
        admin_paths = ['/admin', '/administrator', '/wp-admin', '/admin.php', '/login', '/auth']
        parsed_url = urlparse(url)

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)

            for admin_path in admin_paths:
                if admin_path in href.lower():
                    issues.append({
                        "type": "exposed_admin_panel",
                        "url": full_url,
                        "text": link.get_text(strip=True),
                        "severity": "high"
                    })

        # Check for exposed API endpoints
        api_patterns = [r'/api/', r'/v[0-9]+/', r'/rest/', r'/graphql']
        for link in soup.find_all('a', href=True):
            href = link['href']
            for pattern in api_patterns:
                if re.search(pattern, href, re.I):
                    issues.append({
                        "type": "exposed_api_endpoint",
                        "url": urljoin(url, href),
                        "pattern": pattern,
                        "severity": "medium"
                    })

        # Check for debug information
        debug_patterns = ['debug', 'trace', 'stack', 'error', 'exception']
        for element in soup.find_all(text=re.compile('|'.join(debug_patterns), re.I)):
            issues.append({
                "type": "debug_information",
                "content": element.strip()[:200],
                "severity": "medium"
            })

        return issues

    def _identify_vulnerabilities(self, soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
        """Identify potential vulnerabilities related to hidden elements"""
        vulnerabilities = []

        # Check for hidden forms that might be used for CSRF or parameter pollution
        hidden_forms = soup.find_all('input', attrs={'type': 'hidden'})
        if len(hidden_forms) > 5:
            vulnerabilities.append({
                "type": "multiple_hidden_inputs",
                "count": len(hidden_forms),
                "description": "Multiple hidden inputs found - potential for parameter pollution or CSRF",
                "severity": "medium"
            })

        # Check for disabled but visible elements that might be bypassable
        disabled_visible = []
        for element in soup.find_all(attrs={'disabled': True}):
            if not element.get('style') or 'display: none' not in element.get('style', '').lower():
                disabled_visible.append(element)

        if disabled_visible:
            vulnerabilities.append({
                "type": "disabled_but_visible",
                "count": len(disabled_visible),
                "description": "Disabled elements that are still visible - potential for client-side bypass",
                "severity": "high"
            })

        # Check for readonly fields that might contain sensitive data
        readonly_inputs = soup.find_all(attrs={'readonly': True})
        sensitive_keywords = ['password', 'secret', 'key', 'token', 'auth']

        for element in readonly_inputs:
            name = element.get('name', '').lower()
            id_attr = element.get('id', '').lower()

            for keyword in sensitive_keywords:
                if keyword in name or keyword in id_attr:
                    vulnerabilities.append({
                        "type": "sensitive_readonly_field",
                        "field_name": element.get('name'),
                        "field_id": element.get('id'),
                        "description": f"Readonly field with sensitive name containing '{keyword}'",
                        "severity": "high"
                    })

        return vulnerabilities

    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on findings"""
        recommendations = []

        hidden_count = len(analysis_results["hidden_elements"])
        disabled_count = len(analysis_results["disabled_elements"])
        security_count = len(analysis_results["security_findings"])
        vuln_count = len(analysis_results["potential_vulnerabilities"])

        if vuln_count > 0:
            recommendations.append("🚨 CRITICAL: Potential security vulnerabilities found. Manual review required.")

        if hidden_count > 10:
            recommendations.append("⚠️ Many hidden elements detected. Verify they don't contain sensitive functionality.")

        if disabled_count > 5:
            recommendations.append("ℹ️ Multiple disabled elements found. Test if client-side restrictions can be bypassed.")

        if security_count > 0:
            recommendations.append("🔍 Security-sensitive elements exposed. Consider access controls and obfuscation.")

        recommendations.append("💡 Use the bookmarklet to interactively test hidden element behavior.")
        recommendations.append("🔧 Consider implementing server-side validation for all client-side restrictions.")

        return recommendations

    def generate_comprehensive_report(self, analysis_results: Dict[str, Any], output_file: str) -> None:
        """Generate detailed HTML report of hidden element analysis"""
        html_report = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hidden Elements Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .section {{
            background: white;
            margin: 20px 0;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .severity-high {{ background-color: #ffebee; border-left: 4px solid #f44336; }}
        .severity-medium {{ background-color: #fff3e0; border-left: 4px solid #ff9800; }}
        .severity-low {{ background-color: #e8f5e8; border-left: 4px solid #4caf50; }}
        .severity-info {{ background-color: #e3f2fd; border-left: 4px solid #2196f3; }}
        .finding {{
            margin: 10px 0;
            padding: 10px;
            border-radius: 4px;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }}
        .stat-box {{
            background: #f8f9fa;
            padding: 15px;
            margin: 10px;
            border-radius: 8px;
            text-align: center;
            min-width: 150px;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Hidden Elements Analysis Report</h1>
        <p>Comprehensive Security Assessment for {analysis_results['url']}</p>
        <small>Generated on {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(analysis_results['analysis_time']))}</small>
    </div>

    <div class="section">
        <h2>📊 Summary Statistics</h2>
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{len(analysis_results['hidden_elements'])}</div>
                <div>Hidden Elements</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(analysis_results['disabled_elements'])}</div>
                <div>Disabled Elements</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(analysis_results['security_findings'])}</div>
                <div>Security Findings</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(analysis_results['potential_vulnerabilities'])}</div>
                <div>Vulnerabilities</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🎯 Recommendations</h2>
        <ul>
"""

        for rec in analysis_results['recommendations']:
            html_report += f"            <li>{rec}</li>\n"

        html_report += """
        </ul>
    </div>
"""

        # Hidden Elements Section
        if analysis_results['hidden_elements']:
            html_report += """
    <div class="section">
        <h2>👻 Hidden Elements</h2>
"""
            for element in analysis_results['hidden_elements']:
                severity_class = f"severity-{element['severity']}"
                html_report += f"""
        <div class="finding {severity_class}">
            <strong>{element['type'].replace('_', ' ').title()}</strong> - {element['tag']}
            {f" (ID: {element['id']})" if element['id'] else ""}
            {f" (Class: {element['class']})" if element['class'] else ""}
            <br><small>Preview: {element['text_preview']}</small>
        </div>
"""
            html_report += "    </div>\n"

        # Security Findings Section
        if analysis_results['security_findings']:
            html_report += """
    <div class="section">
        <h2>🔒 Security Findings</h2>
"""
            for finding in analysis_results['security_findings']:
                severity_class = f"severity-{finding['severity']}"
                html_report += f"""
        <div class="finding {severity_class}">
            <strong>{finding['type'].replace('_', ' ').title()}</strong><br>
            {finding.get('url', finding.get('content', 'N/A'))}
        </div>
"""
            html_report += "    </div>\n"

        # Vulnerabilities Section
        if analysis_results['potential_vulnerabilities']:
            html_report += """
    <div class="section">
        <h2>⚠️ Potential Vulnerabilities</h2>
"""
            for vuln in analysis_results['potential_vulnerabilities']:
                severity_class = f"severity-{vuln['severity']}"
                html_report += f"""
        <div class="finding {severity_class}">
            <strong>{vuln['type'].replace('_', ' ').title()}</strong><br>
            {vuln['description']}
        </div>
"""
            html_report += "    </div>\n"

        html_report += """
</body>
</html>
"""

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_report)

        logging.info(f"Comprehensive report saved to {output_file}")

# Example usage:
if __name__ == "__main__":
    uncover = LostUncover()
    print("Bookmarklet Code:")
    print(uncover.get_bookmarklet())
    print("\nTest page saved to:", uncover.save_test_page())