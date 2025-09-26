"""
ZAP Manager - OWASP ZAP Integration
"""

import subprocess
import time
import requests
from PyQt6.QtCore import QObject, pyqtSignal, QThread, QTimer
from zapv2 import ZAPv2

class ZAPManager(QObject):
    status_changed = pyqtSignal(str)
    scan_progress = pyqtSignal(int, str)
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.zap = None
        self.zap_process = None
        self.is_connected = False
        
        # Get ZAP configuration
        self.zap_config = config_manager.get_zap_config()
        self.host = self.zap_config.get('host', '127.0.0.1')
        self.port = self.zap_config.get('port', 8080)
        self.api_key = self.zap_config.get('api_key', '')
        self.proxy_port = self.zap_config.get('proxy_port', 8081)
    
    def start_zap(self):
        """Start ZAP daemon"""
        try:
            # Check if ZAP is already running
            if self.is_zap_running():
                self.status_changed.emit("Already Running")
                return True
            
            # Start ZAP daemon
            zap_cmd = [
                'zaproxy',
                '-daemon',
                '-host', self.host,
                '-port', str(self.port),
                '-config', f'api.key={self.api_key}',
                '-config', 'api.addrs.addr.name=.*',
                '-config', 'api.addrs.addr.regex=true'
            ]
            
            self.zap_process = subprocess.Popen(
                zap_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for ZAP to start
            self.status_changed.emit("Starting...")
            
            # Check if ZAP started successfully
            for _ in range(30):  # Wait up to 30 seconds
                if self.is_zap_running():
                    self.status_changed.emit("Started")
                    return True
                time.sleep(1)
            
            self.status_changed.emit("Failed to Start")
            return False
            
        except Exception as e:
            print(f"Error starting ZAP: {e}")
            self.status_changed.emit("Error")
            return False
    
    def is_zap_running(self):
        """Check if ZAP is running"""
        try:
            response = requests.get(
                f'http://{self.host}:{self.port}',
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def connect(self):
        """Connect to ZAP"""
        try:
            # Initialize ZAP API client
            self.zap = ZAPv2(
                proxies={
                    'http': f'http://{self.host}:{self.port}',
                    'https': f'http://{self.host}:{self.port}'
                }
            )
            
            # Test connection
            version = self.zap.core.version
            self.is_connected = True
            self.status_changed.emit("Connected")
            return True
            
        except Exception as e:
            print(f"Error connecting to ZAP: {e}")
            self.is_connected = False
            self.status_changed.emit("Connection Failed")
            return False
    
    def disconnect(self):
        """Disconnect from ZAP"""
        self.zap = None
        self.is_connected = False
        self.status_changed.emit("Disconnected")
    
    def start_spider(self, target_url):
        """Start spider scan"""
        if not self.is_connected:
            return False
        
        try:
            # Start spider
            scan_id = self.zap.spider.scan(target_url)
            
            # Monitor spider progress
            self.monitor_spider_progress(scan_id)
            return True
            
        except Exception as e:
            print(f"Error starting spider: {e}")
            return False
    
    def monitor_spider_progress(self, scan_id):
        """Monitor spider scan progress"""
        def check_progress():
            try:
                status = int(self.zap.spider.status(scan_id))
                self.scan_progress.emit(status, f"Spider scan: {status}%")
                
                if status >= 100:
                    self.scan_progress.emit(100, "Spider scan completed")
                    timer.stop()
                    
            except Exception as e:
                print(f"Error checking spider progress: {e}")
                timer.stop()
        
        timer = QTimer()
        timer.timeout.connect(check_progress)
        timer.start(2000)  # Check every 2 seconds
    
    def start_active_scan(self, target_url):
        """Start active scan"""
        if not self.is_connected:
            return False
        
        try:
            # Start active scan
            scan_id = self.zap.ascan.scan(target_url)
            
            # Monitor active scan progress
            self.monitor_active_scan_progress(scan_id)
            return True
            
        except Exception as e:
            print(f"Error starting active scan: {e}")
            return False
    
    def monitor_active_scan_progress(self, scan_id):
        """Monitor active scan progress"""
        def check_progress():
            try:
                status = int(self.zap.ascan.status(scan_id))
                self.scan_progress.emit(status, f"Active scan: {status}%")
                
                if status >= 100:
                    self.scan_progress.emit(100, "Active scan completed")
                    timer.stop()
                    
            except Exception as e:
                print(f"Error checking active scan progress: {e}")
                timer.stop()
        
        timer = QTimer()
        timer.timeout.connect(check_progress)
        timer.start(3000)  # Check every 3 seconds
    
    def get_alerts(self):
        """Get security alerts from ZAP"""
        if not self.is_connected:
            return []
        
        try:
            alerts = self.zap.core.alerts()
            return alerts
        except Exception as e:
            print(f"Error getting alerts: {e}")
            return []
    
    def get_urls(self):
        """Get discovered URLs from ZAP"""
        if not self.is_connected:
            return []
        
        try:
            urls = self.zap.core.urls()
            return urls
        except Exception as e:
            print(f"Error getting URLs: {e}")
            return []
    
    def export_report(self, format_type="html"):
        """Export ZAP report"""
        if not self.is_connected:
            return None
        
        try:
            if format_type.lower() == "html":
                report = self.zap.core.htmlreport()
            elif format_type.lower() == "xml":
                report = self.zap.core.xmlreport()
            elif format_type.lower() == "json":
                report = self.zap.core.jsonreport()
            else:
                return None
            
            return report
            
        except Exception as e:
            print(f"Error exporting report: {e}")
            return None
    
    def set_proxy_config(self, target_url):
        """Configure ZAP as proxy for target"""
        if not self.is_connected:
            return False
        
        try:
            # Add target to context
            context_id = self.zap.context.new_context("BugBountyContext")
            self.zap.context.include_in_context("BugBountyContext", f"{target_url}.*")
            
            return True
            
        except Exception as e:
            print(f"Error setting proxy config: {e}")
            return False
    
    def stop_all_scans(self):
        """Stop all running scans"""
        if not self.is_connected:
            return False
        
        try:
            # Stop spider scans
            self.zap.spider.stop_all_scans()
            
            # Stop active scans
            self.zap.ascan.stop_all_scans()
            
            return True
            
        except Exception as e:
            print(f"Error stopping scans: {e}")
            return False
    
    def shutdown(self):
        """Shutdown ZAP"""
        if self.zap_process:
            self.zap_process.terminate()
            self.zap_process = None
        
        self.disconnect()
        self.status_changed.emit("Shutdown")