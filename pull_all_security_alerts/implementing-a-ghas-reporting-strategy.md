# Implementing a GitHub Advanced Security (GHAS) Reporting Strategy

> **Note:** Security Overview reporting is only available for Enterprise Cloud customers.

## Thesis

A useful security reporting and analytics solution requires some strategic preparation. This document describes a strategic framework for how you can approach building meaningful security insights, metrics, and KPIs around GHAS reporting solutions and data.The approach described in this document can assist in integrating into existing solutions or providing stand alone reporting and insights on the GHAS itself. 

## Introduction

The GitHub Advanced Security (GHAS) suite of tools provides valuable analysis and reporting into the security posture of your codebase. Multiple tools form the GHAS suite including Code Scanning, Dependabot (Vulnerably Analysis), Secret Scanning, and Security Advisories. Each of these tools provides a unique set of security alerts and reporting that can be used to find and remediate security vulnerabilities in your code. As with any security tool, monitoring and measuring the performance of security alerts is key to its success. 

This article will provide an overview of steps you can take to build your own security reporting strategy using the GHAS Security Overview and Alert reporting as well as considerations for building your own custom reporting. We'll start our GHAS reporting strategy with five (5) primary questions to answer before formalizing a strategy and begin to build, report, and act on your security alerts.

* [Pre-requisites: Understand the security culture](#pre-requisites)
* [What questions are you trying to answer?](#what-questions-are-you-trying-to-answer)
* [What GHAS reporting exists to answer these questions?](#what-ghas-reporting-exists-to-answer-these-questions)
* [Who has access to the built-in GHAS reporting?](#who-has-access-to-the-built-in-ghas-reporting)
* [Do we need to consider any custom reporting?](#do-we-need-to-consider-any-custom-reporting)

The article will help you devise a strategy to quickly answer these questions. However, before we start, you should be aware of some references that are part of the scope of this article.

## References

This document assumes you are familiar with these concepts in the references below. If you are not, you may want to review these references before continuing.

* [Integrating GitHub Advanced Security with third party reporting and analytics platforms](https://resources.github.com/security/integrating-github-advanced-security-with-third-party-platforms/). Github, September 2022. This white paper details the tooling options for building custom reporting such as APIs and Webhooks. It also includes some common metrics you may want to consider for your own reporting strategy.
* [Security Overview](https://docs.github.com/en/enterprise-cloud@latest/code-security/security-overview/about-security-overview) - This is required reading to understand the breadth of features and reporting available in GHAS.

# Strategic Understanding

## Pre-requisites 

 
Adding a security alerting tool to your software development lifecycle won’t fix anything if you don’t have the right structures in place. If your software developers don’t have the right training and expectations on how to respond to security alerts, the tool will quickly become a source of noise and likely be ignored. Setting these development practice expectations will help ensure you can measure the efficacy of your security program as well as help you tune and improve the alerting precision. 

Consider these pre-requisites and how they affect the integration and eventual deployment of your tool. You may want to consider how rolling out a GHAS solution across your enterprise works in concert with these concepts: 

* Do you have an information security policy with clear SLAs for remediating code level vulnerabilities? 
* Do you have a vulnerability and patch management standard with clearly documented SLAs? 
* Do you have a process for which you can evaluate the severity of a security defect/vulnerability? 
* Have you set up clear ownership to find the owners of any vulnerability or code defect? 
* Do you have a way to escalate and review vulnerabilities? 
* Are there requirements to track alerts in bug tracking systems? 

Having a clear understanding of your organizational maturity in these areas can help you forecast how well the rollout of your security monitoring solution will be. If you see gaps in any of these areas and a relationship to negatively impacting the rollout of your security tooling, you may consider hardening these areas of your security culture.   

## What questions are you trying to answer?

The first step in building a reporting strategy is to formulate the questions you want to answer. For example, you may be interested in understanding the net flow of critical code scanning alerts. Or you may want to track the SLA adherence for critical vulnerabilities reported in dependabot to ensure critical dependencies are patched on time. There is no one-size-fits-all answer to this question, rather it depends on the goals of the organization and what you are trying to control. Do you want to ensure all your repositories are compliant? Do you want to send alerts to teams that are not meeting SLAs? Again, this will be entirely dependent on what is important to your own organization.

### Who is the target of the answers to the questions?

The second level of any question is the target audience. Consider the audience for each question. Is this a board-level metrics? Does a Github team need their own insights? Who handles monitoring specific metrics and acting upon them. Being able to differentiate the target audience will help you prioritize the focus on producing the right metrics in the right timeframe. 

### Measure what you want to control 

The question should not be, what metrics should I care about, rather, what characteristics of my environment and I trying to control.  A control can be any improvement or tracking of a KPI – these are the material questions that directly impact your business and bottom line.  Simply picking the most popular metrics to track is typically not a great strategy. You need to consider the outcomes you are looking for and the appropriate measures to track the success or failure of those outcomes.  

### Make sure your insights are actionable!

While some reporting can give us an idea of the volume of alerts, volume alone is likely to lead to an action. Be sure you differentiate between reporting and insights: an insight is a piece of information that can be used directly to take some defined action.  A metric is a numeric value that may not indicate that some response is required. 

For example, consider the Secrets Push Protection feature and a generated insight. Say our metric will be the volume of secrets bypassed by a developer and the insight is the change in weekly volume. If the weekly volume increases week-over-week, we want to take some action which may involve: 

* Review the push protection bypassed alerts. 
* Decide if the bypass is a valid secret (true positive) or not (false positive) 
* If the bypass was a valid secret, work with the developer to remove the secret from the codebase and rotate the secret. Educate the developer on the impacts of bypassing secrets push protection. 
* If it's a legitimate bypass, consider other bypass patterns and if you can build exclusion roles (e.g., for unit tests). 

As the program continues to mature, continue to educate developers and build better detection rules and filters. The expectation will be that the false positive rate and bypass of secrets push alerts will fall to a reasonable level.  

## What GHAS reporting exists to answer these questions?

The next step in building a reporting strategy is to understand what reporting is available to you "out-of-the-box". Github Advanced Security has excellent reporting capabilities documented (see References). It can be difficult to get a "bird's eye view" of the reporting feature across Enterprise, Organization, and Repository scopes. I've built a template in a Google Sheet, [GHAS Security Reporting Capabilities](https://docs.google.com/spreadsheets/d/1gZz0dPl6jLYyNqhglIyzkoy-oq_Q38wh3xx6_WKW8sg/edit#gid=0) which offers a flattened view of what metrics are available for each scope. A scope is defined as the ownership level: Enterprise, Organization, or Repository. By comparing your own questions and desired insights against existing capabilities you can get a quick glimpse of what you can get out-of-the-box versus what you would need to build custom reporting for.

![Reporting Capabilities Image](./img/reporting_capabilities_checklist.png)

## Who has access to the built-in GHAS reporting?

Once you know the level of built-in reporting by scopes, you need to decide who gets access to reporting. This is generally described in the [Permission to view data in security overview](https://docs.github.com/en/enterprise-cloud@latest/code-security/security-overview/about-security-overview#permission-to-view-data-in-security-overview), however I offer a flattened view of all the permissions in [Security Reporting Permissions](https://docs.google.com/spreadsheets/d/1gZz0dPl6jLYyNqhglIyzkoy-oq_Q38wh3xx6_WKW8sg/edit#gid=486941505) (a Google Sheet).

Understanding who needs access will help you build your report visibility strategy for those edge cases where stakeholders may not have default access. Using the [Security Manager role in Github](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization) is a great way to allow non-admins and owners visibility to Security reporting and alerts.

![Security Reporting Roles](./img/alert_and_reporting_roles.png)

## Do we need to consider any custom reporting?

At the last stage, we should have a fairly good idea of the insights we need, what we can get out of the box, and who needs access to them. You can now perform a gap analysis and decide if the ROI is of value to build custom reporting. I'm assuming you will use the REST API to retrieve data to build custom reporting, or leverage Webhooks to push data to a third-party reporting tool or SIEM.

### Leverage Existing Analytics & Reporting Infrastructure

Some considerations that may help you accelerate your custom reporting strategy technical rollout:

* Do you have an existing data warehouse or data lake that can be used to store and report on GHAS data?
* Are there existing design patterns for building data pipelines for data transformation and ingest?
* Does your organization run a SIEM that can be used to ingest GHAS data?
* At what frequency do you need the data?
* What does the freshness of your data need to be? (Hourly, Daily, Weekly?)
* What data visualization tools are available to you?

### Evaluate the Github Alert Schemas

Knowing your schema is critical to review against what you want to report on. Github does not publish a known schema, but it can be easily derived from the REST API. I've offered a flattened view of the schema in this Google Sheet: [Security Alerts REST Response Schema](hhttps://docs.google.com/spreadsheets/d/1gZz0dPl6jLYyNqhglIyzkoy-oq_Q38wh3xx6_WKW8sg/edit#gid=1731893230). Here you can see what data and types are available to you. 

An entity relationship (ER) diagram of the schemas is available below:

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

### Protype your Custom Reporting!

Once you have done a thorough evaluation, start scripting your custom reporting solution. Make sure you understand the data schema and temporal nature of the data to pull the actionable insights you need! Iterate, rinse, repeat. At some point if an insight is shown to no longer produce value or action, drop it and measure the next thing you want to improve. 

## Checking the Github Advanced Security Roadmap 

Github is continuously pushing releasing new features, pushing beta features, and updating roadmap. Please consider these resources to help keep you abreast on upcoming Github and Github Advanced Security releases and roadmaps: 

* [Github Advanced Security Roadmap](https://github.com/orgs/github/projects/4247/views/6) 
* Join the discussion on [Code Security in the Github Discussion](https://github.com/orgs/community/discussions/categories/code-security) group. 
* Check the Security Overview reporting in Github for opportunities to schedule time with the Github Advanced Security Product Team.  

 
Happy Insight Mining! 


