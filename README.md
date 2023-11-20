# GHAS Scan

This is a Python script that interacts with the GitHub API to fetch repository details and code scanning analysis information.
Make sure the repository exists and your GitHub token has the necessary permissions to access it.
## Prerequisites

- Python 3.6 or higher
- `requests` library

## Installation

1. Clone this repository:
    ```bash
    git clone git@github.com:austimkelly/ghas-utils.git
    ```
2. Navigate to the cloned repository:
    ```bash
    cd ghas-utils
    ```
3. Install the required Python libraries:
    ```bash
    pip3 install requests
    ```
    or

     ```bash
    pip3 install -r requests.txt
    ```   

## Usage

1. Open `ghas-scan.py` in your favorite text editor.
2. Replace `access_token` variable value with your GitHub personal access token.
3. Replace `owner_type` variabe value with `user` or `org`. 
4. Replace `owner_name` variable value with the corresponding user or org name.
5. Run the script:
    ```bash
    python3 ghas-scan.py
    ```

Output is written to `github_data.json` at the repository root.
