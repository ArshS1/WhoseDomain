# checks whats already in WHOIS database

import whois

def get_whois_info(domain):
    """Fetch WHOIS data for the domain."""
    try:
        w = whois.whois(domain)
        return w.name or w.org or "WHOIS Data: Redacted"
    except:
        return "WHOIS Data: Unavailable"
