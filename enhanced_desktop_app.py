#!/usr/bin/env python3
"""
Enhanced Desktop Application - Robust Bug Bounty Hunter Pro for Parrot Linux
33x More Robust with Comprehensive Testing Capabilities
"""

import sys
import os
import json
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QLineEdit, QPushButton, QLabel, QProgressBar,
    QTableWidget, QTableWidgetItem, QComboBox, QCheckBox, QSpinBox,
    QGroupBox, QScrollArea, QSplitter, QTreeWidget, QTreeWidgetItem,
    QMessageBox, QFileDialog, QDialog, QDialogButtonBox, QFormLayout,
    QListWidget, QListWidgetItem, QFrame, QGridLayout, QSlider,
    QTextBrowser, QMenuBar, QMenu, QStatusBar, QToolBar
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QSettings, QSize, QRect
)
from PyQt6.QtGui import (
    QFont, QIcon, QPixmap, QPalette, QColor, QTextCursor, QAction
)

# Import our enhanced modules
from enhanced_xss_engine import EnhancedXSSEngine
from tool_integrations import ToolIntegrations
from enhanced_wordlists import get_all_endpoints, get_all_parameters, get_all_payloads
from auth_manager import AuthManager
from config_manager import ConfigManager

class EducationalDisclaimerDialog(QDialog):
    """Educational use disclaimer dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Educational Use Only - Important Notice")
        self.setModal(True)
        self.setFixedSize(600, 400)
        
        layout = QVBoxLayout()
        
        # Warning icon and title
        title_layout = QHBoxLayout()
        title_label = QLabel("⚠️ EDUCATIONAL USE ONLY")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ff6b35;")
        title_layout.addWidget(title_label)
        layout.addLayout(title_layout)
        
        # Disclaimer text
        disclaimer_text = QTextBrowser()
        disclaimer_content = """
<h3 style="color: #d32f2f;">IMPORTANT LEGAL NOTICE</h3>

<p><strong>This tool is designed exclusively for educational purposes and authorized security testing.</strong></p>

<h4>PERMITTED USES:</h4>
<ul>
<li>✅ Learning about web application security</li>
<li>✅ Testing applications you own or have explicit permission to test</li>
<li>✅ Authorized penetration testing with proper documentation</li>
<li>✅ Security research in controlled environments</li>
<li>✅ Educational demonstrations and training</li>
</ul>

<h4>PROHIBITED USES:</h4>
<ul>
<li>❌ Testing applications without explicit permission</li>
<li>❌ Unauthorized access to systems or data</li>
<li>❌ Malicious activities or attacks</li>
<li>❌ Violating terms of service or laws</li>
<li>❌ Any illegal or unethical activities</li>
</ul>

<h4>USER RESPONSIBILITIES:</h4>
<p>By using this tool, you agree to:</p>
<ul>
<li>Use it only for legitimate, authorized purposes</li>
<li>Comply with all applicable laws and regulations</li>
<li>Obtain proper authorization before testing any systems</li>
<li>Respect the privacy and security of others</li>
<li>Use the tool responsibly and ethically</li>
</ul>

<p style="color: #d32f2f;"><strong>The developers of this tool are not responsible for any misuse or illegal activities performed with this software.</strong></p>

