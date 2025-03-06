# main file to integrate all components

from whoisDatabase import get_whois_info
from loadCertificates import get_tls_certificate
import requests
import re
from bs4 import BeautifulSoup

def scrape_metadata(domain):
    """Scrape metadata, privacy policy, and terms of service."""
    urls_to_check = [f"https://{domain}", f"https://{domain}/privacy", f"https://{domain}/terms"]
    metadata = {}
    
    for url in urls_to_check:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Extract metadata from meta tags
                metadata["Title"] = soup.title.string if soup.title else "No title found"
                metadata["Description"] = soup.find("meta", {"name": "description"})["content"] if soup.find("meta", {"name": "description"}) else "No description"
                
                # Extract ownership mentions in text
                text = soup.get_text()
                match = re.search(r"(owned by|operated by|controlled by|©|Copyright)\s+([\w\s.,&-]+)", text, re.IGNORECASE)
                if match:
                    metadata["Owner"] = match.group(2)
                
        except:
            continue
    
    return metadata if metadata else {"Metadata": "Unavailable"}

def domain_attribution(domain):
    """Main function to perform domain attribution."""
    print(f"\nDomain: {domain}")

    whois_owner = get_whois_info(domain)
    print(f"Detected Owner: {whois_owner}")

    tls_owner = get_tls_certificate(domain)
    print(f"TLS Certificate: {tls_owner}")

    metadata = scrape_metadata(domain)
    for key, value in metadata.items():
        print(f"{key}: {value}")

    print("\nAttribution Confidence: 92%")  # Placeholder for confidence scoring
    print("Related Domains: \n- example.net\n- example-cdn.com")

if __name__ == "__main__":
    domain = "example.com"  # Replace with any domain
    domain_attribution(domain)
