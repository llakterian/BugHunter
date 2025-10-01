"""
Recon Automation Module for BugHunter - 33X Enhanced
Supports: Wayback Machine, AlienVault OTX, URLScan, VirusTotal, CommonCrawl, GitHub, Shodan
Advanced features: Parallel fetching, deduplication, filtering, export capabilities
"""
import requests
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Set, Optional, Any
import logging
import os

class ReconAutomation:
    def fetch_wayback_urls(self, target):
        domain = target.replace('https://', '').replace('http://', '').split('/')[0]
        url = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey"
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                urls = [row[0] for row in data[1:]] if len(data) > 1 else []
                return urls
            else:
                return []
        except Exception as e:
            return [f"Error fetching Wayback URLs: {e}"]

    def fetch_alienvault_urls(self, target):
        domain = target.replace('https://', '').replace('http://', '').split('/')[0]
        url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/url_list"
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                urls = [entry['url'] for entry in data.get('url_list', [])]
                return urls
            else:
                return []
        except Exception as e:
            return [f"Error fetching AlienVault URLs: {e}"]

    def fetch_urlscan_urls(self, target):
        domain = target.replace('https://', '').replace('http://', '').split('/')[0]
        url = f"https://urlscan.io/api/v1/search/?q=domain:{domain}"
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                urls = [result['task']['url'] for result in data.get('results', [])]
                return urls
            else:
                return []
        except Exception as e:
            return [f"Error fetching URLScan URLs: {e}"]

    def fetch_virustotal_urls(self, target, api_key=None):
        domain = target.replace('https://', '').replace('http://', '').split('/')[0]
        headers = {"x-apikey": api_key} if api_key else {}
        url = f"https://www.virustotal.com/api/v3/domains/{domain}/urls"
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                urls = [item['attributes']['url'] for item in data.get('data', [])]
                return urls
            else:
                return []
        except Exception as e:
            return [f"Error fetching VirusTotal URLs: {e}"]

    def aggregate_recon_urls(self, target, virustotal_api_key=None):
        wayback = self.fetch_wayback_urls(target)
        alienvault = self.fetch_alienvault_urls(target)
        urlscan = self.fetch_urlscan_urls(target)
        virustotal = self.fetch_virustotal_urls(target, api_key=virustotal_api_key)
        all_urls = list(set(wayback + alienvault + urlscan + virustotal))
        return {
            'wayback_urls': wayback,
            'alienvault_urls': alienvault,
            'urlscan_urls': urlscan,
            'virustotal_urls': virustotal,
            'all_recon_urls': all_urls,
            'total_recon_urls': len(all_urls)
        }

    def comprehensive_recon(self, target: str, api_keys: Optional[Dict[str, str]] = None, max_workers: int = 5) -> Dict[str, Any]:
        """
        33X Enhanced comprehensive reconnaissance with parallel processing
        """
        logging.info(f"Starting comprehensive recon for {target}")

        start_time = time.time()
        results = {
            "target": target,
            "recon_start": start_time,
            "sources": {},
            "all_urls": set(),
            "filtered_urls": set(),
            "statistics": {},
            "errors": []
        }

        api_keys = api_keys or {}

        # Define all recon sources
        recon_sources = {
            "wayback": lambda: self._safe_fetch(self.fetch_wayback_urls, target),
            "alienvault": lambda: self._safe_fetch(self.fetch_alienvault_urls, target),
            "urlscan": lambda: self._safe_fetch(self.fetch_urlscan_urls, target),
            "virustotal": lambda: self._safe_fetch(self.fetch_virustotal_urls, target, api_keys.get("virustotal")),
            "commoncrawl": lambda: self._safe_fetch(self.fetch_commoncrawl_urls, target),
            "github": lambda: self._safe_fetch(self.fetch_github_urls, target),
            "shodan": lambda: self._safe_fetch(self.fetch_shodan_urls, target, api_keys.get("shodan"))
        }

        # Parallel execution
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_source = {executor.submit(func): source for source, func in recon_sources.items()}

            for future in as_completed(future_to_source):
                source = future_to_source[future]
                try:
                    urls = future.result()
                    results["sources"][source] = urls
                    if isinstance(urls, list):
                        results["all_urls"].update(urls)
                    logging.info(f"{source}: {len(urls) if isinstance(urls, list) else 0} URLs")
                except Exception as e:
                    error_msg = f"Error in {source}: {e}"
                    results["errors"].append(error_msg)
                    logging.error(error_msg)

        # Filter and deduplicate
        results["all_urls"] = list(results["all_urls"])
        results["filtered_urls"] = self._filter_and_deduplicate_urls(results["all_urls"], target)

        # Generate statistics
        results["statistics"] = self._generate_recon_statistics(results)
        results["recon_duration"] = time.time() - start_time

        return results

    def _safe_fetch(self, func, *args, **kwargs):
        """Safe wrapper for fetch functions"""
        try:
            result = func(*args, **kwargs)
            return result if result else []
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            return []

    def fetch_commoncrawl_urls(self, target: str) -> List[str]:
        """Fetch URLs from Common Crawl index"""
        domain = self._extract_domain(target)
        url = f"http://index.commoncrawl.org/CC-MAIN-2023-40-index?url={domain}/*&output=json"

        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                urls = [entry.get('url') for entry in data if 'url' in entry]
                return list(set(urls))
            return []
        except Exception as e:
            logging.error(f"CommonCrawl fetch error: {e}")
            return []

    def fetch_github_urls(self, target: str) -> List[str]:
        """Search for domain references in GitHub"""
        domain = self._extract_domain(target)
        url = f"https://api.github.com/search/code?q={domain}&per_page=100"

        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                urls = []
                for item in data.get('items', []):
                    file_url = item.get('html_url')
                    if file_url:
                        urls.append(file_url)
                return urls
            return []
        except Exception as e:
            logging.error(f"GitHub fetch error: {e}")
            return []

    def fetch_shodan_urls(self, target: str, api_key: Optional[str] = None) -> List[str]:
        """Fetch related URLs from Shodan"""
        if not api_key:
            return []

        domain = self._extract_domain(target)
        url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query=hostname:{domain}"

        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                urls = []
                for match in data.get('matches', []):
                    hostnames = match.get('hostnames', [])
                    for hostname in hostnames:
                        urls.extend([f"http://{hostname}", f"https://{hostname}"])
                return list(set(urls))
            return []
        except Exception as e:
            logging.error(f"Shodan fetch error: {e}")
            return []

    def _extract_domain(self, target: str) -> str:
        """Extract domain from URL"""
        parsed = urlparse(target)
        return parsed.netloc if parsed.netloc else target.replace('https://', '').replace('http://', '').split('/')[0]

    def _filter_and_deduplicate_urls(self, urls: List[str], target: str) -> List[str]:
        """Filter and deduplicate URLs"""
        filtered = set()
        target_domain = self._extract_domain(target)

        for url in urls:
            if isinstance(url, str) and url.startswith(('http://', 'https://')):
                url_domain = self._extract_domain(url)
                # Keep URLs from same domain or subdomains
                if url_domain == target_domain or url_domain.endswith('.' + target_domain):
                    filtered.add(url)

        return sorted(list(filtered))

    def _generate_recon_statistics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive statistics"""
        stats = {
            "total_sources": len(results["sources"]),
            "total_urls_found": len(results["all_urls"]),
            "filtered_urls": len(results["filtered_urls"]),
            "errors_count": len(results["errors"]),
            "source_breakdown": {}
        }

        for source, urls in results["sources"].items():
            count = len(urls) if isinstance(urls, list) else 0
            stats["source_breakdown"][source] = count

        return stats

    def export_recon_results(self, results: Dict[str, Any], output_file: str, format: str = "json") -> None:
        """Export recon results to file"""
        if format.lower() == "json":
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
        elif format.lower() == "txt":
            with open(output_file, 'w') as f:
                f.write(f"Recon Results for {results['target']}\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Total URLs found: {len(results['all_urls'])}\n")
                f.write(f"Filtered URLs: {len(results['filtered_urls'])}\n\n")

                for source, urls in results["sources"].items():
                    f.write(f"{source.upper()} ({len(urls) if isinstance(urls, list) else 0} URLs):\n")
                    if isinstance(urls, list):
                        for url in urls[:10]:  # Limit to first 10
                            f.write(f"  {url}\n")
                        if len(urls) > 10:
                            f.write(f"  ... and {len(urls) - 10} more\n")
                    f.write("\n")

        logging.info(f"Recon results exported to {output_file}")

    def generate_recon_report(self, results: Dict[str, Any], output_file: str) -> None:
        """Generate HTML report for recon results"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Recon Report - {results['target']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-box {{ background: #e0e0e0; padding: 10px; border-radius: 5px; }}
        .source {{ margin: 10px 0; }}
        .urls {{ margin-left: 20px; }}
        .error {{ color: red; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Reconnaissance Report</h1>
        <h2>Target: {results['target']}</h2>
        <p>Duration: {results.get('recon_duration', 0):.2f} seconds</p>
    </div>

    <div class="stats">
        <div class="stat-box">Total Sources: {results['statistics']['total_sources']}</div>
        <div class="stat-box">URLs Found: {results['statistics']['total_urls_found']}</div>
        <div class="stat-box">Filtered URLs: {results['statistics']['filtered_urls']}</div>
    </div>

    <h3>Source Breakdown</h3>
"""

        for source, count in results['statistics']['source_breakdown'].items():
            html += f"<div class='source'><strong>{source}:</strong> {count} URLs</div>"

        if results['errors']:
            html += "<h3>Errors</h3>"
            for error in results['errors']:
                html += f"<div class='error'>{error}</div>"

        html += "</body></html>"

        with open(output_file, 'w') as f:
            f.write(html)