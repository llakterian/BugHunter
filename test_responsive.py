#!/usr/bin/env python3
"""
Test responsive layout on different screen sizes
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication

def test_screen_info():
    """Test screen information and responsive calculations"""
    app = QApplication(sys.argv)
    
    screen = QGuiApplication.primaryScreen()
    screen_geometry = screen.geometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()
    
    print("🖥️  Screen Information:")
    print(f"   Resolution: {screen_width} x {screen_height}")
    print(f"   DPI: {screen.logicalDotsPerInch()}")
    
    # Calculate responsive window size
    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)
    
    min_width = min(1000, int(screen_width * 0.6))
    min_height = min(700, int(screen_height * 0.6))
    
    print(f"\n📐 Calculated Window Sizes:")
    print(f"   Default: {window_width} x {window_height}")
    print(f"   Minimum: {min_width} x {min_height}")
    
    # Determine layout type
    if screen_width <= 1366:
        layout_type = "Compact (Small Screen)"
        left_panel_width = "250-280px"
        font_sizes = "10-11px (Improved)"
    else:
        layout_type = "Full (Large Screen)"
        left_panel_width = "280-320px"
        font_sizes = "11-12px"
    
    print(f"\n🎨 Layout Configuration:")
    print(f"   Type: {layout_type}")
    print(f"   Left Panel: {left_panel_width}")
    print(f"   Font Sizes: {font_sizes}")
    
    if screen_width <= 1366:
        print(f"\n💡 Optimizations for your screen:")
        print(f"   - Compact header with 'BB Hunter Pro'")
        print(f"   - Tabbed wordlist selectors")
        print(f"   - Grid layout for scan options")
        print(f"   - Smaller fonts and spacing")
        print(f"   - Scrollable left panel")
    
    app.quit()

if __name__ == "__main__":
    test_screen_info()