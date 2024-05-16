# GHAS Utils

# Utils

Here's a table with all the demo/utilities and what they do:

> NOTE: There are not meant to be production grade scripts. They are meant to be education and to help you understand some areas where you would want to use the GitHub API. 

| Demo name | Demo description |
|-----------|-----------------|
|  [ghas-org-scan](./ghas-org-scan/)         |   This is a sort of compliance report that builds a table of settings and security alert volumes for all repositories in an organization. This is a great way to quickly spot out-of-compliance repositories where GitHub reporting may fall short.             |
|  [ghas-settings](./ghas-settings/)         |      This is a simple demo to show you want GHAS settings you can read and write for an organization. GitHub does support https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository now, but this is good if you want to keep things programatically synchronized or have tons or orgs.           |
|  [pull_all_org_security_alerts](./pull_all_org_security_alerts/)         |     This pulls all the dependabot, secret, and code scanning alerts into 3 CSV files for an organization.            |
|  [pull_all_repo_security_alerts](./pull_all_repo_security_alerts/)         |     This just pulls security alerts and advisories for a repo. There's some extra documentation in there about the alert schemas and how to think about your security alert observability program.            |
|  [sbom-visualizer](./sbom-visualizer/)         |      This is just a quick hack to see how to parse the SBOM export from GitHub. It's nothing special here.           |
|  [secret-alert-pull](./secret-alert-pull/)         |      Pulls all secrets for an org.           |
|  [update-security-alerts](./update-security-alerts/)         |    This demo show how to update security alerts. This can be useful when needing to bulk modify hundreds or thousands of security alerts.             |


# GitHub Personal Access Token

All these example require the use of a personal access token. See [Setting a Personal Access Token for your Organization](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization).

