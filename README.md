# 🔥 BruteForge Pro

![BruteForge Pro Banner](https://raw.githubusercontent.com/yourusername/bruteforge-pro/main/docs/banner.png)

## 📖 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Attack Types](#attack-types)
- [Protocol Support](#protocol-support)
- [Configuration](#configuration)
- [Output & Logging](#output--logging)
- [Advanced Techniques](#advanced-techniques)
- [Troubleshooting](#troubleshooting)
- [Legal Disclaimer](#legal-disclaimer)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

**BruteForge Pro** is an advanced, multi-threaded brute force tool designed for security professionals and penetration testers. It supports multiple protocols with proper authentication flows, NTLM hash attacks, and advanced techniques like SMB session hijacking and WebDAV NTLM forced authentication.

## ✨ Features

### ✅ **Core Features**
- **Multi-Protocol Support**: SSH, RDP, SMB, WinRM, HTTP, WebDAV
- **Multi-Threading**: High-performance concurrent attacks
- **Smart Throttling Bypass**: Configurable delays and jitter
- **Connection State Detection**: Pre-attack service verification
- **Comprehensive Logging**: Detailed attack logs and results
- **Interactive & Auto Modes**: User-friendly interface

### ✅ **Advanced Capabilities**
- **NTLM Authentication**: Full LM/NT hash support
- **Pass-the-Hash Attacks**: Direct hash authentication
- **WebDAV NTLM Forced Auth**: Trigger NTLM authentication
- **SMB Session Analysis**: Check for hijacking vulnerabilities
- **Protocol Auto-Detection**: Smart service identification
- **Custom Wordlist Support**: Multiple wordlist formats

### ✅ **Technical Excellence**
- **Proper Authentication Flows**: Real protocol handshakes
- **Error Handling**: Comprehensive error detection and reporting
- **Progress Tracking**: Real-time progress visualization
- **Results Export**: JSON, CSV, and text output formats
- **Modular Architecture**: Easy to extend and customize

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- System dependencies (see below)

### Quick Install
```bash
# Clone repository
git clone https://github.com/yourusername/bruteforge-pro.git
cd bruteforge-pro

# Install requirements
pip install -r requirements.txt

# Install system dependencies (Linux)
sudo apt-get install freerdp2-x11 rdesktop
System Dependencies
Windows
powershell
# Install Python packages
pip install impacket colorama pywinrm requests

# For RDP support, install FreeRDP:
# Download from: https://github.com/FreeRDP/FreeRDP/releases
Linux (Ubuntu/Debian)
bash
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    freerdp2-x11 \
    rdesktop \
    nmap

pip3 install -r requirements.txt
macOS
bash
brew install python freerdp
pip3 install -r requirements.txt
Requirements File
txt
# requirements.txt
impacket>=0.11.0
colorama>=0.4.6
requests>=2.31.0
pywinrm>=0.4.3
requests-ntlm>=1.2.0
paramiko>=3.4.0
🎮 Quick Start
Interactive Mode (Recommended)
bash
python bruteforge.py
Follow the interactive menu to configure your attack.

Quick Test Mode
bash
python bruteforge.py --quick
Command Line Mode
bash
python bruteforge.py --target 192.168.1.100 --username admin --protocol smb
📊 Usage Examples
Example 1: Basic SMB Brute Force
bash
python bruteforge.py --target 192.168.1.100 --username Administrator \
    --protocol smb --wordlist passwords.txt --threads 20
Example 2: RDP Attack with Delay
bash
python bruteforge.py --target 192.168.1.100 --username admin \
    --protocol rdp --delay 0.5 --jitter 0.2 --timeout 15
Example 3: Pass-the-Hash Attack
bash
python bruteforge.py --target 192.168.1.100 --username Administrator \
    --hash aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
Example 4: WebDAV NTLM Forced Authentication
bash
python bruteforge.py --target 192.168.1.100 --protocol webdav --port 80
Example 5: Multi-Protocol Auto Detection
bash
python bruteforge.py --target 192.168.1.100 --username admin --auto-detect
🛠️ Attack Types
1. Standard Brute Force
Password guessing against various protocols

Configurable wordlists and patterns

Rate limiting and delay controls

2. NTLM Hash Attacks
Pass-the-Hash authentication

LM/NT hash computation and usage

Domain authentication support

3. WebDAV NTLM Forced Auth
Trigger NTLM authentication via WebDAV

Capture NTLM hashes (with proper setup)

HTTP protocol exploitation

4. SMB Session Analysis
Check SMB signing requirements

List active SMB sessions

Identify relay vulnerabilities

5. Protocol-Specific Attacks
SSH key-based authentication attempts

RDP NLA bypass techniques

WinRM PowerShell command execution

🌐 Protocol Support
Protocol	Port	Method	Status
SMB	445	NTLM/NTLMv2	✅ Fully Supported
RDP	3389	NLA/SSL	✅ Fully Supported
WinRM	5985/5986	HTTP/HTTPS	✅ Fully Supported
SSH	22	Password/Key	✅ Fully Supported
HTTP	80/443	Basic/Digest Auth	✅ Fully Supported
WebDAV	80/443	NTLM Forced Auth	✅ Fully Supported
FTP	21	Plaintext Auth	⚠️ Limited
MySQL	3306	Native Auth	⚙️ Experimental
MSSQL	1433	Windows Auth	⚙️ Experimental
⚙️ Configuration
Command Line Arguments
bash
Required:
  --target TARGET       Target IP address or hostname
  --username USERNAME   Username for authentication

Optional:
  --protocol {ssh,rdp,smb,winrm,http,webdav}
                        Protocol to attack
  --port PORT           Target port (auto-detected if not specified)
  --wordlist WORDLIST   Password wordlist file
  --threads THREADS     Number of threads (default: 10)
  --timeout TIMEOUT     Connection timeout in seconds (default: 10)
  --delay DELAY         Delay between attempts in seconds (default: 0)
  --jitter JITTER       Random jitter to add to delay (default: 0)
  --hash HASH           NTLM hash for pass-the-hash (LM:NT format)
  --domain DOMAIN       Domain for Windows authentication
  --output OUTPUT       Output file for results (default: results.json)
  --quick               Quick test mode
  --auto-detect         Auto-detect protocol and port
  --verbose             Verbose output mode
Configuration File
Create config.json:

json
{
    "defaults": {
        "threads": 15,
        "timeout": 12,
        "delay": 0.3,
        "jitter": 0.1,
        "output_format": "json"
    },
    "wordlists": {
        "default": "wordlists/common.txt",
        "windows": "wordlists/windows.txt",
        "linux": "wordlists/linux.txt"
    },
    "protocols": {
        "smb": {
            "port": 445,
            "domain": "WORKGROUP"
        },
        "rdp": {
            "port": 3389,
            "use_nla": true
        }
    }
}
📊 Output & Logging
Results Format
Results are saved in multiple formats:

JSON Output (Default)
json
{
    "attack_summary": {
        "target": "192.168.1.100",
        "protocol": "smb",
        "duration": "45.23s",
        "attempts": 1000,
        "successful": 1
    },
    "credentials_found": [
        {
            "username": "Administrator",
            "password": "P@ssw0rd123",
            "timestamp": "2024-01-15T14:30:22"
        }
    ],
    "statistics": {
        "attempts_per_second": 22.1,
        "success_rate": "0.1%"
    }
}
Text Log
text
[2024-01-15 14:30:22] START Attack on 192.168.1.100:445 (SMB)
[2024-01-15 14:30:25] TRY Administrator:password123 - FAILED
[2024-01-15 14:30:27] TRY Administrator:admin123 - FAILED
[2024-01-15 14:30:45] SUCCESS Administrator:P@ssw0rd123
[2024-01-15 14:31:07] END Attack completed in 45.23s
Console Output
text
╔══════════════════════════════════════════════════════════╗
║                    ATTACK SUMMARY                        ║
╚══════════════════════════════════════════════════════════╝

Target: 192.168.1.100:445
Protocol: SMB
Username: Administrator
Duration: 45.23 seconds
Attempts: 1000
Success Rate: 1/1000 (0.1%)
Speed: 22.1 attempts/second

[✓] CREDENTIALS FOUND:
  Administrator:P@ssw0rd123
    SMB login successful - Found 3 shares

Results saved to: results_20240115_143022.json
🔧 Advanced Techniques
Throttling Bypass
bash
# Add random delays to avoid detection
python bruteforge.py --target 192.168.1.100 --delay 1.5 --jitter 0.5

# Exponential backoff on failure
python bruteforge.py --target 192.168.1.100 --adaptive-delay
Domain Authentication
bash
# Attack domain account
python bruteforge.py --target dc.company.local --username jdoe \
    --domain COMPANY --protocol smb
Custom Wordlist Generation
bash
# Generate custom wordlist based on target
python tools/wordlist_gen.py --target 192.168.1.100 --output custom.txt
Session Hijacking Detection
bash
# Check for SMB session hijacking possibilities
python bruteforge.py --target 192.168.1.100 --check-sessions
🐛 Troubleshooting
Common Issues
Issue: "Attempts: 0" in results
Solution: Ensure proper protocol handlers are installed:

bash
# For SMB
pip install impacket

# For RDP
sudo apt-get install freerdp2-x11  # Linux
# or install FreeRDP on Windows
Issue: Connection timeouts
Solution: Adjust timeout settings:

bash
python bruteforge.py --target 192.168.1.100 --timeout 30 --delay 2
Issue: Missing dependencies
Solution: Install all requirements:

bash
pip install -r requirements.txt --upgrade
Issue: RDP authentication fails
Solution: Check NLA requirements:

bash
# Try different authentication methods
python bruteforge.py --target 192.168.1.100 --protocol rdp --no-nla
Debug Mode
bash
python bruteforge.py --target 192.168.1.100 --debug --verbose
⚖️ Legal Disclaimer
BruteForge Pro is intended for:

✅ Authorized penetration testing
✅ Security research
✅ Educational purposes
✅ System hardening
✅ Legal security assessments

WARNING:
❌ NEVER use against systems you don't own or have permission to test

❌ NEVER use for illegal activities

❌ NEVER violate laws or regulations

❌ ALWAYS obtain proper authorization

Compliance:
Complies with penetration testing standards

Supports responsible disclosure

Includes safety features to prevent abuse

🤝 Contributing
We welcome contributions! Here's how:

Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add AmazingFeature')

Push to branch (git push origin feature/AmazingFeature)

Open a Pull Request

Development Setup
bash
# Clone and setup
git clone https://github.com/yourusername/bruteforge-pro.git
cd bruteforge-pro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
