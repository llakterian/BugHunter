"""
Wordlist Manager - Comprehensive wordlist management for Bug Bounty Hunter Pro
Manages various security testing wordlists and provides selection interface
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QListWidget, QListWidgetItem,
                             QComboBox, QDialog, QGridLayout, QFileDialog,
                             QMessageBox, QGroupBox, QTabWidget, QSplitter,
                             QTextEdit, QProgressBar, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import os
import json
from typing import Dict, List, Optional


class WordlistSelector(QWidget):
    """Wordlist selector widget for specific categories"""

    wordlist_changed = pyqtSignal(str, str)  # category, file_path

    def __init__(self, category: str, config_manager):
        super().__init__()
        self.category = category
        self.config_manager = config_manager
        self.wordlist_dir = "wordlists"

        self.setup_ui()
        self.load_wordlists()

    def setup_ui(self):
        """Setup the wordlist selector UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.combo = QComboBox()
        self.combo.setMinimumWidth(120)
        self.combo.currentTextChanged.connect(self.on_selection_changed)

        layout.addWidget(self.combo)

    def load_wordlists(self):
        """Load available wordlists for this category"""
        self.combo.clear()

        # Default option
        self.combo.addItem("Default", "")

        # Load from wordlists directory
        if os.path.exists(self.wordlist_dir):
            for file in os.listdir(self.wordlist_dir):
                if file.startswith(self.category) or self.category in file:
                    filepath = os.path.join(self.wordlist_dir, file)
                    if os.path.isfile(filepath):
                        self.combo.addItem(file, filepath)

        # Load saved selection
        saved = self.config_manager.get_wordlists_config().get(self.category, "")
        if saved and os.path.exists(saved):
            index = self.combo.findData(saved)
            if index >= 0:
                self.combo.setCurrentIndex(index)

    def on_selection_changed(self, text):
        """Handle wordlist selection change"""
        filepath = self.combo.currentData()
        if filepath:
            self.wordlist_changed.emit(self.category, filepath)


