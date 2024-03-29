import subprocess
import requests
import sys
import csv
from datetime import datetime
import os

def write_to_csv(alerts, alert_type, org):

    if not alerts: 
        print(f'Skipping {alert_type} alerts for {org} because there were no alerts')
        return 

    os.makedirs('_reports', exist_ok=True)  # Create _reports directory if it doesn't exist
    filename = f"_reports/{org}_{alert_type}_{datetime.now().strftime('%Y%m%d%H%M')}.csv"
    print(f'Writing {alert_type} alerts for {org} to {filename}')
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=alerts[0].keys())
        writer.writeheader()
        writer.writerows(alerts)

def get_github_token():
    try:
        gh_token = subprocess.check_output(['gh', 'auth', 'status', '--show-token'], text=True)
        gh_token = gh_token.split('Token: ')[1].split('\n')[0].strip()
        return gh_token
    except Exception as e:
        print(f"Failed to get GitHub token via gh: {e}")
        return None

# https://docs.github.com/en/rest/dependabot/alerts?apiVersion=2022-11-28
def get_dependabot_alerts(org, token):
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

    print(f'Dependabot alerts for {org}: {len(alerts)}')
    write_to_csv(alerts, 'dependabot', org)

# https://docs.github.com/en/rest/code-scanning/code-scanning?apiVersion=2022-11-28#list-code-scanning-alerts-for-an-organization
def get_code_scanning_alerts(org, token):
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

    print(f'Code scanning alerts for {org}: {len(alerts)}')
    write_to_csv(alerts, 'code-scanning', org)

# https://docs.github.com/en/rest/secret-scanning/secret-scanning?apiVersion=2022-11-28#list-secret-scanning-alerts-for-an-organization
def get_secret_alerts(org, token):
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

    print(f'Secret scanning alerts for {org}: {len(alerts)}')
    write_to_csv(alerts, 'secret', org)

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

    if not token:
        print("No GitHub token provided and failed to get token via gh")
        return

    get_dependabot_alerts(org, token)
    get_code_scanning_alerts(org, token)
    get_secret_alerts(org, token)

if __name__ == "__main__":
    main()