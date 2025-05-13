# WhoseDomain - 2025

# It also fetches the TLS certificate for the domain and extracts detailed information from it.

import ssl
import socket
from OpenSSL import crypto

def get_tls_certificate(domain, port=443):
    """Fetch the TLS certificate of a domain."""
    try:
        # Establish a connection to the server
        context = ssl.create_default_context()
        with socket.create_connection((domain, port)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert(binary_form=True)
                x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)
                return x509
    except Exception as e:
        print(f"Error fetching certificate for {domain}: {e}")
        return None

def extract_certificate_details(cert):
    """Extract detailed information from the certificate."""
    try:
        subject = cert.get_subject()
        details = {
            "Common Name (CN)": getattr(subject, 'CN', None),
            "Organization (O)": getattr(subject, 'O', None),
            "Organizational Unit (OU)": getattr(subject, 'OU', None),
            "Country (C)": getattr(subject, 'C', None),
            "State (ST)": getattr(subject, 'ST', None),
            "Locality (L)": getattr(subject, 'L', None),
        }
        return details
    except Exception as e:
        print(f"Error extracting certificate details: {e}")
        return {}

if __name__ == "__main__":
    domain = input("Enter the domain: ").strip()
    cert = get_tls_certificate(domain)
    if cert:
        details = extract_certificate_details(cert)
        print("\nCertificate Details:")
        for field, value in details.items():
            print(f"{field}: {value}")
    else:
        print("Failed to fetch the certificate.")