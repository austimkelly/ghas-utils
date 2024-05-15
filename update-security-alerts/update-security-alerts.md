You can update security alerts for a particular alert number in a specific repository. There are 3 different APIs that will you to modify existing alerts:

> Security alerts do not have the ability to add custom tags or custom resolutions. Additionally, there is no mechanism to snooze, silence or otherwise defer alerts for a later time. If you need to track these types of actions, you may want to consider automating specific text in the resolution/dismissed comments.

1. [Update a Dependabot alert](https://docs.github.com/en/rest/dependabot/alerts?apiVersion=2022-11-28#update-a-dependabot-alert) - When updating a Dependabot alert, you can update the `state`, `dismissed_reason`, and `dismissed_comment` fields.
1. [Update a code scanning alert](https://docs.github.com/en/rest/code-scanning/code-scanning?apiVersion=2022-11-28#update-a-code-scanning-alert) - When updating a code scanning alert, you can update the `state`, `dismissed_reason`, and `dismissed_comment` fields.
1. [Update a secret scanning alert](https://docs.github.com/en/rest/secret-scanning/secret-scanning?apiVersion=2022-11-28#update-a-secret-scanning-alert - Here you can update the `state`, `resolution`, and `resolution_comment` fields.

# TODO: Example python script . . .