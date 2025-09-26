#!/usr/bin/env python3
"""
Bug Bounty Site Finder - Find active bug bounty programs
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict
import re

class BugBountySiteFinder:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Known bug bounty platforms
        self.platforms = {
            'HackerOne': 'https://hackerone.com',
            'Bugcrowd': 'https://bugcrowd.com',
            'Intigriti': 'https://intigriti.com',
            'YesWeHack': 'https://yeswehack.com',
            'HackenProof': 'https://hackenproof.com',
            'Synack': 'https://synack.com'
        }
        
        # Popular companies with bug bounty programs
        self.known_programs = [
            {'name': 'Google', 'url': 'https://bughunters.google.com', 'platform': 'Google VRP', 'max_payout': '$31337+'},
            {'name': 'Microsoft', 'url': 'https://msrc.microsoft.com', 'platform': 'Microsoft MSRC', 'max_payout': '$15000+'},
            {'name': 'Apple', 'url': 'https://developer.apple.com/security-bounty/', 'platform': 'Apple Security Bounty', 'max_payout': '$1000000+'},
            {'name': 'Facebook/Meta', 'url': 'https://facebook.com/whitehat', 'platform': 'Meta Bug Bounty', 'max_payout': '$40000+'},
            {'name': 'Tesla', 'url': 'https://bugcrowd.com/tesla', 'platform': 'Bugcrowd', 'max_payout': '$15000+'},
            {'name': 'Netflix', 'url': 'https://hackerone.com/netflix', 'platform': 'HackerOne', 'max_payout': '$15000+'},
            {'name': 'Uber', 'url': 'https://hackerone.com/uber', 'platform': 'HackerOne', 'max_payout': '$10000+'},
            {'name': 'Airbnb', 'url': 'https://hackerone.com/airbnb', 'platform': 'HackerOne', 'max_payout': '$5000+'},
            {'name': 'Twitter', 'url': 'https://hackerone.com/twitter', 'platform': 'HackerOne', 'max_payout': '$20160+'},
            {'name': 'GitHub', 'url': 'https://bounty.github.com', 'platform': 'GitHub Security Bug Bounty', 'max_payout': '$30000+'},
            {'name': 'Shopify', 'url': 'https://hackerone.com/shopify', 'platform': 'HackerOne', 'max_payout': '$25000+'},
            {'name': 'Dropbox', 'url': 'https://hackerone.com/dropbox', 'platform': 'HackerOne', 'max_payout': '$32768+'},
            {'name': 'PayPal', 'url': 'https://hackerone.com/paypal', 'platform': 'HackerOne', 'max_payout': '$30000+'},
            {'name': 'Coinbase', 'url': 'https://hackerone.com/coinbase', 'platform': 'HackerOne', 'max_payout': '$50000+'},
            {'name': 'Slack', 'url': 'https://hackerone.com/slack', 'platform': 'HackerOne', 'max_payout': '$17500+'},
            {'name': 'Spotify', 'url': 'https://hackerone.com/spotify', 'platform': 'HackerOne', 'max_payout': '$10000+'},
            {'name': 'Reddit', 'url': 'https://hackerone.com/reddit', 'platform': 'HackerOne', 'max_payout': '$5000+'},
            {'name': 'TikTok', 'url': 'https://hackerone.com/tiktok', 'platform': 'HackerOne', 'max_payout': '$15000+'},
            {'name': 'Discord', 'url': 'https://hackerone.com/discord', 'platform': 'HackerOne', 'max_payout': '$25000+'},
            {'name': 'Zoom', 'url': 'https://hackerone.com/zoom', 'platform': 'HackerOne', 'max_payout': '$50000+'}
        ]
    
    def find_active_programs(self) -> List[Dict]:
        """Find active bug bounty programs"""
        print("🔍 Searching for active bug bounty programs...")
        
        active_programs = []
        
        # Check known programs
        for program in self.known_programs:
            try:
                print(f"Checking {program['name']}...")
                status = self.check_program_status(program['url'])
                
                program_info = {
                    'name': program['name'],
                    'url': program['url'],
                    'platform': program['platform'],
                    'max_payout': program['max_payout'],
                    'status': status,
                    'last_checked': datetime.now().isoformat()
                }
                
                active_programs.append(program_info)
                time.sleep(1)  # Be respectful with requests
                
            except Exception as e:
                print(f"Error checking {program['name']}: {e}")
        
        # Sort by estimated payout (extract numbers from max_payout)
        active_programs.sort(key=lambda x: self.extract_payout_value(x['max_payout']), reverse=True)
        
        return active_programs
    
    def check_program_status(self, url: str) -> str:
        """Check if a bug bounty program is active"""
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for active indicators
                active_indicators = [
                    'bug bounty', 'vulnerability', 'security', 'reward',
                    'responsible disclosure', 'hall of fame', 'submit'
                ]
                
                inactive_indicators = [
                    'program closed', 'no longer accepting', 'discontinued',
                    'suspended', 'paused', 'ended'
                ]
                
                # Check for inactive indicators first
                for indicator in inactive_indicators:
                    if indicator in content:
                        return 'Inactive'
                
                # Check for active indicators
                active_count = sum(1 for indicator in active_indicators if indicator in content)
                
                if active_count >= 2:
                    return 'Active'
                elif active_count >= 1:
                    return 'Possibly Active'
                else:
                    return 'Unknown'
            
            elif response.status_code == 404:
                return 'Not Found'
            else:
                return f'HTTP {response.status_code}'
                
        except requests.exceptions.RequestException:
            return 'Connection Error'
    
    def extract_payout_value(self, payout_str: str) -> int:
        """Extract numeric value from payout string for sorting"""
        # Extract numbers from strings like "$15000+", "$1000000+"
        numbers = re.findall(r'\d+', payout_str)
        if numbers:
            return int(numbers[0])
        return 0
    
    def get_top_programs(self, programs: List[Dict], count: int = 6) -> List[Dict]:
        """Get top N programs by payout"""
        return programs[:count]
    
    def display_programs(self, programs: List[Dict]):
        """Display programs in a formatted way"""
        print("\n" + "="*80)
        print("🎯 TOP BUG BOUNTY PROGRAMS")
        print("="*80)
        
        for i, program in enumerate(programs, 1):
            status_emoji = {
                'Active': '✅',
                'Possibly Active': '🟡',
                'Inactive': '❌',
                'Unknown': '❓',
                'Not Found': '🚫',
                'Connection Error': '⚠️'
            }.get(program['status'], '❓')
            
            print(f"\n{i}. {program['name']} {status_emoji}")
            print(f"   Platform: {program['platform']}")
            print(f"   Max Payout: {program['max_payout']}")
            print(f"   URL: {program['url']}")
            print(f"   Status: {program['status']}")
            print("-" * 60)
    
    def save_results(self, programs: List[Dict], filename: str = None):
        """Save results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bug_bounty_programs_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'total_programs': len(programs),
                'programs': programs
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")
        return filename

def main():
    """Main function to run the bug bounty finder"""
    print("🚀 Bug Bounty Site Finder - Finding Active Programs")
    print("=" * 60)
    
    finder = BugBountySiteFinder()
    
    # Find all active programs
    all_programs = finder.find_active_programs()
    
    # Get top 6 programs
    top_programs = finder.get_top_programs(all_programs, 6)
    
    # Display results
    finder.display_programs(top_programs)
    
    # Save results
    filename = finder.save_results(all_programs)
    
    print(f"\n🎉 Found {len(all_programs)} bug bounty programs")
    print(f"📊 Top 6 programs displayed above")
    print(f"💰 Highest payout: {top_programs[0]['max_payout'] if top_programs else 'N/A'}")
    
    return top_programs

if __name__ == "__main__":
    main()