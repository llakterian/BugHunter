"""
Intelligence Dashboard - GUI for bug bounty intelligence and automated target discovery
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QHeaderView, QTabWidget, QTextEdit, QProgressBar,
                            QGroupBox, QFormLayout, QSpinBox, QCheckBox,
                            QComboBox, QMessageBox, QSplitter, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QFont, QColor

from bounty_intelligence import BountyIntelligence
import json
from datetime import datetime

class IntelligenceWorker(QThread):
    """Worker thread for intelligence gathering"""
    progress_updated = pyqtSignal(int, str)
    intelligence_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, config_manager, days_back=30):
        super().__init__()
        self.config_manager = config_manager
        self.days_back = days_back
        self.intelligence = BountyIntelligence(config_manager)
    
    def run(self):
        """Run intelligence gathering"""
        try:
            self.progress_updated.emit(10, "Fetching recent bug bounty programs...")
            programs = self.intelligence.fetch_recent_programs(self.days_back)
            
            self.progress_updated.emit(40, "Analyzing vulnerability trends...")
            trends = self.intelligence.analyze_vulnerability_trends()
            
            self.progress_updated.emit(70, "Generating target suggestions...")
            suggestions = self.intelligence.suggest_targets(programs, trends)
            
            self.progress_updated.emit(90, "Preparing intelligence report...")
            report = self.intelligence.generate_intelligence_report()
            
            self.progress_updated.emit(100, "Intelligence gathering complete!")
            self.intelligence_ready.emit(report)
            
        except Exception as e:
            self.error_occurred.emit(str(e))

class IntelligenceDashboard(QWidget):
    """Main intelligence dashboard widget"""
    target_selected = pyqtSignal(str, list)  # target_url, recommended_scans
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.intelligence_data = {}
        self.worker = None
        
        self.setup_ui()
        self.setup_styling()
    
    def setup_ui(self):
        """Setup the intelligence dashboard UI"""
        layout = QVBoxLayout()
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Main content
        main_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Controls and status
        controls_panel = self.create_controls_panel()
        main_splitter.addWidget(controls_panel)
        
        # Results tabs
        results_tabs = self.create_results_tabs()
        main_splitter.addWidget(results_tabs)
        
        main_splitter.setSizes([150, 400])
        layout.addWidget(main_splitter)
        
        self.setLayout(layout)
    
    def create_header(self):
        """Create header with title and status"""
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        # Title
        title_label = QLabel("🎯 Bug Bounty Intelligence")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Status
        self.status_label = QLabel("Ready to gather intelligence")
        self.status_label.setFont(QFont("Arial", 10))
        header_layout.addWidget(self.status_label)
        
        return header_frame
    
    def create_controls_panel(self):
        """Create controls panel"""
        panel = QFrame()
        layout = QHBoxLayout(panel)
        
        # Intelligence gathering controls
        intel_group = QGroupBox("Intelligence Gathering")
        intel_layout = QFormLayout(intel_group)
        
        # Days back selector
        self.days_back_spin = QSpinBox()
        self.days_back_spin.setRange(1, 90)
        self.days_back_spin.setValue(30)
        self.days_back_spin.setSuffix(" days")
        intel_layout.addRow("Look back:", self.days_back_spin)
        
        # Platform selection
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["All Platforms", "HackerOne", "Bugcrowd", "Intigriti"])
        intel_layout.addRow("Platform:", self.platform_combo)
        
        # Gather intelligence button
        self.gather_btn = QPushButton("🔍 Gather Intelligence")
        self.gather_btn.clicked.connect(self.start_intelligence_gathering)
        intel_layout.addRow("", self.gather_btn)
        
        layout.addWidget(intel_group)
        
        # Auto-scan controls
        auto_group = QGroupBox("Automated Scanning")
        auto_layout = QFormLayout(auto_group)
        
        # Max targets
        self.max_targets_spin = QSpinBox()
        self.max_targets_spin.setRange(1, 50)
        self.max_targets_spin.setValue(10)
        auto_layout.addRow("Max targets:", self.max_targets_spin)
        
        # Auto-scan options
        self.auto_scan_cb = QCheckBox("Enable auto-scan")
        auto_layout.addRow("", self.auto_scan_cb)
        
        # Start auto-scan button
        self.auto_scan_btn = QPushButton("🚀 Start Auto-Scan")
        self.auto_scan_btn.clicked.connect(self.start_auto_scan)
        self.auto_scan_btn.setEnabled(False)
        auto_layout.addRow("", self.auto_scan_btn)
        
        layout.addWidget(auto_group)
        
        # Progress bar
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        progress_layout.addWidget(self.progress_label)
        
        layout.addWidget(progress_group)
        
        layout.addStretch()
        
        return panel
    
    def create_results_tabs(self):
        """Create results tabs"""
        self.tabs = QTabWidget()
        
        # Target suggestions tab
        self.targets_tab = self.create_targets_tab()
        self.tabs.addTab(self.targets_tab, "🎯 Target Suggestions")
        
        # Vulnerability trends tab
        self.trends_tab = self.create_trends_tab()
        self.tabs.addTab(self.trends_tab, "📈 Vulnerability Trends")
        
        # Intelligence report tab
        self.report_tab = self.create_report_tab()
        self.tabs.addTab(self.report_tab, "📊 Intelligence Report")
        
        # Auto-scan queue tab
        self.queue_tab = self.create_queue_tab()
        self.tabs.addTab(self.queue_tab, "🤖 Auto-Scan Queue")
        
        return self.tabs
    
    def create_targets_tab(self):
        """Create target suggestions tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Targets table
        self.targets_table = QTableWidget()
        self.targets_table.setColumnCount(7)
        self.targets_table.setHorizontalHeaderLabels([
            "Priority", "Target URL", "Program", "Platform", 
            "Bounty Range", "Vulnerability Potential", "Actions"
        ])
        
        # Make table responsive
        header = self.targets_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # URL column
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Program
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Platform
        
        self.targets_table.setAlternatingRowColors(True)
        self.targets_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.targets_table)
        
        return widget
    
    def create_trends_tab(self):
        """Create vulnerability trends tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Trends table
        self.trends_table = QTableWidget()
        self.trends_table.setColumnCount(4)
        self.trends_table.setHorizontalHeaderLabels([
            "Vulnerability Type", "Trend Score", "Recent Reports", "Recommended Scans"
        ])
        
        header = self.trends_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.trends_table)
        
        return widget
    
    def create_report_tab(self):
        """Create intelligence report tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Report text area
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.report_text)
        
        # Export button
        export_btn = QPushButton("📄 Export Report")
        export_btn.clicked.connect(self.export_report)
        layout.addWidget(export_btn)
        
        return widget
    
    def create_queue_tab(self):
        """Create auto-scan queue tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Queue table
        self.queue_table = QTableWidget()
        self.queue_table.setColumnCount(5)
        self.queue_table.setHorizontalHeaderLabels([
            "Status", "Target URL", "Program", "Scans", "Progress"
        ])
        
        header = self.queue_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.queue_table)
        
        return widget
    
    def setup_styling(self):
        """Apply styling to the dashboard"""
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 6px;
                color: white;
                padding: 8px 12px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #106ebe;
            }
            
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
            
            QTableWidget {
                background-color: #2d2d2d;
                border: 1px solid #555555;
                color: #ffffff;
                gridline-color: #555555;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #555555;
            }
            
            QTableWidget::item:selected {
                background-color: #0078d4;
            }
            
            QHeaderView::section {
                background-color: #3d3d3d;
                border: 1px solid #555555;
                padding: 8px;
                font-weight: bold;
            }
            
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #2d2d2d;
            }
            
            QTabBar::tab {
                background-color: #3d3d3d;
                border: 1px solid #555555;
                padding: 8px 16px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: #0078d4;
            }
        """)
    
    def start_intelligence_gathering(self):
        """Start intelligence gathering process"""
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Warning", "Intelligence gathering already in progress")
            return
        
        # Update UI
        self.gather_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Gathering intelligence...")
        
        # Start worker thread
        days_back = self.days_back_spin.value()
        self.worker = IntelligenceWorker(self.config_manager, days_back)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.intelligence_ready.connect(self.intelligence_gathered)
        self.worker.error_occurred.connect(self.intelligence_error)
        self.worker.start()
    
    def update_progress(self, value, message):
        """Update progress bar and message"""
        self.progress_bar.setValue(value)
        self.progress_label.setText(message)
        self.status_label.setText(message)
    
    def intelligence_gathered(self, report):
        """Handle intelligence gathering completion"""
        self.intelligence_data = report
        
        # Update UI
        self.gather_btn.setEnabled(True)
        self.auto_scan_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.clear()
        self.status_label.setText("Intelligence gathering complete")
        
        # Populate tables
        self.populate_targets_table(report.get('top_targets', []))
        self.populate_trends_table(report.get('summary', {}).get('trending_vulnerabilities', {}))
        self.populate_report_text(report)
        
        # Show summary
        summary = report.get('summary', {})
        QMessageBox.information(
            self, "Intelligence Complete",
            f"Found {summary.get('total_targets_found', 0)} targets from "
            f"{summary.get('total_programs_analyzed', 0)} programs.\n"
            f"{summary.get('high_priority_targets', 0)} high-priority targets identified."
        )
    
    def intelligence_error(self, error_message):
        """Handle intelligence gathering error"""
        self.gather_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.clear()
        self.status_label.setText("Intelligence gathering failed")
        
        QMessageBox.critical(self, "Error", f"Intelligence gathering failed:\n{error_message}")
    
    def populate_targets_table(self, targets):
        """Populate the targets table"""
        self.targets_table.setRowCount(len(targets))
        
        for row, target in enumerate(targets):
            # Priority score
            priority_score = target.get('program_score', 0) + target.get('vulnerability_potential', 0)
            priority_item = QTableWidgetItem(f"{priority_score:.2f}")
            
            # Color code by priority
            if priority_score > 1.5:
                priority_item.setBackground(QColor(76, 175, 80))  # Green
            elif priority_score > 1.0:
                priority_item.setBackground(QColor(255, 193, 7))  # Yellow
            else:
                priority_item.setBackground(QColor(244, 67, 54))  # Red
            
            self.targets_table.setItem(row, 0, priority_item)
            
            # Target URL
            url_item = QTableWidgetItem(target.get('target_url', ''))
            self.targets_table.setItem(row, 1, url_item)
            
            # Program name
            program_item = QTableWidgetItem(target.get('program_name', ''))
            self.targets_table.setItem(row, 2, program_item)
            
            # Platform
            platform_item = QTableWidgetItem(target.get('platform', '').title())
            self.targets_table.setItem(row, 3, platform_item)
            
            # Bounty range
            bounty_item = QTableWidgetItem(str(target.get('bounty_range', 'Unknown')))
            self.targets_table.setItem(row, 4, bounty_item)
            
            # Vulnerability potential
            potential_item = QTableWidgetItem(f"{target.get('vulnerability_potential', 0):.2f}")
            self.targets_table.setItem(row, 5, potential_item)
            
            # Actions button
            scan_btn = QPushButton("🔍 Scan")
            scan_btn.clicked.connect(lambda checked, t=target: self.scan_target(t))
            self.targets_table.setCellWidget(row, 6, scan_btn)
    
    def populate_trends_table(self, trends):
        """Populate the vulnerability trends table"""
        self.trends_table.setRowCount(len(trends))
        
        sorted_trends = sorted(trends.items(), key=lambda x: x[1], reverse=True)
        
        for row, (vuln_type, score) in enumerate(sorted_trends):
            # Vulnerability type
            type_item = QTableWidgetItem(vuln_type.replace('_', ' ').title())
            self.trends_table.setItem(row, 0, type_item)
            
            # Trend score
            score_item = QTableWidgetItem(f"{score:.3f}")
            
            # Color code by score
            if score > 0.7:
                score_item.setBackground(QColor(244, 67, 54))  # Red (hot)
            elif score > 0.4:
                score_item.setBackground(QColor(255, 193, 7))  # Yellow (warm)
            else:
                score_item.setBackground(QColor(76, 175, 80))  # Green (cool)
            
            self.trends_table.setItem(row, 1, score_item)
            
            # Recent reports (placeholder)
            reports_item = QTableWidgetItem("Multiple")
            self.trends_table.setItem(row, 2, reports_item)
            
            # Recommended scans
            scans = self.get_recommended_scans_for_vuln(vuln_type)
            scans_item = QTableWidgetItem(", ".join(scans))
            self.trends_table.setItem(row, 3, scans_item)
    
    def populate_report_text(self, report):
        """Populate the intelligence report text"""
        report_text = f"""
# Bug Bounty Intelligence Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total Programs Analyzed: {report.get('summary', {}).get('total_programs_analyzed', 0)}
- Total Targets Found: {report.get('summary', {}).get('total_targets_found', 0)}
- High Priority Targets: {report.get('summary', {}).get('high_priority_targets', 0)}

## Top Recommendations
"""
        
        recommendations = report.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            report_text += f"{i}. {rec}\n"
        
        report_text += "\n## Auto-Scan Ready Targets\n"
        auto_scan_targets = report.get('auto_scan_ready', [])
        for target in auto_scan_targets[:10]:
            report_text += f"- {target.get('target_url', '')} ({target.get('program_name', '')})\n"
        
        report_text += "\n## Trending Vulnerabilities\n"
        trends = report.get('summary', {}).get('trending_vulnerabilities', {})
        sorted_trends = sorted(trends.items(), key=lambda x: x[1], reverse=True)
        
        for vuln_type, score in sorted_trends[:5]:
            report_text += f"- {vuln_type.replace('_', ' ').title()}: {score:.3f}\n"
        
        self.report_text.setPlainText(report_text)
    
    def scan_target(self, target):
        """Initiate scan for selected target"""
        target_url = target.get('target_url', '')
        recommended_scans = target.get('recommended_scans', [])
        
        # Emit signal to main dashboard
        self.target_selected.emit(target_url, recommended_scans)
        
        # Show confirmation
        QMessageBox.information(
            self, "Scan Initiated",
            f"Scan initiated for {target_url}\n"
            f"Recommended scans: {', '.join(recommended_scans)}"
        )
    
    def start_auto_scan(self):
        """Start automated scanning of top targets"""
        if not self.intelligence_data:
            QMessageBox.warning(self, "Warning", "Please gather intelligence first")
            return
        
        auto_scan_targets = self.intelligence_data.get('auto_scan_ready', [])
        max_targets = self.max_targets_spin.value()
        
        if not auto_scan_targets:
            QMessageBox.information(self, "Info", "No targets ready for auto-scan")
            return
        
        # Populate auto-scan queue
        self.populate_queue_table(auto_scan_targets[:max_targets])
        
        # Switch to queue tab
        self.tabs.setCurrentWidget(self.queue_tab)
        
        QMessageBox.information(
            self, "Auto-Scan Started",
            f"Added {min(len(auto_scan_targets), max_targets)} targets to auto-scan queue"
        )
    
    def populate_queue_table(self, targets):
        """Populate the auto-scan queue table"""
        self.queue_table.setRowCount(len(targets))
        
        for row, target in enumerate(targets):
            # Status
            status_item = QTableWidgetItem("Queued")
            status_item.setBackground(QColor(255, 193, 7))  # Yellow
            self.queue_table.setItem(row, 0, status_item)
            
            # Target URL
            url_item = QTableWidgetItem(target.get('target_url', ''))
            self.queue_table.setItem(row, 1, url_item)
            
            # Program
            program_item = QTableWidgetItem(target.get('program_name', ''))
            self.queue_table.setItem(row, 2, program_item)
            
            # Scans
            scans_item = QTableWidgetItem(", ".join(target.get('recommended_scans', [])))
            self.queue_table.setItem(row, 3, scans_item)
            
            # Progress bar
            progress_bar = QProgressBar()
            progress_bar.setValue(0)
            self.queue_table.setCellWidget(row, 4, progress_bar)
    
    def export_report(self):
        """Export intelligence report"""
        if not self.intelligence_data:
            QMessageBox.warning(self, "Warning", "No intelligence data to export")
            return
        
        from PyQt6.QtWidgets import QFileDialog
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Intelligence Report", 
            f"intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json);;Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w') as f:
                        json.dump(self.intelligence_data, f, indent=2, default=str)
                else:
                    with open(filename, 'w') as f:
                        f.write(self.report_text.toPlainText())
                
                QMessageBox.information(self, "Success", f"Report exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export report: {str(e)}")
    
    def get_recommended_scans_for_vuln(self, vuln_type):
        """Get recommended scans for vulnerability type"""
        scan_mapping = {
            'jwt_vulnerabilities': ['JWT Analysis', 'Authentication Testing'],
            'directory_traversal': ['Directory Fuzzing', 'LFI Testing'],
            'sql_injection': ['SQL Injection Testing', 'Parameter Fuzzing'],
            'xss_vulnerabilities': ['XSS Testing', 'Parameter Fuzzing'],
            'admin_panel_exposure': ['Admin Panel Discovery', 'Directory Fuzzing'],
            'subdomain_takeover': ['Subdomain Enumeration', 'DNS Analysis']
        }
        
        return scan_mapping.get(vuln_type, ['General Scanning'])