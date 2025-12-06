# 🔥 BruteForge Pro

![BruteForge Pro Banner](https://raw.githubusercontent.com/DonatelloXP/BruteForge-Pro/main/docs/banner.png)

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

**BruteForge Pro** is an advanced, multi-threaded security testing tool built for authorized penetration tests, security research, and system hardening. It implements proper protocol handshakes and supports multiple authentication flows (including NTLM/NTLMv2 and pass-the-hash) to allow realistic testing of authentication mechanisms across services such as SMB, RDP, SSH, WinRM, HTTP/WebDAV, and more.

This project is intended for use by security professionals with explicit permission to test the target systems. Do not use BruteForge Pro on systems you do not own or do not have authorization to test.

## ✨ Features

### ✅ Core Features
- Multi-protocol support: SSH, RDP, SMB, WinRM, HTTP, WebDAV, FTP and databases (experimental).
- Multi-threading: configurable concurrency for high-performance testing.
- Throttling & jitter: avoid detection and simulate realistic traffic patterns.
- Connection state detection: pre-attack checks for reachable services.
- Comprehensive logging: JSON, CSV, and plain-text outputs.
- Interactive and command-line modes.

### ✅ Advanced Capabilities
- NTLM authentication and support for LM/NT hash formats.
- Pass-the-hash attacks (when applicable and authorized).
- WebDAV NTLM forced-auth techniques.
- SMB session analysis (signing, active sessions, potential relay issues).
- Protocol auto-detection and modular architecture for extensions.
- Custom wordlist formats and generators.

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip
- Recommended system packages for RDP/SMB functionality (platform-dependent)

### Clone the repository
```bash
git clone https://github.com/DonatelloXP/BruteForge-Pro.git
cd BruteForge-Pro
```

### Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows (PowerShell)
```

### Install Python dependencies
```bash
pip install -r requirements.txt
```

### Platform-specific system dependencies (examples)

Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y freerdp2-x11 rdesktop nmap
```

macOS (Homebrew)
```bash
brew install freerdp
```

Windows
- Install Python and pip.
- Optional: Install FreeRDP builds or RDP client for RDP integration if required.

Note: Some features depend on external tools (FreeRDP, rdesktop) and Python modules (impacket, pywinrm). See `requirements.txt` and system package managers for details.

## 🎮 Quick Start

Interactive mode (recommended)
```bash
python bruteforge.py
```

Quick test mode
```bash
python bruteforge.py --quick
```

Command-line example
```bash
python bruteforge.py --target 192.168.1.100 --username admin --protocol smb
```

## 📊 Usage Examples

Example 1: Basic SMB brute force
```bash
python bruteforge.py --target 192.168.1.100 --username Administrator \
  --protocol smb --wordlist wordlists/passwords.txt --threads 20
```

Example 2: RDP attack with delay and jitter
```bash
python bruteforge.py --target 192.168.1.100 --username admin \
  --protocol rdp --delay 0.5 --jitter 0.2 --timeout 15
```

Example 3: Pass-the-Hash (LM:NT format)
```bash
python bruteforge.py --target 192.168.1.100 --username Administrator \
  --hash aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
```

Example 4: WebDAV NTLM forced-auth
```bash
python bruteforge.py --target 192.168.1.100 --protocol webdav --port 80
```

Example 5: Auto-detect protocol and run
```bash
python bruteforge.py --target 192.168.1.100 --username admin --auto-detect
```

## 🛠️ Attack Types

1. Standard Brute Force
   - Password guessing against supported protocols with configurable wordlists, delays, and patterns.

2. NTLM Hash Attacks
   - Pass-the-hash testing using LM/NT hashes where applicable and authorized.

3. WebDAV NTLM Forced Auth
   - Techniques to trigger NTLM authentication flows for testing.

4. SMB Session Analysis
   - Check SMB signing requirements, enumerate sessions, and identify relay-related issues.

5. Protocol-Specific Techniques
   - SSH key-based attempts, RDP NLA checks, WinRM command execution (authorized only).

## 🌐 Protocol Support

| Protocol | Port(s)       | Methods / Notes                 | Status        |
|---------:|---------------:|----------------------------------|---------------|
| SMB      | 445            | NTLM / NTLMv2, session analysis  | ✅ Supported  |
| RDP      | 3389           | NLA / SSL                        | ✅ Supported  |
| WinRM    | 5985 / 5986    | HTTP / HTTPS                     | ✅ Supported  |
| SSH      | 22             | Password / Key                   | ✅ Supported  |
| HTTP     | 80 / 443       | Basic / Digest / NTLM (WebDAV)   | ✅ Supported  |
| WebDAV   | 80 / 443       | NTLM forced auth                 | ✅ Supported  |
| FTP      | 21             | Plaintext auth                   | ⚠️ Limited   |
| MySQL    | 3306           | Native auth                      | ⚙️ Experimental |
| MSSQL    | 1433           | Windows auth                     | ⚙️ Experimental |

## ⚙️ Configuration

Command-Line Arguments (shortened)
```
Required:
  --target TARGET       Target IP address or hostname
  --username USERNAME   Username for authentication

Optional:
  --protocol {ssh,rdp,smb,winrm,http,webdav,ftp,mysql,mssql}
  --port PORT
  --wordlist FILE
  --threads N
  --timeout SECONDS
  --delay SECONDS
  --jitter SECONDS
  --hash LM:NT
  --domain DOMAIN
  --output FILE
  --quick
  --auto-detect
  --verbose
  --debug
```

Configuration file (optional) — config.json
```json
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
```

## 📊 Output & Logging

Results are saved in JSON, CSV, and plain-text formats. Example JSON (summary):
```json
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
```

Console logging provides a human-readable summary and progress updates. All outputs include timestamps and can be configured with `--output` and `--verbose`.

## 🔧 Advanced Techniques

Throttling bypass and adaptive delays:
```bash
python bruteforge.py --target 192.168.1.100 --delay 1.5 --jitter 0.5
python bruteforge.py --target 192.168.1.100 --adaptive-delay
```

Domain attacks (authorized testing against AD/Domain controllers):
```bash
python bruteforge.py --target dc.company.local --username jdoe \
  --domain COMPANY --protocol smb
```

Custom wordlist generation:
```bash
python tools/wordlist_gen.py --target 192.168.1.100 --output custom.txt
```

Session hijacking detection (SMB):
```bash
python bruteforge.py --target 192.168.1.100 --check-sessions
```

## 🐛 Troubleshooting

Common issues and solutions:

- Attempts show 0:
  - Ensure required protocol handlers are installed (e.g., `impacket` for SMB).
  - Check network connectivity and firewall rules.

- Connection timeouts:
  - Increase `--timeout` and add `--delay` between attempts.

- Missing dependencies:
  - `pip install -r requirements.txt`
  - For system dependencies, use your OS package manager.

- RDP authentication failures:
  - Try `--no-nla` or verify target NLA requirements.

Debug mode:
```bash
python bruteforge.py --target 192.168.1.100 --debug --verbose
```

## ⚖️ Legal Disclaimer

BruteForge Pro is intended only for:
- Authorized penetration testing
- Security research with explicit permission
- Educational purposes and system hardening

WARNING:
- Do NOT use BruteForge Pro against systems you do not own or have written permission to test.
- Illegal use is prohibited and the responsibility of the user.

Always obtain authorization and follow responsible disclosure procedures.

## 🤝 Contributing

We welcome contributions:
1. Fork the repository.
2. Create a feature branch: git checkout -b feature/AmazingFeature
3. Commit your changes: git commit -m "Add AmazingFeature"
4. Push: git push origin feature/AmazingFeature
5. Open a pull request.

Development setup:
```bash
git clone https://github.com/DonatelloXP/BruteForge-Pro.git
cd BruteForge-Pro
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest tests/
```

Please include tests for new features and follow the project's coding standards.

## 📄 License

This project is provided under the MIT License. See LICENSE for details.
