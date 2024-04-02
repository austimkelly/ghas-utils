**Note:** In the following ER diagram, names with '-(FK)' suffix denote items that can be used as a foreign key.

**Note:** The fields `dismissed_by`, `dismissed_comment`, `fixed_at`, and `dismissed_reason`, can be normalized for Code Scanning Alerts and Dependabot Alerts, but not Secret scanning alerts. For normalizing joins with Secret Alerts with Code/Dependabot alerts, you can use secret alert fields `resolved_by`, `resolution_comment`, and `resolved_at` respectively.

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

