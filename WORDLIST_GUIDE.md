# Wordlist Management Guide 📝

## Overview

Bug Bounty Hunter Pro includes a comprehensive wordlist management system that allows you to easily add, manage, and customize wordlists for different types of security testing.

## Wordlist Categories

The application supports the following wordlist categories:

### 🗂️ **Directory/File Fuzzing**
- **Purpose:** Discover hidden directories and files
- **Default File:** `wordlists/directories.txt`
- **Examples:** admin, api, backup, config, uploads

### 🌐 **Subdomain Enumeration**
- **Purpose:** Find subdomains of target domains
- **Default File:** `wordlists/subdomains.txt`
- **Examples:** www, api, admin, test, dev, staging

### 🔍 **Parameter Discovery**
- **Purpose:** Discover hidden parameters in web applications
- **Default File:** `wordlists/parameters.txt`
- **Examples:** id, user, admin, debug, token, key

### 👑 **Admin Panel Discovery**
- **Purpose:** Find administrative interfaces
- **Default File:** `wordlists/admin_panels.txt`
- **Examples:** admin, administrator, login, dashboard, panel

### 🔑 **JWT Weak Secrets**
- **Purpose:** Test JWT tokens for weak signing secrets
- **Default File:** `wordlists/jwt_secrets.txt`
- **Examples:** secret, key, password, admin, test

### 👤 **Usernames**
- **Purpose:** Common usernames for credential testing
- **Default File:** `wordlists/usernames.txt`
- **Examples:** admin, root, user, test, guest

### 🔐 **Passwords**
- **Purpose:** Common passwords for credential testing
- **Default File:** `wordlists/passwords.txt`
- **Examples:** password, 123456, admin, letmein

### 📄 **File Extensions**
- **Purpose:** File extension fuzzing
- **Default File:** `wordlists/extensions.txt`
- **Examples:** php, asp, jsp, html, js, css

## Using the Wordlist Manager

### Accessing the Wordlist Manager

1. **From Main Dashboard:**
   - Click on the "Wordlists" tab in the main interface
   - Or click "Manage All Wordlists" in the Target Configuration section

2. **From Individual Selectors:**
   - Click the "Manage" button next to any wordlist selector

### Managing Wordlists

#### **Adding New Wordlists**

1. **Import from File:**
   ```
   1. Select a category from the left panel
   2. Click "Add Wordlist"
   3. Choose "Import from File"
   4. Select your .txt file
   5. Enter a custom name
   6. Click OK
   ```

2. **Create New Wordlist:**
   ```
   1. Select a category
   2. Click "Add Wordlist"
   3. Choose "Create New"
   4. Enter a name
   5. Edit in the "Edit" tab
   6. Click "Save Changes"
   ```

#### **Editing Wordlists**

1. **Select a wordlist** from the right panel
2. **Switch to "Edit" tab**
3. **Make your changes** in the text editor
4. **Use editing tools:**
   - **Add Line:** Add individual entries
   - **Remove Duplicates:** Clean up duplicate entries
   - **Sort:** Alphabetically sort entries
   - **Clean:** Remove empty lines and trim whitespace
5. **Click "Save Changes"**

#### **Wordlist Statistics**

The "Statistics" tab shows:
- Total lines
- Valid entries
- Empty lines
- Comment lines
- Unique entries
- Duplicates
- Average/Min/Max length

### Advanced Features

#### **Merging Wordlists**

Combine multiple wordlists into one:

1. Click "Merge Wordlists"
2. Select 2 or more wordlist files
3. Enter a name for the merged wordlist
4. The tool will automatically remove duplicates and sort entries

#### **Downloading Popular Wordlists**

Access curated wordlists from the security community:

1. Click "Download Popular"
2. Select wordlists from categories:
   - **SecLists** - Industry standard wordlists
   - **Assetnote** - High-quality DNS and parameter lists
   - **DirBuster** - Classic directory lists
3. Check desired wordlists
4. Click "Download Selected"

Popular wordlists include:
- **SecLists Common** - General purpose directory list
- **SecLists Directory List 2.3 Medium** - Comprehensive directory list
- **Assetnote Best DNS** - High-quality subdomain list
- **Burp Parameter Names** - Common parameter names

#### **Exporting Wordlists**

Save wordlists for use in other tools:

1. Select a wordlist
2. Click "Export"
3. Choose destination and filename
4. The wordlist will be saved as a .txt file

## File Structure

