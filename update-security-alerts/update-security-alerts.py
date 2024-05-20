import requests
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Update a security alert in a GitHub repository.')
parser.add_argument("--repo", required=True, help="The GitHub repository to update security alerts for, in the format 'owner/repo'.")
parser.add_argument("--gh_token", required=True, help="The GitHub token used for authentication. Should have write security_event permissions.")
parser.add_argument("--alert_type", required=True, choices=["dependabot", "code-scanning", "secret-scanning"], help="The type of the security alert. Can be 'dependabot', 'code-scanning', or 'secret-scanning'.")
parser.add_argument("--state", required=True, help="The state of the security alert. For 'dependabot' and 'code-scanning' alerts, can be 'open' or 'dismissed'. For 'secret-scanning' alerts, can be 'open' or 'resolved'.")
parser.add_argument("--dismissed_reason", help="The reason for dismissing the security alert. Required when '--state' is 'dismissed' for 'dependabot' and 'code-scanning' alerts, and when '--state' is 'resolved' for 'secret-scanning' alerts.")
parser.add_argument("--dismissed_comment", help="An optional comment about the dismissal of the security alert.")
parser.add_argument("--alert_number", required=True, help="The number of the security alert to update.")
args = parser.parse_args()

dependabot_reasons = ["fix_started", "inaccurate", "no_bandwidth", "not_used", "tolerable_risk"]
code_reasons = ["null", "false positive", "won't fix", "used in tests"]
secret_reasons = ["false_positive", "won't fix", "revoked", "used_in_tests", "null"]

if args.state == "dismissed":
    if args.dismissed_reason is None:
        parser.error("--dismissed_reason is required when --state is 'dismissed'")
    elif args.alert_type == "dependabot" and args.dismissed_reason not in dependabot_reasons:
        parser.error("Invalid --dismissed_reason for dependabot. Choices are: " + ", ".join(dependabot_reasons))
    elif args.alert_type == "code-scanning" and args.dismissed_reason not in code_reasons:
        parser.error("Invalid --dismissed_reason for code. Choices are: " + ", ".join(code_reasons))

if args.alert_type == "secret-scanning":
    if args.state not in ["open", "resolved"]:
        parser.error("Invalid --state for secret-scanning. Choices are: open, resolved")
    if args.state == "resolved":
        if args.dismissed_reason is None:
            parser.error("--dismissed_reason is required when --alert_type is 'secret-scanning' and --state is 'resolved'")
        elif args.dismissed_reason not in secret_reasons:
            parser.error("Invalid --dismissed_reason for secret-scanning. Choices are: " + ", ".join(secret_reasons))


# Update a secret scanning alert
# API Endpoint: https://docs.github.com/en/rest/secret-scanning/secret-scanning?apiVersion=2022-11-28
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
    if args.dismissed_comment is not None:
        data["dismissed_comment"] = args.dismissed_comment

if args.alert_type == "secret-scanning" and args.state == "resolved":
    data["resolution"] = args.dismissed_reason
    if args.dismissed_comment is not None:
        data["resolution_comment"] = args.dismissed_comment

# Make the API request
response = requests.patch(url, headers=headers, json=data)

# Check the response
if response.status_code == 200:
    print("Successfully updated the security alert.")
else:
    print(f"Failed to update the security alert. Status code: {response.status_code}. Response: {response.text}")