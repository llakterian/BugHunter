"""
LostFuzzer - Quick & Easy DAST Scanner using Nuclei
Passive URL Fuzzing & Vulnerability Detection
"""

import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class LostFuzzer:
    def __init__(self):
        self.nuclei_cmd = ["nuclei"]
        self.default_templates = ["vulnerabilities", "cves", "misconfiguration", "exposures"]

    def run_nuclei_dast(self, target, templates=None, output_file=None, severity=None):
        """Run Nuclei DAST scan on a single target."""
        cmd = self.nuclei_cmd + ["-u", target]

        if templates:
            if isinstance(templates, list):
                cmd += ["-t"] + templates
            else:
                cmd += ["-t", templates]

        if severity:
            cmd += ["-severity", severity]

        if output_file:
            cmd += ["-o", output_file]

        # Add common flags for efficiency
        cmd += ["-bs", "50", "-c", "50", "-es", "info"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return {
                "target": target,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                "target": target,
                "error": "Scan timed out",
                "success": False
            }
        except Exception as e:
            return {
                "target": target,
                "error": str(e),
                "success": False
            }

    def scan_domains(self, domains, templates=None, max_workers=5, output_dir="reports"):
        """Scan multiple domains concurrently."""
        if isinstance(domains, str):
            domains = [domains]

        os.makedirs(output_dir, exist_ok=True)

        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_domain = {
                executor.submit(self.run_nuclei_dast, domain, templates,
                              os.path.join(output_dir, f"{domain.replace('.', '_')}_scan.txt")): domain
                for domain in domains
            }

            for future in as_completed(future_to_domain):
                domain = future_to_domain[future]
                try:
                    result = future.result()
                    results.append(result)
                    print(f"Completed scan for {domain}: {'Success' if result['success'] else 'Failed'}")
                except Exception as exc:
                    print(f"Scan for {domain} generated an exception: {exc}")
                    results.append({"target": domain, "error": str(exc), "success": False})

        return results

    def scan_from_file(self, file_path, templates=None, max_workers=5, output_dir="reports"):
        """Scan domains from a file."""
        try:
            with open(file_path, 'r') as f:
                domains = [line.strip() for line in f if line.strip()]
            return self.scan_domains(domains, templates, max_workers, output_dir)
        except FileNotFoundError:
            return [{"error": f"File not found: {file_path}"}]

    def get_available_templates(self):
        """Get list of available Nuclei templates."""
        try:
            result = subprocess.run(["nuclei", "-tl"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.splitlines()
            else:
                return ["Error fetching templates"]
        except Exception as e:
            return [f"Error: {e}"]

# Example usage:
if __name__ == "__main__":
    fuzzer = LostFuzzer()

    # Scan single domain
    result = fuzzer.run_nuclei_dast("https://example.com")
    print("Single scan result:", result)

    # Scan multiple domains
    domains = ["https://example.com", "https://httpbin.org"]
    results = fuzzer.scan_domains(domains)
    print("Multi-domain scan results:", results)