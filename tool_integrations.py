
"""
Tool Integrations - Enhanced Reconnaissance and Automation
"""

import subprocess
import os

class ToolIntegrations:
    def run_uro(self, target):
        """Run Uro (URL deduplication/normalization) against a target."""
        try:
            result = subprocess.run(["uro", target], capture_output=True, text=True)
            return result.stdout.splitlines()
        except Exception as e:
            return [f"Error running Uro: {e}"]
    def install_missing_tools(self):
        """Attempt to install missing tools using common package managers. Improved error handling and feedback."""
        required_tools = ["gau", "fff", "gf", "uro", "nuclei"]
        results = {}
        for tool in required_tools:
            # Check if tool is already installed
            result = subprocess.run(["which", tool], capture_output=True, text=True)
            if result.stdout.strip():
                results[tool] = "Already installed"
                continue
            # Try installing with go install (assumes Go is installed)
            try:
                if tool == "gau":
                    install_cmd = "go install github.com/lc/gau/v2/cmd/gau@latest"
                elif tool == "fff":
                    install_cmd = "go install github.com/tomnomnom/fff@latest"
                elif tool == "gf":
                    install_cmd = "go install github.com/tomnomnom/gf@latest"
                elif tool == "uro":
                    install_cmd = "pip install uro"
                elif tool == "nuclei":
                    install_cmd = "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
                else:
                    results[tool] = "Unknown tool"
                    continue
                proc = subprocess.run(install_cmd, shell=True, capture_output=True, text=True)
                if proc.returncode == 0:
                    # Check if tool is now in PATH
                    result_check = subprocess.run(["which", tool], capture_output=True, text=True)
                    if result_check.stdout.strip():
                        results[tool] = "Installed successfully"
                    else:
                        results[tool] = "Installed, but not found in PATH. Add $GOPATH/bin to your PATH."
                else:
                    results[tool] = f"Install failed: {proc.stderr.strip()}"
            except Exception as e:
                results[tool] = f"Error: {e}"
        return results

    def install_gf_patterns(self):
        """Install GF patterns from GitHub repository."""
        gf_patterns_repo = "https://github.com/coffinxp/GFpattren"
        gf_patterns_dir = os.path.expanduser("~/.gf")

        try:
            # Create .gf directory if it doesn't exist
            os.makedirs(gf_patterns_dir, exist_ok=True)

            # Clone or pull the patterns repo
            if os.path.exists(os.path.join(gf_patterns_dir, ".git")):
                # Update existing repo
                result = subprocess.run(["git", "-C", gf_patterns_dir, "pull"], capture_output=True, text=True)
            else:
                # Clone new repo
                result = subprocess.run(["git", "clone", gf_patterns_repo, gf_patterns_dir], capture_output=True, text=True)

            if result.returncode == 0:
                return {"status": "GF patterns installed/updated successfully", "path": gf_patterns_dir}
            else:
                return {"error": f"Failed to install GF patterns: {result.stderr}"}
        except Exception as e:
            return {"error": f"Error installing GF patterns: {e}"}
    def check_tool_availability(self):
        """Check if required external tools are available in PATH."""
        required_tools = ["gau", "fff", "gf", "uro", "nuclei", "shef"]
        status = {}
        for tool in required_tools:
            result = subprocess.run(["which", tool], capture_output=True, text=True)
            status[tool] = bool(result.stdout.strip())
        return status
    """Integrates external tools for reconnaissance and automation."""

    def run_recon_automation(self, target, virustotal_api_key=None):
        """Aggregate URLs from Wayback, AlienVault OTX, URLScan, VirusTotal."""
        try:
            from recon_automation import ReconAutomation
            recon = ReconAutomation()
            results = recon.aggregate_recon_urls(target, virustotal_api_key=virustotal_api_key)
            return results
        except Exception as e:
            return {'error': str(e)}

    def run_gau(self, target):
        """Run GAU (GetAllURLs) against a target."""
        try:
            result = subprocess.run(["gau", target], capture_output=True, text=True)
            return result.stdout.splitlines()
        except Exception as e:
            return [f"Error running GAU: {e}"]

    def run_fff(self, target):
        """Run FFF (Fast File Finder) against a target."""
        try:
            result = subprocess.run(["fff", target], capture_output=True, text=True)
            return result.stdout.splitlines()
        except Exception as e:
            return [f"Error running FFF: {e}"]

    def run_gf(self, target):
        """Run GF (Grep for patterns) against a target."""
        try:
            result = subprocess.run(["gf", target], capture_output=True, text=True)
            return result.stdout.splitlines()
        except Exception as e:
            return [f"Error running GF: {e}"]

    def filter_urls_with_gf(self, url_file, patterns, output_dir="temp"):
        """Filter URLs using GF patterns and deduplicate with Uro."""
        os.makedirs(output_dir, exist_ok=True)
        results = {}

        for pattern in patterns:
            try:
                # Run gf on the URL file
                gf_cmd = f"cat {url_file} | gf {pattern}"
                gf_result = subprocess.run(gf_cmd, shell=True, capture_output=True, text=True)

                if gf_result.returncode == 0 and gf_result.stdout.strip():
                    # Deduplicate with uro
                    uro_cmd = f"echo '{gf_result.stdout}' | uro"
                    uro_result = subprocess.run(uro_cmd, shell=True, capture_output=True, text=True)

                    if uro_result.returncode == 0:
                        unique_urls = uro_result.stdout.strip().split('\n')
                        output_file = os.path.join(output_dir, f"unique_{pattern}_targets.txt")
                        with open(output_file, 'w') as f:
                            f.write('\n'.join(unique_urls))
                        results[pattern] = {
                            "count": len(unique_urls),
                            "file": output_file,
                            "urls": unique_urls
                        }
                    else:
                        results[pattern] = {"error": f"Uro failed: {uro_result.stderr}"}
                else:
                    results[pattern] = {"count": 0, "urls": []}
            except Exception as e:
                results[pattern] = {"error": str(e)}

        return results

    def comprehensive_url_discovery(self, target):
        """Run GAU and FFF for real URL and parameter discovery."""
        endpoints = self.run_gau(target)
        files = self.run_fff(target)
        uro_urls = self.run_uro(target)
        # Use custom wordlists if available
        custom_endpoints = []
        try:
            with open('wordlists/endpoints.txt') as f:
                custom_endpoints = [line.strip() for line in f if line.strip()]
        except Exception:
            pass
        all_urls = list(set(endpoints + files + uro_urls + custom_endpoints))
        # Extract parameters from all URLs
        parameters = []
        for url in all_urls:
            if '?' in url:
                param_str = url.split('?', 1)[1]
                for param in param_str.split('&'):
                    param_name = param.split('=')[0]
                    if param_name and param_name not in parameters:
                        parameters.append(param_name)
        results = {
            'endpoints_found': all_urls,
            'parameters_found': parameters,
            'total_urls': len(all_urls),
            'js_urls': len([u for u in all_urls if u.endswith('.js')]),
            'parameter_urls': len([u for u in all_urls if '?' in u])
        }
        return results

    def automated_secrets_hunting(self, target):
        """Run GF for secrets hunting and parse results."""
        patterns = ['aws-keys', 'apikey', 'authorization', 'password', 'secret', 'token']
        secrets_found = {}
        high_value_findings = []
        for pattern in patterns:
            output = self.run_gf(f"{pattern} {target}")
            findings = [line for line in output if line and not line.startswith('Error')]
            secrets_found[pattern] = findings
            if findings:
                high_value_findings.extend(findings)
        results = {
            'secrets_found': secrets_found,
            'high_value_findings': high_value_findings
        }
        return results