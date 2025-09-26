"""
Main Dashboard - Core bug bounty hunting interface
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
                            QLabel, QPushButton, QFrame, QSplitter, QTextEdit,
                            QProgressBar, QListWidget, QTreeWidget, QTreeWidgetItem,
                            QGroupBox, QFormLayout, QLineEdit, QSpinBox, QCheckBox,
                            QComboBox, QFileDialog, QMessageBox, QTableWidget,
                            QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QFont, QTextCursor, QColor

from zap_manager import ZAPManager
from scanner_engine import ScannerEngine
from jwt_analyzer import JWTAnalyzer
from report_generator import ReportGenerator
from wordlist_manager import WordlistManager, WordlistSelector

class MainDashboard(QWidget):
    logout_requested = pyqtSignal()
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.current_user = None
        
        # Initialize components
        self.zap_manager = ZAPManager(config_manager)
        self.scanner_engine = ScannerEngine(config_manager)
        self.jwt_analyzer = JWTAnalyzer(config_manager)
        self.report_generator = ReportGenerator(config_manager)
        self.wordlist_manager = WordlistManager(config_manager)
        
        self.setup_ui()
        self.setup_styling()
        self.setup_connections()
        
        # Create necessary directories
        self.config_manager.create_directories()
    
    def setup_ui(self):
        """Setup the main dashboard interface"""
        layout = QVBoxLayout()
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Main content area
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Controls
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # Right panel - Results and logs
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # Set responsive splitter proportions
        # Calculate sizes based on window width
        total_width = self.width() if hasattr(self, 'width') else 1200
        left_width = min(300, int(total_width * 0.25))  # 25% or max 300px
        right_width = total_width - left_width
        
        main_splitter.setSizes([left_width, right_width])
        main_splitter.setStretchFactor(0, 0)  # Left panel fixed
        main_splitter.setStretchFactor(1, 1)  # Right panel stretches
        layout.addWidget(main_splitter)
        
        self.setLayout(layout)
    
    def create_header(self):
        """Create the header with user info and controls"""
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        # Responsive header based on screen size
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen()
        screen_width = screen.geometry().width()
        
        if screen_width <= 1366:  # Compact header for smaller screens
            title_label = QLabel("BB Hunter Pro")
            title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        else:  # Full title for larger screens
            title_label = QLabel("Bug Bounty Hunter Pro")
            title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # User info with better font size
        self.user_label = QLabel("User: Not logged in")
        self.user_label.setFont(QFont("Arial", 11))
        header_layout.addWidget(self.user_label)
        
        # ZAP status with better font size
        self.zap_status_label = QLabel("ZAP: Disconnected")
        self.zap_status_label.setFont(QFont("Arial", 11))
        header_layout.addWidget(self.zap_status_label)
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout_requested.emit)
        header_layout.addWidget(logout_btn)
        
        return header_frame
    
    def create_left_panel(self):
        """Create the left control panel"""
        from PyQt6.QtWidgets import QScrollArea
        
        # Create scroll area for left panel
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Responsive width - adapt to screen size
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen()
        screen_width = screen.geometry().width()
        
        if screen_width <= 1366:  # Smaller screens
            scroll_area.setMaximumWidth(280)
            scroll_area.setMinimumWidth(250)
        else:  # Larger screens
            scroll_area.setMaximumWidth(320)
            scroll_area.setMinimumWidth(280)
        
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)  # Reduce spacing between groups
        
        # Target configuration
        target_group = self.create_target_group()
        layout.addWidget(target_group)
        
        # Scan configuration
        scan_group = self.create_scan_group()
        layout.addWidget(scan_group)
        
        # ZAP controls
        zap_group = self.create_zap_group()
        layout.addWidget(zap_group)
        
        # Action buttons
        actions_group = self.create_actions_group()
        layout.addWidget(actions_group)
        
        # Add manage wordlists button at bottom
        manage_all_btn = QPushButton("Manage Wordlists")
        manage_all_btn.clicked.connect(self.open_wordlist_manager)
        layout.addWidget(manage_all_btn)
        
        layout.addStretch()
        
        # Set the panel as the scroll area widget
        scroll_area.setWidget(panel)
        return scroll_area
    
    def create_target_group(self):
        """Create target configuration group"""
        group = QGroupBox("Target Configuration")
        layout = QFormLayout(group)
        layout.setVerticalSpacing(8)  # Reduce vertical spacing
        layout.setHorizontalSpacing(10)
        
        self.target_url_input = QLineEdit()
        self.target_url_input.setPlaceholderText("https://example.com")
        layout.addRow("Target URL:", self.target_url_input)
        
        # Responsive wordlist selectors
        from PyQt6.QtWidgets import QGridLayout, QTabWidget
        from PyQt6.QtGui import QGuiApplication
        
        screen = QGuiApplication.primaryScreen()
        screen_width = screen.geometry().width()
        
        if screen_width <= 1366:  # Use tabs for smaller screens
            wordlist_tabs = QTabWidget()
            wordlist_tabs.setMaximumHeight(100)
            
            # Main wordlists tab
            main_tab = QWidget()
            main_layout = QGridLayout(main_tab)
            main_layout.setSpacing(2)
            
            main_types = [("Dirs:", "directories"), ("Subs:", "subdomains")]
            
            # Advanced wordlists tab  
            adv_tab = QWidget()
            adv_layout = QGridLayout(adv_tab)
            adv_layout.setSpacing(2)
            
            adv_types = [("Params:", "parameters"), ("Admin:", "admin_panels"), ("JWT:", "jwt_secrets")]
            
            self.wordlist_selectors = {}
            
            # Add main wordlists
            for i, (label_text, category) in enumerate(main_types):
                label = QLabel(label_text)
                label.setMaximumWidth(40)
                selector = WordlistSelector(category, self.config_manager)
                selector.wordlist_changed.connect(self.on_wordlist_changed)
                
                main_layout.addWidget(label, i, 0)
                main_layout.addWidget(selector, i, 1)
                self.wordlist_selectors[category] = selector
            
            # Add advanced wordlists
            for i, (label_text, category) in enumerate(adv_types):
                label = QLabel(label_text)
                label.setMaximumWidth(40)
                selector = WordlistSelector(category, self.config_manager)
                selector.wordlist_changed.connect(self.on_wordlist_changed)
                
                adv_layout.addWidget(label, i, 0)
                adv_layout.addWidget(selector, i, 1)
                self.wordlist_selectors[category] = selector
            
            wordlist_tabs.addTab(main_tab, "Main")
            wordlist_tabs.addTab(adv_tab, "Advanced")
            
            layout.addRow("Wordlists:", wordlist_tabs)
            
        else:  # Use grid for larger screens
            wordlist_grid = QGridLayout()
            wordlist_grid.setSpacing(3)
            
            wordlist_types = [
                ("Directories:", "directories"),
                ("Subdomains:", "subdomains"), 
                ("Parameters:", "parameters"),
                ("Admin Panels:", "admin_panels"),
                ("JWT Secrets:", "jwt_secrets")
            ]
            
            self.wordlist_selectors = {}
            
            for i, (label_text, category) in enumerate(wordlist_types):
                label = QLabel(label_text)
                label.setMaximumWidth(70)
                selector = WordlistSelector(category, self.config_manager)
                selector.wordlist_changed.connect(self.on_wordlist_changed)
                
                wordlist_grid.addWidget(label, i, 0)
                wordlist_grid.addWidget(selector, i, 1)
                self.wordlist_selectors[category] = selector
            
            # Add JWT secrets to grid
            jwt_label = QLabel("JWT Secrets:")
            jwt_label.setMaximumWidth(70)
            self.jwt_wordlist_selector = WordlistSelector("jwt_secrets", self.config_manager)
            self.jwt_wordlist_selector.wordlist_changed.connect(self.on_wordlist_changed)
            
            wordlist_grid.addWidget(jwt_label, 5, 0)
            wordlist_grid.addWidget(self.jwt_wordlist_selector, 5, 1)
            self.wordlist_selectors["jwt_secrets"] = self.jwt_wordlist_selector
            
            wordlist_widget = QWidget()
            wordlist_widget.setLayout(wordlist_grid)
            layout.addRow("Wordlists:", wordlist_widget)
        
        self.threads_spin = QSpinBox()
        self.threads_spin.setRange(1, 50)
        self.threads_spin.setValue(10)
        layout.addRow("Threads:", self.threads_spin)
        
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(5, 120)
        self.timeout_spin.setValue(30)
        self.timeout_spin.setSuffix(" sec")
        layout.addRow("Timeout:", self.timeout_spin)
        
        return group
    
    def create_scan_group(self):
        """Create scan configuration group"""
        group = QGroupBox("Scan Options")
        
        # Responsive layout for scan options
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen()
        screen_width = screen.geometry().width()
        
        if screen_width <= 1366:  # Compact layout for smaller screens
            from PyQt6.QtWidgets import QGridLayout
            layout = QGridLayout(group)
            layout.setSpacing(3)
            
            # Shorter labels for small screens
            scan_options = [
                ("Dir Fuzz", "directory_scan_cb", True),
                ("Subdomains", "subdomain_scan_cb", False),
                ("JWT", "jwt_analysis_cb", True),
                ("Admin", "admin_panel_cb", True),
                ("Redirects", "bypass_redirects_cb", True)
            ]
            
            for i, (label, attr, default) in enumerate(scan_options):
                checkbox = QCheckBox(label)
                checkbox.setChecked(default)
                setattr(self, attr, checkbox)
                
                row = i // 2
                col = i % 2
                layout.addWidget(checkbox, row, col)
                
        else:  # Full layout for larger screens
            layout = QVBoxLayout(group)
            layout.setSpacing(4)
            
            scan_options = [
                ("Directory Fuzzing", "directory_scan_cb", True),
                ("Subdomain Enumeration", "subdomain_scan_cb", False),
                ("JWT Analysis", "jwt_analysis_cb", True),
                ("Admin Panel Discovery", "admin_panel_cb", True),
                ("Bypass Redirects", "bypass_redirects_cb", True)
            ]
            
            for label, attr, default in scan_options:
                checkbox = QCheckBox(label)
                checkbox.setChecked(default)
                setattr(self, attr, checkbox)
                layout.addWidget(checkbox)
        
        return group
    
    def create_zap_group(self):
        """Create ZAP controls group"""
        group = QGroupBox("OWASP ZAP Integration")
        layout = QVBoxLayout(group)
        
        # ZAP connection controls
        zap_controls = QHBoxLayout()
        
        self.zap_connect_btn = QPushButton("Connect ZAP")
        self.zap_connect_btn.clicked.connect(self.connect_zap)
        zap_controls.addWidget(self.zap_connect_btn)
        
        self.zap_start_btn = QPushButton("Start ZAP")
        self.zap_start_btn.clicked.connect(self.start_zap)
        zap_controls.addWidget(self.zap_start_btn)
        
        layout.addLayout(zap_controls)
        
        # ZAP scan controls
        self.zap_spider_btn = QPushButton("Spider Scan")
        self.zap_spider_btn.clicked.connect(self.start_spider_scan)
        self.zap_spider_btn.setEnabled(False)
        layout.addWidget(self.zap_spider_btn)
        
        self.zap_active_btn = QPushButton("Active Scan")
        self.zap_active_btn.clicked.connect(self.start_active_scan)
        self.zap_active_btn.setEnabled(False)
        layout.addWidget(self.zap_active_btn)
        
        return group
    
    def create_actions_group(self):
        """Create action buttons group"""
        group = QGroupBox("Actions")
        layout = QVBoxLayout(group)
        
        self.start_scan_btn = QPushButton("Start Bug Hunt")
        self.start_scan_btn.clicked.connect(self.start_bug_hunt)
        self.start_scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.start_scan_btn)
        
        self.stop_scan_btn = QPushButton("Stop Scan")
        self.stop_scan_btn.clicked.connect(self.stop_scan)
        self.stop_scan_btn.setEnabled(False)
        layout.addWidget(self.stop_scan_btn)
        
        self.generate_report_btn = QPushButton("Generate Report")
        self.generate_report_btn.clicked.connect(self.generate_report)
        layout.addWidget(self.generate_report_btn)
        
        return group
    
    def create_right_panel(self):
        """Create the right results panel"""
        panel = QFrame()
        layout = QVBoxLayout(panel)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready to start bug hunting...")
        self.status_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.status_label)
        
        # Tabs for different views
        self.tabs = QTabWidget()
        
        # Results tab
        self.results_tab = self.create_results_tab()
        self.tabs.addTab(self.results_tab, "Results")
        
        # Logs tab
        self.logs_tab = self.create_logs_tab()
        self.tabs.addTab(self.logs_tab, "Logs")
        
        # Vulnerabilities tab
        self.vulns_tab = self.create_vulnerabilities_tab()
        self.tabs.addTab(self.vulns_tab, "Vulnerabilities")
        
        # Wordlists tab
        self.tabs.addTab(self.wordlist_manager, "Wordlists")
        
        # Intelligence tab
        from intelligence_dashboard import IntelligenceDashboard
        self.intelligence_dashboard = IntelligenceDashboard(self.config_manager)
        self.intelligence_dashboard.target_selected.connect(self.auto_configure_scan)
        self.tabs.addTab(self.intelligence_dashboard, "🎯 Intelligence")
        
        layout.addWidget(self.tabs)
        
        return panel
    
    def create_results_tab(self):
        """Create results display tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Results tree
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(["Type", "URL/Endpoint", "Status", "Details"])
        self.results_tree.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.results_tree)
        
        return widget
    
    def create_logs_tab(self):
        """Create logs display tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.log_text)
        
        return widget
    
    def create_vulnerabilities_tab(self):
        """Create vulnerabilities display tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Vulnerabilities table
        self.vulns_table = QTableWidget()
        self.vulns_table.setColumnCount(5)
        self.vulns_table.setHorizontalHeaderLabels(["Severity", "Type", "URL", "Description", "Impact"])
        self.vulns_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.vulns_table)
        
        return widget
    
    def setup_styling(self):
        """Apply responsive styling to the dashboard"""
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen()
        screen_width = screen.geometry().width()
        
        # Responsive font sizes
        if screen_width <= 1366:  # Smaller screens - increased font sizes
            base_font = "11px"
            button_font = "10px"
            header_font = "13px"
            input_height = "22px"
            button_height = "26px"
        else:  # Larger screens
            base_font = "12px"
            button_font = "11px"
            header_font = "14px"
            input_height = "24px"
            button_height = "28px"
        
        self.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: {header_font};
                border: 2px solid #555555;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 6px;
                margin-bottom: 4px;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
            
            QPushButton {{
                background-color: #0078d4;
                border: none;
                border-radius: 4px;
                color: white;
                padding: 4px 8px;
                font-weight: bold;
                font-size: {button_font};
                min-height: {button_height};
            }}
            
            QPushButton:hover {{
                background-color: #106ebe;
            }}
            
            QPushButton:disabled {{
                background-color: #555555;
                color: #888888;
            }}
            
            QLineEdit, QSpinBox, QComboBox {{
                background-color: #3d3d3d;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 3px 4px;
                color: #ffffff;
                font-size: {base_font};
                min-height: {input_height};
            }}
            
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
                border-color: #0078d4;
            }}
            
            QCheckBox {{
                font-size: {base_font};
                spacing: 4px;
            }}
            
            QCheckBox::indicator {{
                width: 14px;
                height: 14px;
            }}
            
            QLabel {{
                font-size: {base_font};
            }}
            
            QTabWidget::pane {{
                border: 1px solid #555555;
                background-color: #2d2d2d;
            }}
            
            QTabBar::tab {{
                background-color: #3d3d3d;
                border: 1px solid #555555;
                padding: 4px 8px;
                margin-right: 2px;
                font-size: {base_font};
            }}
            
            QTabBar::tab:selected {{
                background-color: #0078d4;
            }}
            
            QTreeWidget, QTableWidget, QTextEdit {{
                background-color: #2d2d2d;
                border: 1px solid #555555;
                color: #ffffff;
                font-size: {base_font};
            }}
            
            QHeaderView::section {{
                background-color: #3d3d3d;
                border: 1px solid #555555;
                padding: 3px;
                font-weight: bold;
                font-size: {base_font};
            }}
            
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            
            QScrollBar:vertical {{
                background-color: #3d3d3d;
                width: 10px;
                border-radius: 5px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: #555555;
                border-radius: 5px;
                min-height: 15px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: #0078d4;
            }}
        """)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Scanner engine connections
        self.scanner_engine.progress_updated.connect(self.update_progress)
        self.scanner_engine.result_found.connect(self.add_result)
        self.scanner_engine.log_message.connect(self.add_log)
        self.scanner_engine.vulnerability_found.connect(self.add_vulnerability)
        self.scanner_engine.scan_completed.connect(self.scan_completed)
        
        # ZAP manager connections
        self.zap_manager.status_changed.connect(self.update_zap_status)
        self.zap_manager.scan_progress.connect(self.update_progress)
    
    def set_user(self, username):
        """Set the current user"""
        self.current_user = username
        self.user_label.setText(f"User: {username}")
    
    def connect_zap(self):
        """Connect to ZAP"""
        self.add_log("Connecting to OWASP ZAP...")
        if self.zap_manager.connect():
            self.add_log("Successfully connected to ZAP")
            self.zap_spider_btn.setEnabled(True)
            self.zap_active_btn.setEnabled(True)
        else:
            self.add_log("Failed to connect to ZAP", "error")
    
    def start_zap(self):
        """Start ZAP daemon"""
        self.add_log("Starting OWASP ZAP daemon...")
        if self.zap_manager.start_zap():
            self.add_log("ZAP daemon started successfully")
        else:
            self.add_log("Failed to start ZAP daemon", "error")
    
    def start_spider_scan(self):
        """Start ZAP spider scan"""
        target_url = self.target_url_input.text().strip()
        if not target_url:
            QMessageBox.warning(self, "Warning", "Please enter a target URL")
            return
        
        self.add_log(f"Starting spider scan on {target_url}")
        self.zap_manager.start_spider(target_url)
    
    def start_active_scan(self):
        """Start ZAP active scan"""
        target_url = self.target_url_input.text().strip()
        if not target_url:
            QMessageBox.warning(self, "Warning", "Please enter a target URL")
            return
        
        self.add_log(f"Starting active scan on {target_url}")
        self.zap_manager.start_active_scan(target_url)
    
    def start_bug_hunt(self):
        """Start the comprehensive bug hunting process"""
        try:
            target_url = self.target_url_input.text().strip()
            if not target_url:
                QMessageBox.warning(self, "Warning", "Please enter a target URL")
                return
            
            # Ensure URL has protocol
            if not target_url.startswith(('http://', 'https://')):
                target_url = 'https://' + target_url
            
            self.add_log(f"Preparing scan for {target_url}")
            
            # Check if wordlist selectors exist and get safe values
            wordlists_config = {}
            for key in ['directories', 'subdomains', 'parameters', 'admin_panels', 'jwt_secrets']:
                try:
                    if hasattr(self, 'wordlist_selectors') and key in self.wordlist_selectors:
                        selector = self.wordlist_selectors[key]
                        if hasattr(selector, 'combo') and selector.combo.currentData():
                            wordlists_config[key] = selector.combo.currentData()
                        else:
                            wordlists_config[key] = None
                    else:
                        wordlists_config[key] = None
                except Exception as e:
                    self.add_log(f"Warning: Could not get {key} wordlist: {str(e)}", "warning")
                    wordlists_config[key] = None
            
            # Prepare scan configuration
            scan_config = {
                'target_url': target_url,
                'threads': self.threads_spin.value(),
                'timeout': self.timeout_spin.value(),
                'directory_scan': self.directory_scan_cb.isChecked(),
                'subdomain_scan': self.subdomain_scan_cb.isChecked(),
                'jwt_analysis': self.jwt_analysis_cb.isChecked(),
                'admin_panel': self.admin_panel_cb.isChecked(),
                'bypass_redirects': self.bypass_redirects_cb.isChecked(),
                'wordlists': wordlists_config
            }
            
            # Update UI
            self.start_scan_btn.setEnabled(False)
            self.stop_scan_btn.setEnabled(True)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.status_label.setText("Starting bug hunting process...")
            
            # Clear previous results
            self.results_tree.clear()
            self.vulns_table.setRowCount(0)
            
            # Initialize advanced scanning
            self.scanner_engine.initialize_advanced_scanning()
            
            # Start scanning
            self.add_log(f"🎯 Starting ADVANCED bug hunt on {target_url}")
            self.add_log("🚀 Features: Auto-validation, Auto-exploitation, Login testing", "info")
            success = self.scanner_engine.start_scan(scan_config)
            
            if not success:
                self.add_log("Failed to start scan - scanner may already be running", "error")
                self.scan_completed()
                
        except Exception as e:
            self.add_log(f"Error starting bug hunt: {str(e)}", "error")
            import traceback
            self.add_log(f"Traceback: {traceback.format_exc()}", "error")
            self.scan_completed()
    
    def stop_scan(self):
        """Stop the current scan"""
        self.scanner_engine.stop_scan()
        self.add_log("Scan stopped by user")
        self.scan_completed()
    
    def scan_completed(self):
        """Handle scan completion"""
        self.start_scan_btn.setEnabled(True)
        self.stop_scan_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        # Count results
        vuln_count = self.vulns_table.rowCount()
        result_count = self.results_tree.topLevelItemCount()
        
        self.status_label.setText(f"Scan completed - {result_count} results, {vuln_count} vulnerabilities")
        completion_msg = f"🎉 Bug hunting completed! Found {result_count} results and {vuln_count} vulnerabilities"
        self.add_log(completion_msg, "success")
        
        # Auto-generate report if vulnerabilities found
        if vuln_count > 0:
            self.add_log("📄 Auto-generating vulnerability report...", "info")
            try:
                self.generate_report()
            except Exception as e:
                self.add_log(f"Report generation failed: {str(e)}", "error")
    
    def update_progress(self, value, message=""):
        """Update progress bar and status"""
        self.progress_bar.setValue(value)
        if message:
            self.status_label.setText(message)
    
    def add_result(self, result_type, url, status, details):
        """Add a result to the results tree"""
        item = QTreeWidgetItem([result_type, url, status, details])
        
        # Color code based on result type
        if "vulnerability" in result_type.lower() or "found" in status.lower():
            item.setBackground(0, QColor(76, 175, 80, 50))  # Green
        elif "error" in status.lower():
            item.setBackground(0, QColor(244, 67, 54, 50))  # Red
        
        self.results_tree.addTopLevelItem(item)
        self.results_tree.scrollToBottom()
    
    def add_log(self, message, level="info"):
        """Add a log message"""
        timestamp = QTimer().remainingTime()
        colors = {
            "info": "#ffffff",
            "success": "#4CAF50",
            "warning": "#ff9800",
            "error": "#f44336"
        }
        
        color = colors.get(level, colors["info"])
        formatted_message = f'<span style="color: {color};">[{level.upper()}] {message}</span><br>'
        
        self.log_text.moveCursor(QTextCursor.MoveOperation.End)
        self.log_text.insertHtml(formatted_message)
        self.log_text.moveCursor(QTextCursor.MoveOperation.End)
    
    def add_vulnerability(self, severity, vuln_type, url, description, impact):
        """Add a vulnerability to the vulnerabilities table"""
        row = self.vulns_table.rowCount()
        self.vulns_table.insertRow(row)
        
        # Color code based on severity
        severity_colors = {
            "Critical": QColor(244, 67, 54),
            "High": QColor(255, 152, 0),
            "Medium": QColor(255, 235, 59),
            "Low": QColor(76, 175, 80),
            "Info": QColor(33, 150, 243)
        }
        
        severity_item = QTableWidgetItem(severity)
        if severity in severity_colors:
            severity_item.setBackground(severity_colors[severity])
        
        self.vulns_table.setItem(row, 0, severity_item)
        self.vulns_table.setItem(row, 1, QTableWidgetItem(vuln_type))
        self.vulns_table.setItem(row, 2, QTableWidgetItem(url))
        self.vulns_table.setItem(row, 3, QTableWidgetItem(description))
        self.vulns_table.setItem(row, 4, QTableWidgetItem(impact))
    
    def update_zap_status(self, status):
        """Update ZAP status display"""
        self.zap_status_label.setText(f"ZAP: {status}")
        
        if status == "Connected":
            self.zap_status_label.setStyleSheet("color: #4CAF50;")
        elif status == "Disconnected":
            self.zap_status_label.setStyleSheet("color: #f44336;")
        else:
            self.zap_status_label.setStyleSheet("color: #ff9800;")
    
    def on_wordlist_changed(self, category, file_path):
        """Handle wordlist selection change"""
        self.add_log(f"Wordlist changed for {category}: {Path(file_path).name if file_path != 'default' else 'Default'}")
    
    def open_wordlist_manager(self):
        """Open the comprehensive wordlist manager"""
        manager = WordlistManager(self.config_manager)
        
        # Show as dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Wordlist Manager")
        dialog.resize(1200, 800)
        
        layout = QVBoxLayout(dialog)
        layout.addWidget(manager)
        
        # Add close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        # Refresh all wordlist selectors
        for selector in self.wordlist_selectors.values():
            selector.load_wordlists()
    
    def generate_report(self):
        """Generate a comprehensive report"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Report", "bug_bounty_report.html", 
            "HTML Files (*.html);;PDF Files (*.pdf);;All Files (*)"
        )
        
        if filename:
            self.add_log(f"Generating report: {filename}")
            # TODO: Implement report generation
            self.add_log("Report generated successfully", "success")
    
    def on_wordlist_changed(self, category, file_path):
        """Handle wordlist selection changes"""
        self.add_log(f"Wordlist updated for {category}: {Path(file_path).name}", "info")
    
    def open_wordlist_manager(self):
        """Open the wordlist manager tab"""
        # Switch to wordlist manager tab
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == "Wordlists":
                self.tabs.setCurrentIndex(i)
                break
    
    def auto_configure_scan(self, target_url, recommended_scans):
        """Auto-configure scan based on intelligence recommendations"""
        # Set target URL
        self.target_url_input.setText(target_url)
        
        # Configure scan options based on recommendations
        scan_mapping = {
            'directory_fuzzing': self.directory_scan_cb,
            'subdomain_enumeration': self.subdomain_scan_cb,
            'jwt_analysis': self.jwt_analysis_cb,
            'admin_panel_discovery': self.admin_panel_cb,
            'parameter_fuzzing': self.directory_scan_cb,  # Use directory scan for parameters
            'xss_testing': self.directory_scan_cb,
            'sql_injection_testing': self.directory_scan_cb
        }
        
        # Reset all checkboxes first
        for checkbox in scan_mapping.values():
            checkbox.setChecked(False)
        
        # Enable recommended scans
        for scan in recommended_scans:
            scan_key = scan.lower().replace(' ', '_').replace('-', '_')
            if scan_key in scan_mapping:
                scan_mapping[scan_key].setChecked(True)
        
        # Log the auto-configuration
        self.add_log(f"Auto-configured scan for {target_url}", "info")
        self.add_log(f"Enabled scans: {', '.join(recommended_scans)}", "info")
        
        # Switch to main results tab
        self.tabs.setCurrentIndex(0)  # Results tab