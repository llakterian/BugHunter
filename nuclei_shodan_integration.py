"""
Nuclei and Shodan Integration for BugHunter - Mass CVE Scanning
Enhanced for 33X more robust scanning capabilities
"""
import subprocess
import requests
import json
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
import logging

class NucleiShodanIntegration:
    def run_nuclei_scan(self, target, templates=None, batch_size=50, concurrency=50, silent_info=True):
        """Run Nuclei scan against target using specified templates."""
        cmd = ["nuclei", "-u", target, "-bs", str(batch_size), "-c", str(concurrency)]
        if templates:
            cmd += ["-t", templates]
        if silent_info:
            cmd += ["-es", "info"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout.splitlines()
        except Exception as e:
            return [f"Error running Nuclei: {e}"]

    def run_shodan_query(self, api_key, query):
        """Run Shodan search query using API key."""
        url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query={query}"
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        except Exception as e:
            return {"error": str(e)}

    def extract_ips_from_shodan(self, shodan_results):
        """Extract IPs from Shodan search results."""
        ips = []
        if "matches" in shodan_results:
            for match in shodan_results["matches"]:
                ips.append(match.get("ip_str", ""))
        return list(set(ips))  # Remove duplicates

    def extract_domains_from_shodan(self, shodan_results):
        """Extract domains from Shodan search results."""
        domains = []
        if "matches" in shodan_results:
            for match in shodan_results["matches"]:
                hostnames = match.get("hostnames", [])
                domains.extend(hostnames)
        return list(set(domains))  # Remove duplicates

    def mass_cve_scan(self, targets: List[str], shodan_api_key: str, cve_queries: List[str], max_workers: int = 10) -> Dict[str, Any]:
        """
        Perform mass CVE scanning across multiple targets using Shodan and Nuclei
        33X enhanced: Parallel processing, comprehensive reporting, vulnerability correlation
        """
        logging.info(f"Starting mass CVE scan on {len(targets)} targets with {len(cve_queries)} queries")

        results = {
            "scan_start": time.time(),
            "targets_scanned": len(targets),
            "cve_queries": len(cve_queries),
            "vulnerabilities_found": [],
            "shodan_results": {},
            "nuclei_results": {},
            "correlations": [],
            "stats": {
                "high_severity": 0,
                "medium_severity": 0,
                "low_severity": 0,
                "info": 0
            }
        }

        # Parallel Shodan queries
        def shodan_worker(query):
            return self.run_shodan_query(shodan_api_key, query)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            shodan_futures = {executor.submit(shodan_worker, query): query for query in cve_queries}

            for future in as_completed(shodan_futures):
                query = shodan_futures[future]
                try:
                    shodan_result = future.result()
                    results["shodan_results"][query] = shodan_result

                    if "matches" in shodan_result:
                        ips = self.extract_ips_from_shodan(shodan_result)
                        domains = self.extract_domains_from_shodan(shodan_result)

                        # Add to targets if not already present
                        for ip in ips:
                            if ip not in targets:
                                targets.append(ip)
                        for domain in domains:
                            if domain not in targets:
                                targets.append(domain)

                except Exception as e:
                    logging.error(f"Shodan query failed for {query}: {e}")

        # Enhanced Nuclei scanning with parallel processing
        nuclei_results = self.parallel_nuclei_scan(targets, max_workers=max_workers)
        results["nuclei_results"] = nuclei_results

        # Correlate findings
        results["correlations"] = self.correlate_vulnerabilities(results["shodan_results"], nuclei_results)

        # Update statistics
        for vuln in nuclei_results:
            severity = vuln.get("severity", "info").lower()
            if severity in results["stats"]:
                results["stats"][severity] += 1

        results["scan_end"] = time.time()
        results["scan_duration"] = results["scan_end"] - results["scan_start"]

        return results

    def parallel_nuclei_scan(self, targets: List[str], templates: str = "cves", max_workers: int = 20) -> List[Dict[str, Any]]:
        """
        Run Nuclei scans in parallel across multiple targets
        """
        results = []

        def nuclei_worker(target):
            return self.run_nuclei_scan(target, templates=templates)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            nuclei_futures = {executor.submit(nuclei_worker, target): target for target in targets}

            for future in as_completed(nuclei_futures):
                target = nuclei_futures[future]
                try:
                    scan_result = future.result()
                    for line in scan_result:
                        if line.strip():
                            # Parse Nuclei output (assuming JSON format)
                            try:
                                vuln_data = json.loads(line)
                                vuln_data["target"] = target
                                results.append(vuln_data)
                            except json.JSONDecodeError:
                                # If not JSON, treat as raw output
                                results.append({
                                    "target": target,
                                    "raw_output": line,
                                    "severity": "unknown"
                                })
                except Exception as e:
                    logging.error(f"Nuclei scan failed for {target}: {e}")

        return results

    def correlate_vulnerabilities(self, shodan_results: Dict[str, Any], nuclei_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Correlate Shodan findings with Nuclei vulnerabilities
        """
        correlations = []

        for vuln in nuclei_results:
            target = vuln.get("target", "")
            cve_id = vuln.get("info", {}).get("tags", [])

            # Find related Shodan data
            for query, shodan_data in shodan_results.items():
                if "matches" in shodan_data:
                    for match in shodan_data["matches"]:
                        if target in [match.get("ip_str"), *match.get("hostnames", [])]:
                            correlations.append({
                                "vulnerability": vuln,
                                "shodan_match": match,
                                "query": query,
                                "correlation_type": "direct_match"
                            })
                            break

        return correlations

    def generate_mass_scan_report(self, scan_results: Dict[str, Any], output_file: str) -> None:
        """
        Generate comprehensive report for mass CVE scanning
        """
        report = {
            "report_title": "Bug Bounty Hunter Pro - Mass CVE Scan Report",
            "generated_at": time.time(),
            "summary": {
                "targets_scanned": scan_results["targets_scanned"],
                "cve_queries_executed": scan_results["cve_queries"],
                "vulnerabilities_found": len(scan_results["vulnerabilities_found"]),
                "correlations_found": len(scan_results["correlations"]),
                "scan_duration_seconds": scan_results["scan_duration"]
            },
            "statistics": scan_results["stats"],
            "top_vulnerabilities": self.get_top_vulnerabilities(scan_results["nuclei_results"]),
            "recommendations": self.generate_recommendations(scan_results)
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)

    def get_top_vulnerabilities(self, nuclei_results: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Get top vulnerabilities by severity
        """
        severity_order = {"critical": 5, "high": 4, "medium": 3, "low": 2, "info": 1}

        sorted_vulns = sorted(
            nuclei_results,
            key=lambda x: severity_order.get(x.get("severity", "info").lower(), 0),
            reverse=True
        )

        return sorted_vulns[:top_n]

    def generate_recommendations(self, scan_results: Dict[str, Any]) -> List[str]:
        """
        Generate actionable recommendations based on scan results
        """
        recommendations = []

        stats = scan_results["stats"]

        if stats["high_severity"] > 0 or stats["critical_severity"] > 0:
            recommendations.append("🚨 IMMEDIATE ACTION REQUIRED: High/critical severity vulnerabilities found. Prioritize remediation.")
        elif stats["medium_severity"] > 10:
            recommendations.append("⚠️ Multiple medium severity issues detected. Schedule remediation within 30 days.")

        if len(scan_results["correlations"]) > 0:
            recommendations.append("🔗 Shodan-Nuclei correlations found. Cross-reference with threat intelligence for prioritization.")

        if stats["info"] > 50:
            recommendations.append("ℹ️ Large number of informational findings. Focus on high-impact vulnerabilities first.")

        return recommendations

    def save_to_file(self, items, filename):
        """Save list of items to a file."""
        try:
            with open(filename, 'w') as f:
                f.write('\n'.join(items))
            return True
        except Exception as e:
            return f"Error saving to file: {e}"
