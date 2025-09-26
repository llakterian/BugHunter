"""
Configuration Manager - Handle application settings and configurations
"""

import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    def __init__(self, config_file="data/config.json"):
        self.config_file = config_file
        self.config = {}
        self.ensure_data_directory()
        self.load_config()
        self.setup_default_config()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = {}
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def setup_default_config(self):
        """Setup default configuration values"""
        defaults = {
            "zap": {
                "host": "127.0.0.1",
                "port": 8080,
                "api_key": "",
                "auto_start": True,
                "proxy_port": 8081
            },
            "scanning": {
                "max_threads": 10,
                "timeout": 30,
                "user_agent": "BugBountyHunterPro/1.0",
                "follow_redirects": False,
                "max_redirects": 3
            },
            "wordlists": {
                "directories": "wordlists/directories.txt",
                "files": "wordlists/files.txt",
                "parameters": "wordlists/parameters.txt",
                "subdomains": "wordlists/subdomains.txt"
            },
            "jwt": {
                "weak_secrets_file": "wordlists/jwt_secrets.txt",
                "algorithms": ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]
            },
            "output": {
                "reports_dir": "reports",
                "screenshots_dir": "screenshots",
                "logs_dir": "logs"
            },
            "ui": {
                "theme": "dark",
                "auto_save": True,
                "update_interval": 1000
            }
        }
        
        # Merge defaults with existing config
        for key, value in defaults.items():
            if key not in self.config:
                self.config[key] = value
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if subkey not in self.config[key]:
                        self.config[key][subkey] = subvalue
        
        self.save_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        self.save_config()
    
    def get_zap_config(self) -> Dict[str, Any]:
        """Get ZAP configuration"""
        return self.config.get("zap", {})
    
    def get_scanning_config(self) -> Dict[str, Any]:
        """Get scanning configuration"""
        return self.config.get("scanning", {})
    
    def get_wordlists_config(self) -> Dict[str, Any]:
        """Get wordlists configuration"""
        return self.config.get("wordlists", {})
    
    def get_jwt_config(self) -> Dict[str, Any]:
        """Get JWT configuration"""
        return self.config.get("jwt", {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration"""
        return self.config.get("output", {})
    
    def update_zap_config(self, **kwargs):
        """Update ZAP configuration"""
        zap_config = self.config.get("zap", {})
        zap_config.update(kwargs)
        self.config["zap"] = zap_config
        self.save_config()
    
    def create_directories(self):
        """Create necessary directories"""
        output_config = self.get_output_config()
        
        directories = [
            output_config.get("reports_dir", "reports"),
            output_config.get("screenshots_dir", "screenshots"),
            output_config.get("logs_dir", "logs"),
            "wordlists",
            "data"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def export_config(self, filename: str) -> bool:
        """Export configuration to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False
    
    def import_config(self, filename: str) -> bool:
        """Import configuration from file"""
        try:
            with open(filename, 'r') as f:
                imported_config = json.load(f)
            
            # Merge imported config with current config
            self.config.update(imported_config)
            self.save_config()
            return True
        except Exception as e:
            print(f"Error importing config: {e}")
            return False