<div align="center">🔥 BruteForge Pro</div>
<div align="center"> <img src="https://raw.githubusercontent.com/DonatelloXP/BruteForge-Pro/main/docs/banner.png" width="90%"> </div> <br> <p align="center"> <img src="https://img.shields.io/badge/BruteForge-Pro-red?style=for-the-badge"> <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge"> <img src="https://img.shields.io/badge/Platforms-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge"> <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"> </p> <p align="center"> <b>Multi-Protocol Brute Force & NTLM Attack Framework for Professional Red Teams.</b><br> Designed for real-world authentication testing, NTLM exploitation, credential discovery, and advanced Windows network enumeration. </p>
📖 Table of Contents

Overview

Key Features

Framework Architecture

Installation

Quick Start

Usage Scenarios

Supported Attacks

Protocol Matrix

Configuration

Output & Logging

Advanced Workflow

Troubleshooting

Ethical & Legal Notice

Contributing

License

🎯 Overview

BruteForge Pro is a modern, modular, offensive-security framework used by Red Teams to audit authentication systems, discover weak credentials, analyze NTLM authentication flows, and perform realistic brute force & credential-based attacks across multiple network services.

It is not مجرد أداة Brute Force —
بالعكس، هي Framework كاملة تحتوى على:

✔ Protocol Engines
✔ Attack Modules
✔ NTLM Engine
✔ Session Hijacking Detection
✔ Wordlist Intelligence
✔ Workflow Automation

✨ Key Features
🚀 Core Engines

Multi-Protocol Attack Engine

SSH, RDP, SMB, WinRM, HTTP/WebDAV, FTP, MySQL, MSSQL

Real Protocol Handshakes

Multi-Thread Distributed Brute Force

Smart Throttling (Delay/Jitter)

Full Logging System (JSON, CSV, TXT)

🔥 NTLM Capabilities

Pass-the-Hash (LM:NT)

NTLMv1 / NTLMv2 Auth

SMB Signing Detection

WebDAV NTLM Forced Authentication

Session Enumeration & Relay-Check

⚙️ Operational Capabilities

Protocol Auto-Detection

Service Probe / Banner Grabbing

Adaptive Timeout Engine

Wordlist Optimizer

Modular & Extensible Attack Modules

offline mode / Simulation mode

🧠 Framework Architecture
BruteForge-Pro/
├── /core
│   ├── protocol_detector.py
│   ├── auth_handlers.py
│   ├── ntlm_engine.py
│   └── session_hijacker.py
├── /modules
│   ├── smb.py
│   ├── ssh.py
│   ├── rdp.py
│   └── webdav.py
├── /tools
│   ├── wordlist_generator.py
│   ├── hash_calculator.py
│   └── results_analyzer.py
└── bruteforge.py

🛠️ Installation
Clone
git clone https://github.com/DonatelloXP/BruteForge-Pro
cd BruteForge-Pro

Install Dependencies
pip install -r requirements.txt

Recommended (Linux)
sudo apt install freerdp2-x11 rdesktop nmap

🚀 Quick Start
Interactive Mode
python bruteforge.py

One-Line Attack Example
python bruteforge.py --target 192.168.1.10 --protocol smb \
  --username Administrator --wordlist wordlists/top_100.txt

Pass-the-Hash
python bruteforge.py --target 192.168.1.10 \
  --username admin \
  --hash LM:NT

🎮 Usage Scenarios
🧱 Windows Domain Weak Password Discovery

Test weak AD passwords before attackers exploit them.

🕵️ Red Team Credential Access

NTLM forced authentication, session enumeration, relay-checking.

🔐 SecOps Hardening

Validate password policies, auditing misconfigurations.

🔥 Supported Attacks
Attack Type	Description
Brute Force	Multi-thread high-speed guessing
Pass-the-Hash	LM/NT authentication
WebDAV Forced Auth	Trigger NTLM hashes
SMB Session Hijacking Analysis	Check relay/signed sessions
SSH/RDP Hardening Tests	Validate login security
🌐 Protocol Matrix
Protocol	Port	Auth	Status
SMB	445	NTLMv1/v2	Full
RDP	3389	NLA/SSL	Full
SSH	22	Password/Key	Full
WinRM	5985/5986	Token/Basic	Full
HTTP	80/443	Basic/Digest	Full
WebDAV	80/443	NTLM	Full
FTP	21	Plain	Limited
MySQL	3306	DB Auth	Experimental
MSSQL	1433	Windows Auth	Experimental
⚙️ Configuration
CLI Arguments
--target 192.168.1.10
--protocol smb
--username admin
--wordlist passwords.txt
--threads 20
--delay 0.2
--jitter 0.1
--hash LM:NT
--auto-detect
--check-sessions

config.json Template
{
  "defaults": {
    "threads": 20,
    "timeout": 15,
    "delay": 0.4
  }
}

📊 Output & Logging
JSON Example
{
  "target": "192.168.1.10",
  "protocol": "smb",
  "success": [
     {"username": "Administrator", "password": "P@ssw0rd!"}
  ]
}

Console Summary
[✓] SUCCESS admin:Winter2024
Attempts: 420
Speed: 21.8/sec

🔧 Advanced Workflow
⚡ Throttling Bypass
python bruteforge.py --delay 1.2 --jitter 0.5

🏢 Domain Authentication
python bruteforge.py --domain CORP --protocol smb

🧬 Intelligent Wordlist
python tools/wordlist_generator.py --target 192.168.1.10

🐛 Troubleshooting
Issue	Cause	Fix
Attempts = 0	Missing dependencies	pip install impacket
RDP fails	NLA enabled	Use --no-nla
SMB timeout	Firewall	--timeout 30

Debug:

python bruteforge.py --debug

⚖️ Ethical & Legal Notice

BruteForge Pro is for authorized testing ONLY.
Using it without explicit permission is illegal.

Allowed Use Cases:
✔ Pentest with written authorization
✔ Red Team engagements
✔ Internal security audits
✔ Educational & research labs

🤝 Contributing
Development Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Pull requests are welcome.

📄 License

MIT License — See LICENSE.

<div align="center">
⭐ If BruteForge Pro helps you, leave a star on GitHub!

Because Authentication CAN Be Forged.

</div>