class WordlistManager(QDialog):
    """Comprehensive wordlist manager dialog"""

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.wordlist_dir = "wordlists"

        self.setWindowTitle("Wordlist Manager - Bug Bounty Hunter Pro")
        self.setModal(True)
        self.resize(800, 600)

        self.setup_ui()
        self.load_wordlists()

    def setup_ui(self):
        """Setup the wordlist manager UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Wordlist Manager")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        # Splitter for categories and content
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - Categories
        self.category_list = QListWidget()
        self.category_list.itemClicked.connect(self.on_category_selected)
        splitter.addWidget(self.category_list)

        # Right panel - Wordlist details
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Wordlist list
        self.wordlist_list = QListWidget()
        self.wordlist_list.itemDoubleClicked.connect(self.view_wordlist)
        right_layout.addWidget(self.wordlist_list)

        # Action buttons
        button_layout = QHBoxLayout()

        self.view_btn = QPushButton("View Content")
        self.view_btn.clicked.connect(self.view_wordlist)
        button_layout.addWidget(self.view_btn)

        self.import_btn = QPushButton("Import Wordlist")
        self.import_btn.clicked.connect(self.import_wordlist)
        button_layout.addWidget(self.import_btn)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_wordlist)
        button_layout.addWidget(self.delete_btn)

        right_layout.addLayout(button_layout)

        splitter.addWidget(right_panel)
        splitter.setSizes([200, 600])

        layout.addWidget(splitter)

        # Bottom buttons
        bottom_layout = QHBoxLayout()

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_wordlists)
        bottom_layout.addWidget(self.refresh_btn)

        bottom_layout.addStretch()

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        bottom_layout.addWidget(self.close_btn)

        layout.addLayout(bottom_layout)

    def load_wordlists(self):
        """Load wordlists from directory"""
        self.category_list.clear()

        if not os.path.exists(self.wordlist_dir):
            os.makedirs(self.wordlist_dir, exist_ok=True)
            return

        # Group wordlists by category
        categories = {}
        for file in os.listdir(self.wordlist_dir):
            if file.endswith('.txt'):
                # Determine category from filename
                category = "misc"
                if "password" in file.lower():
                    category = "passwords"
                elif "user" in file.lower():
                    category = "usernames"
                elif "subdomain" in file.lower():
                    category = "subdomains"
                elif "directory" in file.lower() or "endpoint" in file.lower():
                    category = "directories"
                elif "param" in file.lower():
                    category = "parameters"
                elif "xss" in file.lower():
                    category = "xss"
                elif "sqli" in file.lower():
                    category = "sqli"
                elif "lfi" in file.lower():
                    category = "lfi"
                elif "ssrf" in file.lower():
                    category = "ssrf"
                elif "jwt" in file.lower():
                    category = "jwt"

                if category not in categories:
                    categories[category] = []
                categories[category].append(file)

        # Add to category list
        for category in sorted(categories.keys()):
            item = QListWidgetItem(f"{category.title()} ({len(categories[category])} files)")
            item.setData(Qt.ItemDataRole.UserRole, (category, categories[category]))
            self.category_list.addItem(item)

    def on_category_selected(self, item):
        """Handle category selection"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if data:
            category, files = data
            self.wordlist_list.clear()
            for file in files:
                filepath = os.path.join(self.wordlist_dir, file)
                try:
                    # Get file size and line count
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        size = len(lines)
                        file_size = os.path.getsize(filepath)

                    display_text = f"{file} ({size} entries, {file_size} bytes)"
                    list_item = QListWidgetItem(display_text)
                    list_item.setData(Qt.ItemDataRole.UserRole, filepath)
                    self.wordlist_list.addItem(list_item)
                except Exception as e:
                    display_text = f"{file} (Error reading file)"
                    list_item = QListWidgetItem(display_text)
                    list_item.setData(Qt.ItemDataRole.UserRole, filepath)
                    self.wordlist_list.addItem(list_item)

    def view_wordlist(self):
        """View selected wordlist content"""
        current_item = self.wordlist_list.currentItem()
        if not current_item:
            return

        filepath = current_item.data(Qt.ItemDataRole.UserRole)
        if not filepath or not os.path.exists(filepath):
            QMessageBox.warning(self, "Error", "Wordlist file not found")
            return

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(10000)  # First 10KB

            # Show content in dialog
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Wordlist Content - {os.path.basename(filepath)}")
            dialog.resize(600, 400)

            layout = QVBoxLayout(dialog)

            text_edit = QTextEdit()
            text_edit.setPlainText(content)
            text_edit.setReadOnly(True)
            layout.addWidget(text_edit)

            close_btn = QPushButton("Close")
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)

            dialog.exec()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to read wordlist: {str(e)}")

    def import_wordlist(self):
        """Import a wordlist file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Wordlist", "", "Text Files (*.txt);;All Files (*)"
        )

        if not file_path:
            return

        # Ask for category
        categories = ["passwords", "usernames", "subdomains", "directories",
                     "parameters", "xss", "sqli", "lfi", "ssrf", "jwt", "misc"]

        category, ok = QInputDialog.getItem(
            self, "Import Wordlist", "Select category:",
            categories, 0, False
        )

        if not ok:
            return

        # Copy file to wordlists directory
        filename = f"{category}_{os.path.basename(file_path)}"
        dest_path = os.path.join(self.wordlist_dir, filename)

        try:
            import shutil
            shutil.copy2(file_path, dest_path)
            QMessageBox.information(self, "Success", "Wordlist imported successfully")
            self.load_wordlists()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to import wordlist: {str(e)}")

    def delete_wordlist(self):
        """Delete selected wordlist"""
        current_item = self.wordlist_list.currentItem()
        if not current_item:
            return

        filepath = current_item.data(Qt.ItemDataRole.UserRole)
        if not filepath:
            return

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{os.path.basename(filepath)}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(filepath)
                QMessageBox.information(self, "Success", "Wordlist deleted successfully")
                self.load_wordlists()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete wordlist: {str(e)}")


# Import here to avoid circular imports
from PyQt6.QtWidgets import QInputDialog