<p><em>Remember: With great power comes great responsibility. Use your skills to make the internet safer for everyone.</em></p>
        """
        disclaimer_text.setHtml(disclaimer_content)
        layout.addWidget(disclaimer_text)
        
        # Checkbox for agreement
        self.agree_checkbox = QCheckBox("I understand and agree to use this tool only for educational and authorized purposes")
        self.agree_checkbox.stateChanged.connect(self.on_agreement_changed)
        layout.addWidget(self.agree_checkbox)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.ok_button.setText("I Agree - Continue")
        self.ok_button.setEnabled(False)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def on_agreement_changed(self, state):
        """Enable/disable OK button based on agreement"""
        self.ok_button.setEnabled(state == Qt.CheckState.Checked.value)

class ScanWorker(QThread):
    """Worker thread for running scans"""
    
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, scan_type: str, target: str, parameters: Dict):
        super().__init__()
        self.scan_type = scan_type
        self.target = target
        self.parameters = parameters
        self.is_running = True
    
    def run(self):
        """Run the scan based on type"""
        try:
            if self.scan_type == "xss":
                self.run_xss_scan()
            elif self.scan_type == "url_discovery":
                self.run_url_discovery()
            elif self.scan_type == "secrets_hunting":
                self.run_secrets_hunting()
            elif self.scan_type == "comprehensive":
                self.run_comprehensive_scan()
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def run_xss_scan(self):
        """Run XSS scan"""
        self.status_updated.emit("Initializing XSS engine...")
        xss_engine = EnhancedXSSEngine(
            max_threads=self.parameters.get('threads', 5),
            timeout=self.parameters.get('timeout', 10)
        )
        
        self.progress_updated.emit(20)
        self.status_updated.emit("Starting XSS scan...")
        
        test_params = self.parameters.get('parameters', get_all_parameters()[:20])
        methods = self.parameters.get('methods', ['GET', 'POST'])
        
        results = xss_engine.comprehensive_xss_scan(self.target, test_params, methods)
        
        self.progress_updated.emit(100)
        self.status_updated.emit("XSS scan completed")
        self.result_ready.emit(results)
    
    def run_url_discovery(self):
        """Run URL discovery"""
        self.status_updated.emit("Initializing tool integrations...")
        tools = ToolIntegrations()
        
        self.progress_updated.emit(30)
        self.status_updated.emit("Running URL discovery...")
        
        results = tools.comprehensive_url_discovery(self.target)
        
        self.progress_updated.emit(100)
        self.status_updated.emit("URL discovery completed")
        self.result_ready.emit(results)
    
    def run_secrets_hunting(self):
        """Run secrets hunting"""
        self.status_updated.emit("Initializing secrets hunting...")
        tools = ToolIntegrations()
        
        self.progress_updated.emit(20)
        self.status_updated.emit("Running automated secrets hunting...")
        
        results = tools.automated_secrets_hunting(self.target)
        
        self.progress_updated.emit(100)
        self.status_updated.emit("Secrets hunting completed")
        self.result_ready.emit(results)
    
    def run_comprehensive_scan(self):
        """Run comprehensive scan"""
        self.status_updated.emit("Starting comprehensive scan...")
        
        # URL Discovery
        self.progress_updated.emit(10)
        self.status_updated.emit("Phase 1: URL Discovery...")
        tools = ToolIntegrations()
        url_results = tools.comprehensive_url_discovery(self.target)
        
        # XSS Testing
        self.progress_updated.emit(40)
        self.status_updated.emit("Phase 2: XSS Testing...")
        xss_engine = EnhancedXSSEngine(max_threads=3)
        xss_results = xss_engine.comprehensive_xss_scan(
            self.target, 
            get_all_parameters()[:15], 
            ['GET', 'POST']
        )
        
        # Secrets Hunting
        self.progress_updated.emit(70)
        self.status_updated.emit("Phase 3: Secrets Hunting...")
        secrets_results = tools.automated_secrets_hunting(self.target)
        
        # Combine results
        comprehensive_results = {
            'target': self.target,
            'url_discovery': url_results,
            'xss_testing': xss_results,
            'secrets_hunting': secrets_results,
            'scan_time': time.time()
        }
        
        self.progress_updated.emit(100)
        self.status_updated.emit("Comprehensive scan completed")
        self.result_ready.emit(comprehensive_results)
    
    def stop(self):
        """Stop the scan"""
        self.is_running = False
        self.terminate()

class EnhancedDesktopApp(QMainWindow):
    """Enhanced Desktop Application for Bug Bounty Hunting"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bug Bounty Hunter Pro - Enhanced Edition (Educational Use Only)")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize components
        self.config_manager = ConfigManager()
        self.auth_manager = AuthManager("data/users.json")
        self.current_scan_worker = None
        self.scan_results = {}
        
        # Show educational disclaimer
        if not self.show_educational_disclaimer():
            sys.exit()
        
        # Setup UI
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.setup_toolbar()
        
        # Apply dark theme
        self.apply_dark_theme()
        
        # Load settings
        self.load_settings()
    
    def show_educational_disclaimer(self) -> bool:
        """Show educational disclaimer dialog"""
        disclaimer = EducationalDisclaimerDialog(self)
        return disclaimer.exec() == QDialog.DialogCode.Accepted
    
    def setup_ui(self):
        """Setup the main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Configuration and Tools
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Results and Output
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 1000])
    
    def create_left_panel(self) -> QWidget:
        """Create left configuration panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Target configuration
        target_group = QGroupBox("🎯 Target Configuration")
        target_layout = QVBoxLayout(target_group)
        
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("https://example.com")
        target_layout.addWidget(QLabel("Target URL:"))
        target_layout.addWidget(self.target_input)
        
        layout.addWidget(target_group)
        
        # Scan options
        options_group = QGroupBox("⚙️ Scan Options")
        options_layout = QFormLayout(options_group)
        
        self.threads_spinbox = QSpinBox()
        self.threads_spinbox.setRange(1, 20)
        self.threads_spinbox.setValue(5)
        options_layout.addRow("Threads:", self.threads_spinbox)
        
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setRange(5, 60)
        self.timeout_spinbox.setValue(10)
        options_layout.addRow("Timeout (s):", self.timeout_spinbox)
        
        self.methods_combo = QComboBox()
        self.methods_combo.addItems(["GET", "POST", "Both"])
        self.methods_combo.setCurrentText("Both")
        options_layout.addRow("HTTP Methods:", self.methods_combo)
        
        layout.addWidget(options_group)
        
        # Scan types
        scan_group = QGroupBox("🔍 Scan Types")
        scan_layout = QVBoxLayout(scan_group)
        
        self.xss_scan_btn = QPushButton("🚨 XSS Vulnerability Scan")
        self.xss_scan_btn.clicked.connect(lambda: self.start_scan("xss"))
        scan_layout.addWidget(self.xss_scan_btn)
        
        self.url_discovery_btn = QPushButton("🔗 URL Discovery (GAU)")
        self.url_discovery_btn.clicked.connect(lambda: self.start_scan("url_discovery"))
        scan_layout.addWidget(self.url_discovery_btn)
        
        self.secrets_btn = QPushButton("🔐 Secrets Hunting")
        self.secrets_btn.clicked.connect(lambda: self.start_scan("secrets_hunting"))
        scan_layout.addWidget(self.secrets_btn)
        
        self.comprehensive_btn = QPushButton("🎯 Comprehensive Scan")
        self.comprehensive_btn.clicked.connect(lambda: self.start_scan("comprehensive"))
        scan_layout.addWidget(self.comprehensive_btn)
        
        layout.addWidget(scan_group)
        
        # Tool status
        tools_group = QGroupBox("🛠️ Tool Status")
        tools_layout = QVBoxLayout(tools_group)
        
        self.tool_status_list = QListWidget()
        self.update_tool_status()
        tools_layout.addWidget(self.tool_status_list)
        
        self.install_tools_btn = QPushButton("📦 Install Missing Tools")
        self.install_tools_btn.clicked.connect(self.install_tools)
        tools_layout.addWidget(self.install_tools_btn)
        
        layout.addWidget(tools_group)
        
        # Progress
        progress_group = QGroupBox("📊 Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        progress_layout.addWidget(self.status_label)
        
        self.stop_scan_btn = QPushButton("⏹️ Stop Scan")
        self.stop_scan_btn.clicked.connect(self.stop_scan)
        self.stop_scan_btn.setEnabled(False)
        progress_layout.addWidget(self.stop_scan_btn)
        
        layout.addWidget(progress_group)
        
        layout.addStretch()
        return panel
    
    def create_right_panel(self) -> QWidget:
        """Create right results panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Results tabs
        self.results_tabs = QTabWidget()
        
        # XSS Results tab
        self.xss_results_tab = self.create_xss_results_tab()
        self.results_tabs.addTab(self.xss_results_tab, "🚨 XSS Results")
        
        # URL Discovery tab
        self.url_results_tab = self.create_url_results_tab()
        self.results_tabs.addTab(self.url_results_tab, "🔗 URL Discovery")
        
        # Secrets tab
        self.secrets_results_tab = self.create_secrets_results_tab()
        self.results_tabs.addTab(self.secrets_results_tab, "🔐 Secrets")
        
        # Raw output tab
        self.raw_output_tab = QTextEdit()
        self.raw_output_tab.setFont(QFont("Consolas", 10))
        self.results_tabs.addTab(self.raw_output_tab, "📄 Raw Output")
        
        layout.addWidget(self.results_tabs)
        
        # Export buttons
        export_layout = QHBoxLayout()
        
        self.export_json_btn = QPushButton("💾 Export JSON")
        self.export_json_btn.clicked.connect(self.export_json)
        export_layout.addWidget(self.export_json_btn)
        
        self.export_html_btn = QPushButton("🌐 Export HTML")
        self.export_html_btn.clicked.connect(self.export_html)
        export_layout.addWidget(self.export_html_btn)
        
        self.clear_results_btn = QPushButton("🗑️ Clear Results")
        self.clear_results_btn.clicked.connect(self.clear_results)
        export_layout.addWidget(self.clear_results_btn)
        
        export_layout.addStretch()
        layout.addLayout(export_layout)
        
        return panel
    
    def create_xss_results_tab(self) -> QWidget:
        """Create XSS results tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Summary
        self.xss_summary_label = QLabel("No XSS scan results yet")
        layout.addWidget(self.xss_summary_label)
        
        # Results table
        self.xss_results_table = QTableWidget()
        self.xss_results_table.setColumnCount(6)
        self.xss_results_table.setHorizontalHeaderLabels([
            "Parameter", "Method", "Context", "Severity", "Payload", "Evidence"
        ])
        layout.addWidget(self.xss_results_table)
        
        return widget
    
    def create_url_results_tab(self) -> QWidget:
        """Create URL discovery results tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Summary
        self.url_summary_label = QLabel("No URL discovery results yet")
        layout.addWidget(self.url_summary_label)
        
        # URLs tree
        self.urls_tree = QTreeWidget()
        self.urls_tree.setHeaderLabels(["URLs", "Type", "Parameters"])
        layout.addWidget(self.urls_tree)
        
        return widget
    
    def create_secrets_results_tab(self) -> QWidget:
        """Create secrets results tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Summary
        self.secrets_summary_label = QLabel("No secrets scan results yet")
        layout.addWidget(self.secrets_summary_label)
        
        # Secrets tree
        self.secrets_tree = QTreeWidget()
        self.secrets_tree.setHeaderLabels(["Pattern", "Findings"])
        layout.addWidget(self.secrets_tree)
        
        return widget
    
    def setup_menu_bar(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Scan", self)
        new_action.triggered.connect(self.new_scan)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        check_tools_action = QAction("Check Tool Status", self)
        check_tools_action.triggered.connect(self.update_tool_status)
        tools_menu.addAction(check_tools_action)
        
        install_tools_action = QAction("Install Missing Tools", self)
        install_tools_action.triggered.connect(self.install_tools)
        tools_menu.addAction(install_tools_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        disclaimer_action = QAction("Educational Disclaimer", self)
        disclaimer_action.triggered.connect(self.show_educational_disclaimer)
        help_menu.addAction(disclaimer_action)
    
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready - Educational Use Only")
    
    def setup_toolbar(self):
        """Setup toolbar"""
        toolbar = self.addToolBar("Main")
        
        # Quick scan action
        quick_scan_action = QAction("🚀 Quick Scan", self)
        quick_scan_action.triggered.connect(lambda: self.start_scan("xss"))
        toolbar.addAction(quick_scan_action)
        
        toolbar.addSeparator()
        
        # Stop action
        stop_action = QAction("⏹️ Stop", self)
        stop_action.triggered.connect(self.stop_scan)
        toolbar.addAction(stop_action)
    
    def apply_dark_theme(self):
        """Apply dark theme to the application"""
        dark_stylesheet = """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QGroupBox {
            font-weight: bold;
            border: 2px solid #555555;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        QPushButton {
            background-color: #404040;
            border: 1px solid #555555;
            padding: 8px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QPushButton:pressed {
            background-color: #353535;
        }
        QLineEdit, QTextEdit, QComboBox, QSpinBox {
            background-color: #404040;
            border: 1px solid #555555;
            padding: 5px;
            border-radius: 3px;
        }
        QTableWidget {
            background-color: #353535;
            alternate-background-color: #404040;
        }
        QTreeWidget {
            background-color: #353535;
            alternate-background-color: #404040;
        }
        QTabWidget::pane {
            border: 1px solid #555555;
        }
        QTabBar::tab {
            background-color: #404040;
            padding: 8px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #555555;
        }
        """
        self.setStyleSheet(dark_stylesheet)
    
    def update_tool_status(self):
        """Update tool status display"""
        self.tool_status_list.clear()
        
        tools = ToolIntegrations()
        status = tools.check_tool_availability()
        
        for tool, available in status.items():
            item = QListWidgetItem()
            if available:
                item.setText(f"✅ {tool.upper()} - Available")
            else:
                item.setText(f"❌ {tool.upper()} - Not Available")
            self.tool_status_list.addItem(item)
    
    def install_tools(self):
        """Install missing tools"""
        self.status_label.setText("Installing tools...")
        
        def install_worker():
            tools = ToolIntegrations()
            results = tools.install_missing_tools()
            
            # Update UI in main thread
            QTimer.singleShot(0, lambda: self.on_tools_installed(results))
        
        threading.Thread(target=install_worker, daemon=True).start()
    
    def on_tools_installed(self, results: Dict[str, str]):
        """Handle tool installation results"""
        self.status_label.setText("Tool installation completed")
        self.update_tool_status()
        
        # Show results
        message = "Tool Installation Results:\n\n"
        for tool, result in results.items():
            message += f"{tool}: {result}\n"
        
        QMessageBox.information(self, "Installation Results", message)
    
    def start_scan(self, scan_type: str):
        """Start a scan"""
        target = self.target_input.text().strip()
        if not target:
            QMessageBox.warning(self, "Warning", "Please enter a target URL")
            return
        
        if not target.startswith(('http://', 'https://')):
            target = 'https://' + target
            self.target_input.setText(target)
        
        # Prepare parameters
        methods = []
        if self.methods_combo.currentText() == "GET":
            methods = ["GET"]
        elif self.methods_combo.currentText() == "POST":
            methods = ["POST"]
        else:
            methods = ["GET", "POST"]
        
        parameters = {
            'threads': self.threads_spinbox.value(),
            'timeout': self.timeout_spinbox.value(),
            'methods': methods,
            'parameters': get_all_parameters()[:30]  # Limit for performance
        }
        
        # Start scan worker
        self.current_scan_worker = ScanWorker(scan_type, target, parameters)
        self.current_scan_worker.progress_updated.connect(self.progress_bar.setValue)
        self.current_scan_worker.status_updated.connect(self.status_label.setText)
        self.current_scan_worker.result_ready.connect(self.on_scan_completed)
        self.current_scan_worker.error_occurred.connect(self.on_scan_error)
        
        # Update UI
        self.progress_bar.setValue(0)
        self.stop_scan_btn.setEnabled(True)
        self.disable_scan_buttons()
        
        # Start scan
        self.current_scan_worker.start()
        self.status_bar.showMessage(f"Running {scan_type} scan on {target}")
    
    def stop_scan(self):
        """Stop current scan"""
        if self.current_scan_worker:
            self.current_scan_worker.stop()
            self.current_scan_worker = None
        
        self.progress_bar.setValue(0)
        self.status_label.setText("Scan stopped")
        self.stop_scan_btn.setEnabled(False)
        self.enable_scan_buttons()
        self.status_bar.showMessage("Ready")
    
    def on_scan_completed(self, results: Dict):
        """Handle scan completion"""
        self.scan_results = results
        self.stop_scan_btn.setEnabled(False)
        self.enable_scan_buttons()
        
        # Update results display
        if 'vulnerabilities' in results:
            self.update_xss_results(results)
        elif 'total_urls' in results:
            self.update_url_results(results)
        elif 'secrets_found' in results:
            self.update_secrets_results(results)
        elif 'xss_testing' in results:
            self.update_comprehensive_results(results)
        
        # Update raw output
        self.raw_output_tab.setPlainText(json.dumps(results, indent=2))
        
        self.status_bar.showMessage("Scan completed successfully")
    
    def on_scan_error(self, error: str):
        """Handle scan error"""
        self.stop_scan_btn.setEnabled(False)
        self.enable_scan_buttons()
        self.status_label.setText(f"Error: {error}")
        self.status_bar.showMessage("Scan failed")
        
        QMessageBox.critical(self, "Scan Error", f"Scan failed with error:\n{error}")
    
    def update_xss_results(self, results: Dict):
        """Update XSS results display"""
        vulnerabilities = results.get('vulnerabilities', [])
        dom_vulns = results.get('dom_vulnerabilities', [])
        
        # Update summary
        total_vulns = len(vulnerabilities) + len(dom_vulns)
        self.xss_summary_label.setText(
            f"Found {total_vulns} XSS vulnerabilities "
            f"({len(vulnerabilities)} reflected/stored, {len(dom_vulns)} DOM-based)"
        )
        
        # Update table
        self.xss_results_table.setRowCount(total_vulns)
        
        row = 0
        for vuln in vulnerabilities:
            self.xss_results_table.setItem(row, 0, QTableWidgetItem(vuln.get('parameter', '')))
            self.xss_results_table.setItem(row, 1, QTableWidgetItem(vuln.get('method', '')))
            self.xss_results_table.setItem(row, 2, QTableWidgetItem(vuln.get('context', '')))
            self.xss_results_table.setItem(row, 3, QTableWidgetItem(vuln.get('severity', '')))
            self.xss_results_table.setItem(row, 4, QTableWidgetItem(vuln.get('payload', '')[:50] + '...'))
            self.xss_results_table.setItem(row, 5, QTableWidgetItem(vuln.get('evidence', '')[:50] + '...'))
            row += 1
        
        for vuln in dom_vulns:
            self.xss_results_table.setItem(row, 0, QTableWidgetItem('DOM XSS'))
            self.xss_results_table.setItem(row, 1, QTableWidgetItem('GET'))
            self.xss_results_table.setItem(row, 2, QTableWidgetItem('DOM'))
            self.xss_results_table.setItem(row, 3, QTableWidgetItem(vuln.get('severity', '')))
            self.xss_results_table.setItem(row, 4, QTableWidgetItem(vuln.get('payload', '')[:50] + '...'))
            self.xss_results_table.setItem(row, 5, QTableWidgetItem(vuln.get('evidence', '')[:50] + '...'))
            row += 1
        
        self.xss_results_table.resizeColumnsToContents()
        
        # Switch to XSS results tab
        self.results_tabs.setCurrentIndex(0)
    
    def update_url_results(self, results: Dict):
        """Update URL discovery results"""
        self.url_summary_label.setText(
            f"Discovered {results.get('total_urls', 0)} URLs "
            f"({results.get('js_urls', 0)} JavaScript files, "
            f"{results.get('parameter_urls', 0)} with parameters)"
        )
        
        # Clear and populate tree
        self.urls_tree.clear()
        
        # Add endpoints
        if results.get('endpoints_found'):
            endpoints_item = QTreeWidgetItem(["Interesting Endpoints", "Endpoint", ""])
            for endpoint in results['endpoints_found'][:50]:  # Limit display
                child = QTreeWidgetItem([endpoint, "Endpoint", ""])
                endpoints_item.addChild(child)
            self.urls_tree.addTopLevelItem(endpoints_item)
        
        # Add parameters
        if results.get('parameters_found'):
            params_item = QTreeWidgetItem(["Parameters Found", "Parameter", ""])
            for param in results['parameters_found'][:50]:  # Limit display
                child = QTreeWidgetItem([param, "Parameter", ""])
                params_item.addChild(child)
            self.urls_tree.addTopLevelItem(params_item)
        
        self.urls_tree.expandAll()
        
        # Switch to URL results tab
        self.results_tabs.setCurrentIndex(1)
    
    def update_secrets_results(self, results: Dict):
        """Update secrets results"""
        secrets = results.get('secrets_found', {})
        high_value = results.get('high_value_findings', [])
        
        self.secrets_summary_label.setText(
            f"Found {len(secrets)} secret patterns "
            f"({len(high_value)} high-value findings)"
        )
        
        # Clear and populate tree
        self.secrets_tree.clear()
        
        for pattern, findings in secrets.items():
            if findings and findings != ['Timeout occurred']:
                pattern_item = QTreeWidgetItem([pattern, f"{len(findings)} findings"])
                for finding in findings[:10]:  # Limit display
                    child = QTreeWidgetItem([finding[:100] + '...', "Finding"])
                    pattern_item.addChild(child)
                self.secrets_tree.addTopLevelItem(pattern_item)
        
        self.secrets_tree.expandAll()
        
        # Switch to secrets tab
        self.results_tabs.setCurrentIndex(2)
    
    def update_comprehensive_results(self, results: Dict):
        """Update comprehensive scan results"""
        # Update all tabs with respective results
        if 'xss_testing' in results:
            self.update_xss_results(results['xss_testing'])
        
        if 'url_discovery' in results:
            self.update_url_results(results['url_discovery'])
        
        if 'secrets_hunting' in results:
            self.update_secrets_results(results['secrets_hunting'])
    
    def disable_scan_buttons(self):
        """Disable scan buttons during scan"""
        self.xss_scan_btn.setEnabled(False)
        self.url_discovery_btn.setEnabled(False)
        self.secrets_btn.setEnabled(False)
        self.comprehensive_btn.setEnabled(False)
    
    def enable_scan_buttons(self):
        """Enable scan buttons after scan"""
        self.xss_scan_btn.setEnabled(True)
        self.url_discovery_btn.setEnabled(True)
        self.secrets_btn.setEnabled(True)
        self.comprehensive_btn.setEnabled(True)
    
    def export_json(self):
        """Export results as JSON"""
        if not self.scan_results:
            QMessageBox.warning(self, "Warning", "No results to export")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export JSON", f"scan_results_{int(time.time())}.json", "JSON Files (*.json)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.scan_results, f, indent=2)
                QMessageBox.information(self, "Success", f"Results exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def export_html(self):
        """Export results as HTML report"""
        if not self.scan_results:
            QMessageBox.warning(self, "Warning", "No results to export")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export HTML", f"scan_report_{int(time.time())}.html", "HTML Files (*.html)"
        )
        
        if filename:
            try:
                html_content = self.generate_html_report()
                with open(filename, 'w') as f:
                    f.write(html_content)
                QMessageBox.information(self, "Success", f"Report exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def generate_html_report(self) -> str:
        """Generate HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bug Bounty Hunter Pro - Scan Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
                .vulnerability {{ background: #ffebee; padding: 10px; margin: 10px 0; border-left: 4px solid #f44336; }}
                .high {{ border-left-color: #d32f2f; }}
                .medium {{ border-left-color: #ff9800; }}
                .low {{ border-left-color: #4caf50; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .disclaimer {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🛡️ Bug Bounty Hunter Pro - Scan Report</h1>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Target: {self.scan_results.get('target', 'N/A')}</p>
            </div>
            
            <div class="disclaimer">
                <h3>⚠️ EDUCATIONAL USE ONLY</h3>
                <p>This report was generated for educational purposes and authorized security testing only. 
                Do not use this information for malicious activities.</p>
            </div>
            
            <div class="section">
                <h2>📊 Scan Summary</h2>
                <pre>{json.dumps(self.scan_results, indent=2)}</pre>
            </div>
        </body>
        </html>
        """
        return html
    
    def clear_results(self):
        """Clear all results"""
        self.scan_results = {}
        self.xss_results_table.setRowCount(0)
        self.urls_tree.clear()
        self.secrets_tree.clear()
        self.raw_output_tab.clear()
        
        self.xss_summary_label.setText("No XSS scan results yet")
        self.url_summary_label.setText("No URL discovery results yet")
        self.secrets_summary_label.setText("No secrets scan results yet")
    
    def new_scan(self):
        """Start new scan"""
        self.clear_results()
        self.target_input.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("Ready")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>Bug Bounty Hunter Pro - Enhanced Edition</h2>
        <p><strong>Version:</strong> 2.0.0 (33x More Robust)</p>
        <p><strong>Purpose:</strong> Educational security testing tool</p>
        
        <h3>Features:</h3>
        <ul>
        <li>🚨 Advanced XSS Detection (33+ evasion techniques)</li>
        <li>🔗 Comprehensive URL Discovery (GAU integration)</li>
        <li>🔐 Automated Secrets Hunting (GF patterns)</li>
        <li>🛠️ Tool Integration (GAU, FFF, GF)</li>
        <li>📊 Detailed Reporting</li>
        <li>🎯 Multi-threaded Scanning</li>
        </ul>
        
        <h3>Supported Endpoints:</h3>
        <ul>
        <li>PHP (.php)</li>
        <li>ASP (.asp)</li>
        <li>ASP.NET (.aspx)</li>
        <li>ColdFusion (.cfm)</li>
        <li>Java (.jsp)</li>
        </ul>
        
        <p><strong>⚠️ EDUCATIONAL USE ONLY</strong></p>
        <p>This tool is designed for learning and authorized testing only.</p>
        """
        
        QMessageBox.about(self, "About Bug Bounty Hunter Pro", about_text)
    
    def load_settings(self):
        """Load application settings"""
        settings = QSettings("BugHunterPro", "Enhanced")
        
        # Restore window geometry
        geometry = settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        # Restore target
        target = settings.value("target", "")
        self.target_input.setText(target)
        
        # Restore scan options
        threads = settings.value("threads", 5, type=int)
        self.threads_spinbox.setValue(threads)
        
        timeout = settings.value("timeout", 10, type=int)
        self.timeout_spinbox.setValue(timeout)
    
    def save_settings(self):
        """Save application settings"""
        settings = QSettings("BugHunterPro", "Enhanced")
        
        # Save window geometry
        settings.setValue("geometry", self.saveGeometry())
        
        # Save target
        settings.setValue("target", self.target_input.text())
        
        # Save scan options
        settings.setValue("threads", self.threads_spinbox.value())
        settings.setValue("timeout", self.timeout_spinbox.value())
    
    def closeEvent(self, event):
        """Handle application close"""
        # Stop any running scans
        if self.current_scan_worker:
            self.current_scan_worker.stop()
        
        # Save settings
        self.save_settings()
        
        event.accept()

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Bug Bounty Hunter Pro - Enhanced")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("Educational Security Tools")
    
    # Set application icon (if available)
    try:
        app.setWindowIcon(QIcon("icon.png"))
    except:
        pass
    
    # Create and show main window
    window = EnhancedDesktopApp()
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()