@echo off
REM Bug Bounty Hunter Pro - Installation Script for Windows
REM This script installs all dependencies and sets up the application

echo 🚀 Bug Bounty Hunter Pro - Installation Script
echo ================================================

REM Colors (Windows CMD doesn't support ANSI colors easily, so using plain text)

echo [INFO] Starting Bug Bounty Hunter Pro installation...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.11+ from https://python.org
    echo [ERROR] Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [SUCCESS] Python is installed

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Python version: %PYTHON_VERSION%

REM Create virtual environment
echo [INFO] Creating virtual environment...
python -m venv bug_bounty_env
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment created

REM Activate virtual environment and install dependencies
echo [INFO] Installing Python dependencies...
call bug_bounty_env\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install ^
    PyQt6 ^
    requests ^
    python-owasp-zap-v2.4 ^
    websockets ^
    bcrypt ^
    pyjwt ^
    cryptography ^
    pyinstaller ^
    beautifulsoup4 ^
    lxml ^
    dnspython ^
    python-nmap ^
    scapy ^
    colorlog ^
    jsonschema ^
    flask ^
    uro ^
    pytest ^
    pytest-cov ^
    black ^
    flake8 ^
    isort ^
    mypy ^
    pylint

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo [SUCCESS] Python dependencies installed

REM Create directories
echo [INFO] Creating application directories...
if not exist data mkdir data
if not exist reports mkdir reports
if not exist screenshots mkdir screenshots
if not exist logs mkdir logs
if not exist wordlists mkdir wordlists
echo [SUCCESS] Application directories created

REM Create run script
echo [INFO] Creating run script...
(
echo @echo off
echo REM Bug Bounty Hunter Pro - Run Script
echo.
echo cd /d "%~dp0"
echo.
echo REM Activate virtual environment
echo call bug_bounty_env\Scripts\activate.bat
echo.
echo REM Run the application
echo python main.py %%*
) > run.bat
echo [SUCCESS] Run script created

REM Create desktop shortcut
echo [INFO] Creating desktop shortcut...
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

powershell -Command "
$WshShell = New-Object -comObject WScript.Shell;
$Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Bug Bounty Hunter Pro.lnk');
$Shortcut.TargetPath = '%SCRIPT_DIR%\run.bat';
$Shortcut.WorkingDirectory = '%SCRIPT_DIR%';
$Shortcut.IconLocation = '%SCRIPT_DIR%\assets\icon.ico';
$Shortcut.Description = 'Advanced Security Testing Platform';
$Shortcut.Save();
"

if %errorlevel% neq 0 (
    echo [WARNING] Failed to create desktop shortcut automatically
    echo [INFO] You can manually create a shortcut to run.bat on your desktop
) else (
    echo [SUCCESS] Desktop shortcut created
)

REM Create assets if missing
echo [INFO] Checking application assets...
if not exist assets mkdir assets

REM Create a simple icon placeholder (you can replace with actual icon)
echo [INFO] Creating icon placeholder...
echo. > assets\icon.ico

REM Set permissions (Windows doesn't need chmod)
echo [INFO] Setting file permissions...
REM No chmod needed on Windows

echo.
echo [SUCCESS] Installation completed successfully!
echo.
echo 🎉 Bug Bounty Hunter Pro is now installed!
echo.
echo To run the application:
echo   Double-click run.bat or the desktop shortcut
echo.
echo Default login credentials:
echo   Username: admin
echo   Password: BugHunter2024!
echo.
echo For bug bounty site finder:
echo   bug_bounty_env\Scripts\python.exe bug_bounty_finder.py
echo.
echo [WARNING] Remember to change the default password after first login!
echo.

pause