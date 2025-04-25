# WhoseDomain - 2025

import subprocess
import threading
import os
from queue import Queue

def process_domain(domain, output_queue):
    """Run whoseDomain.py for a single domain and capture the output."""
    try:
        result = subprocess.run(
            ["python3", "whoseDomain.py", domain],
            capture_output=True,
            text=True,
            check=True
        )
        output_queue.put((domain, result.stdout))
    except subprocess.CalledProcessError as e:
        output_queue.put((domain, f"Error: {e.stderr}"))

def main():
    # Read domains from domains.txt
    domains_file = "domains.txt"
    if not os.path.exists(domains_file):
        print(f"Error: {domains_file} not found.")
        return

    with open(domains_file, "r") as file:
        domains = [line.strip() for line in file if line.strip()]

    # Queue to store results
    output_queue = Queue()

    # Create threads for concurrent processing
    threads = []
    for domain in domains:
        thread = threading.Thread(target=process_domain, args=(domain, output_queue))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Collect and display results
    while not output_queue.empty():
        domain, output = output_queue.get()
        print(f"\n--- Output for {domain} ---")
        print(output)

if __name__ == "__main__":
    main()