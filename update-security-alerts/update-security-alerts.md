# GitHub REST API to Update Security Alerts

You can update security alerts for a particular alert number in a specific repository. Note that you can only update one alert type and one alert ID for each API request. This example uses a common set of command-line parameters, however, the input values will vary depending on the alert type you want to update. As such, make sure to pay attention to the nuances of the input parameters for each alert type.

## API References

There are 3 different APIs that will you to modify existing alerts:

1. [Update a Dependabot alert](https://docs.github.com/en/rest/dependabot/alerts?apiVersion=2022-11-28#update-a-dependabot-alert) - When updating a Dependabot alert, you can update the `state`, `dismissed_reason`, and `dismissed_comment` fields.
1. [Update a code scanning alert](https://docs.github.com/en/rest/code-scanning/code-scanning?apiVersion=2022-11-28#update-a-code-scanning-alert) - When updating a code scanning alert, you can update the `state`, `dismissed_reason`, and `dismissed_comment` fields.
1. [Update a secret scanning alert](https://docs.github.com/en/rest/secret-scanning/secret-scanning?apiVersion=2022-11-28#update-a-secret-scanning-alert) - Here you can update the `state`, `resolution`, and `resolution_comment` fields.

> Security alerts do not have the ability to add custom tags or custom resolutions. Additionally, there is no mechanism to snooze, silence or otherwise defer alerts for a later time. If you need to track these types of actions, you may want to consider automating specific text in the resolution/dismissed comments.

## Fetching the alerts

In order to get the alert IDs you want, you will need to identify them in advance with some specific API calls. Checkout the demo in this repository on [Pull All Org Alerts](../pull_all_org_security_alerts/fetch-org-alerts.md) to see how you can fetch all the alerts for a specific organization.


# Running the sample script

The [update-security-alerts.py](./update-security-alerts.py) script is a command-line tool can open or dismiss any security alert type. See the usage and example below for the difference between the alert types.

## Usage

``` bash
usage: update-security-alerts.py [-h] --repo REPO --gh_token GH_TOKEN --alert_type
                                 {dependabot,code-scanning,secret-scanning} --state STATE
                                 [--dismissed_reason DISMISSED_REASON] [--dismissed_comment DISMISSED_COMMENT]
                                 --alert_number ALERT_NUMBER

Update a security alert in a GitHub repository.

options:
  -h, --help            show this help message and exit
  --repo REPO           The GitHub repository to update security alerts for, in the format 'owner/repo'.
  --gh_token GH_TOKEN   The GitHub token used for authentication. Should have write security_event permissions.
  --alert_type {dependabot,code-scanning,secret-scanning}
                        The type of the security alert. Can be 'dependabot', 'code-scanning', or 'secret-scanning'.
  --state STATE         The state of the security alert. For 'dependabot' and 'code-scanning' alerts, can be 'open' or
                        'dismissed'. For 'secret-scanning' alerts, can be 'open' or 'resolved'.
  --dismissed_reason DISMISSED_REASON
                        The reason for dismissing the security alert. Required when '--state' is 'dismissed' for
                        'dependabot' and 'code-scanning' alerts, and when '--state' is 'resolved' for 'secret-scanning'
                        alerts.
  --dismissed_comment DISMISSED_COMMENT
                        An optional comment about the dismissal of the security alert.
  --alert_number ALERT_NUMBER
                        The number of the security alert to update.
```

## Dependabot

### Dismissing a Dependabot alert:

```bash
python3 update-security-alerts.py --repo "swell-consulting/swiss-cheese" --gh_token "YOUR_TOKEN" --alert_type dependabot --state dismissed --dismissed_reason tolerable_risk --dismissed_comment "This alert is accurate but we use a sanitizer." --alert_number 1
```

### Reopening a Dependabot alert:

``` bash
python3 update-security-alerts.py --repo "swell-consulting/swiss-cheese" --gh_token "YOUR_TOKEN" --alert_type dependabot --state open  --alert_number 1
```

### Dismissing a Code Scanning alert:

```bash
python3 update-security-alerts.py --repo "swell-consulting/swiss-cheese" --gh_token "YOUR_TOKEN" --alert_type code-scanning --state open  --alert_number 1
```

## Code Scanning 

## Reopening a Code Scanning alert:

```bash
python3 update-security-alerts.py --repo "swell-consulting/swiss-cheese" --gh_token ""YOUR_TOEKN" --alert_type code-scanning --state dismissed  --alert_number 1 --dismissed_reason "won't fix" --dismissed_comment "API testing"
```

## Secret Scanning

### Dismissing a Secret Scanning alert:

```bash
python3 update-security-alerts.py --repo "swell-consulting/swiss-cheese" --gh_token "YOUR_TOKEN" --alert_type secret-scanning --state resolved --dismissed_reason used_in_tests --dismissed_comment "secret API testing" --alert_number 1
```

### Reopening a Secret Scanning alert:

```bash
python3 update-security-alerts.py --repo "swell-consulting/swiss-cheese" --gh_token "YOUR_TOKEN --alert_type secret-scanning --state open --dismissed_reason used_in_tests --dismissed_comment "secret API testing" --alert_number 1
```