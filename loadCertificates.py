# fetches certificates for analyzing

import ssl
import socket

def get_tls_certificate(domain):
    """Extract organization name from the TLS certificate."""
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.connect((domain, 443))
            cert = s.getpeercert()
            for field in cert.get("subject", []):
                for name, value in field:
                    if name == "organizationName":
                        return value
        return "TLS Certificate: No organization found"
    except:
        return "TLS Certificate: Unavailable"
