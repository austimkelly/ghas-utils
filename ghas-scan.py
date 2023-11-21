import csv
import requests
import os

# Set the GitHub owner type, owner name, and personal access token
owner_type = 'user'  # Change to 'org' if needed
owner_name = 'austimkelly'
# Get the access token from the environment variable
access_token = os.environ.get('GITHUB_ACCESS_TOKEN')

# Include or don't include forked repositories?
skip_forks = True

# Set up headers with the access token
headers = {'Authorization': f'token {access_token}'}

def get_dependabot_alerts(owner, repo_name, headers):
    dependabot_url = f'https://api.github.com/repos/{owner}/{repo_name}/dependabot/alerts'
    dependabot_alerts = requests.get(dependabot_url, headers=headers)

    # Check if Dependabot alerts are available
    if dependabot_alerts.status_code == 200:
        dependabot_alerts_data = dependabot_alerts.json()

        # Check if Dependabot is enabled
        dependabot_enabled = True if dependabot_alerts_data else False

        # Filter open alerts
        open_alerts = [alert for alert in dependabot_alerts_data if alert['state'] == 'open']

        # Count the number of open alerts
        open_alerts_count = len(open_alerts)

        # Initialize severity counts
        num_critical_dep_alerts = 0
        num_high_dep_alerts = 0
        num_medium_dep_alerts = 0
        num_low_dep_alerts = 0

        # Categorize open alerts based on severity
        for alert in open_alerts:
            severity = alert['security_advisory']['severity']
            if severity == 'critical':
                num_critical_dep_alerts += 1
            elif severity == 'high':
                num_high_dep_alerts += 1
            elif severity == 'medium':
                num_medium_dep_alerts += 1
            elif severity == 'low':
                num_low_dep_alerts += 1

    else:
        dependabot_enabled = False
        open_alerts_count = 0
        num_critical_dep_alerts = 0
        num_high_dep_alerts = 0
        num_medium_dep_alerts = 0
        num_low_dep_alerts = 0

    return (
        dependabot_enabled,
        open_alerts_count,
        num_critical_dep_alerts,
        num_high_dep_alerts,
        num_medium_dep_alerts,
        num_low_dep_alerts
    )

def get_code_scanning_tool_names(owner, repo_name, headers):
    url = f'https://api.github.com/repos/{owner}/{repo_name}/code-scanning/analyses'
    #print("Request URL:", url)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx

        data = response.json()

        if data:
            # Extract unique tools from the analyses
            tools = list(set(analysis['tool']['name'] for analysis in data))
            return ', '.join(tools)
        else:
            return "No data received from the server"
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return "Code scanning not set up for this repository."
        else:
            return f"HTTPError: {http_err}"
    except Exception as err:
        return f"Error occurred: {err}"

def is_secrets_scanning_enabled(owner, repo_name, headers):
        secrets_scanning_url = f'https://api.github.com/repos/{owner}/{repo_name}/secret-scanning/alerts'
        response = requests.get(secrets_scanning_url, headers=headers)
        return len(response.json()) > 0

def get_codeowners(owner, repo_name, headers):
    codeowners_locations = [
        f'https://api.github.com/repos/{owner}/{repo_name}/CODEOWNERS',
        f'https://api.github.com/repos/{owner}/{repo_name}/.github/CODEOWNERS',
        f'https://api.github.com/repos/{owner}/{repo_name}/docs/CODEOWNERS'
    ]

    for location in codeowners_locations:
        codeowners_response = requests.get(location, headers=headers)

        #print(f"Location: {location}, Status Code: {codeowners_response.status_code}")
        
        if codeowners_response.status_code == 200:
            codeowners = codeowners_response.text
            return codeowners

    return "Not found"


