import requests
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--repo", required=True, help="GitHub repository")
parser.add_argument("--gh_token", required=True, help="GitHub token")
parser.add_argument("--alert_type", required=True, choices=["dependabot", "code", "secret"], help="Alert type")
parser.add_argument("--state", required=True, choices=["dismissed", "open"], help="State")
parser.add_argument("--dismissed_reason", required=True, choices=["fix_started", "inaccurate", "no_bandwidth", "not_used", "tolerable_risk"], help="Dismissed reason")
parser.add_argument("--dismissed_comment", required=True, help="Dismissed comment")
parser.add_argument("--alert_number", required=True, help="Alert number")
args = parser.parse_args()

# API Endpoint: https://docs.github.com/en/rest/dependabot/alerts?apiVersion=2022-11-28#update-a-dependabot-alert
url = f"https://api.github.com/repos/{args.repo}/{args.alert_type}/alerts/{args.alert_number}"

# Define the headers
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {args.gh_token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

# Define the data
data = {
    "state": args.state,
    "dismissed_reason": args.dismissed_reason,
    "dismissed_comment": args.dismissed_comment
}

# Make the API request
response = requests.patch(url, headers=headers, json=data)

# Check the response
if response.status_code == 200:
    print("Successfully updated the security alert.")
else:
    print(f"Failed to update the security alert. Status code: {response.status_code}. Response: {response.text}")