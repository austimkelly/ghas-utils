import argparse
import requests
import pprint
import sys
import json

def get_security_settings(org, token, verbose):
    url = f"https://api.github.com/orgs/{org}"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    data = response.json()

    fields = [
        "dependency_graph_enabled_for_new_repositories",
        "dependabot_alerts_enabled_for_new_repositories",
        "dependabot_security_updates_enabled_for_new_repositories",
        "advanced_security_enabled_for_new_repositories",
        "secret_scanning_enabled_for_new_repositories",
        "secret_scanning_push_protection_enabled_for_new_repositories",
        "secret_scanning_push_protection_custom_link",
        "secret_scanning_push_protection_custom_link_enabled"
    ]

    if verbose:
        for field in fields:
            if field in data:
                print(f"{field}: {data[field]}")
            else:
                print(f"{field} not found in the response.")

    return data

def update_security_settings(org, token, new_settings):
    url = f"https://api.github.com/orgs/{org}"
    headers = {'Authorization': f'token {token}'}
    response = requests.patch(url, headers=headers, json=new_settings)
    if response.status_code != 200:
        print(f"Error: Failed to update security settings. Server responded with status code {response.status_code}.", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Get security settings for an organization.')
    parser.add_argument('org', help='The name of the organization.')
    parser.add_argument('token', help='The personal access token.')
    parser.add_argument('--org-security-settings', help='The input file with security settings.', default=None)
    parser.add_argument('--verbose', action='store_true', help='Print all JSON responses to stdout.')
    args = parser.parse_args()

    settings = get_security_settings(args.org, args.token, args.verbose)
    #print(f"Security settings for {args.org}: {settings}")

    if args.org_security_settings:
        try:
            with open(args.org_security_settings, 'r') as f:
                new_settings = json.load(f)
            print(f"Do you want to write these settings to {args.org}?")
            print(json.dumps(new_settings, indent=4))
            confirmation = input("Please confirm (y/n): ")
            if confirmation.lower() == 'y':
                update_security_settings(args.org, args.token, new_settings)
            else:
                print("Operation cancelled.")
        except FileNotFoundError:
            print(f"Error: The file {args.org_security_settings} does not exist.", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: The file {args.org_security_settings} is not valid JSON.", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()