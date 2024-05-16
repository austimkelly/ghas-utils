import requests
import argparse

def fetch_custom_properties(repo, gh_pat):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {gh_pat}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = f"https://api.github.com/repos/{repo}/properties/values"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise exception if the request failed
    properties = response.json()
    for prop in properties:
        print(f"Custom Property Key:Value Pairs for repo: {repo}")
        print("-------------------------------")
        if not properties:
            print("The repository has no custom properties.")
        else:
            for prop in properties:
                print(f"{prop['property_name']}: {prop['value']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch custom properties for a GitHub repository.')
    parser.add_argument('--repo', required=True, help='Repository in the format "owner/repo"')
    parser.add_argument('--gh_pat', required=True, help='GitHub Personal Access Token')
    args = parser.parse_args()
    fetch_custom_properties(args.repo, args.gh_pat)