# GHAS Secret Alerts

This script fetches repositories from a give user or set of org names and then pulls all the secret alerts for each repository. The script will then output the results to a CSV file.

## Installation

1. Ensure you have Python installed on your machine. You can download Python [here](https://www.python.org/downloads/).

2. Install the `requests` library using pip:

```bash
pip install requests
```

## Configuration

1. Set the `GITHUB_ACCESS_TOKEN` environment variable to your GitHub personal access token. You can create a personal access token by following the instructions [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

`export GITHUB_ACCESS_TOKEN=your_token_here`

2. Modify the `account_type` variable in the script to be either 'users' or 'orgs' depending on whether you're fetching repositories from user accounts or organizations.

3. Modify the `owners` variable in the script to be a list of the GitHub accounts you want to fetch repositories from.

# Running the script

`python get-ghas-secret-alerts.py`
