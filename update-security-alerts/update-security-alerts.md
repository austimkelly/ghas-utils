You can update security alerts for a particular alert number in a specific repository. There are 3 different APIs that will you to modify existing alerts:

> WARNING: This is a working progress. The script is not fully functional yet.

> Security alerts do not have the ability to add custom tags or custom resolutions. Additionally, there is no mechanism to snooze, silence or otherwise defer alerts for a later time. If you need to track these types of actions, you may want to consider automating specific text in the resolution/dismissed comments.

1. [Update a Dependabot alert](https://docs.github.com/en/rest/dependabot/alerts?apiVersion=2022-11-28#update-a-dependabot-alert) - When updating a Dependabot alert, you can update the `state`, `dismissed_reason`, and `dismissed_comment` fields.
1. [Update a code scanning alert](https://docs.github.com/en/rest/code-scanning/code-scanning?apiVersion=2022-11-28#update-a-code-scanning-alert) - When updating a code scanning alert, you can update the `state`, `dismissed_reason`, and `dismissed_comment` fields.
1. [Update a secret scanning alert](https://docs.github.com/en/rest/secret-scanning/secret-scanning?apiVersion=2022-11-28#update-a-secret-scanning-alert - Here you can update the `state`, `resolution`, and `resolution_comment` fields.

# Running the sample script

``` bash
python3 update-security-alerts.py --repo "OWNER/REPO" --gh_token "YOUR-TOKEN" --alert_type "dependabot" --state "dismissed" --dismissed_reason "tolerable_risk" --dismissed_comment "This alert is accurate but we use a sanitizer." --alert_number "ALERT_NUMBER"
```

