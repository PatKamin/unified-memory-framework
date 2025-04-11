import argparse
import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_registration_token(owner, repo, token):
    logging.info(f"Requesting registration token for repository {owner}/{repo}.")
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runners/registration-token"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    logging.info("Successfully retrieved registration token.")
    return response.json()["token"]

def download_runner(os_type, architecture, download_url, destination):
    logging.info(f"Downloading runner binary for {os_type} {architecture} to {destination}.")
    response = requests.get(download_url, stream=True)
    response.raise_for_status()
    with open(destination, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    logging.info("Runner binary downloaded successfully.")

def configure_runner(destination, token):
    logging.info(f"Configuring runner in {destination}.")
    os.chdir(destination)
    os.system(f"./config.sh --url https://github.com/{owner}/{repo} --token {token}")
    logging.info("Runner configured successfully.")

def create_runners(owner, repo, token, runner_count, runner_name):
    logging.info(f"Starting creation of {runner_count} runners for repository {owner}/{repo}.")
    registration_token = get_registration_token(owner, repo, token)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    for i in range(runner_count):
        runner_dir = os.path.join(base_dir, f"{runner_name}_{i}")
        os.makedirs(runner_dir, exist_ok=True)

        # Download runner binary
        download_url = "https://github.com/actions/runner/releases/download/v2.323.0/actions-runner-linux-x64-2.323.0.tar.gz"
        tar_path = os.path.join(runner_dir, "actions-runner.tar.gz")
        download_runner("linux", "x64", download_url, tar_path)

        # Extract runner binary
        os.system(f"tar -xzf {tar_path} -C {runner_dir}")

        # Configure runner
        configure_runner(runner_dir, registration_token)
        logging.info(f"Runner {runner_name}_{i} created successfully in {runner_dir}.")
    logging.info("All runners created successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create multiple GitHub Actions runners.")
    parser.add_argument("--owner", required=True, help="The GitHub owner (user or organization).")
    parser.add_argument("--repo", required=True, help="The GitHub repository name.")
    parser.add_argument("--token", required=True, help="The GitHub personal access token.")
    parser.add_argument("--runner_count", type=int, required=True, help="The number of runners to create.")
    parser.add_argument("--runner_name", required=True, help="The base name for the runners. A number will be appended to this name.")

    args = parser.parse_args()
    create_runners(args.owner, args.repo, args.token, args.runner_count, args.runner_name)
