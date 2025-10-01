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

# Enhanced features imports
from nuclei_shodan_integration import NucleiShodanIntegration
from lost_uncover import LostUncover
from lost_fuzzer import LostFuzzer
from recon_automation import ReconAutomation
from bug_hunting_workflow import BugHuntingWorkflow

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

        # Enhanced components (33X more robust)
        self.nuclei_shodan = NucleiShodanIntegration()
        self.lost_uncover = LostUncover()
        self.lost_fuzzer = LostFuzzer()
        self.recon_automation = ReconAutomation()
        self.bug_hunting_workflow = BugHuntingWorkflow()
        
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

            # Add numeric inputs after checkboxes
            threads_layout = QHBoxLayout()
            threads_label = QLabel("Threads:")
            self.threads_input = QSpinBox()
            self.threads_input.setRange(1, 50)
            self.threads_input.setValue(10)
            threads_layout.addWidget(threads_label)
            threads_layout.addWidget(self.threads_input)

            timeout_layout = QHBoxLayout()
            timeout_label = QLabel("Timeout:")
            self.timeout_input = QSpinBox()
            self.timeout_input.setRange(1, 300)
            self.timeout_input.setValue(30)
            timeout_layout.addWidget(timeout_label)
            timeout_layout.addWidget(self.timeout_input)

            layout.addLayout(threads_layout, len(scan_options)//2 + 1, 0)
            layout.addLayout(timeout_layout, len(scan_options)//2 + 1, 1)

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

            # Add numeric inputs
            threads_layout = QHBoxLayout()
            threads_label = QLabel("Threads:")
            self.threads_input = QSpinBox()
            self.threads_input.setRange(1, 50)
            self.threads_input.setValue(10)
            threads_layout.addWidget(threads_label)
            threads_layout.addWidget(self.threads_input)
            layout.addLayout(threads_layout)

            timeout_layout = QHBoxLayout()
            timeout_label = QLabel("Timeout (sec):")
            self.timeout_input = QSpinBox()
            self.timeout_input.setRange(1, 300)
            self.timeout_input.setValue(30)
            timeout_layout.addWidget(timeout_label)
            timeout_layout.addWidget(self.timeout_input)
            layout.addLayout(timeout_layout)

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

        self.open_reports_btn = QPushButton("Open Reports Directory")
        self.open_reports_btn.clicked.connect(self.open_reports_directory)
        layout.addWidget(self.open_reports_btn)
        
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

        # Enhanced Features Tabs (33X More Robust)
        self.tabs.addTab(self.create_mass_cve_tab(), "🔍 Mass CVE Scan")
        self.tabs.addTab(self.create_hidden_elements_tab(), "👁️ Hidden Elements")
        self.tabs.addTab(self.create_automated_recon_tab(), "🔎 Auto Recon")
        self.tabs.addTab(self.create_lost_fuzzer_tab(), "⚡ LostFuzzer")
        self.tabs.addTab(self.create_workflow_tab(), "🚀 Complete Workflow")
        
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
            self.add_log("🚀 Features: Directory Fuzzing, Admin Discovery, Parameter Testing, Nuclei Scanning", "info")
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
    
    def generate_report(self, auto=False):
        """Generate a comprehensive report"""

        if not auto:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save Report", "bug_bounty_report.html",
                "HTML Files (*.html);;JSON Files (*.json);;All Files (*)"
            )

            if not filename:
                return
        else:
            # Auto-generate with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bug_bounty_report_{timestamp}.html"

        self.add_log(f"Generating report: {filename}")

        # Collect scan data
        scan_data = self._collect_scan_data()

        # Generate report
        try:
            if filename.endswith('.html'):
                filepath = self.report_generator.generate_html_report(scan_data, os.path.basename(filename))
            elif filename.endswith('.json'):
                filepath = self.report_generator.generate_json_report(scan_data, os.path.basename(filename))
            else:
                filepath = self.report_generator.generate_html_report(scan_data, os.path.basename(filename))

            self.add_log(f"Report generated successfully: {filepath}", "success")

            # If auto-generated, show in browser or notify
            if auto:
                import webbrowser
                webbrowser.open(f"file://{os.path.abspath(filepath)}")
                self.add_log("Report opened in default browser", "info")

        except Exception as e:
            self.add_log(f"Error generating report: {e}", "error")

    def _collect_scan_data(self):
        """Collect all scan data for report generation"""
        scan_data = {
            'vulnerabilities': [],
            'results': [],
            'scan_config': {},
            'target_url': self.target_url_input.text(),
            'scan_timestamp': None
        }

        # Collect vulnerabilities from table
        row_count = self.vulns_table.rowCount()
        for row in range(row_count):
            vuln = {
                'severity': self.vulns_table.item(row, 0).text() if self.vulns_table.item(row, 0) else '',
                'type': self.vulns_table.item(row, 1).text() if self.vulns_table.item(row, 1) else '',
                'url': self.vulns_table.item(row, 2).text() if self.vulns_table.item(row, 2) else '',
                'description': self.vulns_table.item(row, 3).text() if self.vulns_table.item(row, 3) else '',
                'impact': self.vulns_table.item(row, 4).text() if self.vulns_table.item(row, 4) else ''
            }
            scan_data['vulnerabilities'].append(vuln)

        # Collect results from other tabs (simplified - collect from logs or specific widgets)
        # For now, collect from results tabs
        results_tabs = ['Directory Results', 'Subdomain Results', 'Admin Panel Results', 'JWT Results']
        for tab_name in results_tabs:
            for i in range(self.tabs.count()):
                if self.tabs.tabText(i) == tab_name:
                    tab_widget = self.tabs.widget(i)
                    # Assuming each tab has a text area or list
                    if hasattr(tab_widget, 'toPlainText'):
                        content = tab_widget.toPlainText()
                        if content.strip():
                            scan_data['results'].append({
                                'type': tab_name,
                                'content': content
                            })
                    break

        # Collect scan configuration
        scan_data['scan_config'] = {
            'target_url': self.target_url_input.text(),
            'threads': self.threads_input.value(),
            'timeout': self.timeout_input.value(),
            'directory_scan': self.directory_scan_cb.isChecked(),
            'subdomain_scan': self.subdomain_scan_cb.isChecked(),
            'jwt_analysis': self.jwt_analysis_cb.isChecked(),
            'admin_panel': self.admin_panel_cb.isChecked(),
            'bypass_redirects': self.bypass_redirects_cb.isChecked(),
            'wordlist': getattr(self, 'wordlist_path', 'default')
        }

        # Add timestamp
        from datetime import datetime
        scan_data['scan_timestamp'] = datetime.now().isoformat()

        return scan_data

    def open_reports_directory(self):
        """Open the reports directory in file explorer"""
        import os
        import subprocess
        reports_dir = self.config_manager.get_output_config().get('reports_dir', 'reports')
        if os.path.exists(reports_dir):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(reports_dir)
                elif os.name == 'posix':  # macOS/Linux
                    subprocess.run(['xdg-open', reports_dir])
                self.add_log(f"Opened reports directory: {reports_dir}", "info")
            except Exception as e:
                self.add_log(f"Could not open reports directory: {e}", "error")
        else:
            self.add_log(f"Reports directory does not exist: {reports_dir}", "warning")

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

    # Enhanced Features Tab Methods (33X More Robust)

    def create_mass_cve_tab(self):
        """Create Mass CVE Scanning tab with Shodan integration"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Header
        header = QLabel("🔍 Mass CVE Scanning with Shodan & Nuclei")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(header)

        # Description
        desc = QLabel("Scan thousands of IPs/domains for CVEs using Shodan API and Nuclei templates")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Input form
        form_group = QGroupBox("Scan Configuration")
        form_layout = QFormLayout(form_group)

        self.shodan_api_input = QLineEdit()
        self.shodan_api_input.setPlaceholderText("Enter your Shodan API key")
        self.shodan_api_input.setText("0aUw9tLCL1DczQvQJ0a01OxhSKG1Cq9i")  # Pre-filled
        form_layout.addRow("Shodan API Key:", self.shodan_api_input)

        self.cve_query_input = QLineEdit()
        self.cve_query_input.setPlaceholderText("e.g., grafana, apache, nginx")
        self.cve_query_input.setText("grafana")
        form_layout.addRow("CVE Query:", self.cve_query_input)

        self.cve_templates_input = QLineEdit()
        self.cve_templates_input.setPlaceholderText("e.g., grafana, cves")
        self.cve_templates_input.setText("grafana")
        form_layout.addRow("Nuclei Templates:", self.cve_templates_input)

        layout.addWidget(form_group)

        # Control buttons
        button_layout = QHBoxLayout()

        self.mass_cve_scan_btn = QPushButton("🚀 Start Mass CVE Scan")
        self.mass_cve_scan_btn.clicked.connect(self.start_mass_cve_scan)
        button_layout.addWidget(self.mass_cve_scan_btn)

        self.mass_cve_stop_btn = QPushButton("⏹️ Stop Scan")
        self.mass_cve_stop_btn.clicked.connect(self.stop_mass_cve_scan)
        self.mass_cve_stop_btn.setEnabled(False)
        button_layout.addWidget(self.mass_cve_stop_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Results area
        self.mass_cve_results = QTextEdit()
        self.mass_cve_results.setPlaceholderText("Mass CVE scan results will appear here...")
        layout.addWidget(self.mass_cve_results)

        return widget

    def create_hidden_elements_tab(self):
        """Create Hidden Elements Discovery tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Header
        header = QLabel("👁️ Hidden Elements Discovery")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(header)

        # Description
        desc = QLabel("Discover hidden elements on web pages that may reveal client-side restrictions")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Control buttons
        button_layout = QHBoxLayout()

        self.generate_bookmarklet_btn = QPushButton("🔗 Generate Bookmarklet")
        self.generate_bookmarklet_btn.clicked.connect(self.generate_bookmarklet)
        button_layout.addWidget(self.generate_bookmarklet_btn)

        self.create_test_page_btn = QPushButton("📄 Create Test Page")
        self.create_test_page_btn.clicked.connect(self.create_test_page)
        button_layout.addWidget(self.create_test_page_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Results area
        self.hidden_elements_results = QTextEdit()
        self.hidden_elements_results.setPlaceholderText("Bookmarklet and test page information will appear here...")
        layout.addWidget(self.hidden_elements_results)

        return widget

    def create_automated_recon_tab(self):
        """Create Automated Reconnaissance tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Header
        header = QLabel("🔎 Automated Reconnaissance")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(header)

        # Description
        desc = QLabel("Multi-source URL discovery from AlienVault, Wayback Machine, URLScan, and VirusTotal")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Input form
        form_group = QGroupBox("Target Configuration")
        form_layout = QFormLayout(form_group)

        self.recon_target_input = QLineEdit()
        self.recon_target_input.setPlaceholderText("example.com")
        form_layout.addRow("Target Domain:", self.recon_target_input)

        self.virustotal_api_input = QLineEdit()
        self.virustotal_api_input.setPlaceholderText("VirusTotal API key (optional)")
        form_layout.addRow("VirusTotal API:", self.virustotal_api_input)

        layout.addWidget(form_group)

        # Control buttons
        button_layout = QHBoxLayout()

        self.start_recon_btn = QPushButton("🔍 Start Recon")
        self.start_recon_btn.clicked.connect(self.start_automated_recon)
        button_layout.addWidget(self.start_recon_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Results area
        self.recon_results = QTextEdit()
        self.recon_results.setPlaceholderText("Reconnaissance results will appear here...")
        layout.addWidget(self.recon_results)

        return widget

    def create_lost_fuzzer_tab(self):
        """Create LostFuzzer DAST Scanner tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Header
        header = QLabel("⚡ LostFuzzer - Quick DAST Scanner")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(header)

        # Description
        desc = QLabel("Passive URL fuzzing and Nuclei DAST scanning for domains")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Input form
        form_group = QGroupBox("Scan Configuration")
        form_layout = QFormLayout(form_group)

        self.fuzzer_target_input = QLineEdit()
        self.fuzzer_target_input.setPlaceholderText("example.com")
        form_layout.addRow("Target Domain:", self.fuzzer_target_input)

        self.fuzzer_templates_input = QLineEdit()
        self.fuzzer_templates_input.setPlaceholderText("e.g., exposures, misconfigurations")
        self.fuzzer_templates_input.setText("exposures")
        form_layout.addRow("Nuclei Templates:", self.fuzzer_templates_input)

        layout.addWidget(form_group)

        # Control buttons
        button_layout = QHBoxLayout()

        self.start_fuzzer_btn = QPushButton("⚡ Start LostFuzzer")
        self.start_fuzzer_btn.clicked.connect(self.start_lost_fuzzer)
        button_layout.addWidget(self.start_fuzzer_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Results area
        self.fuzzer_results = QTextEdit()
        self.fuzzer_results.setPlaceholderText("LostFuzzer results will appear here...")
        layout.addWidget(self.fuzzer_results)

        return widget

    def create_workflow_tab(self):
        """Create Complete Workflow Automation tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Header
        header = QLabel("🚀 Complete Bug Hunting Workflow")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(header)

        # Description
        desc = QLabel("End-to-end automated bug hunting pipeline combining all methods")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Workflow steps display
        steps_group = QGroupBox("Workflow Steps")
        steps_layout = QVBoxLayout(steps_group)

        steps_text = """
        1. 🔍 Mass CVE Scanning (Shodan + Nuclei)
        2. 👁️ Hidden Elements Discovery
        3. 🔎 Automated Reconnaissance (Multi-source)
        4. ⚡ LostFuzzer DAST Scanning
        5. 📊 Results Compilation & Reporting
        """
        steps_label = QLabel(steps_text.strip())
        steps_label.setFont(QFont("Courier New", 10))
        steps_layout.addWidget(steps_label)

        layout.addWidget(steps_group)

        # Configuration
        config_group = QGroupBox("Workflow Configuration")
        config_layout = QFormLayout(config_group)

        self.workflow_target_input = QLineEdit()
        self.workflow_target_input.setPlaceholderText("example.com")
        config_layout.addRow("Target Domain:", self.workflow_target_input)

        self.workflow_shodan_api_input = QLineEdit()
        self.workflow_shodan_api_input.setText("0aUw9tLCL1DczQvQJ0a01OxhSKG1Cq9i")
        config_layout.addRow("Shodan API Key:", self.workflow_shodan_api_input)

        self.workflow_virustotal_api_input = QLineEdit()
        self.workflow_virustotal_api_input.setPlaceholderText("Optional")
        config_layout.addRow("VirusTotal API:", self.workflow_virustotal_api_input)

        layout.addWidget(config_group)

        # Control buttons
        button_layout = QHBoxLayout()

        self.start_workflow_btn = QPushButton("🚀 Start Complete Workflow")
        self.start_workflow_btn.clicked.connect(self.start_complete_workflow)
        button_layout.addWidget(self.start_workflow_btn)

        self.stop_workflow_btn = QPushButton("⏹️ Stop Workflow")
        self.stop_workflow_btn.clicked.connect(self.stop_complete_workflow)
        self.stop_workflow_btn.setEnabled(False)
        button_layout.addWidget(self.stop_workflow_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Progress and results
        self.workflow_progress = QProgressBar()
        self.workflow_progress.setVisible(False)
        layout.addWidget(self.workflow_progress)

        self.workflow_results = QTextEdit()
        self.workflow_results.setPlaceholderText("Complete workflow results will appear here...")
        layout.addWidget(self.workflow_results)

        return widget

    # Enhanced Features Methods

    def start_mass_cve_scan(self):
        """Start mass CVE scanning"""
        shodan_api = self.shodan_api_input.text().strip()
        cve_query = self.cve_query_input.text().strip()
        templates = self.cve_templates_input.text().strip()

        if not shodan_api or not cve_query:
            QMessageBox.warning(self, "Missing Input", "Please provide Shodan API key and CVE query.")
            return

        self.mass_cve_scan_btn.setEnabled(False)
        self.mass_cve_stop_btn.setEnabled(True)
        self.mass_cve_results.clear()
        self.mass_cve_results.append("🔍 Starting Mass CVE Scan...")
        self.mass_cve_results.append(f"Query: {cve_query}")
        self.mass_cve_results.append(f"Templates: {templates}")
        self.mass_cve_results.append("")

        # Run in thread to avoid blocking UI
        from PyQt6.QtCore import QThread, pyqtSignal

        class CVEScanWorker(QThread):
            finished = pyqtSignal(dict)
            error = pyqtSignal(str)

            def __init__(self, shodan_api, cve_query, templates):
                super().__init__()
                self.shodan_api = shodan_api
                self.cve_query = cve_query
                self.templates = templates

            def run(self):
                try:
                    from nuclei_shodan_integration import NucleiShodanIntegration
                    nuclei = NucleiShodanIntegration()
                    results = nuclei.mass_cve_scan(self.shodan_api, self.cve_query, self.templates)
                    self.finished.emit(results)
                except Exception as e:
                    self.error.emit(str(e))

        self.cve_worker = CVEScanWorker(shodan_api, cve_query, templates)
        self.cve_worker.finished.connect(self.on_mass_cve_finished)
        self.cve_worker.error.connect(self.on_mass_cve_error)
        self.cve_worker.start()

    def on_mass_cve_finished(self, results):
        """Handle mass CVE scan completion"""
        self.mass_cve_scan_btn.setEnabled(True)
        self.mass_cve_stop_btn.setEnabled(False)

        if "error" in results:
            self.mass_cve_results.append(f"❌ Error: {results['error']}")
            return

        self.mass_cve_results.append("✅ Mass CVE Scan Completed!")
        self.mass_cve_results.append(f"📊 IPs Found: {results.get('total_ips', 0)}")
        self.mass_cve_results.append(f"🌐 Domains Found: {results.get('total_domains', 0)}")
        self.mass_cve_results.append(f"🎯 Nuclei Findings: {len(results.get('nuclei_findings', []))}")

        if results.get('ip_file'):
            self.mass_cve_results.append(f"💾 IPs saved to: {results['ip_file']}")
        if results.get('domain_file'):
            self.mass_cve_results.append(f"💾 Domains saved to: {results['domain_file']}")

    def on_mass_cve_error(self, error_msg):
        """Handle mass CVE scan error"""
        self.mass_cve_scan_btn.setEnabled(True)
        self.mass_cve_stop_btn.setEnabled(False)
        self.mass_cve_results.append(f"❌ Error: {error_msg}")

    def stop_mass_cve_scan(self):
        """Stop mass CVE scan"""
        if hasattr(self, 'cve_worker'):
            self.cve_worker.terminate()
        self.mass_cve_scan_btn.setEnabled(True)
        self.mass_cve_stop_btn.setEnabled(False)
        self.mass_cve_results.append("⏹️ Scan stopped by user")

    def generate_bookmarklet(self):
        """Generate Lost Uncover bookmarklet"""
        try:
            bookmarklet = self.lost_uncover.get_bookmarklet()
            self.hidden_elements_results.clear()
            self.hidden_elements_results.append("🔗 Lost Uncover Bookmarklet Generated!")
            self.hidden_elements_results.append("")
            self.hidden_elements_results.append("📋 Copy this bookmarklet to your browser bookmarks:")
            self.hidden_elements_results.append("")
            self.hidden_elements_results.append(bookmarklet)
            self.hidden_elements_results.append("")
            self.hidden_elements_results.append("📖 Instructions:")
            self.hidden_elements_results.append("1. Drag the bookmarklet above to your browser bookmarks bar")
            self.hidden_elements_results.append("2. Navigate to any webpage")
            self.hidden_elements_results.append("3. Click the bookmarklet to reveal hidden elements")
        except Exception as e:
            self.hidden_elements_results.append(f"❌ Error generating bookmarklet: {str(e)}")

    def create_test_page(self):
        """Create test page for Lost Uncover"""
        try:
            test_page = self.lost_uncover.save_test_page()
            self.hidden_elements_results.append("📄 Test Page Created!")
            self.hidden_elements_results.append(f"📍 Location: {test_page}")
            self.hidden_elements_results.append("")
            self.hidden_elements_results.append("🧪 Open this page in your browser and click the bookmarklet to test.")
        except Exception as e:
            self.hidden_elements_results.append(f"❌ Error creating test page: {str(e)}")

    def start_automated_recon(self):
        """Start automated reconnaissance"""
        target = self.recon_target_input.text().strip()
        vt_api = self.virustotal_api_input.text().strip()

        if not target:
            QMessageBox.warning(self, "Missing Target", "Please provide a target domain.")
            return

        self.start_recon_btn.setEnabled(False)
        self.recon_results.clear()
        self.recon_results.append(f"🔎 Starting Automated Recon for: {target}")
        if vt_api:
            self.recon_results.append("🔑 Using VirusTotal API")
        self.recon_results.append("")

        # Run in thread
        from PyQt6.QtCore import QThread, pyqtSignal

        class ReconWorker(QThread):
            finished = pyqtSignal(dict)
            error = pyqtSignal(str)

            def __init__(self, target, vt_api):
                super().__init__()
                self.target = target
                self.vt_api = vt_api

            def run(self):
                try:
                    from recon_automation import ReconAutomation
                    recon = ReconAutomation()
                    results = recon.aggregate_recon_urls(self.target, self.vt_api or None)
                    self.finished.emit(results)
                except Exception as e:
                    self.error.emit(str(e))

        self.recon_worker = ReconWorker(target, vt_api)
        self.recon_worker.finished.connect(self.on_recon_finished)
        self.recon_worker.error.connect(self.on_recon_error)
        self.recon_worker.start()

    def on_recon_finished(self, results):
        """Handle recon completion"""
        self.start_recon_btn.setEnabled(True)

        self.recon_results.append("✅ Reconnaissance Completed!")
        self.recon_results.append(f"🔗 Total URLs Found: {len(results.get('all_urls', []))}")
        self.recon_results.append(f"📊 Sources Used: {len(results.get('sources', []))}")

        # Show breakdown by source
        sources = results.get('sources', {})
        for source, count in sources.items():
            self.recon_results.append(f"  • {source}: {count} URLs")

        # Show some sample URLs
        urls = results.get('all_urls', [])[:10]  # Show first 10
        if urls:
            self.recon_results.append("")
            self.recon_results.append("📋 Sample URLs:")
            for url in urls:
                self.recon_results.append(f"  {url}")

    def on_recon_error(self, error_msg):
        """Handle recon error"""
        self.start_recon_btn.setEnabled(True)
        self.recon_results.append(f"❌ Error: {error_msg}")

    def start_lost_fuzzer(self):
        """Start LostFuzzer scan"""
        target = self.fuzzer_target_input.text().strip()
        templates = self.fuzzer_templates_input.text().strip()

        if not target:
            QMessageBox.warning(self, "Missing Target", "Please provide a target domain.")
            return

        self.start_fuzzer_btn.setEnabled(False)
        self.fuzzer_results.clear()
        self.fuzzer_results.append(f"⚡ Starting LostFuzzer for: {target}")
        self.fuzzer_results.append(f"📋 Templates: {templates}")
        self.fuzzer_results.append("")

        # Run in thread
        from PyQt6.QtCore import QThread, pyqtSignal

        class FuzzerWorker(QThread):
            finished = pyqtSignal(dict)
            error = pyqtSignal(str)

            def __init__(self, target, templates):
                super().__init__()
                self.target = target
                self.templates = templates

            def run(self):
                try:
                    from lost_fuzzer import LostFuzzer
                    fuzzer = LostFuzzer()
                    results = fuzzer.run_scan(self.target, self.templates)
                    self.finished.emit(results)
                except Exception as e:
                    self.error.emit(str(e))

        self.fuzzer_worker = FuzzerWorker(target, templates)
        self.fuzzer_worker.finished.connect(self.on_fuzzer_finished)
        self.fuzzer_worker.error.connect(self.on_fuzzer_error)
        self.fuzzer_worker.start()

    def on_fuzzer_finished(self, results):
        """Handle fuzzer completion"""
        self.start_fuzzer_btn.setEnabled(True)

        self.fuzzer_results.append("✅ LostFuzzer Scan Completed!")
        self.fuzzer_results.append(f"🎯 Findings: {len(results.get('findings', []))}")

        # Show findings
        findings = results.get('findings', [])
        if findings:
            self.fuzzer_results.append("")
            self.fuzzer_results.append("📋 Findings:")
            for finding in findings[:20]:  # Show first 20
                self.fuzzer_results.append(f"  • {finding}")
        else:
            self.fuzzer_results.append("No vulnerabilities found.")

    def on_fuzzer_error(self, error_msg):
        """Handle fuzzer error"""
        self.start_fuzzer_btn.setEnabled(True)
        self.fuzzer_results.append(f"❌ Error: {error_msg}")

    def start_complete_workflow(self):
        """Start complete bug hunting workflow"""
        target = self.workflow_target_input.text().strip()
        shodan_api = self.workflow_shodan_api_input.text().strip()
        vt_api = self.workflow_virustotal_api_input.text().strip()

        if not target or not shodan_api:
            QMessageBox.warning(self, "Missing Input", "Please provide target domain and Shodan API key.")
            return

        self.start_workflow_btn.setEnabled(False)
        self.stop_workflow_btn.setEnabled(True)
        self.workflow_progress.setVisible(True)
        self.workflow_progress.setValue(0)
        self.workflow_results.clear()

        self.workflow_results.append("🚀 Starting Complete Bug Hunting Workflow")
        self.workflow_results.append(f"🎯 Target: {target}")
        self.workflow_results.append("")

        # Run workflow
        from PyQt6.QtCore import QThread, pyqtSignal

        class WorkflowWorker(QThread):
            progress = pyqtSignal(int, str)
            finished = pyqtSignal(dict)
            error = pyqtSignal(str)

            def __init__(self, target, shodan_api, vt_api):
                super().__init__()
                self.target = target
                self.shodan_api = shodan_api
                self.vt_api = vt_api

            def run(self):
                try:
                    from bug_hunting_workflow import BugHuntingWorkflow
                    workflow = BugHuntingWorkflow()

                    results = {}

                    # Step 1: Mass CVE Scan
                    self.progress.emit(10, "Step 1: Mass CVE Scanning...")
                    cve_results = workflow.method_1_mass_cve_scanning(self.shodan_api, "grafana", "grafana")
                    results['cve'] = cve_results

                    # Step 2: Hidden Elements
                    self.progress.emit(30, "Step 2: Hidden Elements Discovery...")
                    hidden_results = workflow.method_2_uncover_hidden_elements()
                    results['hidden'] = hidden_results

                    # Step 3: Automated Recon
                    self.progress.emit(50, "Step 3: Automated Reconnaissance...")
                    recon_results = workflow.method_3_automated_toolkit(self.target, self.vt_api or None)
                    results['recon'] = recon_results

                    # Step 4: LostFuzzer
                    self.progress.emit(80, "Step 4: LostFuzzer DAST Scanning...")
                    fuzzer_results = workflow.lost_fuzzer.run_scan(self.target, "exposures")
                    results['fuzzer'] = fuzzer_results

                    self.progress.emit(100, "Workflow completed!")
                    self.finished.emit(results)

                except Exception as e:
                    self.error.emit(str(e))

        self.workflow_worker = WorkflowWorker(target, shodan_api, vt_api)
        self.workflow_worker.progress.connect(self.on_workflow_progress)
        self.workflow_worker.finished.connect(self.on_workflow_finished)
        self.workflow_worker.error.connect(self.on_workflow_error)
        self.workflow_worker.start()

    def on_workflow_progress(self, percent, message):
        """Handle workflow progress"""
        self.workflow_progress.setValue(percent)
        self.workflow_results.append(message)

    def on_workflow_finished(self, results):
        """Handle workflow completion"""
        self.start_workflow_btn.setEnabled(True)
        self.stop_workflow_btn.setEnabled(False)
        self.workflow_progress.setVisible(False)

        self.workflow_results.append("")
        self.workflow_results.append("✅ Complete Workflow Finished!")
        self.workflow_results.append("📊 Summary:")

        # Show results summary
        if 'cve' in results and 'error' not in results['cve']:
            self.workflow_results.append(f"🔍 CVE Scan: {results['cve'].get('total_ips', 0)} IPs, {len(results['cve'].get('nuclei_findings', []))} findings")

        if 'recon' in results:
            self.workflow_results.append(f"🔎 Recon: {len(results['recon'].get('all_urls', []))} URLs discovered")

        if 'fuzzer' in results:
            self.workflow_results.append(f"⚡ LostFuzzer: {len(results['fuzzer'].get('findings', []))} findings")

        self.workflow_results.append("")
        self.workflow_results.append("📁 Check individual tabs for detailed results.")

    def on_workflow_error(self, error_msg):
        """Handle workflow error"""
        self.start_workflow_btn.setEnabled(True)
        self.stop_workflow_btn.setEnabled(False)
        self.workflow_progress.setVisible(False)
        self.workflow_results.append(f"❌ Workflow Error: {error_msg}")

    def stop_complete_workflow(self):
        """Stop complete workflow"""
        if hasattr(self, 'workflow_worker'):
            self.workflow_worker.terminate()
        self.start_workflow_btn.setEnabled(True)
        self.stop_workflow_btn.setEnabled(False)
        self.workflow_progress.setVisible(False)
        self.workflow_results.append("⏹️ Workflow stopped by user")