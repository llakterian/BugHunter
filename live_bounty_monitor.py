#!/usr/bin/env python3
"""
Live Bounty Monitor - Real-time monitoring of bug bounty programs and new targets
"""

import requests
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import feedparser
import re

class LiveBountyMonitor(QObject):
    """Real-time bug bounty program monitor"""
    
    new_program_found = pyqtSignal(dict)
    new_target_found = pyqtSignal(dict)
    vulnerability_trend_updated = pyqtSignal(str, float)
    monitoring_status_changed = pyqtSignal(str)
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Monitoring sources
        self.sources = {
            'twitter_feeds': [
                'https://nitter.net/hackerone/rss',
                'https://nitter.net/bugcrowd/rss',
                'https://nitter.net/intigriti/rss'
            ],
            'rss_feeds': [
                'https://feeds.feedburner.com/oreilly/security',
                'https://krebsonsecurity.com/feed/',
                'https://threatpost.com/feed/'
            ],
            'github_repos': [
                'https://api.github.com/repos/arkadiyt/bounty-targets-data/commits',
                'https://api.github.com/repos/projectdiscovery/public-bugbounty-programs/commits'
            ]
        }
        
        # Cache for seen items
        self.seen_programs = set()
        self.seen_targets = set()
        self.last_check = datetime.now()
        
        # Setup monitoring timer
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.check_for_updates)
    
    def start_monitoring(self, interval_minutes: int = 30):
        """Start real-time monitoring"""
        if self.is_monitoring:
            return False
        
        self.is_monitoring = True
        self.monitoring_status_changed.emit("Starting monitoring...")
        
        # Start monitoring timer
        self.monitor_timer.start(interval_minutes * 60 * 1000)  # Convert to milliseconds
        
        # Do initial check
        self.check_for_updates()
        
        self.monitoring_status_changed.emit(f"Monitoring active (every {interval_minutes}m)")
        return True
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        self.monitor_timer.stop()
        self.monitoring_status_changed.emit("Monitoring stopped")
    
    def check_for_updates(self):
        """Check all sources for updates"""
        if not self.is_monitoring:
            return
        
        self.monitoring_status_changed.emit("Checking for updates...")
        
        # Check different sources in parallel
        with threading.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            
            # Check RSS feeds
            futures.append(executor.submit(self.check_rss_feeds))
            
            # Check GitHub repositories
            futures.append(executor.submit(self.check_github_repos))
            
            # Check platform APIs
            futures.append(executor.submit(self.check_platform_apis))
            
            # Wait for all checks to complete
            for future in futures:
                try:
                    future.result(timeout=60)
                except Exception as e:
                    print(f"Monitoring check error: {e}")
        
        self.last_check = datetime.now()
        self.monitoring_status_changed.emit(f"Last check: {self.last_check.strftime('%H:%M:%S')}")
    
    def check_rss_feeds(self):
        """Check RSS feeds for new content"""
        for feed_url in self.sources['rss_feeds']:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries:
                    # Check if entry is new (since last check)
                    try:
                        entry_date = datetime(*entry.published_parsed[:6])
                        if entry_date > self.last_check:
                            self.analyze_feed_entry(entry, feed_url)
                    except:
                        # If no date, assume it's new
                        self.analyze_feed_entry(entry, feed_url)
                        
            except Exception as e:
                print(f"RSS feed error ({feed_url}): {e}")
    
    def analyze_feed_entry(self, entry, source_url):
        """Analyze RSS feed entry for bug bounty relevance"""
        title = entry.get('title', '').lower()
        description = entry.get('description', '').lower()
        content = f"{title} {description}"
        
        # Bug bounty keywords
        bounty_keywords = [
            'bug bounty', 'vulnerability disclosure', 'security researcher',
            'responsible disclosure', 'hall of fame', 'security program',
            'bounty program', 'vulnerability reward', 'security bounty'
        ]
        
        # Vulnerability keywords
        vuln_keywords = [
            'xss', 'sql injection', 'csrf', 'rce', 'lfi', 'ssrf',
            'jwt', 'authentication bypass', 'privilege escalation',
            'directory traversal', 'command injection', 'xxe'
        ]
        
        # Check for bug bounty program announcements
        if any(keyword in content for keyword in bounty_keywords):
            program_info = {
                'title': entry.get('title', ''),
                'url': entry.get('link', ''),
                'description': entry.get('description', ''),
                'source': source_url,
                'found_at': datetime.now().isoformat(),
                'type': 'program_announcement'
            }
            
            program_id = f"{entry.get('link', '')}{entry.get('title', '')}"
            if program_id not in self.seen_programs:
                self.seen_programs.add(program_id)
                self.new_program_found.emit(program_info)
        
        # Check for vulnerability disclosures
        if any(keyword in content for keyword in vuln_keywords):
            vuln_info = {
                'title': entry.get('title', ''),
                'url': entry.get('link', ''),
                'description': entry.get('description', ''),
                'source': source_url,
                'found_at': datetime.now().isoformat(),
                'type': 'vulnerability_disclosure',
                'vulnerability_types': [kw for kw in vuln_keywords if kw in content]
            }
            
            # Update vulnerability trends
            for vuln_type in vuln_info['vulnerability_types']:
                self.vulnerability_trend_updated.emit(vuln_type, 1.0)
    
    def check_github_repos(self):
        """Check GitHub repositories for new bug bounty targets"""
        for repo_url in self.sources['github_repos']:
            try:
                response = requests.get(repo_url, timeout=30)
                
                if response.status_code == 200:
                    commits = response.json()
                    
                    for commit in commits[:5]:  # Check last 5 commits
                        commit_date = datetime.fromisoformat(
                            commit['commit']['author']['date'].replace('Z', '+00:00')
                        )
                        
                        if commit_date.replace(tzinfo=None) > self.last_check:
                            self.analyze_github_commit(commit, repo_url)
                            
            except Exception as e:
                print(f"GitHub check error ({repo_url}): {e}")
    
    def analyze_github_commit(self, commit, repo_url):
        """Analyze GitHub commit for new targets"""
        commit_message = commit['commit']['message'].lower()
        
        # Look for new program additions
        if any(keyword in commit_message for keyword in ['add', 'new', 'program', 'target']):
            target_info = {
                'commit_message': commit['commit']['message'],
                'commit_url': commit['html_url'],
                'repository': repo_url,
                'author': commit['commit']['author']['name'],
                'date': commit['commit']['author']['date'],
                'type': 'new_target_commit'
            }
            
            commit_id = commit['sha']
            if commit_id not in self.seen_targets:
                self.seen_targets.add(commit_id)
                self.new_target_found.emit(target_info)
    
    def check_platform_apis(self):
        """Check platform APIs for new programs"""
        # HackerOne new programs
        try:
            response = requests.get(
                'https://hackerone.com/programs.json?sort=launched_at&order=desc',
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                for program in data.get('results', [])[:10]:  # Check top 10 newest
                    launched_at = program.get('launched_at')
                    if launched_at:
                        try:
                            launch_date = datetime.fromisoformat(launched_at.replace('Z', '+00:00'))
                            if launch_date.replace(tzinfo=None) > self.last_check:
                                program_info = {
                                    'name': program.get('name', ''),
                                    'handle': program.get('handle', ''),
                                    'url': f"https://hackerone.com/{program.get('handle', '')}",
                                    'launched_at': launched_at,
                                    'platform': 'hackerone',
                                    'type': 'new_program'
                                }
                                
                                program_id = program.get('handle', '')
                                if program_id not in self.seen_programs:
                                    self.seen_programs.add(program_id)
                                    self.new_program_found.emit(program_info)
                        except:
                            continue
                            
        except Exception as e:
            print(f"HackerOne API check error: {e}")
    
    def get_monitoring_stats(self) -> Dict:
        """Get monitoring statistics"""
        return {
            'is_monitoring': self.is_monitoring,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'programs_tracked': len(self.seen_programs),
            'targets_tracked': len(self.seen_targets),
            'uptime': str(datetime.now() - self.last_check) if self.last_check else "0:00:00"
        }