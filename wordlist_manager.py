"""
Wordlist Manager - Manage custom wordlists for bug bounty hunting
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QListWidget, QListWidgetItem, QTextEdit,
                            QFileDialog, QMessageBox, QInputDialog, QTabWidget,
                            QGroupBox, QFormLayout, QLineEdit, QSpinBox,
                            QComboBox, QCheckBox, QProgressBar, QSplitter,
                            QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QFont, QIcon

class WordlistSelector(QWidget):
    """Simple wordlist selector widget for use in other components"""
    wordlist_changed = pyqtSignal(str, str)  # category, file_path
    
    def __init__(self, category, config_manager):
        super().__init__()
        self.category = category
        self.config_manager = config_manager
        self.wordlists_dir = Path("wordlists")
        self.custom_wordlists_dir = Path("wordlists/custom")
        
        self.setup_ui()
        self.load_wordlists()
    
    def setup_ui(self):
        """Setup the selector UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Responsive sizing
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen()
        screen_width = screen.geometry().width()
        
        if screen_width <= 1366:  # Smaller screens - increased sizes
            combo_height = 22
            btn_width = 26
            btn_height = 22
        else:  # Larger screens
            combo_height = 26
            btn_width = 30
            btn_height = 26
        
        self.wordlist_combo = QComboBox()
        self.wordlist_combo.setMaximumHeight(combo_height)
        self.wordlist_combo.currentTextChanged.connect(self.on_selection_changed)
        layout.addWidget(self.wordlist_combo)
        
        self.manage_btn = QPushButton("⚙")
        self.manage_btn.setMaximumWidth(btn_width)
        self.manage_btn.setMaximumHeight(btn_height)
        self.manage_btn.setToolTip("Manage wordlists")
        self.manage_btn.clicked.connect(self.open_manager)
        layout.addWidget(self.manage_btn)
        
        self.setLayout(layout)
    
    def load_wordlists(self):
        """Load available wordlists for this category"""
        self.wordlist_combo.clear()
        
        # Default wordlist
        default_file = self.wordlists_dir / f"{self.category}.txt"
        if default_file.exists():
            self.wordlist_combo.addItem("Default", str(default_file))
        
        # Custom wordlists
        if self.custom_wordlists_dir.exists():
            custom_pattern = f"{self.category}_*.txt"
            for custom_file in self.custom_wordlists_dir.glob(custom_pattern):
                name = custom_file.stem.replace(f"{self.category}_", "")
                self.wordlist_combo.addItem(f"Custom: {name}", str(custom_file))
    
    def on_selection_changed(self):
        """Handle selection change"""
        current_data = self.wordlist_combo.currentData()
        if current_data:
            self.wordlist_changed.emit(self.category, current_data)
    
    def open_manager(self):
        """Open wordlist manager dialog"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Manage {self.category.title()} Wordlists")
        dialog.setModal(True)
        dialog.resize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        manager = WordlistManager(self.config_manager)
        layout.addWidget(manager)
        
        # Connect to reload when wordlists are updated
        manager.wordlist_updated.connect(self.on_wordlist_updated)
        
        dialog.exec()
    
    def on_wordlist_updated(self, category, file_path):
        """Handle wordlist updates"""
        if category == self.category:
            self.load_wordlists()
    
    def get_selected_wordlist(self):
        """Get the currently selected wordlist path"""
        return self.wordlist_combo.currentData()

class WordlistManager(QWidget):
    wordlist_updated = pyqtSignal(str, str)  # wordlist_type, file_path
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.wordlists_dir = Path("wordlists")
        self.custom_wordlists_dir = Path("wordlists/custom")
        
        # Ensure directories exist
        self.wordlists_dir.mkdir(exist_ok=True)
        self.custom_wordlists_dir.mkdir(exist_ok=True)
        
        # Wordlist categories
        self.wordlist_categories = {
            'directories': 'Directory/File Fuzzing',
            'subdomains': 'Subdomain Enumeration',
            'parameters': 'Parameter Discovery',
            'admin_panels': 'Admin Panel Discovery',
            'jwt_secrets': 'JWT Weak Secrets',
            'usernames': 'Username Lists',
            'passwords': 'Password Lists',
            'extensions': 'File Extensions',
            'backup_files': 'Backup Files',
            'config_files': 'Configuration Files',
            'api_endpoints': 'API Endpoints',
            'technologies': 'Technology Detection'
        }
        
        self.setup_ui()
        self.load_wordlists()
    
    def setup_ui(self):
        """Setup the wordlist manager interface"""
        layout = QVBoxLayout()
        
        # Header
        header_label = QLabel("Wordlist Manager")
        header_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(header_label)
        
        # Main content
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Wordlist categories and files
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # Right panel - Wordlist content and management
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        main_splitter.setSizes([300, 500])
        layout.addWidget(main_splitter)
        
        self.setLayout(layout)
    
    def create_left_panel(self):
        """Create left panel with wordlist categories"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Category selection
        category_group = QGroupBox("Wordlist Categories")
        category_layout = QVBoxLayout(category_group)
        
        self.category_list = QListWidget()
        for category, description in self.wordlist_categories.items():
            item = QListWidgetItem(f"{description} ({category})")
            item.setData(Qt.ItemDataRole.UserRole, category)
            self.category_list.addItem(item)
        
        self.category_list.currentItemChanged.connect(self.on_category_changed)
        category_layout.addWidget(self.category_list)
        
        layout.addWidget(category_group)
        
        # Wordlist files for selected category
        files_group = QGroupBox("Available Wordlists")
        files_layout = QVBoxLayout(files_group)
        
        self.wordlist_files = QListWidget()
        self.wordlist_files.currentItemChanged.connect(self.on_wordlist_changed)
        files_layout.addWidget(self.wordlist_files)
        
        # File management buttons
        file_buttons = QHBoxLayout()
        
        self.add_wordlist_btn = QPushButton("Add Wordlist")
        self.add_wordlist_btn.clicked.connect(self.add_wordlist)
        file_buttons.addWidget(self.add_wordlist_btn)
        
        self.delete_wordlist_btn = QPushButton("Delete")
        self.delete_wordlist_btn.clicked.connect(self.delete_wordlist)
        self.delete_wordlist_btn.setEnabled(False)
        file_buttons.addWidget(self.delete_wordlist_btn)
        
        files_layout.addLayout(file_buttons)
        layout.addWidget(files_group)
        
        return panel
    
    def create_right_panel(self):
        """Create right panel with wordlist content"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Wordlist info
        info_group = QGroupBox("Wordlist Information")
        info_layout = QFormLayout(info_group)
        
        self.wordlist_name_label = QLabel("No wordlist selected")
        self.wordlist_size_label = QLabel("-")
        self.wordlist_lines_label = QLabel("-")
        self.wordlist_type_label = QLabel("-")
        
        info_layout.addRow("Name:", self.wordlist_name_label)
        info_layout.addRow("Size:", self.wordlist_size_label)
        info_layout.addRow("Lines:", self.wordlist_lines_label)
        info_layout.addRow("Type:", self.wordlist_type_label)
        
        layout.addWidget(info_group)
        
        # Wordlist content tabs
        self.content_tabs = QTabWidget()
        
        # Preview tab
        self.preview_tab = self.create_preview_tab()
        self.content_tabs.addTab(self.preview_tab, "Preview")
        
        # Edit tab
        self.edit_tab = self.create_edit_tab()
        self.content_tabs.addTab(self.edit_tab, "Edit")
        
        # Statistics tab
        self.stats_tab = self.create_statistics_tab()
        self.content_tabs.addTab(self.stats_tab, "Statistics")
        
        layout.addWidget(self.content_tabs)
        
        # Action buttons
        action_buttons = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_wordlist)
        self.save_btn.setEnabled(False)
        action_buttons.addWidget(self.save_btn)
        
        self.export_btn = QPushButton("Export")
        self.export_btn.clicked.connect(self.export_wordlist)
        self.export_btn.setEnabled(False)
        action_buttons.addWidget(self.export_btn)
        
        self.merge_btn = QPushButton("Merge Wordlists")
        self.merge_btn.clicked.connect(self.merge_wordlists)
        action_buttons.addWidget(self.merge_btn)
        
        self.download_btn = QPushButton("Download Popular")
        self.download_btn.clicked.connect(self.download_popular_wordlists)
        action_buttons.addWidget(self.download_btn)
        
        layout.addLayout(action_buttons)
        
        return panel
    
    def create_preview_tab(self):
        """Create preview tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Search box
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search in wordlist...")
        self.search_input.textChanged.connect(self.filter_preview)
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        
        # Preview text
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.preview_text)
        
        return widget
    
    def create_edit_tab(self):
        """Create edit tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Edit controls
        edit_controls = QHBoxLayout()
        
        self.add_line_btn = QPushButton("Add Line")
        self.add_line_btn.clicked.connect(self.add_line)
        edit_controls.addWidget(self.add_line_btn)
        
        self.remove_duplicates_btn = QPushButton("Remove Duplicates")
        self.remove_duplicates_btn.clicked.connect(self.remove_duplicates)
        edit_controls.addWidget(self.remove_duplicates_btn)
        
        self.sort_btn = QPushButton("Sort")
        self.sort_btn.clicked.connect(self.sort_wordlist)
        edit_controls.addWidget(self.sort_btn)
        
        self.clean_btn = QPushButton("Clean")
        self.clean_btn.clicked.connect(self.clean_wordlist)
        edit_controls.addWidget(self.clean_btn)
        
        layout.addLayout(edit_controls)
        
        # Edit text
        self.edit_text = QTextEdit()
        self.edit_text.setFont(QFont("Consolas", 10))
        self.edit_text.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.edit_text)
        
        return widget
    
    def create_statistics_tab(self):
        """Create statistics tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Statistics table
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.stats_table)
        
        return widget
    
    def load_wordlists(self):
        """Load available wordlists"""
        # Select first category by default
        if self.category_list.count() > 0:
            self.category_list.setCurrentRow(0)
    
    def on_category_changed(self, current, previous):
        """Handle category selection change"""
        if not current:
            return
        
        category = current.data(Qt.ItemDataRole.UserRole)
        self.load_wordlists_for_category(category)
    
    def load_wordlists_for_category(self, category):
        """Load wordlists for specific category"""
        self.wordlist_files.clear()
        
        # Default wordlist
        default_file = self.wordlists_dir / f"{category}.txt"
        if default_file.exists():
            item = QListWidgetItem(f"{category}.txt (Default)")
            item.setData(Qt.ItemDataRole.UserRole, str(default_file))
            self.wordlist_files.addItem(item)
        
        # Custom wordlists
        custom_pattern = f"{category}_*.txt"
        for custom_file in self.custom_wordlists_dir.glob(custom_pattern):
            item = QListWidgetItem(f"{custom_file.name} (Custom)")
            item.setData(Qt.ItemDataRole.UserRole, str(custom_file))
            self.wordlist_files.addItem(item)
        
        # Other wordlists in custom directory
        for wordlist_file in self.custom_wordlists_dir.glob("*.txt"):
            if category in wordlist_file.name.lower():
                item = QListWidgetItem(f"{wordlist_file.name} (Custom)")
                item.setData(Qt.ItemDataRole.UserRole, str(wordlist_file))
                self.wordlist_files.addItem(item)
    
    def on_wordlist_changed(self, current, previous):
        """Handle wordlist selection change"""
        if not current:
            self.clear_wordlist_display()
            return
        
        file_path = current.data(Qt.ItemDataRole.UserRole)
        self.load_wordlist_content(file_path)
    
    def load_wordlist_content(self, file_path):
        """Load and display wordlist content"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Update info
            file_info = Path(file_path)
            self.wordlist_name_label.setText(file_info.name)
            self.wordlist_size_label.setText(f"{file_info.stat().st_size:,} bytes")
            
            lines = content.split('\n')
            self.wordlist_lines_label.setText(f"{len(lines):,} lines")
            
            # Determine type
            if 'custom' in str(file_path):
                self.wordlist_type_label.setText("Custom")
            else:
                self.wordlist_type_label.setText("Default")
            
            # Update preview
            self.preview_text.setPlainText(content)
            self.edit_text.setPlainText(content)
            
            # Update statistics
            self.update_statistics(lines)
            
            # Enable buttons
            self.delete_wordlist_btn.setEnabled('custom' in str(file_path))
            self.export_btn.setEnabled(True)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load wordlist: {str(e)}")
    
    def update_statistics(self, lines):
        """Update wordlist statistics"""
        # Clean lines (remove empty and comments)
        clean_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
        
        # Calculate statistics
        stats = {
            "Total Lines": len(lines),
            "Valid Entries": len(clean_lines),
            "Empty Lines": len(lines) - len([l for l in lines if l.strip()]),
            "Comment Lines": len([l for l in lines if l.strip().startswith('#')]),
            "Unique Entries": len(set(clean_lines)),
            "Duplicates": len(clean_lines) - len(set(clean_lines)),
            "Average Length": f"{sum(len(l) for l in clean_lines) / len(clean_lines):.1f}" if clean_lines else "0",
            "Min Length": min(len(l) for l in clean_lines) if clean_lines else 0,
            "Max Length": max(len(l) for l in clean_lines) if clean_lines else 0,
        }
        
        # Update table
        self.stats_table.setRowCount(len(stats))
        for i, (metric, value) in enumerate(stats.items()):
            self.stats_table.setItem(i, 0, QTableWidgetItem(metric))
            self.stats_table.setItem(i, 1, QTableWidgetItem(str(value)))
    
    def clear_wordlist_display(self):
        """Clear wordlist display"""
        self.wordlist_name_label.setText("No wordlist selected")
        self.wordlist_size_label.setText("-")
        self.wordlist_lines_label.setText("-")
        self.wordlist_type_label.setText("-")
        self.preview_text.clear()
        self.edit_text.clear()
        self.stats_table.setRowCount(0)
        self.delete_wordlist_btn.setEnabled(False)
        self.export_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
    
    def filter_preview(self, text):
        """Filter preview based on search text"""
        if not text:
            # Show all content
            current_item = self.wordlist_files.currentItem()
            if current_item:
                file_path = current_item.data(Qt.ItemDataRole.UserRole)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    self.preview_text.setPlainText(f.read())
        else:
            # Filter content
            content = self.preview_text.toPlainText()
            lines = content.split('\n')
            filtered_lines = [line for line in lines if text.lower() in line.lower()]
            self.preview_text.setPlainText('\n'.join(filtered_lines))
    
    def add_wordlist(self):
        """Add new wordlist"""
        current_category_item = self.category_list.currentItem()
        if not current_category_item:
            QMessageBox.warning(self, "Warning", "Please select a category first")
            return
        
        category = current_category_item.data(Qt.ItemDataRole.UserRole)
        
        # Choose method
        reply = QMessageBox.question(
            self, "Add Wordlist",
            "How would you like to add a wordlist?",
            QMessageBox.StandardButton.Open | QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel
        )
        
        if reply == QMessageBox.StandardButton.Open:
            self.import_wordlist(category)
        elif reply == QMessageBox.StandardButton.Save:
            self.create_new_wordlist(category)
    
    def import_wordlist(self, category):
        """Import wordlist from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Wordlist", "", 
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            # Get custom name
            name, ok = QInputDialog.getText(
                self, "Wordlist Name", 
                "Enter name for the wordlist:",
                text=Path(file_path).stem
            )
            
            if ok and name:
                # Copy to custom directory
                custom_path = self.custom_wordlists_dir / f"{category}_{name}.txt"
                shutil.copy2(file_path, custom_path)
                
                # Reload wordlists
                self.load_wordlists_for_category(category)
                
                QMessageBox.information(self, "Success", f"Wordlist imported as {custom_path.name}")
    
    def create_new_wordlist(self, category):
        """Create new empty wordlist"""
        name, ok = QInputDialog.getText(
            self, "New Wordlist", 
            "Enter name for the new wordlist:"
        )
        
        if ok and name:
            custom_path = self.custom_wordlists_dir / f"{category}_{name}.txt"
            
            # Create empty file with header
            with open(custom_path, 'w') as f:
                f.write(f"# Custom {self.wordlist_categories[category]} Wordlist\n")
                f.write(f"# Created: {QTimer().remainingTime()}\n")
                f.write("# Add your entries below:\n\n")
            
            # Reload and select new wordlist
            self.load_wordlists_for_category(category)
            
            # Find and select the new wordlist
            for i in range(self.wordlist_files.count()):
                item = self.wordlist_files.item(i)
                if custom_path.name in item.text():
                    self.wordlist_files.setCurrentItem(item)
                    break
            
            QMessageBox.information(self, "Success", f"New wordlist created: {custom_path.name}")
    
    def delete_wordlist(self):
        """Delete selected wordlist"""
        current_item = self.wordlist_files.currentItem()
        if not current_item:
            return
        
        file_path = current_item.data(Qt.ItemDataRole.UserRole)
        
        if 'custom' not in str(file_path):
            QMessageBox.warning(self, "Warning", "Cannot delete default wordlists")
            return
        
        reply = QMessageBox.question(
            self, "Delete Wordlist",
            f"Are you sure you want to delete {Path(file_path).name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(file_path)
                
                # Reload wordlists
                current_category_item = self.category_list.currentItem()
                if current_category_item:
                    category = current_category_item.data(Qt.ItemDataRole.UserRole)
                    self.load_wordlists_for_category(category)
                
                QMessageBox.information(self, "Success", "Wordlist deleted successfully")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete wordlist: {str(e)}")
    
    def on_text_changed(self):
        """Handle text changes in edit tab"""
        self.save_btn.setEnabled(True)
    
    def save_wordlist(self):
        """Save wordlist changes"""
        current_item = self.wordlist_files.currentItem()
        if not current_item:
            return
        
        file_path = current_item.data(Qt.ItemDataRole.UserRole)
        content = self.edit_text.toPlainText()
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.save_btn.setEnabled(False)
            
            # Reload content to update statistics
            self.load_wordlist_content(file_path)
            
            QMessageBox.information(self, "Success", "Wordlist saved successfully")
            
            # Emit signal for other components
            current_category_item = self.category_list.currentItem()
            if current_category_item:
                category = current_category_item.data(Qt.ItemDataRole.UserRole)
                self.wordlist_updated.emit(category, file_path)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save wordlist: {str(e)}")
    
    def export_wordlist(self):
        """Export wordlist to file"""
        current_item = self.wordlist_files.currentItem()
        if not current_item:
            return
        
        file_path = current_item.data(Qt.ItemDataRole.UserRole)
        source_name = Path(file_path).name
        
        export_path, _ = QFileDialog.getSaveFileName(
            self, "Export Wordlist", source_name,
            "Text Files (*.txt);;All Files (*)"
        )
        
        if export_path:
            try:
                shutil.copy2(file_path, export_path)
                QMessageBox.information(self, "Success", f"Wordlist exported to {export_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export wordlist: {str(e)}")
    
    def add_line(self):
        """Add new line to wordlist"""
        text, ok = QInputDialog.getText(self, "Add Line", "Enter new line:")
        
        if ok and text:
            current_content = self.edit_text.toPlainText()
            if current_content and not current_content.endswith('\n'):
                current_content += '\n'
            current_content += text + '\n'
            self.edit_text.setPlainText(current_content)
    
    def remove_duplicates(self):
        """Remove duplicate lines from wordlist"""
        content = self.edit_text.toPlainText()
        lines = content.split('\n')
        
        # Preserve comments and empty lines at the top
        header_lines = []
        content_lines = []
        
        for line in lines:
            if line.strip().startswith('#') or not line.strip():
                if not content_lines:  # Only preserve header comments
                    header_lines.append(line)
            else:
                content_lines.append(line.strip())
        
        # Remove duplicates while preserving order
        seen = set()
        unique_lines = []
        for line in content_lines:
            if line and line not in seen:
                seen.add(line)
                unique_lines.append(line)
        
        # Combine header and unique content
        result = header_lines + unique_lines
        self.edit_text.setPlainText('\n'.join(result))
        
        QMessageBox.information(self, "Success", f"Removed {len(content_lines) - len(unique_lines)} duplicates")
    
    def sort_wordlist(self):
        """Sort wordlist alphabetically"""
        content = self.edit_text.toPlainText()
        lines = content.split('\n')
        
        # Separate comments/empty lines from content
        header_lines = []
        content_lines = []
        
        for line in lines:
            if line.strip().startswith('#') or not line.strip():
                if not content_lines:  # Only preserve header comments
                    header_lines.append(line)
            else:
                content_lines.append(line.strip())
        
        # Sort content lines
        content_lines.sort(key=str.lower)
        
        # Combine
        result = header_lines + content_lines
        self.edit_text.setPlainText('\n'.join(result))
        
        QMessageBox.information(self, "Success", "Wordlist sorted alphabetically")
    
    def clean_wordlist(self):
        """Clean wordlist (remove empty lines, trim whitespace)"""
        content = self.edit_text.toPlainText()
        lines = content.split('\n')
        
        # Clean lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # Keep non-empty lines
                if line.strip().startswith('#'):
                    cleaned_lines.append(line)  # Keep comments as-is
                else:
                    cleaned_lines.append(line.strip())  # Trim whitespace
        
        self.edit_text.setPlainText('\n'.join(cleaned_lines))
        
        QMessageBox.information(self, "Success", f"Cleaned wordlist ({len(lines) - len(cleaned_lines)} lines removed)")
    
    def merge_wordlists(self):
        """Merge multiple wordlists"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Wordlists to Merge", "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if len(files) < 2:
            QMessageBox.warning(self, "Warning", "Please select at least 2 wordlists to merge")
            return
        
        # Get merge name
        name, ok = QInputDialog.getText(
            self, "Merge Wordlists",
            "Enter name for merged wordlist:"
        )
        
        if not ok or not name:
            return
        
        try:
            # Merge files
            merged_lines = set()
            
            for file_path in files:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            merged_lines.add(line)
            
            # Save merged wordlist
            current_category_item = self.category_list.currentItem()
            if current_category_item:
                category = current_category_item.data(Qt.ItemDataRole.UserRole)
                merged_path = self.custom_wordlists_dir / f"{category}_{name}.txt"
                
                with open(merged_path, 'w', encoding='utf-8') as f:
                    f.write(f"# Merged {self.wordlist_categories[category]} Wordlist\n")
                    f.write(f"# Merged from {len(files)} wordlists\n")
                    f.write(f"# Total entries: {len(merged_lines)}\n\n")
                    
                    for line in sorted(merged_lines, key=str.lower):
                        f.write(line + '\n')
                
                # Reload wordlists
                self.load_wordlists_for_category(category)
                
                QMessageBox.information(
                    self, "Success", 
                    f"Merged {len(files)} wordlists into {merged_path.name}\n"
                    f"Total unique entries: {len(merged_lines)}"
                )
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to merge wordlists: {str(e)}")
    
    def download_popular_wordlists(self):
        """Download popular wordlists from the internet"""
        popular_wordlists = {
            'directories': [
                ('SecLists - Common', 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt'),
                ('SecLists - Directory List 2.3 Medium', 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/directory-list-2.3-medium.txt'),
                ('DirBuster - Common', 'https://raw.githubusercontent.com/daviddias/node-dirbuster/master/lists/directory-list-2.3-medium.txt')
            ],
            'subdomains': [
                ('SecLists - Subdomains Top 1M', 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-110000.txt'),
                ('Assetnote - Best DNS Wordlist', 'https://wordlists-cdn.assetnote.io/data/manual/best-dns-wordlist.txt')
            ],
            'parameters': [
                ('SecLists - Burp Parameter Names', 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/burp-parameter-names.txt'),
                ('Assetnote - Parameter Names', 'https://wordlists-cdn.assetnote.io/data/manual/param-miner.txt')
            ]
        }
        
        # Show download dialog
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton, QScrollArea
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Download Popular Wordlists")
        dialog.setModal(True)
        dialog.resize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        checkboxes = {}
        
        for category, wordlists in popular_wordlists.items():
            category_label = QLabel(f"{self.wordlist_categories.get(category, category).upper()}")
            category_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            scroll_layout.addWidget(category_label)
            
            for name, url in wordlists:
                checkbox = QCheckBox(name)
                checkbox.setData(Qt.ItemDataRole.UserRole, (category, url, name))
                checkboxes[checkbox] = (category, url, name)
                scroll_layout.addWidget(checkbox)
            
            scroll_layout.addWidget(QLabel(""))  # Spacer
        
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        download_btn = QPushButton("Download Selected")
        download_btn.clicked.connect(lambda: self.perform_downloads(dialog, checkboxes))
        button_layout.addWidget(download_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        dialog.exec()
    
    def perform_downloads(self, dialog, checkboxes):
        """Perform the actual downloads"""
        selected = [(category, url, name) for checkbox, (category, url, name) in checkboxes.items() 
                   if checkbox.isChecked()]
        
        if not selected:
            QMessageBox.warning(dialog, "Warning", "Please select at least one wordlist to download")
            return
        
        dialog.accept()
        
        # Show progress dialog
        progress_dialog = QMessageBox(self)
        progress_dialog.setWindowTitle("Downloading Wordlists")
        progress_dialog.setText("Downloading wordlists, please wait...")
        progress_dialog.setStandardButtons(QMessageBox.StandardButton.NoButton)
        progress_dialog.show()
        
        # Download in separate thread (simplified for this example)
        import requests
        
        downloaded = 0
        failed = 0
        
        for category, url, name in selected:
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                # Save to custom directory
                filename = f"{category}_{name.replace(' ', '_').replace('-', '_')}.txt"
                file_path = self.custom_wordlists_dir / filename
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {name}\n")
                    f.write(f"# Downloaded from: {url}\n")
                    f.write(f"# Date: {QTimer().remainingTime()}\n\n")
                    f.write(response.text)
                
                downloaded += 1
                
            except Exception as e:
                print(f"Failed to download {name}: {e}")
                failed += 1
        
        progress_dialog.close()
        
        # Reload current category
        current_category_item = self.category_list.currentItem()
        if current_category_item:
            category = current_category_item.data(Qt.ItemDataRole.UserRole)
            self.load_wordlists_for_category(category)
        
        QMessageBox.information(
            self, "Download Complete",
            f"Downloaded: {downloaded}\nFailed: {failed}"
        )
    
    def get_selected_wordlist(self, category):
        """Get the currently selected wordlist for a category"""
        # This method can be called by other components to get the active wordlist
        current_item = self.wordlist_files.currentItem()
        if current_item:
            return current_item.data(Qt.ItemDataRole.UserRole)
        
        # Return default wordlist if none selected
        default_file = self.wordlists_dir / f"{category}.txt"
        if default_file.exists():
            return str(default_file)
        
        return None