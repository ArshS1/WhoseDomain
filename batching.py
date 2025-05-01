# WhoseDomain - 2025

# This script is designed to batch process a list of domains, running the scraper and certificate check for each.

import subprocess
import os

def process_domain(domain):
    """Run whoseDomain.py for a single domain and provide the domain as input."""
    try:
        # Start the whoseDomain.py process
        process = subprocess.Popen(
            ["python3", "whoseDomain.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Provide the domain as input to the script
        stdout, stderr = process.communicate(input=domain)
        
        # Print the output and errors
        print(f"\n--- Output for {domain} ---")
        print(stdout)
        if stderr:
            print(f"\n--- Error for {domain} ---")
            print(stderr)
    except Exception as e:
        print(f"An error occurred while processing {domain}: {e}")

def main():
    # Read domains from domains.txt
    domains_file = "domains.txt"
    if not os.path.exists(domains_file):
        print(f"Error: {domains_file} not found.")
        return

    with open(domains_file, "r") as file:
        domains = [line.strip() for line in file if line.strip()]

    # Process each domain
    for domain in domains:
        process_domain(domain)

if __name__ == "__main__":
    main()