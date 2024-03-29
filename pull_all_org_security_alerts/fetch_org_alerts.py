import subprocess
import requests
import sys
import csv
from datetime import datetime
import os
import pandas as pd


def generate_report(org, secrets_file, dependencies_file, code_scanning_file):
   
    secrets_df = pd.read_csv(secrets_file, on_bad_lines='skip') if os.path.isfile(secrets_file) else pd.DataFrame()
    dependencies_df = pd.read_csv(dependencies_file, on_bad_lines='skip') if os.path.isfile(dependencies_file) else pd.DataFrame()
    code_scanning_df = pd.read_csv(code_scanning_file, on_bad_lines='skip') if os.path.isfile(code_scanning_file) else pd.DataFrame()
  
    # Count the number of active and open secrets
    active_open_secrets = ((secrets_df['state'] == 'open') & (secrets_df['validity'] == 'active')).sum()

    # Count the number of open critical alerts for dependencies and code scanning
    #print(dependencies_df[(dependencies_df['state'] == 'open') & (dependencies_df['security_advisory_severity'] == 'critical')])
    #print(code_scanning_df[(code_scanning_df['state'] == 'open') & (code_scanning_df['rule_severity'] == 'critical')])
    open_critical_dependencies = dependencies_df[(dependencies_df['state'] == 'open') & 
                                             (dependencies_df['security_advisory_severity'].isin(['critical', 'high']))
                                             ].shape[0] if not dependencies_df.empty else 0
    open_critical_code_scanning = code_scanning_df[(code_scanning_df['state'] == 'open') & 
                                                   ((code_scanning_df['rule_security_severity_level'] == 'critical') |
                                                    (code_scanning_df['rule_severity'] == 'error'))
                                                   ].shape[0] if not code_scanning_df.empty else 0

    # Print the results
    print(f'Number of active and open secrets for {org}: {active_open_secrets}')
    print(f'Number of open critical alerts for dependencies for {org}: {open_critical_dependencies}')
    print(f'Number of open critical alerts for code scanning for {org}: {open_critical_code_scanning}')

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

def write_to_csv(alerts, alert_type, org, filename):

    if not isinstance(alerts, list) or not alerts:
        print(f'Skipping {alert_type} alerts for {org} because there were no alerts or alerts is not a list')
        return 

    if not isinstance(alerts[0], dict):
        print(f'Alerts are not in the expected format. Alerts: {alerts}')
        return 

    # Define the CSV headers based on the keys of the first alert
    csv_headers = list(alerts[0].keys())

    os.makedirs('_reports', exist_ok=True)  # Create _reports directory if it doesn't exist
    print(f'Writing alert to {filename}')
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        writer.writeheader()
        for alert in alerts:
            # If new keys are introduced, add them to the fieldnames and update the writer
            new_keys = set(alert.keys()) - set(csv_headers)
            if new_keys:
                csv_headers.extend(new_keys)
                writer = csv.DictWriter(file, fieldnames=csv_headers)
            writer.writerow(alert)

def get_github_token():
    try:
        gh_token = subprocess.check_output(['gh', 'auth', 'status', '--show-token'], text=True)
        gh_token = gh_token.split('Token: ')[1].split('\n')[0].strip()
        return gh_token
    except Exception as e:
        print(f"Failed to get GitHub token via gh: {e}")
        return None

# https://docs.github.com/en/rest/dependabot/alerts?apiVersion=2022-11-28
def get_dependabot_alerts(org, token, filename):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    url = f'https://api.github.com/orgs/{org}/dependabot/alerts'
    params = {
        'per_page': 100
    }
    alerts = []

    while url:
        response = requests.get(url, headers=headers, params=params)
        alerts.extend(response.json())
        url = response.links.get('next', {}).get('url')  # Get the URL for the next page

    # Flatten each alert
    flattened_alerts = [flatten_dict(alert) for alert in alerts]
    
    print(f'Dependabot alerts for {org}: {len(flattened_alerts)}')
    write_to_csv(flattened_alerts, 'dependabot', org, filename)

# https://docs.github.com/en/rest/code-scanning/code-scanning?apiVersion=2022-11-28#list-code-scanning-alerts-for-an-organization
def get_code_scanning_alerts(org, token, filename):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    url = f'https://api.github.com/orgs/{org}/code-scanning/alerts'
    params = {
        'per_page': 100
    }
    alerts = []

    while url:
        response = requests.get(url, headers=headers, params=params)
        alerts.extend(response.json())
        url = response.links.get('next', {}).get('url')  # Get the URL for the next page

    flattened_alerts = [flatten_dict(alert) for alert in alerts]

    print(f'Code scanning alerts for {org}: {len(flattened_alerts)}')
    write_to_csv(flattened_alerts, 'code-scanning', org, filename)

# https://docs.github.com/en/rest/secret-scanning/secret-scanning?apiVersion=2022-11-28#list-secret-scanning-alerts-for-an-organization
def get_secret_alerts(org, token, filename):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    url = f'https://api.github.com/orgs/{org}/secret-scanning/alerts'
    params = {
        'per_page': 100
    }
    alerts = []

    while url:
        response = requests.get(url, headers=headers, params=params)
        alerts.extend(response.json())
        url = response.links.get('next', {}).get('url')  # Get the URL for the next page
    
    flattened_alerts = [flatten_dict(alert) for alert in alerts]
    
    print(f'Secret scanning alerts for {org}: {len(flattened_alerts)}')
    write_to_csv(flattened_alerts, 'secret', org, filename)

def print_help():
    print("Usage: python fetch_org_alerts.py <org> [token]")
    print("org: The name of the GitHub organization")
    print("token: The GitHub token (optional). If not token is supplied the 'gh' CLI will be used to get the token.")

def main():

    if len(sys.argv) < 2:
        print_help()
        return

    org = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 else get_github_token()
    
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Generate the filenames
    secrets_file = f'_reports/{org}_secrets_{timestamp}.csv'
    dependencies_file = f'_reports/{org}_dependencies_{timestamp}.csv'
    code_scanning_file = f'_reports/{org}_code_scanning_{timestamp}.csv'

    if not token:
        print("No GitHub token provided and failed to get token via gh")
        return

    get_dependabot_alerts(org, token, dependencies_file)
    get_code_scanning_alerts(org, token, code_scanning_file)
    get_secret_alerts(org, token, secrets_file)

    # In your main function:
    generate_report(org, secrets_file, dependencies_file, code_scanning_file)

if __name__ == "__main__":
    main()