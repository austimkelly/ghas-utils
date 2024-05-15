import csv
import os
import time
from ghas_scan_helpers import get_repos, get_repo_details, print_aggregated_metrics_from_csv

# Set the GitHub owner type, owner name, and personal access token
owner_type = 'user'  # Options are 'org' or 'user'
owner_names = ['austimkelly']

# Get the access token from the environment variable
access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
if not access_token:
    raise Exception("Access token is missing or empty. Please set the GITHUB_ACCESS_TOKEN environment variable.")

# Include or don't include forked repositories?
skip_forks = False
skip_archives = True

# Set up headers with the access token
headers = {'Authorization': f'token {access_token}'}

# Get the start time
start_time = time.time()

# Initialize an empty list to store all repositories
all_repos = []

# Loop over the owner names
for owner_name in owner_names:
    # Get list of repositories for the current owner
    print(f"Getting list of repositories for {owner_name}...")
    repos = get_repos(owner_name, headers, owner_type, skip_forks, skip_archives)

    # Append the repositories to the all_repos list
    all_repos.extend(repos)

# Write data to CSV
csv_filename = 'github_data.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['repo_name',
                    'owner_type',
                    'owner_name', 
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

    print(f"Fetching repo security configs for {owner_name} . . . (this may take a while))")
    for repo in all_repos:
        repo_details = get_repo_details(repo['owner']['login'], repo['name'], headers)
        
         # If repo_details is None, skip this iteration
         # Sometimes a repo can be listed but meta-info cannot be retrieved 
        if repo_details is None:
            # print repo name we are skipping
            print(f"Skipping repo with no information: {repo['name']}")
            continue

        # Add the owner_type and owner_name to the repo_details
        repo_details['owner_type'] = owner_type
        repo_details['owner_name'] = repo['owner']['login']
        
        writer.writerow(repo_details)
    
    csvfile.close()
    print(f"CSV file '{csv_filename}' written successfully.")

    with open(csv_filename, 'r') as csvfile:
        lines = csvfile.readlines()
        if len(lines) <= 1:
            print(f"ERROR: File {csv_filename} is empty or only contains headers")
        else:
            try:
                print_aggregated_metrics_from_csv(csv_filename)
            except Exception as e:
                print(f"ERROR: An error occurred when trying to parse the file {csv_filename}: {str(e)}")
        
# Get the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time
hours, rem = divmod(elapsed_time, 3600)
minutes, seconds = divmod(rem, 60)

# Print the elapsed time
print(f"Elapsed Time: {int(hours)} hours, {int(minutes)} min, {int(seconds)} seconds")

print("Done.")
