# 🔥 BruteForge Pro

![BruteForge Pro Banner](https://raw.githubusercontent.com/mamdouh911/bruteforge-pro/main/docs/banner.png)

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
git clone https://github.com/mamdouh911/bruteforge-pro.git
cd bruteforge-pro

# Install requirements
pip install -r requirements.txt

# Install system dependencies (Linux)
sudo apt-get install freerdp2-x11 rdesktop
