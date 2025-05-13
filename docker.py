# WhoseDomain - 2025

# This script uses Docker to run the WhoseDomain tool for domain attribution. (Original Tool)

import subprocess
import os

def run_whosedomain(domain_or_url, iterations):
    # Get absolute paths
    config_path = os.path.abspath("config.ini")
    log_path = os.path.abspath("whosedomain.log")

    # Ensure log file exists
    open(log_path, "a").close()

    # Docker command
    command = [
        "docker", "run", "--rm", "--name", "whosedomain",
        "--platform", "linux/amd64",  # Override platform for compatibility
        "-v", f"{config_path}:/app/attribution-master/framework/data/config.ini",
        "-v", f"{log_path}:/app/attribution-master/framework/whosedomain.log",
        "dianecode/whosedomain:latest",
        "-c", "data/config.ini",
        "-i", domain_or_url,
        "-n", str(iterations)
    ]

    # Run the command
    subprocess.run(command, check=True)

if __name__ == "__main__":
    print("Pulling WhoseDomain Docker image...")

    # Pull latest image
    subprocess.run(["docker", "pull", "dianecode/whosedomain:latest"], check=True)

    print("Docker image pulled successfully.")

    # Open the domains file and read line by line
    domains_file_path = "./domains.txt"  # Adjust this to your file path

    with open(domains_file_path, "r") as file:
        domains = file.readlines()

    # Get user input for iterations
    iterations = input("Enter max iterations (default 50): ").strip() or "50"

    # Loop through domains and run WhoseDomain for each
    for domain_or_url in domains:
        domain_or_url = domain_or_url.strip()  # Remove any extra whitespace or newline
        if domain_or_url:  # Ensure the line is not empty
            print(f"Running WhoseDomain for {domain_or_url}...")
            run_whosedomain(domain_or_url, iterations)
