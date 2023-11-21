import csv
import requests
import os
import base64
import pandas as pd

# Set the GitHub owner type, owner name, and personal access token
owner_type = 'user'  # Change to 'org' if needed
owner_name = 'austimkelly'
# Get the access token from the environment variable
access_token = os.environ.get('GITHUB_ACCESS_TOKEN')

# Include or don't include forked repositories?
skip_forks = True

# Set up headers with the access token
headers = {'Authorization': f'token {access_token}'}

def print_aggregated_metrics_from_csv(csv_file):
    df = pd.read_csv(csv_file)

    total_repos = len(df)
    public_repos = len(df[df['is_private'] == False])
    forked_repos = len(df[df['is_fork'] == True])
    repos_with_codeowners = len(df[df['codeowners'].notna() & (df['codeowners'] != 'Not found') & (df['codeowners'] != '')])
    repos_with_secrets_scanning = len(df[df['secret_scanning_enabled'] == True])
    repos_with_secrets_push_protection = len(df[df['secret_scanning_push_protection_enabled'] == True])
    open_critical_high_alerts = df['code_scanning_critical_alert_count'].sum() + df['code_scanning_high_alert_count'].sum()
    open_critical_dependabot_alerts = df['num_critical_dep_alerts'].sum()

    print(f"Total repositories: {total_repos}")
    print(f"Total public repositories: {public_repos}")
    print(f"Percent of repositories that are forked: {forked_repos / total_repos * 100}%")
    print(f"Percent of repositories with Codeowners: {repos_with_codeowners / total_repos * 100}%")
    print(f"Percent of repositories with Secrets Scanning Enabled: {repos_with_secrets_scanning / total_repos * 100}%")
    print(f"Percent of repositories with Secrets Push Protection Enabled: {repos_with_secrets_push_protection / total_repos * 100}%")
    print(f"Total number of open critical and high code scanning alerts: {open_critical_high_alerts}")
    print(f"Total number of open critical dependabot alerts: {open_critical_dependabot_alerts}")

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

# API Ref: https://docs.github.com/en/rest/code-scanning/code-scanning
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
            return "None"
        else:
            return f"HTTPError: {http_err}"
    except Exception as err:
        return f"Error occurred: {err}"

# API Ref: https://docs.github.com/en/rest/reference/code-scanning#list-code-scanning-alerts-for-a-repository
def get_code_scanning_alert_counts(owner, repo_name, headers):
    # Get the code scanning alerts for the repository
    url = f'https://api.github.com/repos/{owner}/{repo_name}/code-scanning/alerts'
    response = requests.get(url, headers=headers)

    code_scanning_critical_alert_count = 0
    code_scanning_high_alert_count = 0
    code_scanning_medium_alert_count = 0
    code_scanning_low_alert_count = 0
    code_scanning_warning_alert_count = 0
    code_scanning_note_alert_count = 0
    code_scanning_error_alert_count = 0

    if response.status_code == 200:
        alerts_data = response.json()

        # Filter open code scanning alerts
        open_alerts = [alert for alert in alerts_data if alert['state'] == 'open']

        # Count alerts based on severity
        for alert in open_alerts:
            severity = alert['rule']['severity']
            if severity == 'critical':
                code_scanning_critical_alert_count += 1
            elif severity == 'high':
                code_scanning_high_alert_count += 1
            elif severity == 'medium':
                code_scanning_medium_alert_count += 1
            elif severity == 'low':
                code_scanning_low_alert_count += 1
            elif severity == 'warning':
                code_scanning_warning_alert_count += 1
            elif severity == 'note':
                code_scanning_note_alert_count += 1
            elif severity == 'error':
                code_scanning_error_alert_count += 1

    return (
        code_scanning_critical_alert_count,
        code_scanning_high_alert_count,
        code_scanning_medium_alert_count,
        code_scanning_low_alert_count,
        code_scanning_warning_alert_count,
        code_scanning_note_alert_count,
        code_scanning_error_alert_count
    )

