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
5. Set `skip_forks` to `True` if you want to omit forked repos from the results.
6. Run the script:
    ```bash
    python3 ghas-scan.py
    ```

### Output and Example

Output is written to `github_data.csv` at the repository root.  It looks something like this:

```
Getting list of repositories...
Fetching repo security configs...
CSV file 'github_data.csv' written successfully.
Total repositories: 16
Total public repositories: 16
Percent of repositories that are forked: 0.0%
Percent of repositories with Codeowners: 6.25%
Percent of repositories with Secrets Scanning Enabled: 12.5%
Percent of repositories with Secrets Push Protection Enabled: 12.5%
Total number of open critical and high code scanning alerts: 0
Total number of open critical dependabot alerts: 0
Done.
```


You can see an example in [./example/example_output.csv](./example/example_output.csv). This is just a basic example to give you an idea of the scehma.

# References

* [Github REST API Documentation](https://docs.github.com/en/rest)
* [Secret Scanning API](https://docs.github.com/en/rest/secret-scanning/secret-scanning)
* [Code Scanning API](https://docs.github.com/en/rest/code-scanning/code-scanning)
* [Dependabot Alerts API](https://docs.github.com/en/rest/dependabot/alerts)