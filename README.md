🔥 BruteForge Pro

Advanced Multi-Protocol Brute Force & NTLM Attack Suite








BruteForge Pro is a professional penetration-testing toolkit built for real-world brute force automation, NTLM attacks, and authentication exploitation.

📌 Overview

BruteForge Pro is a modern, modular, high-performance attack framework designed for Red Teams and security researchers.
It supports multi-protocol brute force, NTLM pass-the-hash, WebDAV forced authentication, RDP/SSH attacks, and SMB session analysis — all with real protocol handshakes and proper authentication flows.

Built for speed.
Built for stealth.
Built for professionals.

✨ Features
🚀 Core Features

Multi-protocol brute force (SSH, SMB, RDP, WinRM, HTTP, WebDAV)

Multi-threaded attack engine

Smart throttling (delay + jitter)

Service & protocol auto-detection

Interactive mode + CLI mode

JSON / CSV / text log output

Clean modular architecture

🛡️ Advanced Capabilities

Full NTLMv1/v2 authentication support

Pass-the-Hash attacks

SMB session enumeration

WebDAV NTLM forced authentication

Real-time progress bar

Wordlist auto-optimization

Attack simulation & dry-run mode

⚙️ Installation
Requirements

Python 3.8+

pip

On Linux (recommended):

sudo apt install freerdp2-x11 rdesktop nmap

Install
git clone https://github.com/yourusername/bruteforge-pro
cd bruteforge-pro
pip install -r requirements.txt

🚀 Quick Start
🧭 Interactive Mode
python bruteforge.py

📌 Command-Line Example
python bruteforge.py --target 192.168.1.10 \
    --protocol smb \
    --username Administrator \
    --wordlist wordlists/top_100.txt \
    --threads 20

🔐 Pass-the-Hash Example
python bruteforge.py --target 192.168.1.10 \
    --username admin \
    --hash aad3b435b51404eeaad3b435b51404ee:31d6cfe0...

🌐 Supported Protocols
Protocol	Port	Authentication	Status
SMB	445	NTLM/NTLMv2	✅ Full
RDP	3389	NLA/SSL	✅ Full
WinRM	5985/5986	HTTP/S	✅ Full
SSH	22	Password / Key	✅ Full
HTTP	80/443	Basic/Digest	✅ Full
WebDAV	80/443	NTLM Forced Auth	✅ Full
FTP	21	Password	⚠️ Limited
MySQL	3306	Native Auth	⚙️ Experimental
MSSQL	1433	Windows Auth	⚙️ Experimental
🛠️ Configuration (config.json)
{
    "defaults": {
        "threads": 15,
        "timeout": 12,
        "delay": 0.3,
        "jitter": 0.1,
        "output_format": "json"
    },
    "wordlists": {
        "default": "wordlists/common_passwords.txt",
        "windows": "wordlists/windows_passwords.txt",
        "top": "wordlists/top_100.txt"
    }
}

📊 Output Examples
JSON Result
{
  "target": "192.168.1.100",
  "protocol": "smb",
  "successful": [
    {
      "username": "Administrator",
      "password": "P@ssw0rd123",
      "timestamp": "2025-01-15T14:30:22"
    }
  ]
}

Console Summary
[✓] SUCCESS — Administrator:P@ssw0rd123  
SMB login successful — Shares: 3  
Attempts: 1000  
Speed: 22.1 attempts/sec  

🐛 Troubleshooting
Problem	Reason	Fix
Attempts = 0	Missing protocol backend	Install impacket, paramiko, etc
RDP fails	NLA required	Use --no-nla
Timeouts	Slow target	Increase: --timeout 30
SMB errors	Port blocked	Check port 445

Debug Mode:

python bruteforge.py --debug --verbose

⚖️ Legal Disclaimer

BruteForge Pro is intended ONLY for:

✔ Authorized penetration testing

✔ Red Team operations

✔ Research & education

✔ Security auditing

🚨 Never attack a system without explicit permission.
Misuse may result in criminal prosecution.

🤝 Contributing
git clone https://github.com/yourusername/bruteforge-pro
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt


Pull requests and contributions are welcome.

📄 License

This project is licensed under the MIT License.
See the LICENSE file for details.

<div align="center">
⭐ BruteForge Pro
Because authentication can be forged.

If you like this project — Star ⭐ the repo!

</div>