def get_codeowners(owner, repo_name, headers):
    codeowners_locations = [
        f'https://api.github.com/repos/{owner}/{repo_name}/contents/CODEOWNERS',
        f'https://api.github.com/repos/{owner}/{repo_name}/contents/.github/CODEOWNERS',
        f'https://api.github.com/repos/{owner}/{repo_name}/contents/docs/CODEOWNERS'
    ]

    for location in codeowners_locations:
        codeowners_response = requests.get(location, headers=headers)

        if codeowners_response.status_code == 200:
            codeowners_content = codeowners_response.json().get('content')
            if codeowners_content is not None:
                codeowners = base64.b64decode(codeowners_content).decode('utf-8')

                # Remove comments from CODEOWNERS
                codeowners_lines = [line for line in codeowners.split('\n') if not line.strip().startswith('#')]

                return '\n'.join(codeowners_lines)

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
    security_and_analysis = repo_info.get('security_and_analysis', {})
    #advanced_security = security_and_analysis.get('advanced_security', {})
    secret_scanning = security_and_analysis.get('secret_scanning', {})
    secret_scanning_push_protection = security_and_analysis.get('secret_scanning_push_protection', {})

    # even though scheam docs say this exists, it doesn't
    # https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-a-user
    # security_and_analysis_enabled = advanced_security.get('status') == 'enabled' if advanced_security else False
    secret_scanning_enabled = secret_scanning.get('status') == 'enabled' if secret_scanning else False
    secret_scanning_push_protection_enabled = secret_scanning_push_protection.get('status') == 'enabled' if secret_scanning_push_protection else False    
    
    # Get names of code scanners
    code_scanners_enabled = get_code_scanning_tool_names(owner, repo_name, headers)

    code_scanning_critical_alert_count,code_scanning_high_alert_count,code_scanning_medium_alert_count,code_scanning_low_alert_count,code_scanning_warning_alert_count,code_scanning_note_alert_count,code_scanning_error_alert_count = get_code_scanning_alert_counts(owner, repo_name, headers)

    security_and_analysis_enabled = False
    if code_scanners_enabled != "None":
        security_and_analysis_enabled = True

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
        'security_and_analysis_enabled': security_and_analysis_enabled,
        'secret_scanning_enabled': secret_scanning_enabled,
        'secret_scanning_push_protection_enabled': secret_scanning_push_protection_enabled,
        'code_scanners_enabled': code_scanners_enabled,
        'code_scanning_critical_alert_count': code_scanning_critical_alert_count,
        'code_scanning_high_alert_count': code_scanning_high_alert_count,
        'code_scanning_medium_alert_count': code_scanning_medium_alert_count,
        'code_scanning_low_alert_count': code_scanning_low_alert_count,
        'code_scanning_warning_alert_count': code_scanning_warning_alert_count,
        'code_scanning_note_alert_count': code_scanning_note_alert_count,
        'code_scanning_error_alert_count': code_scanning_error_alert_count,
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
print("Getting list of repositories...")
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
                    'security_and_analysis_enabled',
                    'secret_scanning_enabled',
                    'secret_scanning_push_protection_enabled',  
                  'code_scanners_enabled',
                    'code_scanning_critical_alert_count',
                    'code_scanning_high_alert_count',
                    'code_scanning_medium_alert_count',
                    'code_scanning_low_alert_count',
                    'code_scanning_warning_alert_count',
                    'code_scanning_note_alert_count',
                    'code_scanning_error_alert_count',
                  'dependabot_enabled',
                  'dependabot_open_alerts_count',
                  'num_critical_dep_alerts',
                  'num_high_dep_alerts',
                  'num_medium_dep_alerts',
                  'num_low_dep_alerts',]
    
    # Add other fieldnames here
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    print("Fetching repo security configs... (this may take a while))")
    for repo in repos:
        repo_details = get_repo_details(owner_name, repo['name'], headers)
        writer.writerow(repo_details)
    
    csvfile.close()
    print(f"CSV file '{csv_filename}' written successfully.")

    with open(csv_filename, 'r') as csvfile:
        print_aggregated_metrics_from_csv(csvfile)
        csvfile.close()

    print("Done.")
