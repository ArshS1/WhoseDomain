# WhoseDomain - 2025

import sys
from scraper import crawl_site
from certificate import get_tls_certificate, extract_certificate_details
# from apis import some_api_function  # Extend if apis.py is implemented later

def run_scraper(domain):
    print("\n--- Running Scraper ---")
    people_names, _, visited_urls = crawl_site(domain)
    print(f"Found {len(people_names)} unique person names:")
    for name in sorted(people_names):
        print(f"- {name}")
    print(f"Visited {len(visited_urls)} pages.")

def run_certificate_check(domain):
    print("\n--- Checking TLS Certificate ---")
    cert = get_tls_certificate(domain)
    if cert:
        details = extract_certificate_details(cert)
        for field, value in details.items():
            print(f"{field}: {value}")
    else:
        print("Failed to retrieve certificate.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 whoseDomain.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    run_scraper(domain)
    run_certificate_check(domain)
    # print("\n--- Running API Checks ---")
    # run_api_checks(domain)  # Extend this when apis.py has logic

if __name__ == "__main__":
    main()
