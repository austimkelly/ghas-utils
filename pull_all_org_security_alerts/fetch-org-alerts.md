This demo shows how to pull all security alerts for an organization. Because security alerts for dependabot, secrets, and code scanning all have a different schema, we need to use different queries to pull them.

## API References

* [Dependabot Alerts REST API](https://docs.github.com/en/rest/dependabot/alerts?apiVersion=2022-11-28)
* [Code Scanning Alerts for your Organization REST API](https://docs.github.com/en/rest/code-scanning/code-scanning?apiVersion=2022-11-28#list-code-scanning-alerts-for-an-organization)
* [Secret Scanning Alerts for your Organization REST API](https://docs.github.com/en/rest/secret-scanning/secret-scanning?apiVersion=2022-11-28#list-secret-scanning-alerts-for-an-organization)

## Running the demo

> NOTE: Running on private/internal repos may need to change the code to filter on the repo visibility. This is currently tested on public repos.

`python3 fetch-org-alerts.py <org name> <your github PAT>`

If you have it all set up right, you will get this output:

```
Dependabot alerts for swell-consulting: 15
Writing alert to _reports/swell-consulting_dependencies_20240516090913.csv
Code scanning alerts for swell-consulting: 19
Writing alert to _reports/swell-consulting_code_scanning_20240516090913.csv
Secret scanning alerts for swell-consulting: 1
Writing alert to _reports/swell-consulting_secrets_20240516090913.csv
Number of active and open secrets for swell-consulting: 0
Number of open critical alerts for dependencies for swell-consulting: 2
Number of open critical alerts for code scanning for swell-consulting: 19
```

As you can see from the console output, each REST API call writes results to a CSV file in the `_reports` directory.

### Example Output

> NOTE: The full schema is available. There has been no filtering on columns for this output.

See the [example_outputs directory](./example_outputs/) for an example of the output file.

## Use cases

While the Security Overview at the Enterprise and Organization level can give you some aggrated metrics on the volume of alerts and access to the raw alerts, there are some cases where you own policy may need to be applied to programmatic access on process of alert data. Some examples include:

* SLA adherence. You may want to track which alert classifications are out of SLA and take some additional action.
* Mass updates. You need to make some decision to change the status of masses of alerts.
* Deferring alerts. You may want to close some alerts with comments to defer them. Currently, there is no way to set a status to "defer" or otherwise track alerts that you want to revisit at a later date.