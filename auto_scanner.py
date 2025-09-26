"""
Automated Scanner - Run multiple scans automatically based on intelligence
"""

import time
import threading
from datetime import datetime
from typing import Dict, List, Optional
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import json

class AutoScanWorker(QThread):
    """Worker thread for automated scanning"""
    
    scan_started = pyqtSignal(str, dict)  # target_url, scan_config
    scan_progress = pyqtSignal(str, int, str)  # target_url, progress, message
    scan_completed = pyqtSignal(str, dict)  # target_url, results
    scan_error = pyqtSignal(str, str)  # target_url, error_message
    all_scans_completed = pyqtSignal(dict)  # summary_results
    
    def __init__(self, scanner_engine, targets_queue):
        super().__init__()
        self.scanner_engine = scanner_engine
        self.targets_queue = targets_queue
        self.is_running = False
        self.current_target = None
        self.results = {}
    
    def run(self):
        """Run automated scans"""
        self.is_running = True
        
        for i, target_config in enumerate(self.targets_queue):
            if not self.is_running:
                break
            
            target_url = target_config['target_url']
            self.current_target = target_url
            
            try:
                # Emit scan started signal
                self.scan_started.emit(target_url, target_config)
                
                # Configure scanner for this target
                scan_config = self.prepare_scan_config(target_config)
                
                # Start scan
                self.scanner_engine.start_scan(scan_config)
                
                # Monitor scan progress
                self.monitor_scan_progress(target_url, i + 1, len(self.targets_queue))
                
                # Wait for scan completion (with timeout)
                timeout = 300  # 5 minutes per target
                start_time = time.time()
                
                while self.scanner_engine.is_scanning and (time.time() - start_time) < timeout:
                    if not self.is_running:
                        break
                    time.sleep(1)
                
                # Collect results
                scan_results = self.collect_scan_results(target_url)
                self.results[target_url] = scan_results
                
                self.scan_completed.emit(target_url, scan_results)
                
                # Brief pause between scans
                if i < len(self.targets_queue) - 1:
                    time.sleep(5)
                    
            except Exception as e:
                self.scan_error.emit(target_url, str(e))
                continue
        
        # Emit completion signal with summary
        summary = self.generate_summary()
        self.all_scans_completed.emit(summary)
        
        self.is_running = False
    
    def prepare_scan_config(self, target_config):
        """Prepare scan configuration for target"""
        recommended_scans = target_config.get('recommended_scans', [])
        
        scan_config = {
            'target_url': target_config['target_url'],
            'threads': 10,
            'timeout': 30,
            'directory_scan': 'directory_fuzzing' in recommended_scans,
            'subdomain_scan': 'subdomain_enumeration' in recommended_scans,
            'jwt_analysis': 'jwt_analysis' in recommended_scans,
            'admin_panel': 'admin_panel_discovery' in recommended_scans,
            'bypass_redirects': True,
            'wordlist': 'Default'
        }
        
        return scan_config
    
    def monitor_scan_progress(self, target_url, current_scan, total_scans):
        """Monitor individual scan progress"""
        while self.scanner_engine.is_scanning and self.is_running:
            # Calculate overall progress
            base_progress = ((current_scan - 1) / total_scans) * 100
            scan_progress = base_progress + (20 / total_scans)  # Assume 20% per scan step
            
            message = f"Scanning {target_url} ({current_scan}/{total_scans})"
            self.scan_progress.emit(target_url, int(scan_progress), message)
            
            time.sleep(2)
    
    def collect_scan_results(self, target_url):
        """Collect scan results for target"""
        # This would collect actual results from the scanner
        # For now, return placeholder results
        return {
            'target_url': target_url,
            'scan_completed_at': datetime.now().isoformat(),
            'vulnerabilities_found': [],
            'endpoints_discovered': [],
            'subdomains_found': [],
            'admin_panels_found': []
        }
    
    def generate_summary(self):
        """Generate summary of all scans"""
        total_targets = len(self.results)
        total_vulnerabilities = sum(len(r.get('vulnerabilities_found', [])) for r in self.results.values())
        
        return {
            'total_targets_scanned': total_targets,
            'total_vulnerabilities_found': total_vulnerabilities,
            'scan_completed_at': datetime.now().isoformat(),
            'results': self.results
        }
    
    def stop(self):
        """Stop the automated scanning"""
        self.is_running = False
        if self.scanner_engine.is_scanning:
            self.scanner_engine.stop_scan()

