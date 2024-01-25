import os
import requests
import csv

# Get the personal access token from the GH_TOKEN environment variable
token = os.getenv('GITHUB_ACCESS_TOKEN')

# Account type can be either 'user' or 'org'
account_type = 'users'  # 'orgs' or 'users'

# Replace with your account name
owner = 'austimkelly' # The org or user name housing the repositories
verbose_logging = True

def fetch_repos(account_type, account, headers, page=1, per_page=100):
    repos = []
    while True:
        repos_url = f'https://api.github.com/{account_type}/{account}/repos?page={page}&per_page={per_page}'
        if verbose_logging:
            print(f"Calling {repos_url}...")
        response = requests.get(repos_url, headers=headers)
        data = response.json()
        repos.extend(data)
        if len(data) < per_page:
            break
        page += 1
    return repos

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
}

# Get all repos of the account
repos = fetch_repos(account_type, owner, headers)

# Open the CSV file
with open('secret_scanning_alerts.csv', 'w', newline='') as csvfile:
    fieldnames = ['owner', 'repo', 'number', 'rule', 'state', 'created_at', 'html_url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    # For each repo, get the secret scanning alerts
    for repo in repos:
        alerts_response = requests.get(f'https://api.github.com/repos/{owner}/{repo["name"]}/secret-scanning/alerts', headers=headers)
        alerts = alerts_response.json()

        # print alerts json response for each repo
        if verbose_logging:
            print(f"Calling https://api.github.com/repos/{owner}/{repo['name']}/secret-scanning/alerts...")
            print(alerts)

        # If the response is a dictionary with a 'message' key, skip this iteration
        if isinstance(alerts, dict) and 'message' in alerts:
            print(f"Skipping {repo['name']}: {alerts['message']}")
            continue

        # Write each alert to the CSV file
        for alert in alerts:
            writer.writerow({
                'owner': owner,  # org or user
                'repo': repo['name'],
                'number': alert['number'],
                'rule': alert['secret_type'],  # Use 'secret_type' instead of 'rule'
                'state': alert['state'],
                'created_at': alert['created_at'],
                'html_url': alert['html_url'],
            })