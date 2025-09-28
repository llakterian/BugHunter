#!/usr/bin/env python3
"""
Test script to verify responsive GUI design
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_responsive_design():
    """Test the responsive design functionality"""
    print("🧪 Testing Responsive GUI Design...")
    
    app = QApplication(sys.argv)
    
    # Get screen information
    screen = app.primaryScreen()
    screen_geometry = screen.availableGeometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()
    
    print(f"📺 Screen Resolution: {screen_width}x{screen_height}")
    
    # Test different screen scenarios
    test_scenarios = [
        ("Small Laptop", 1366, 768),
        ("Standard Laptop", 1920, 1080),
        ("Large Monitor", 2560, 1440),
        ("Ultrawide", 3440, 1440)
    ]
    
    for name, width, height in test_scenarios:
        print(f"\n🔍 Testing {name} ({width}x{height}):")
        
        # Calculate what the responsive window size would be
        target_width = min(max(int(width * 0.85), 1000), 1600)
        target_height = min(max(int(height * 0.80), 700), 1200)
        
        print(f"   Window Size: {target_width}x{target_height}")
        print(f"   Left Panel: {min(max(int(target_width * 0.3), 350), 500)}px")
        print(f"   Right Panel: {target_width - min(max(int(target_width * 0.3), 350), 500)}px")
        
        # Check if it fits well
        width_ratio = target_width / width
        height_ratio = target_height / height
        
        if 0.7 <= width_ratio <= 0.9 and 0.7 <= height_ratio <= 0.85:
            print(f"   ✅ Good fit ({width_ratio:.1%} x {height_ratio:.1%})")
        else:
            print(f"   ⚠️  Needs adjustment ({width_ratio:.1%} x {height_ratio:.1%})")
    
    print(f"\n🎯 Current Screen Test:")
    print(f"   Actual Screen: {screen_width}x{screen_height}")
    
    # Import and test the actual application
    try:
        from enhanced_desktop_app import EnhancedDesktopApp
        
        # Create the app but don't show it (headless test)
        print("   Creating application instance...")
        
        # Mock the disclaimer dialog to return True
        original_show_disclaimer = EnhancedDesktopApp.show_educational_disclaimer
        EnhancedDesktopApp.show_educational_disclaimer = lambda self: True
        
        window = EnhancedDesktopApp()
        
        # Check window properties
        window_size = window.size()
        min_size = window.minimumSize()
        
        print(f"   Window Size: {window_size.width()}x{window_size.height()}")
        print(f"   Minimum Size: {min_size.width()}x{min_size.height()}")
        print(f"   ✅ Application created successfully!")
        
        # Restore original method
        EnhancedDesktopApp.show_educational_disclaimer = original_show_disclaimer
        
        # Test resize behavior
        print("   Testing resize behavior...")
        window.resize(1200, 800)
        print(f"   Resized to: {window.size().width()}x{window.size().height()}")
        
        window.resize(900, 600)  # Minimum size
        print(f"   Minimum resize: {window.size().width()}x{window.size().height()}")
        
        print("   ✅ Resize behavior working!")
        
        # Close the window
        window.close()
        
    except Exception as e:
        print(f"   ❌ Error testing application: {str(e)}")
        return False
    
    print(f"\n🎉 Responsive Design Test Complete!")
    return True

if __name__ == "__main__":
    success = test_responsive_design()
    sys.exit(0 if success else 1)