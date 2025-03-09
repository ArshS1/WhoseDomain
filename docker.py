import subprocess

def pull_docker_image(image_name):
    try:
        result = subprocess.run(["docker", "pull", image_name], check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error pulling Docker image: {e.stderr}")

if __name__ == "__main__":
    pull_docker_image("dianecode/whosedomain")
