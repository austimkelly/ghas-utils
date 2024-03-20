
The sample script `ghas-settings.py` demonstrates how to use the GitHub REST API to retrieve and update the security settings for an organization. NOTE: This does not attempt to determine which custom configurations (e.g. dependabot.yml) or code scanning workflows are enabled in the repository. 

## Installing

`pip install -r requirements.txt`

## Configuring

See [required-ghas-settings.json](./required-ghas-settings.json) for a file that contains the values of the available GHAS settings that can be applied to an org via API.

## Running

Here's a full run to read and write out the desired security settings for an organization:

```bash
% python3 ghas-settings.py {ORG}  github_pat_YOURTOKEN --verbose --org-security-settings ./required-ghas-settings.json
```

## Related APIs

* [Get an Organization](https://docs.github.com/en/rest/orgs/orgs?apiVersion=2022-11-28#get-an-organization)

The relevant security settings returned in the JSON response are:

```json
  "dependency_graph_enabled_for_new_repositories": false,
  "dependabot_alerts_enabled_for_new_repositories": false,
  "dependabot_security_updates_enabled_for_new_repositories": false,
  "advanced_security_enabled_for_new_repositories": false,
  "secret_scanning_enabled_for_new_repositories": false,
  "secret_scanning_push_protection_enabled_for_new_repositories": false,
  "secret_scanning_push_protection_custom_link": "https://github.com/octo-org/octo-repo/blob/main/im-blocked.md",
  "secret_scanning_push_protection_custom_link_enabled": false 
```

* [Enable or Disable a Security Feature for an Organiztion](https://docs.github.com/en/rest/orgs/orgs?apiVersion=2022-11-28#enable-or-disable-a-security-feature-for-an-organization)


