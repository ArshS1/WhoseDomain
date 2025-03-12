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

    # Get user input
    domain_or_url = input("Enter a domain or URL to analyze: ").strip()
    iterations = input("Enter max iterations (default 50): ").strip() or "50"

    print(f"Running WhoseDomain for {domain_or_url}...")

    # Run WhoseDomain
    run_whosedomain(domain_or_url, iterations)
