# Responsive UI Guide 📱

## 🎯 **Optimized for Your 1366x768 Screen**

The Bug Bounty Hunter Pro interface has been optimized for your laptop screen and other common resolutions.

## 📐 **Responsive Features**

### **Window Sizing**
- **Auto-calculates** window size based on your screen (80% of screen size)
- **Your screen:** 1092 x 614 pixels (perfect fit)
- **Minimum size:** 819 x 460 pixels
- **Centered positioning** automatically

### **Compact Layout (≤1366px screens)**
- **Compact header:** "BB Hunter Pro" instead of full title
- **Smaller fonts:** 8-9px for better fit
- **Tabbed wordlists:** Main/Advanced tabs instead of long list
- **Grid scan options:** 2-column layout for checkboxes
- **Scrollable left panel:** 250-280px width
- **Smaller buttons:** 18px height instead of 24px

### **Full Layout (>1366px screens)**
- **Full header:** "Bug Bounty Hunter Pro"
- **Larger fonts:** 10-11px for readability
- **List wordlists:** All wordlists in single column
- **Vertical scan options:** Single column checkboxes
- **Wider left panel:** 280-320px width
- **Standard buttons:** 24px height

## 🎨 **Visual Improvements**

### **Spacing & Sizing**
- **Reduced margins** and padding for compact screens
- **Smaller input fields** (18px height vs 20px)
- **Compact buttons** with proper touch targets
- **Optimized checkbox** sizes (14px vs 16px)

### **Typography**
- **Responsive font sizes** based on screen resolution
- **Readable text** even at smaller sizes
- **Proper contrast** maintained across all sizes

### **Layout Adaptations**
- **Tabbed wordlist selectors** save vertical space
- **Grid layouts** for better space utilization
- **Scrollable panels** prevent content overflow
- **Flexible splitter** ratios (25% left, 75% right)

## 🚀 **How to Use**

### **Starting the App**
```bash
./run.sh
```

### **What You'll See**
1. **Window opens** at optimal size for your screen
2. **Compact interface** with all elements visible
3. **Scrollable left panel** if content is too tall
4. **Tabbed wordlists** in Main/Advanced sections
5. **Grid scan options** in 2 columns

### **Wordlist Management**
- **Main tab:** Directories, Subdomains
- **Advanced tab:** Parameters, Admin Panels, JWT Secrets
- **Gear icon (⚙)** to manage each wordlist type
- **Manage Wordlists** button at bottom for full manager

### **Responsive Elements**
- **Left panel:** Scrolls if content doesn't fit
- **Right panel:** Stretches with window resize
- **All text:** Sized appropriately for your screen
- **Buttons:** Touch-friendly but space-efficient

## 📱 **Screen Size Support**

### **Small Laptops (≤1366px)**
- ✅ **Your screen (1366x768)**
- ✅ **Netbooks (1024x600)**
- ✅ **Small laptops (1280x720)**

### **Standard Laptops (>1366px)**
- ✅ **Full HD (1920x1080)**
- ✅ **QHD (2560x1440)**
- ✅ **4K (3840x2160)**

## 🔧 **Customization**

### **If Text is Still Too Small**
You can adjust the system DPI scaling:
```bash
# Check current DPI
xdpyinfo | grep resolution

# Adjust if needed (example for 120 DPI)
export QT_SCALE_FACTOR=1.25
./run.sh
```

### **If Window is Too Large**
The app automatically sizes to 80% of your screen, but you can:
1. **Resize manually** by dragging window edges
2. **Use window controls** to maximize/restore
3. **Minimum size** is enforced for usability

## 🎯 **Optimizations for Your Setup**

Based on your 1366x768 screen, the app will:

1. **Use compact mode** automatically
2. **Show tabbed wordlists** to save space
3. **Use smaller fonts** (8-9px) for better fit
4. **Grid layout** for scan options (2 columns)
5. **Scrollable left panel** (250-280px wide)
6. **Compact header** with "BB Hunter Pro"

## 🐛 **Troubleshooting**

### **Text Too Small**
```bash
# Increase system font scaling
gsettings set org.gnome.desktop.interface text-scaling-factor 1.25
```

### **Window Too Large**
- **Drag edges** to resize
- **Double-click title bar** to maximize/restore
- **Use Alt+F8** to resize with keyboard

### **Elements Cut Off**
- **Scroll in left panel** if content is hidden
- **Resize window** to see more content
- **Use tabs** to access different wordlist categories

## ✨ **Pro Tips**

1. **Use tabs efficiently:** Main tab for common scans, Advanced for specialized
2. **Resize as needed:** Window remembers your preferred size
3. **Scroll left panel:** All controls are accessible via scrolling
4. **Gear icons:** Quick access to wordlist management
5. **Responsive design:** Works on any screen size automatically

---

**Your interface is now optimized for maximum usability on your 1366x768 laptop screen! 🎯**