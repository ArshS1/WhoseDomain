# WhoseDomain - 2025

import sys
import subprocess
from scraper import crawl_site
from certificate import get_tls_certificate, extract_certificate_details
# from apis import some_api_function  # Extend if apis.py is implemented later

def run_scraper(domain):
    """Run the scraper for a given domain."""
    try:
        # Adjusted to unpack all 5 returned values
        people_names, _, visited_urls, internal_links, external_links = crawl_site(domain)
        
        # Print results
        print("\nPotential Owners Found:")
        for name in sorted(people_names):
            print(f"- {name}")
        
        print("\nInternal Links Found:")
        for link in sorted(internal_links):
            print(f"- {link}")
        
        print("\nExternal Links Found:")
        for link in sorted(external_links):
            print(f"- {link}")
        
        print("\nPages Visited:")
        print(f"- {len(visited_urls)} pages visited")
    
    except Exception as e:
        print(f"An error occurred while running the scraper for {domain}: {e}")
        import traceback
        traceback.print_exc()

def run_certificate_check(domain):
    print("\n--- Checking TLS Certificate ---")
    cert = get_tls_certificate(domain)
    if cert:
        details = extract_certificate_details(cert)
        for field, value in details.items():
            print(f"{field}: {value}")
    else:
        print("Failed to retrieve certificate.")

def run_api_checks(domain):
    """Run API checks for a given domain by calling apis.py."""
    print("\n--- Running API Checks ---")
    try:
        # Call apis.py and pass the domain as input
        process = subprocess.Popen(
            ["python3", "apis.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=domain)
        
        # Print the output and errors
        print(f"\n--- Output from API Checks for {domain} ---")
        print(stdout)
        if stderr:
            print(f"\n--- Error from API Checks for {domain} ---")
            print(stderr)
    except Exception as e:
        print(f"An error occurred while running API checks for {domain}: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function to run the scraper."""
    domain = input("Enter the domain: ").strip()

    run_scraper(domain)
    run_certificate_check(domain)
    run_api_checks(domain)

if __name__ == "__main__":
    main()