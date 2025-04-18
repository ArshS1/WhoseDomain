# WhoseDomain - 2025

import shodan
from domaintools import API as DomainToolsAPI
from virustotal_python import Virustotal
import json

SHODAN_API_KEY = 'y3O9GyWQEs1GB0HoETMGlAQruiQ6hUSK'
DOMAINTOOLS_USER_ID = 'YOUR_DOMAINS_USER_ID'
DOMAINTOOLS_API_KEY = 'YOUR_DOMAINS_API_KEY'
VIRUSTOTAL_API_KEY = '7beb1f8d0ede6db89485bee41b2789ce2e1c82eabad82bace7d6f863428fc4c4'

def query_shodan(domain_or_ip):
    print("\n[+] Shodan Info")
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        result = api.host(domain_or_ip) if domain_or_ip.replace('.', '').isdigit() else api.dns.resolve(domain_or_ip)['addresses'][0]
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"[-] Shodan Error: {e}")

def query_domaintools(domain):
    print("\n[+] DomainTools WHOIS Info")
    try:
        api = DomainToolsAPI(DOMAINTOOLS_USER_ID, DOMAINTOOLS_API_KEY)
        whois = api.whois(domain)
        parsed = whois.data.get('response', {})
        print(json.dumps(parsed, indent=2))
    except Exception as e:
        print(f"[-] DomainTools Error: {e}")

def query_virustotal(domain_or_ip):
    print("\n[+] VirusTotal Info")
    try:
        vtotal = Virustotal(API_KEY=VIRUSTOTAL_API_KEY)
        if domain_or_ip.replace('.', '').isdigit():
            res = vtotal.ip_address_report(domain_or_ip)
        else:
            res = vtotal.domain_report(domain_or_ip)
        print(json.dumps(res.data, indent=2))
    except Exception as e:
        print(f"[-] VirusTotal Error: {e}")

if __name__ == "__main__":
    target = input("Enter domain or IP: ").strip()
    
    if not target.replace('.', '').isdigit():
        try:
            import socket
            ip = socket.gethostbyname(target)
        except socket.gaierror:
            ip = None
            print("[-] Couldn't resolve domain to IP.")
    else:
        ip = target

    query_shodan(ip if ip else target)
    query_domaintools(target)
    query_virustotal(target)
