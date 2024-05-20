import requests
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--repo", required=True, help="GitHub repository")
parser.add_argument("--gh_token", required=True, help="GitHub token")
parser.add_argument("--alert_type", required=True, choices=["dependabot", "code-scanning", "secret"], help="Alert type")
parser.add_argument("--state", required=True, choices=["dismissed", "open"], help="State")
parser.add_argument("--dismissed_reason", help="Dismissed reason")
parser.add_argument("--dismissed_comment", help="Dismissed comment")
parser.add_argument("--alert_number", required=True, help="Alert number")
args = parser.parse_args()

dependabot_reasons = ["fix_started", "inaccurate", "no_bandwidth", "not_used", "tolerable_risk"]
code_reasons = ["null", "false positive", "won't fix", "used in tests"]

if args.state == "dismissed":
    if args.dismissed_reason is None:
        parser.error("--dismissed_reason is required when --state is 'dismissed'")
    elif args.alert_type == "dependabot" and args.dismissed_reason not in dependabot_reasons:
        parser.error("Invalid --dismissed_reason for dependabot. Choices are: " + ", ".join(dependabot_reasons))
    elif args.alert_type == "code-scanning" and args.dismissed_reason not in code_reasons:
        parser.error("Invalid --dismissed_reason for code. Choices are: " + ", ".join(code_reasons))

    if args.dismissed_comment is None:
        # This is not required in the API but would be a smart practice to always have a message
        parser.error("--dismissed_comment is required when --state is 'dismissed'")

args = parser.parse_args()

if args.state == "dismissed" and args.dismissed_reason is None:
    parser.error("--dismissed_reason is required when --state is 'dismissed'")

if args.state == "dismissed" and args.dismissed_comment is None:
    parser.error("--dismissed_comment is required when --state is 'dismissed'")

# Update a dependabot alert
# API Endpoint: https://docs.github.com/en/rest/dependabot/alerts?apiVersion=2022-11-28#update-a-dependabot-alert
# Update a code scanning alert
# API Endpoint: https://docs.github.com/en/rest/code-scanning/code-scanning?apiVersion=2022-11-28#update-a-code-scanning-alert
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
    
}

if args.state == "dismissed":
    data["dismissed_reason"] = args.dismissed_reason
    data["dismissed_comment"] = args.dismissed_comment

# Make the API request
response = requests.patch(url, headers=headers, json=data)

# Check the response
if response.status_code == 200:
    print("Successfully updated the security alert.")
else:
    print(f"Failed to update the security alert. Status code: {response.status_code}. Response: {response.text}")