# Implementing a GitHub Advanced Security Reporting Strategy

> **Note:** Security Overview reporting is only available for Enterprise Cloud customers.

## Introduction

The GitHub Advanced Security (GHAS) suite of tools provide valuable analysis and reporting into the security posture of your codebase. Multiple tools comprise the GHAS suite including: Code Scanning, Dependabot (Vulnerably Analysis), Secret Scanning, and Security Advisories. Each of these tools provides a unique set of security alerts and reporting that can be used to identify and remediate security vulnerabilities in your code. As with any security tool, being able to monitor and measure the performance of security alerts is key to the success of the tool. 

This article will provide an overview of steps you can take to build your own security reporting strategy using the GHAS Security Overview and Alert reporting as well as considerations for building your own custom reporting. We'll start our GHAS reporting strategy with four primary questions to answer before you formalize a strategy and being to build, report, and take action on your security alerts.

* What questions are you trying to answer?
* What reporting exists to answer these questions?
* Who has access to the reporting?
* Do we need to consider any custom reporting?

The article will help you devise a strategy to quickly answer these questions. However, before we start, you should be aware of some references that are part of the scope of this article.

## References

This document assumes you familiar with these concepts. If you are not, you may want to review these references before continuing.

* [Integrating GitHub Advanced Security with third party reporting and analytics platforms](https://resources.github.com/security/integrating-github-advanced-security-with-third-party-platforms/). Github, September 2022. This white paper details the tooling options for building custom reporting such as APIs and Webhooks. It also includes some common metrics you may want to consider for your own reporting strategy.
* [Security Overview](https://docs.github.com/en/enterprise-cloud@latest/code-security/security-overview/about-security-overview) - This would be required reading for understanding the breadth of features and reporting available in GHAS.

# Strategic Understanding

## What questions are you trying to answer?

An initial step in building a reporting strategy is to formulate the questions you want to answer. For example, you may be interested in understanding the net flow of critical code scanning alerts. Or you may want to track the SLA adherence for critical vulnerabilities reported in dependabot to ensure critical dependencies are patched in a timely manner. There is no one-size-fits-all answer to this question, rather it depends on the goals of the organization and what you are trying to control. Do you want to ensure all your repositories are compliant? Do you want to send alerts to teams that are not meeting SLAs? Again, this will be entirely dependent on what is important to your own organization.

### Who are the questions for?

The second level of any question is the target audience. Consider the audience for each question. Is this a board-level metrics? Does a Github team need their own insights? Who is responsible for monitoring specific metrics and taking action.

### Make sure your insights are actionable!

While some reporting can give us an idea to the volume of alerts coming through, that alone is likely not important to take action. Be sure you differential between reporting and insights: an insight is a piece of information can be used directly to take some sort of action. 

For example, consider secrets push protection and insight. The action would be an identified owner to take the following action:

* Review the push protection bypassed alert
* Determine if it's a valid secret or not.
* If a valid secret, work with the developer to remove the secret from the codebase and rotate the secret.
* If it's a legitimate bypass, consider other bypass patterns and if you can build exclusion roles (e.g. for unit tets).

## What reporting exists to answer these questions?

The next step in building a reporting strategy is to understand what reporting is available to you "out-of-the-box". Github Advanced Security has excellent reporting capabilities documented (see References). It can be difficult to get a bird's eye view of the reporting feature across Enterprise, Organization, and Repository scopes. I've built a template in a Google Sheet: [GHAS Security Reporting Capabilities](https://docs.google.com/spreadsheets/d/1gZz0dPl6jLYyNqhglIyzkoy-oq_Q38wh3xx6_WKW8sg/edit#gid=0) that provides a flattened view of what metrics are available for each scope. A scope is defined as the ownership level: Enterprise, Organization, or Repository. By comparing your own questions and desired insights against existing capabilities you can get a quick glimpse of what you can get out-of-the-box versus what you would need to build custom reporting for.

![Reporting Capabilities Image](./img/reporting_capabilities_checklist.png)

## Who has access to the built-in reporting?

Once you know the level of built-in reporting by scopes, you need to determine who gets access to reporting. This is generally described in the [Permission to view data in security overview](https://docs.github.com/en/enterprise-cloud@latest/code-security/security-overview/about-security-overview#permission-to-view-data-in-security-overview), however I provide a flattened view of all the permissions in [Security Reporting Permissions](https://docs.google.com/spreadsheets/d/1gZz0dPl6jLYyNqhglIyzkoy-oq_Q38wh3xx6_WKW8sg/edit#gid=486941505) (a Google Sheet).

Understanding who needs access will help you build your report visibility strategy for those edge cases were stakeholders may not have default access. Using the [Security Manager role in Github](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization) is a great way to allow non-admins and owners visibility to Security reporting and alerts.

![Security Reporting Roles](./img/alert_and_reporting_roles.png)

## Do we need to consider any custom reporting?

At the last stage we should have pretty good idea of the insights we needs, what we can get out of the box, and who needs to get access to them. You can now perform a gap analysis and determine if the ROI is of value to build custom reporting. I'm assuming you will use the REST API to retrieve data to build custom reporting, or leverage Webhooks to push data to a third-party reporting tool or SIEM.

### Leverage Existing Infrastructure

Some considerations that may help you accelerate your custom reporting strategy technical rollout:

* Do you have an existing data warehouse or data lake that can be used to store and report on GHAS data?
* Are there existing design patterns for building data pipelines for data transformation and ingest?
* Does your organization run a SIEM that can be used to ingest GHAS data?
* At what frequency do you need the data?
* What does the freshness of your data need to be? (Hourly, Daily, Weekly?)
* What data visualization tools are available to you?

### Evaluating the Schema

Knowing your schema is critical to review against what you want to report on. Github does not publish a know schema, but it can be easily derived from the REST API. I've provided a flattened view of the schema in this Google Sheet: [Security Alerts REST Response Schema](hhttps://docs.google.com/spreadsheets/d/1gZz0dPl6jLYyNqhglIyzkoy-oq_Q38wh3xx6_WKW8sg/edit#gid=1731893230). Here you can see what data and types are available to you. 

I've additionally provided an entity relationship (ER) diagram of the schema in the collapsible details block below:

<details>
    <summary><b>Click</b> to expand to see the Github Security Alerts Schemas!</summary>

> **Note:** In the following ER diagram, names with `-(FK)` suffix denote items that can be used as a foreign key.

> **Note:** The fields `dismissed_by`, `dismissed_comment`, `fixed_at`, and `dismissed_reason`, can be normalized for Code Scanning Alerts and Dependabot Alerts, but not Secret scanning alerts. For normalizing joins with Secret Alerts with Code/Dependabot alerts, you can use secret alert fields `resolved_by`, `resolution_comment`, and `resolved_at` respectively.
```mermaid
    erDiagram
    CODE-SCANNING-ALERTS {
        number int
        created_at-(FK) datetime
        updated_at-(FK) datetime
        url varchar
        html_url varchar
        state-(FK) varchar
        rule_description varchar
        tool_name varchar
        rule_tags varchar
        tool_guid varchar
        rule_id varchar
        rule_severity varchar
        rule_name varchar
        rule_security_severity_level varchar
        most_recent_instance_classifications varchar
        most_recent_instance_location_path varchar
        most_recent_instance_analysis_key varchar
        dismissed_by varchar
        most_recent_instance_category varchar
        most_recent_instance_message_text varchar
        dismissed_at datetime
        most_recent_instance_environment varchar
        instances_url varchar
        tool_version varchar
        most_recent_instance_location_start_line int
        most_recent_instance_location_start_column int
        most_recent_instance_location_end_line int
        most_recent_instance_ref varchar
        dismissed_reason varchar
        most_recent_instance_state varchar
        fixed_at datetime
        most_recent_instance_location_end_column int
        most_recent_instance_commit_sha varchar
        dismissed_comment varchar
    }
    
    DEPENDABOT-ALERTS {
        number int
        created_at-(FK) datetime
        updated_at-(FK) datetime
        url varchar
        html_url varchar
        state-(FK) varchar
        security_vulnerability_severity varchar
        security_advisory_updated_at datetime
        dependency_scope varchar
        dependency_manifest_path varchar
        security_advisory_vulnerabilities varchar
        security_vulnerability_first_patched_version_identifier varchar
        dismissed_at datetime
        security_advisory_cve_id varchar
        security_advisory_cvss_score varchar
        security_vulnerability_package_ecosystem varchar
        dependency_package_ecosystem varchar
        security_advisory_description varchar
        security_advisory_severity varchar
        security_advisory_cvss_vector_string varchar
        security_advisory_withdrawn_at datetime
        security_vulnerability_vulnerable_version_range varchar
        dismissed_comment varchar
        security_advisory_cwes varchar
        security_vulnerability_package_name varchar
        security_advisory_ghsa_id varchar
        security_advisory_published_at datetime
        security_advisory_identifiers varchar
        dismissed_reason varchar
        security_advisory_references varchar
        security_advisory_summary varchar
        fixed_at datetime
        auto_dismissed_at datetime
        dependency_package_name varchar
        dismissed_by varchar
    }
    
    SECRET-SCANNING-ALERTS {
        number int
        created_at-(FK) datetime
        updated_at-(FK) datetime
        url varchar
        html_url varchar
        state-(FK) varchar
        secret_type varchar
        secret_type_display_name varchar
        secret varchar
        validity varchar
        resolution varchar
        locations_url varchar
        resolved_by varchar
        resolved_at datetime
        resolution_comment varchar
        push_protection_bypassed varchar
        push_protection_bypassed_by varchar
        push_protection_bypassed_at datetime
    }

    SECURITY-ADVISORIES {
        ghsa_id varchar
        cve_id varchar
        url varchar
        html_url varchar
        summary varchar
        description varchar
        severity varchar
        author varchar
        publisher varchar
        state varchar
        created_at datetime
        updated_at datetime
        published_at datetime
    }
```
</details>





