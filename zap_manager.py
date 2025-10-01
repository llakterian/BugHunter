"""
ZAP Manager - OWASP ZAP Integration for Bug Bounty Hunter Pro
Provides interface to OWASP ZAP for web application scanning
"""

from PyQt6.QtCore import QObject, pyqtSignal
import requests
import time
import subprocess
import os
from typing import Optional


class ZAPManager(QObject):
    """OWASP ZAP Manager for web application security scanning"""

    # Signals
    status_changed = pyqtSignal(str)  # Connected, Disconnected, Starting, etc.
    scan_progress = pyqtSignal(int)   # Progress percentage

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.zap_host = "127.0.0.1"
        self.zap_port = 8080
        self.zap_api_key = None
        self.connected = False
        self.zap_process = None

        # Load configuration
        zap_config = config_manager.get_zap_config()
        self.zap_host = zap_config.get('host', '127.0.0.1')
        self.zap_port = zap_config.get('port', 8080)
        self.zap_api_key = zap_config.get('api_key')

    def connect(self) -> bool:
        """Connect to ZAP API"""
        try:
            # Try to connect to ZAP API - try multiple endpoints
            urls_to_try = [
                f"http://{self.zap_host}:{self.zap_port}/JSON/core/view/version/",
                f"http://{self.zap_host}:{self.zap_port}/UI/core/view/version/",
                f"http://{self.zap_host}:{self.zap_port}/"
            ]

            for url in urls_to_try:
                try:
                    params = {}
                    if self.zap_api_key and 'JSON' in url:
                        params['apikey'] = self.zap_api_key

                    response = requests.get(url, params=params, timeout=5)

                    if response.status_code == 200:
                        # For JSON API, check if we got JSON response
                        if 'JSON' in url:
                            try:
                                data = response.json()
                                if 'version' in data:
                                    self.connected = True
                                    self.status_changed.emit("Connected")
                                    return True
                            except:
                                continue
                        else:
                            # For UI, check if it contains ZAP content
                            if 'ZAP' in response.text or 'Zed Attack Proxy' in response.text:
                                self.connected = True
                                self.status_changed.emit("Connected")
                                return True
                except:
                    continue

            self.status_changed.emit("Connection Failed")
            return False

        except requests.exceptions.RequestException:
            self.connected = False
            self.status_changed.emit("Disconnected")
            return False

    def start_zap(self) -> bool:
        """Start ZAP daemon - checks if already running first"""
        try:
            # First, check if ZAP is already running by trying to connect
            self.status_changed.emit("Checking ZAP status")
            if self.connect():
                self.status_changed.emit("ZAP already running and connected")
                return True

            self.status_changed.emit("Starting ZAP")

            # Try to start ZAP using common paths
            zap_paths = [
                "/usr/share/zaproxy/zap.sh",
                "/usr/local/bin/zap.sh",
                "/opt/zaproxy/zap.sh",
                "zap.sh"
            ]

            zap_cmd = None
            for path in zap_paths:
                if os.path.exists(path):
                    zap_cmd = path
                    break

            if not zap_cmd:
                # Try to find in PATH
                try:
                    subprocess.run(["zap.sh", "--version"], capture_output=True, check=True)
                    zap_cmd = "zap.sh"
                except (subprocess.CalledProcessError, FileNotFoundError):
                    self.status_changed.emit("ZAP not found")
                    return False

            # Start ZAP in daemon mode
            cmd = [zap_cmd, "-daemon", "-host", self.zap_host, "-port", str(self.zap_port), "-config", "api.disablekey=true"]
            if self.zap_api_key:
                cmd.extend(["-config", f"api.key={self.zap_api_key}"])

            self.zap_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Wait for ZAP to start
            for i in range(30):  # Wait up to 30 seconds
                if self.connect():
                    self.status_changed.emit("Connected")
                    return True
                time.sleep(1)

            self.status_changed.emit("Failed to start")
            return False

        except Exception as e:
            print(f"Error starting ZAP: {e}")
            self.status_changed.emit("Error")
            return False

    def start_spider(self, target_url: str):
        """Start spider scan on target URL"""
        if not self.connected:
            return

        try:
            url = f"http://{self.zap_host}:{self.zap_port}/JSON/spider/action/scan/"
            params = {"url": target_url}
            if self.zap_api_key:
                params['apikey'] = self.zap_api_key

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                scan_id = response.json().get('scan', '0')
                print(f"Started spider scan with ID: {scan_id}")

                # Monitor progress in background
                self._monitor_scan_progress("spider", scan_id)

        except Exception as e:
            print(f"Error starting spider scan: {e}")

    def start_active_scan(self, target_url: str):
        """Start active scan on target URL"""
        if not self.connected:
            return

        try:
            url = f"http://{self.zap_host}:{self.zap_port}/JSON/ascan/action/scan/"
            params = {"url": target_url}
            if self.zap_api_key:
                params['apikey'] = self.zap_api_key

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                scan_id = response.json().get('scan', '0')
                print(f"Started active scan with ID: {scan_id}")

                # Monitor progress in background
                self._monitor_scan_progress("ascan", scan_id)

        except Exception as e:
            print(f"Error starting active scan: {e}")

    def _monitor_scan_progress(self, scan_type: str, scan_id: str):
        """Monitor scan progress and emit signals"""
        try:
            while True:
                url = f"http://{self.zap_host}:{self.zap_port}/JSON/{scan_type}/view/status/"
                params = {"scanId": scan_id}
                if self.zap_api_key:
                    params['apikey'] = self.zap_api_key

                response = requests.get(url, params=params, timeout=5)

                if response.status_code == 200:
                    status = response.json().get('status', '0')
                    progress = int(status)
                    self.scan_progress.emit(progress)

                    if progress >= 100:
                        break

                time.sleep(2)

        except Exception as e:
            print(f"Error monitoring scan progress: {e}")

    def stop_zap(self):
        """Stop ZAP daemon"""
        if self.zap_process:
            try:
                self.zap_process.terminate()
                self.zap_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.zap_process.kill()

        self.connected = False
        self.status_changed.emit("Disconnected")

    def get_alerts(self, baseurl: Optional[str] = None):
        """Get alerts from ZAP"""
        if not self.connected:
            return []

        try:
            url = f"http://{self.zap_host}:{self.zap_port}/JSON/core/view/alerts/"
            params = {}
            if baseurl:
                params['baseurl'] = baseurl
            if self.zap_api_key:
                params['apikey'] = self.zap_api_key

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json().get('alerts', [])
            return []

        except Exception as e:
            print(f"Error getting alerts: {e}")
            return []