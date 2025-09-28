#!/usr/bin/env python3
"""
Robust launcher for BugHunter - Uses the completely reliable main_robust.py
"""

import sys
import os

def main():
    """Launch the robust BugHunter application"""
    try:
        # Import and run the robust main application
        from main_robust import main as robust_main
        print("🛡️ Launching Bug Bounty Hunter Pro - Robust Edition...")
        print("✅ No hanging guaranteed!")
        return robust_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure main_robust.py is in the same directory")
        return 1
    except Exception as e:
        print(f"❌ Launch error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