class AutoScanner(QObject):
    """Main automated scanner controller"""
    
    scan_queue_updated = pyqtSignal(list)
    scan_started = pyqtSignal(str)
    scan_progress = pyqtSignal(int, str)
    scan_completed = pyqtSignal(dict)
    
    def __init__(self, config_manager, scanner_engine):
        super().__init__()
        self.config_manager = config_manager
        self.scanner_engine = scanner_engine
        self.scan_queue = []
        self.current_worker = None
        self.is_auto_scanning = False
    
    def add_targets_to_queue(self, targets: List[Dict]):
        """Add targets to auto-scan queue"""
        for target in targets:
            if target not in self.scan_queue:
                self.scan_queue.append(target)
        
        self.scan_queue_updated.emit(self.scan_queue)
    
    def start_auto_scan(self):
        """Start automated scanning of queued targets"""
        if not self.scan_queue:
            return False
        
        if self.is_auto_scanning:
            return False
        
        self.is_auto_scanning = True
        
        # Start worker thread
        self.current_worker = AutoScanWorker(self.scanner_engine, self.scan_queue.copy())
        
        # Connect signals
        self.current_worker.scan_started.connect(self.on_scan_started)
        self.current_worker.scan_progress.connect(self.on_scan_progress)
        self.current_worker.scan_completed.connect(self.on_scan_completed)
        self.current_worker.scan_error.connect(self.on_scan_error)
        self.current_worker.all_scans_completed.connect(self.on_all_scans_completed)
        
        self.current_worker.start()
        return True
    
    def stop_auto_scan(self):
        """Stop automated scanning"""
        self.is_auto_scanning = False
        
        if self.current_worker:
            self.current_worker.stop()
            self.current_worker.wait()
    
    def on_scan_started(self, target_url, scan_config):
        """Handle scan started"""
        self.scan_started.emit(f"Started scanning {target_url}")
    
    def on_scan_progress(self, target_url, progress, message):
        """Handle scan progress"""
        self.scan_progress.emit(progress, message)
    
    def on_scan_completed(self, target_url, results):
        """Handle individual scan completion"""
        print(f"✅ Completed scan for {target_url}")
        
        # Log results
        vuln_count = len(results.get('vulnerabilities_found', []))
        if vuln_count > 0:
            print(f"   🎯 Found {vuln_count} potential vulnerabilities")
    
    def on_scan_error(self, target_url, error_message):
        """Handle scan error"""
        print(f"❌ Scan error for {target_url}: {error_message}")
    
    def on_all_scans_completed(self, summary):
        """Handle all scans completion"""
        self.is_auto_scanning = False
        self.scan_completed.emit(summary)
        
        print(f"🎉 Auto-scan completed!")
        print(f"   Targets scanned: {summary['total_targets_scanned']}")
        print(f"   Vulnerabilities found: {summary['total_vulnerabilities_found']}")
    
    def clear_queue(self):
        """Clear the scan queue"""
        self.scan_queue.clear()
        self.scan_queue_updated.emit(self.scan_queue)
    
    def remove_target_from_queue(self, target_url):
        """Remove specific target from queue"""
        self.scan_queue = [t for t in self.scan_queue if t.get('target_url') != target_url]
        self.scan_queue_updated.emit(self.scan_queue)
    
    def get_queue_status(self):
        """Get current queue status"""
        return {
            'queue_length': len(self.scan_queue),
            'is_scanning': self.is_auto_scanning,
            'current_target': self.current_worker.current_target if self.current_worker else None
        }