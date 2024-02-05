import requests
import csv

# Configuration
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN'
REPO_OWNER = 'austimkelly'
REPO_NAME = 'swiss-cheese'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}

# This function is used to flatten a nested dictionary. 
# The arguments are a dictionary to flatten (dd), a separator for the keys (separator), and a prefix for the keys (prefix).
def flatten_dict(dd, separator='_', prefix=''):
    # The function returns a dictionary comprehension.
    # If dd is a dictionary, it will iterate over its items.
    return { 
        # For each item, it checks if a prefix exists. If it does, it concatenates the prefix, separator, and key.
        # If no prefix exists, it simply uses the key.
        f"{prefix}{separator}{k}" if prefix else k : v
        # This is the start of the dictionary comprehension. It iterates over the items in dd.
        for kk, vv in dd.items()
        # For each item, it calls flatten_dict recursively on the value and iterates over the items in the resulting dictionary.
        # It uses the key from dd as the prefix for this recursive call.
        for k, v in flatten_dict(vv, separator, kk).items()
    # If dd is not a dictionary, it simply returns a dictionary with a single item. The key is the prefix and the value is dd.
    } if isinstance(dd, dict) else { prefix : dd }


def parse_dependabot_alerts_to_csv(dependabot_alerts):
    # Define the CSV file
    csv_file = "dependabot_alerts.csv"

    # Flatten the alerts
    flattened_alerts = [flatten_dict(alert) for alert in dependabot_alerts]

    # Define the CSV headers based on the keys of all alerts
    csv_headers = set(key for alert in flattened_alerts for key in alert.keys())

    # Write the alerts to the CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        for alert in flattened_alerts:
            writer.writerow(alert)

    print(f"Dependabot alerts have been written to {csv_file}")

def parse_code_scanning_results_to_csv(code_scanning_results):
    # Define the CSV file
    csv_file = "code_scanning_results.csv"

    # Flatten the results
    flattened_results = [flatten_dict(result) for result in code_scanning_results]

    # Define the CSV headers based on the keys of all results
    csv_headers = set(key for result in flattened_results for key in result.keys())

    # Write the results to the CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        for result in flattened_results:
            writer.writerow(result)

    print(f"Code scanning results have been written to {csv_file}")

def parse_secret_scanning_results_to_csv(secret_scanning_results):
    # Define the CSV file
    csv_file = "secret_scanning_results.csv"

    # Define the CSV headers based on the keys of the first result
    csv_headers = secret_scanning_results[0].keys()

    # Write the results to the CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        for result in secret_scanning_results:
            writer.writerow(result)

    print(f"Secret scanning results have been written to {csv_file}")

# For Secrets scanning REST API, see: https://docs.github.com/en/rest/secret-scanning/secret-scanning?apiVersion=2022-11-28
# For repo-level secret scanning alerts, see: https://docs.github.com/en/rest/secret-scanning/secret-scanning?apiVersion=2022-11-28#list-secret-scanning-alerts-for-a-repository
def get_secret_scanning_alerts():
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/secret-scanning/alerts'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200 and response.text.strip():
        return response.json()
    else:
        print(f"Error in get_secret_scanning_alerts: Received status code {response.status_code} with response: {response.text}")
        return None

# For Code scanning alerts REST API, see: https://docs.github.com/en/rest/code-scanning/code-scanning?apiVersion=2022-11-28
# For Code scanning alerts for a repo, see: https://docs.github.com/en/rest/code-scanning/code-scanning?apiVersion=2022-11-28#list-code-scanning-alerts-for-a-repository
def get_code_scanning_alerts():
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/code-scanning/alerts'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200 and response.text.strip():
        return response.json()
    else:
        print(f"Error in get_code_scanning_alerts: Received status code {response.status_code} with response: {response.text}")
        return None

# For Dependabot alerts REST API, see: https://docs.github.com/en/rest/dependabot/alerts?apiVersion=2022-11-28
# For Dependabot alerts on a repo, see: https://docs.github.com/en/rest/dependabot/alerts?apiVersion=2022-11-28#list-dependabot-alerts-for-a-repository
def get_dependabot_alerts():
    # Dependabot alerts can be obtained from the repository vulnerability alerts
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dependabot/alerts'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200 and response.text.strip():
        return response.json()
    else:
        print(f"Error in get_dependabot_alerts: Received status code {response.status_code} with response: {response.text}")
        return None

def main():
    secret_alerts = get_secret_scanning_alerts()
    code_alerts = get_code_scanning_alerts()
    dependabot_alerts = get_dependabot_alerts()

    print("Secret Scanning Alerts:")
    if secret_alerts is None:
        print("No data available")
    else:
        #print(secret_alerts)
        parse_secret_scanning_results_to_csv(secret_alerts)

    print("\nCode Scanning Alerts:")
    if code_alerts is None:
        print("No data available")
    else:
        #print(code_alerts)
        parse_code_scanning_results_to_csv(code_alerts)

    print("\nDependabot Alerts:")
    if dependabot_alerts is None:
        print("No data available")
    else:
        #print(dependabot_alerts)
        parse_dependabot_alerts_to_csv(dependabot_alerts)

if __name__ == "__main__":
    main()