def get_repo_details(owner, repo_name, headers):
    # Construct the repository URL using the owner and repo_name variables
    repo_url = f'https://api.github.com/repos/{owner}/{repo_name}'

    # Send a GET request to the repo_url and retrieve the repository information
    repo_info = requests.get(repo_url, headers=headers).json()

    # Get CODEOWNERS file
    codeowners = get_codeowners(owner, repo_name, headers)

    # Get last and first commit dates directly from the repo_details
    last_commit_date = repo_info['pushed_at']
    first_commit_date = repo_info['created_at']

    # Is a fork
    is_fork = repo_info['fork']

    # Public or private
    is_private = repo_info['private']

    # Is archived
    is_archived = repo_info['archived']

    # Check if secrets scanning is enabled
    secrets_scanning_enabled = is_secrets_scanning_enabled(owner, repo_name, headers)

    # Get names of code scanners
    code_scanners_enabled = get_code_scanning_tool_names(owner, repo_name, headers)

    # Check the number of Dependabot alerts
    dependabot_enabled, open_alerts_count, num_critical_dep_alerts, num_high_dep_alerts, num_medium_dep_alerts, num_low_dep_alerts = get_dependabot_alerts(owner, repo_name, headers)

    return {
        'repo_name': repo_info['name'],
        'codeowners': codeowners,
        'last_commit_date': last_commit_date,
        'first_commit_date': first_commit_date,
        'is_fork': is_fork,
        'is_private': is_private,
        'is_archived': is_archived,
        'secrets_scanning_enabled': secrets_scanning_enabled,
        'code_scanners_enabled': code_scanners_enabled,
        'dependabot_enabled': dependabot_enabled,
        'dependabot_open_alerts_count': open_alerts_count,
        'num_critical_dep_alerts': num_critical_dep_alerts,
        'num_high_dep_alerts': num_high_dep_alerts,
        'num_medium_dep_alerts': num_medium_dep_alerts,
        'num_low_dep_alerts': num_low_dep_alerts
        # Add other details here
    }
    return {
        'repo_name': repo_info['name'],
        'codeowners': codeowners,
        'last_commit_date': last_commit_date,
        'first_commit_date': first_commit_date,
        'is_fork': is_fork,
        'is_private': is_private,
        'is_archived': is_archived,
        'secrets_scanning_enabled': secrets_scanning_enabled,
        'code_scanners_enabled': code_scanners_enabled,
        'dependabot_enabled': dependabot_enabled,
        'dependabot_open_alerts_count': open_alerts_count,
        'num_critical_dep_alerts': num_critical_dep_alerts,
        'num_high_dep_alerts': num_high_dep_alerts,
        'num_medium_dep_alerts': num_medium_dep_alerts,
        'num_low_dep_alerts': num_low_dep_alerts
        # Add other details here
    }

def get_repos(owner, headers, owner_type):
    if owner_type == 'user':
        repos_url = f'https://api.github.com/users/{owner}/repos'
    elif owner_type == 'org':
        repos_url = f'https://api.github.com/orgs/{owner}/repos'
    else:
        raise ValueError("Invalid owner type. Use 'user' or 'org'.")

    response = requests.get(repos_url, headers=headers)

    if response.status_code == 200:
        repos = response.json()

        # Filter out forked repositories
        if skip_forks:
            non_forked_repos = [repo for repo in repos if not repo['fork']]
            return non_forked_repos
        else:
            return repos
    else:
        raise Exception(f"Failed to fetch repositories. Status code: {response.status_code}, Response: {response.text}")

# Get list of repositories for the user or organization
repos = get_repos(owner_name, headers, owner_type)

# Write data to CSV
csv_filename = 'github_data.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['repo_name', 
                  'codeowners', 
                  'last_commit_date', 
                  'first_commit_date', 
                  'is_fork', 
                  'is_private', 
                  'is_archived', 
                  'secrets_scanning_enabled', 
                  'code_scanners_enabled',
                  'dependabot_enabled',
                  'dependabot_open_alerts_count',
                  'num_critical_dep_alerts',
                  'num_high_dep_alerts',
                  'num_medium_dep_alerts',
                  'num_low_dep_alerts',]
    
    # Add other fieldnames here
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for repo in repos:
        repo_details = get_repo_details(owner_name, repo['name'], headers)
        writer.writerow(repo_details)
