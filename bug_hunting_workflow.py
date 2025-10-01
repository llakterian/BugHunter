"""
Bug Hunting Workflow - Complete implementation of methods from how.txt
Combines Shodan mass scanning, Lost Uncover, LostFuzzer, and automated toolkit
"""

from nuclei_shodan_integration import NucleiShodanIntegration
from lost_uncover import LostUncover
from lost_fuzzer import LostFuzzer
from tool_integrations import ToolIntegrations
from recon_automation import ReconAutomation
import os

class BugHuntingWorkflow:
    def __init__(self):
        self.nuclei_shodan = NucleiShodanIntegration()
        self.lost_uncover = LostUncover()
        self.lost_fuzzer = LostFuzzer()
        self.tool_integrations = ToolIntegrations()
        self.recon_automation = ReconAutomation()

    def method_1_mass_cve_scanning(self, shodan_api_key, cve_query, cve_templates="grafana"):
        """Method 1: Mass Scanning with Shodan & Nuclei"""
        print("=== Method 1: Mass Scanning with Shodan & Nuclei ===")
        results = self.nuclei_shodan.mass_cve_scan(shodan_api_key, cve_query, cve_templates)
        if "error" in results:
            print(f"Error: {results['error']}")
        else:
            print(f"Found {results['total_ips']} IPs and {results['total_domains']} domains")
            print(f"Nuclei findings: {len(results['nuclei_findings'])}")
            print("Files saved:", results['ip_file'], results['domain_file'])
        return results

    def method_2_uncover_hidden_elements(self):
        """Method 2: Uncovering What's Hidden in Plain Sight"""
        print("=== Method 2: Uncovering Hidden Elements ===")
        bookmarklet = self.lost_uncover.get_bookmarklet()
        test_page = self.lost_uncover.save_test_page()
        print("Bookmarklet generated. Drag this to your bookmarks:")
        print(bookmarklet)
        print(f"Test page saved to: {test_page}")
        print("Instructions: Open the test page in browser and click the bookmarklet to unhide elements.")
        return {"bookmarklet": bookmarklet, "test_page": test_page}

    def method_3_automated_toolkit(self, target_domain, virustotal_api_key=None):
        """Method 3: Automated Bug Hunting Toolkit"""
        print("=== Method 3: Automated Bug Hunting Toolkit ===")

        # Step 1: Recon with AlienVault, Wayback, etc.
        print("Step 1: Aggregating URLs from multiple sources...")
        recon_results = self.recon_automation.aggregate_recon_urls(target_domain, virustotal_api_key)

        if "error" in recon_results:
            print(f"Recon error: {recon_results['error']}")
            return recon_results

        all_urls = recon_results['all_recon_urls']
        url_file = f"temp/{target_domain.replace('.', '_')}_all_urls.txt"
        os.makedirs("temp", exist_ok=True)
        with open(url_file, 'w') as f:
            f.write('\n'.join(all_urls))

        print(f"Collected {len(all_urls)} URLs from recon sources")

        # Step 2: Filter with GF patterns
        print("Step 2: Filtering URLs with GF patterns...")
        patterns = ['xss', 'sqli', 'idor', 'ssrf', 'redirect']
        filtered_results = self.tool_integrations.filter_urls_with_gf(url_file, patterns)

        for pattern, data in filtered_results.items():
            if "error" not in data:
                print(f"{pattern.upper()}: {data['count']} unique targets")

        # Step 3: Run LostFuzzer on filtered targets
        print("Step 3: Running LostFuzzer DAST scans...")
        fuzzer_results = {}
        for pattern, data in filtered_results.items():
            if "urls" in data and data['urls']:
                print(f"Scanning {pattern} targets with LostFuzzer...")
                scan_results = self.lost_fuzzer.scan_domains(data['urls'][:10], max_workers=3)  # Limit for demo
                fuzzer_results[pattern] = scan_results

        return {
            "recon_results": recon_results,
            "filtered_targets": filtered_results,
            "fuzzer_results": fuzzer_results
        }

    def run_complete_workflow(self, target_domain, shodan_api_key=None, virustotal_api_key=None):
        """Run the complete bug hunting workflow"""
        print("🚀 Starting Complete Bug Hunting Workflow")
        print(f"Target: {target_domain}")

        # Method 1: If Shodan API provided, do mass scanning
        if shodan_api_key:
            cve_query = f"hostname:{target_domain}"  # Example query
            self.method_1_mass_cve_scanning(shodan_api_key, cve_query)

        # Method 2: Generate uncover tools
        self.method_2_uncover_hidden_elements()

        # Method 3: Automated toolkit
        toolkit_results = self.method_3_automated_toolkit(target_domain, virustotal_api_key)

        print("✅ Workflow completed!")
        return toolkit_results

# Example usage
if __name__ == "__main__":
    workflow = BugHuntingWorkflow()

    # Run individual methods
    # workflow.method_2_uncover_hidden_elements()

    # Run complete workflow (replace with actual API keys)
    # results = workflow.run_complete_workflow("example.com", shodan_api_key="YOUR_KEY", virustotal_api_key="YOUR_KEY")

    print("Bug Hunting Workflow initialized. Use the methods above to run specific workflows.")