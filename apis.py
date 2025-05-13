# WhoseDomain - 2025

# This is a script that queries Shodan and VirusTotal for information about a given domain or IP address.
import shodan
from virustotal_python import Virustotal
import json

SHODAN_API_KEY = 'y3O9GyWQEs1GB0HoETMGlAQruiQ6hUSK'
VIRUSTOTAL_API_KEY = '7beb1f8d0ede6db89485bee41b2789ce2e1c82eabad82bace7d6f863428fc4c4'

def query_shodan(domain_or_ip):
    print("\n[+] Shodan Info")
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        result = api.host(domain_or_ip) if domain_or_ip.replace('.', '').isdigit() else api.dns.resolve(domain_or_ip)['addresses'][0]
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"[-] Shodan Error: {e}")

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
    query_virustotal(target)