```
wordlists/
├── directories.txt          # Default directory wordlist
├── subdomains.txt          # Default subdomain wordlist
├── parameters.txt          # Default parameter wordlist
├── admin_panels.txt        # Default admin panel wordlist
├── jwt_secrets.txt         # Default JWT secrets wordlist
├── usernames.txt           # Default username wordlist
├── passwords.txt           # Default password wordlist
├── extensions.txt          # Default file extensions
└── custom/                 # Custom wordlists directory
    ├── directories_custom1.txt
    ├── subdomains_special.txt
    └── parameters_api.txt
```

## Best Practices

### **Wordlist Selection**

1. **Start Small:** Use smaller wordlists for initial reconnaissance
2. **Scale Up:** Use comprehensive wordlists for thorough testing
3. **Target-Specific:** Create custom wordlists based on target technology
4. **Combine Sources:** Merge wordlists from different sources

### **Custom Wordlist Creation**

1. **Research Target:** Understand the target's technology stack
2. **Industry-Specific:** Include industry-specific terms
3. **Technology-Specific:** Add framework/CMS specific paths
4. **Historical Data:** Include paths from previous assessments

### **Performance Considerations**

1. **Size vs Speed:** Larger wordlists = longer scan times
2. **Threading:** Adjust thread count based on wordlist size
3. **Timeouts:** Set appropriate timeouts for large wordlists
4. **Rate Limiting:** Be respectful to target servers

## Example Workflows

### **Basic Directory Fuzzing**

1. Select "Directory/File Fuzzing" category
2. Choose "Default" wordlist for quick scan
3. Or select "Custom: Comprehensive" for thorough testing
4. Configure threads (10-20 for most targets)
5. Start scan

### **Subdomain Enumeration**

1. Select "Subdomain Enumeration" category
2. Use "Default" for basic enumeration
3. Download "SecLists Subdomains Top 1M" for comprehensive testing
4. Merge multiple subdomain wordlists for maximum coverage

### **API Testing**

1. Create custom parameter wordlist with API-specific terms:
   ```
   api_key
   access_token
   client_id
   client_secret
   refresh_token
   scope
   grant_type
   ```
2. Use for parameter discovery on API endpoints

### **CMS-Specific Testing**

For WordPress targets:
1. Create custom directory wordlist:
   ```
   wp-admin
   wp-content
   wp-includes
   wp-config.php
   xmlrpc.php
   wp-login.php
   ```

For Drupal targets:
1. Create custom wordlist:
   ```
   admin
   user
   node
   sites/default/files
   modules
   themes
   ```

## Integration with Scanning

### **Automatic Selection**

The scanner automatically uses selected wordlists:

1. **Directory Fuzzing:** Uses selected directory wordlist
2. **Subdomain Enumeration:** Uses selected subdomain wordlist
3. **Parameter Discovery:** Uses selected parameter wordlist
4. **Admin Panel Discovery:** Uses selected admin panel wordlist
5. **JWT Analysis:** Uses selected JWT secrets wordlist

### **Real-time Updates**

- Wordlist changes are immediately available to the scanner
- No need to restart the application
- Changes are logged in the main interface

## Troubleshooting

### **Common Issues**

1. **Wordlist Not Loading:**
   - Check file permissions
   - Ensure file is in UTF-8 encoding
   - Verify file path is correct

2. **Performance Issues:**
   - Reduce wordlist size
   - Lower thread count
   - Increase timeout values

3. **Memory Usage:**
   - Large wordlists consume more memory
   - Consider splitting large wordlists
   - Monitor system resources

### **File Format Requirements**

- **Encoding:** UTF-8
- **Line Endings:** Unix (LF) or Windows (CRLF)
- **Comments:** Lines starting with # are ignored
- **Empty Lines:** Ignored during processing

## Security Considerations

### **Responsible Usage**

1. **Authorization:** Only test systems you own or have permission to test
2. **Rate Limiting:** Don't overwhelm target servers
3. **Scope:** Stay within defined testing scope
4. **Documentation:** Keep records of testing activities

### **Wordlist Sources**

1. **Trusted Sources:** Use reputable wordlist sources
2. **Validation:** Review wordlists before use
3. **Updates:** Keep wordlists updated
4. **Backup:** Maintain backups of custom wordlists

---

**Happy Hunting! 🎯**

*Remember: The quality of your wordlists directly impacts the effectiveness of your bug bounty hunting.*