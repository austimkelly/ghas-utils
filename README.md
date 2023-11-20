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

1. Create a [Github Access Token](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) and set the value in a `GITHUB_ACCESS_TOKEN` environment variable.
    * This script is tested with these permissions:
    ```
    Read access to Dependabot alerts, actions, administration, code, codespaces metadata, metadata, pull requests, secret scanning alerts, and security events
    ```
2. Open `ghas-scan.py` in your favorite text editor.
3. Replace `owner_type` variabe value with `user` or `org`. 
4. Replace `owner_name` variable value with the corresponding user or org name.
5. Run the script:
    ```bash
    python3 ghas-scan.py
    ```

### Output

Output is written to `github_data.csv` at the repository root.

# References

* [Github REST API Documentation](https://docs.github.com/en/rest)
* [Secret Scanning API](https://docs.github.com/en/rest/secret-scanning/secret-scanning)
* [Code Scanning API](https://docs.github.com/en/rest/code-scanning/code-scanning)
* [Dependabot Alerts API](https://docs.github.com/en/rest/dependabot/alerts)