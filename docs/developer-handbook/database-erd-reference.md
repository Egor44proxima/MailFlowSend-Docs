# Database ERD / FK / Index Reference

This reference is generated from the current source migration contract at:

~~~text
MailFlowSend/main
Source SHA 0aae214a2e6324b09b4ad1b093fae174abc5ebb0
Schema v53
~~~

The migration source contains **120 CREATE TABLE statements** and **115 unique named tables**. Rebuilt tables use the last declared CREATE TABLE definition in this reference.

The sequential migration declaration leaves **251 active named indexes** after CREATE/DROP processing. The extracted final table definitions contain **218 explicit foreign-key references**.

!!! note
    This page is a source-schema reference, not a live production sqlite_master dump. Runtime DB integrity and migration-ledger validation remain authoritative for a specific database file.

## High-level ERD

~~~mermaid
flowchart LR
    CSM["csm"] --> CL["clients"]
    CL --> CC["client_contacts"]
    CL --> CA["client_attachment_aliases"]

    CAM["campaigns"] --> PR["preflight_*"]
    CL --> PR
    PR --> DS["dispatch_snapshots"]
    DS --> DR["dispatch_recipients"]
    DS --> DI["dispatch_delivery_identities"]

    DR --> Q["send_queue_items"]
    DI --> IQ["send_identity_queue_items"]
    Q --> SA["send_attempts"]
    IQ --> IA["send_identity_attempts"]

    SA --> DEL["delivery_records"]
    IA --> IDEL["delivery_identity_records"]
    DEL --> DSN["dsn_*"]
    IDEL --> DSN

    DEL --> HIST["History read model"]
    IDEL --> HIST
~~~

## GENERAL domain

~~~mermaid
flowchart LR
    MC["mailing_contacts"] --> MGM["mailing_group_members"]
    MG["mailing_contact_groups"] --> MGM
    MC --> MTM["mailing_tag_members"]
    MT["mailing_contact_tags"] --> MTM
    SP["sender_profiles"] --> CAM["campaigns · GENERAL"]
    CAM --> CG["campaign_general_groups / tags / audience"]
    MC --> CG
    CAM --> GA["campaign_general_attachments"]
~~~

## DEBT domain

~~~mermaid
flowchart LR
    DI["debt_imports"] --> ITEM["debt_items"]
    DI --> SNAP["debt_client_snapshots"]
    CL["clients"] --> SNAP
    DI --> CAM["campaigns · DEBT_NOTICE"]
    CAM --> AUD["campaign_debt_audience"]
    CL --> AUD
    CAM --> ATT["campaign_debt_attachments"]
~~~

## Inbound / DSN domain

~~~mermaid
flowchart LR
    P["inbound_mailbox_profiles"] --> SC["inbound_mailbox_scans"]
    P --> SCH["inbound_mailbox_scan_schedules"]
    SC --> SI["inbound_mailbox_scan_items"]
    SI --> ART["dsn_artifacts"]
    ART --> REP["dsn_recipient_reports"]
    REP --> COR["dsn_correlations / dsn_identity_correlations"]
    COR --> DEL["delivery_records / delivery_identity_records"]
~~~

## Complete table catalog

### application_events

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_application_events_campaign | no | campaign_id,occurred_at DESC,id DESC | WHERE campaign_id IS NOT NULL |
| idx_application_events_code | no | code,occurred_at DESC,id DESC | — |
| idx_application_events_delivery_identity | no | dispatch_delivery_identity_id,occurred_at DESC,id DESC | WHERE dispatch_delivery_identity_id IS NOT NULL |
| idx_application_events_dispatch | no | dispatch_snapshot_id,occurred_at DESC,id DESC | WHERE dispatch_snapshot_id IS NOT NULL |
| idx_application_events_message_id | no | message_id,occurred_at DESC,id DESC | WHERE message_id<>'' |
| idx_application_events_occurred | no | occurred_at DESC,id DESC | — |
| idx_application_events_operation | no | operation_id,occurred_at,id | WHERE operation_id<>'' |
| idx_application_events_queue_item | no | queue_item_id,occurred_at DESC,id DESC | WHERE queue_item_id IS NOT NULL |
| idx_application_events_send_attempt | no | send_attempt_id,occurred_at DESC,id DESC | WHERE send_attempt_id IS NOT NULL |
| idx_application_events_severity | no | severity,occurred_at DESC,id DESC | — |
| idx_application_events_smtp_session | no | smtp_session_id,occurred_at DESC,id DESC | WHERE smtp_session_id IS NOT NULL |
| idx_application_events_status | no | status,occurred_at DESC,id DESC | — |
| idx_application_events_subsystem | no | subsystem,occurred_at DESC,id DESC | — |

### application_operations

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_application_operations_campaign | no | campaign_id,started_at DESC,id DESC | WHERE campaign_id IS NOT NULL |
| idx_application_operations_queue_item | no | queue_item_id,started_at DESC,id DESC | WHERE queue_item_id IS NOT NULL |
| idx_application_operations_started | no | started_at DESC,id DESC | — |
| idx_application_operations_status | no | status,started_at DESC,id DESC | — |
| idx_application_operations_subsystem | no | subsystem,started_at DESC,id DESC | — |

### attachment_batches

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_attachment_batches_expected_period | no | expected_document_period | — |
| idx_attachment_batches_period | no | batch_period | — |

### attachment_match_runs

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| batch_id | attachment_batches(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_attachment_match_runs_batch | no | batch_id,id DESC | — |

### attachment_matches

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| attachment_id | attachments(id) |
| client_id | clients(id) |
| alias_id | client_attachment_aliases(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_attachment_matches_attachment | no | attachment_id | — |
| idx_attachment_matches_client | no | client_id | — |

### attachment_near_matches

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| run_id | attachment_match_runs(id) |
| attachment_id | attachments(id) |
| client_id | clients(id) |
| alias_id | client_attachment_aliases(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_attachment_near_matches_attachment | no | attachment_id | — |
| idx_attachment_near_matches_client | no | client_id | — |

### attachment_orphan_classification_candidates

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| classification_id | attachment_orphan_classifications(id) |
| client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_orphan_class_candidate_class | no | classification_id,rank_no | — |

### attachment_orphan_classification_runs

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| match_run_id | attachment_match_runs(id) |
| batch_id | attachment_batches(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_orphan_class_runs_batch | no | batch_id,id DESC | — |
| idx_orphan_class_runs_match | no | match_run_id,id DESC | — |

### attachment_orphan_classifications

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| classification_run_id | attachment_orphan_classification_runs(id) |
| attachment_id | attachments(id) |
| candidate_client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_orphan_classification_attachment | no | attachment_id,id DESC | — |
| idx_orphan_classification_status | no | classification_run_id,classification | — |

### attachment_reconciliation_cases

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| batch_id | attachment_batches(id) |
| attachment_id | attachments(id) |
| classification_run_id | attachment_orphan_classification_runs(id) |
| assigned_csm_id | csm(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_reconciliation_cases_attachment | no | attachment_id | — |
| idx_reconciliation_cases_batch_status | no | batch_id,status,updated_at DESC | — |

### attachment_reconciliation_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| case_id | attachment_reconciliation_cases(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_reconciliation_events_case | no | case_id,id DESC | — |

### attachment_resolution_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| batch_id | attachment_batches(id) |
| attachment_id | attachments(id) |
| client_id | clients(id) |
| alias_id | client_attachment_aliases(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_attachment_resolution_events_attachment | no | attachment_id,id DESC | — |
| idx_attachment_resolution_events_batch | no | batch_id,id DESC | — |
| idx_attachment_resolution_events_client | no | client_id,id DESC | — |

### attachments

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| batch_id | attachment_batches(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_attachments_batch | no | batch_id | — |
| idx_attachments_hash | no | sha256 | — |
| idx_attachments_kind | no | document_kind | — |
| idx_attachments_period | no | document_period | — |
| idx_attachments_period_status | no | period_status | — |
| idx_attachments_sendable | no | is_sendable | — |

### bounce_resend_campaigns

**Primary key:** resend_campaign_id

**Foreign keys**

| Column | References |
|---|---|
| resend_campaign_id | campaigns(id) |
| source_delivery_record_id | delivery_records(id) |
| root_delivery_record_id | delivery_records(id) |
| source_campaign_id | campaigns(id) |
| source_dispatch_snapshot_id | dispatch_snapshots(id) |
| source_dispatch_recipient_id | dispatch_recipients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_bounce_resend_recipient | no | recipient_kind,recipient_ref_id,resend_campaign_id | — |
| idx_bounce_resend_root | no | root_delivery_record_id,generation,resend_campaign_id | — |
| idx_bounce_resend_source_campaign | no | source_campaign_id,resend_campaign_id | — |

### campaign_audience

**Primary key:** campaign_id,client_id

**Foreign keys**

| Column | References |
|---|---|
| campaign_id | campaigns(id) |
| client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_campaign_audience_client | no | client_id,campaign_id | — |
| idx_campaign_audience_included | no | campaign_id,included,client_id | — |

### campaign_csm

**Primary key:** campaign_id,csm_id

**Foreign keys**

| Column | References |
|---|---|
| campaign_id | campaigns(id) |
| csm_id | csm(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_campaign_csm_csm | no | csm_id,campaign_id | — |

### campaign_debt_attachments

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| campaign_id | campaigns(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_campaign_debt_attachments_campaign | no | campaign_id,id | — |
| idx_campaign_debt_attachments_hash | no | sha256,campaign_id | — |

### campaign_debt_audience

**Primary key:** campaign_id,client_id

**Foreign keys**

| Column | References |
|---|---|
| campaign_id | campaigns(id) |
| snapshot_id | debt_client_snapshots(id) |
| client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_campaign_debt_audience_client | no | client_id,campaign_id | — |
| idx_campaign_debt_audience_included | no | campaign_id,included,client_id | — |

### campaign_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| campaign_id | campaigns(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_campaign_events_campaign | no | campaign_id,id DESC | — |

### campaign_general_attachments

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| campaign_id | campaigns(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_campaign_general_attachments_campaign | no | campaign_id,id | — |
| idx_campaign_general_attachments_hash | no | sha256,campaign_id | — |

### campaign_general_audience

**Primary key:** campaign_id,contact_id

**Foreign keys**

| Column | References |
|---|---|
| campaign_id | campaigns(id) |
| contact_id | mailing_contacts(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_campaign_general_audience_contact | no | contact_id,campaign_id | — |
| idx_campaign_general_audience_included | no | campaign_id,included,contact_id | — |

### campaign_general_groups

**Primary key:** campaign_id,group_id

**Foreign keys**

| Column | References |
|---|---|
| campaign_id | campaigns(id) |
| group_id | mailing_contact_groups(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_campaign_general_groups_group | no | group_id,campaign_id | — |

### campaign_general_tags

**Primary key:** campaign_id,tag_id

**Foreign keys**

| Column | References |
|---|---|
| campaign_id | campaigns(id) |
| tag_id | mailing_contact_tags(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_campaign_general_tags_tag | no | tag_id,campaign_id | — |

### campaigns

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| batch_id | attachment_batches(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_campaigns_batch | no | batch_id,id DESC | — |
| idx_campaigns_debt_import | no | debt_import_id,id DESC | — |
| idx_campaigns_sender_profile | no | sender_profile_id,id DESC | — |
| idx_campaigns_status_updated | no | status,updated_at DESC | — |
| idx_campaigns_type_status_updated | no | campaign_type,status,updated_at DESC | — |

### client_attachment_aliases

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_aliases_client | no | client_id | — |
| idx_aliases_normalized | no | alias_normalized | — |

### client_attachment_batch_state

**Primary key:** batch_id,client_id

**Foreign keys**

| Column | References |
|---|---|
| batch_id | attachment_batches(id) |
| client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_client_attachment_batch_state_status | no | batch_id,status | — |

### client_contact_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| client_id | clients(id) |
| contact_id | client_contacts(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_client_contact_events_client | no | client_id,id DESC | — |
| idx_client_contact_events_contact | no | contact_id,id DESC | — |

### client_contacts

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_client_contacts_client | no | client_id | — |
| idx_client_contacts_email | no | email_normalized | — |
| idx_client_contacts_one_active_primary | yes | client_id | WHERE is_active=1 AND is_primary=1 |

### client_cooperation_status_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_client_cooperation_status_events_client | no | client_id,id DESC | — |

### client_csm_transfer_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| client_id | clients(id) |
| from_csm_id | csm(id) |
| to_csm_id | csm(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_client_csm_transfer_client | no | client_id,id DESC | — |
| idx_client_csm_transfer_from | no | from_csm_id,id DESC | — |
| idx_client_csm_transfer_to | no | to_csm_id,id DESC | — |

### client_registry_intake_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| batch_id | attachment_batches(id) |
| attachment_id | attachments(id) |
| classification_run_id | attachment_orphan_classification_runs(id) |
| client_id | clients(id) |
| csm_id | csm(id) |
| contact_id | client_contacts(id) |
| alias_id | client_attachment_aliases(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_registry_intake_attachment | no | attachment_id,id DESC | — |
| idx_registry_intake_batch | no | batch_id,id DESC | — |
| idx_registry_intake_client | no | client_id,id DESC | — |

### clients

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| csm_id | csm(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_clients_cooperation_status | no | cooperation_status | — |
| idx_clients_cooperation_status_management_mode | no | cooperation_status_management_mode | — |
| idx_clients_csm | no | csm_id | — |
| idx_clients_display_name | no | display_name | — |

### csm

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes:** none active in the migration declaration.

### csm_legacy_ids

**Primary key:** legacy_id

**Foreign keys**

| Column | References |
|---|---|
| csm_id | csm(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_csm_legacy_csm | no | csm_id | — |

### debt_client_snapshots

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| import_id | debt_imports(id) |
| client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_debt_client_snapshots_eligible | no | import_id,send_eligible,debt_total_minor DESC | — |
| idx_debt_client_snapshots_import | no | import_id,client_id | — |

### debt_counterparty_mappings

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_debt_counterparty_mappings_client | no | client_id,is_active,id | — |

### debt_imports

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_debt_imports_created | no | id DESC,created_at DESC | — |
| idx_debt_imports_source | no | source_sha256,id DESC | — |

### debt_items

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| import_id | debt_imports(id) |
| client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_debt_items_client | no | import_id,client_id,aggregation_included | — |
| idx_debt_items_import | no | import_id,source_row_number | — |
| idx_debt_items_match | no | import_id,match_status,aggregation_included | — |

### debt_reconciliation_cases

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| matched_client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_debt_reconciliation_identity | no | counterparty_normalized,status,id DESC | — |
| idx_debt_reconciliation_status | no | status,updated_at DESC,id DESC | — |

### debt_reconciliation_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| case_id | debt_reconciliation_cases(id) |
| client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_debt_reconciliation_events_case | no | case_id,id DESC | — |

### delivery_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| delivery_record_id | delivery_records(id) |
| attempt_id | send_attempts(id) |
| smtp_session_id | smtp_sessions(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_delivery_events_attempt | no | attempt_id | WHERE attempt_id IS NOT NULL |
| idx_delivery_events_message_id | no | message_id | WHERE message_id<>'' |
| idx_delivery_events_record | no | delivery_record_id,id | — |

### delivery_identity_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| delivery_identity_record_id | delivery_identity_records(id) |
| identity_attempt_id | send_identity_attempts(id) |
| smtp_identity_session_id | smtp_identity_sessions(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_delivery_identity_events_message_id | no | message_id | WHERE message_id<>'' |
| idx_delivery_identity_events_record | no | delivery_identity_record_id,id | — |

### delivery_identity_records

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| queue_id | send_queue_jobs(id) |
| identity_queue_item_id | send_identity_queue_items(id) |
| campaign_id | campaigns(id) |
| dispatch_snapshot_id | dispatch_snapshots(id) |
| dispatch_delivery_identity_id | dispatch_delivery_identities(id) |
| latest_attempt_id | send_identity_attempts(id) |
| accepted_attempt_id | send_identity_attempts(id) |
| smtp_session_id | smtp_identity_sessions(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_delivery_identity_records_campaign | no | campaign_id,id DESC | — |
| idx_delivery_identity_records_dispatch_identity | no | dispatch_delivery_identity_id,id | — |
| idx_delivery_identity_records_message_id | no | message_id | WHERE message_id<>'' |
| idx_delivery_identity_records_queue | no | queue_id,id | — |

### delivery_records

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| queue_id | send_queue_jobs(id) |
| queue_item_id | send_queue_items(id) |
| campaign_id | campaigns(id) |
| dispatch_snapshot_id | dispatch_snapshots(id) |
| dispatch_recipient_id | dispatch_recipients(id) |
| latest_attempt_id | send_attempts(id) |
| accepted_attempt_id | send_attempts(id) |
| smtp_session_id | smtp_sessions(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_delivery_records_campaign | no | campaign_id,id DESC | — |
| idx_delivery_records_delivery | no | delivery_status,id DESC | — |
| idx_delivery_records_dispatch_recipient | no | dispatch_recipient_id,id DESC | — |
| idx_delivery_records_message_id | no | message_id | WHERE message_id<>'' |
| idx_delivery_records_queue | no | queue_id,id | — |
| idx_delivery_records_submission | no | submission_status,id DESC | — |

### delivery_unknown_review_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| review_id | delivery_unknown_reviews(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_delivery_unknown_review_events_review | no | review_id,id | — |

### delivery_unknown_reviews

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| attempt_id | send_attempts(id) |
| queue_id | send_queue_jobs(id) |
| queue_item_id | send_queue_items(id) |
| smtp_session_id | smtp_sessions(id) |
| campaign_id | campaigns(id) |
| dispatch_snapshot_id | dispatch_snapshots(id) |
| dispatch_recipient_id | dispatch_recipients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_delivery_unknown_reviews_item | no | queue_item_id,id DESC | — |
| idx_delivery_unknown_reviews_queue_status | no | queue_id,status,id DESC | — |
| idx_delivery_unknown_reviews_status | no | status,id DESC | — |

### diagnostic_health_transitions

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| snapshot_id | diagnostic_snapshots(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_diagnostic_transitions_subsystem | no | subsystem_id,occurred_at,id | — |
| idx_diagnostic_transitions_time | no | occurred_at DESC,id DESC | — |

### diagnostic_snapshot_subsystems

**Primary key:** snapshot_id,subsystem_id

**Foreign keys**

| Column | References |
|---|---|
| snapshot_id | diagnostic_snapshots(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_diagnostic_subsystem_history | no | subsystem_id,snapshot_id DESC | — |
| idx_diagnostic_subsystem_status | no | subsystem_id,status,snapshot_id DESC | — |

### diagnostic_snapshots

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_diagnostic_snapshots_captured | no | captured_at DESC,id DESC | — |
| idx_diagnostic_snapshots_fingerprint | no | state_fingerprint,captured_at DESC,id DESC | — |
| idx_diagnostic_snapshots_status | no | overall_status,captured_at DESC,id DESC | — |

### dispatch_attachments

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| dispatch_recipient_id | dispatch_recipients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_dispatch_attachments_recipient | no | dispatch_recipient_id,id | — |
| idx_dispatch_attachments_sha | no | sha256 | — |

### dispatch_delivery_attachments

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| dispatch_delivery_identity_id | dispatch_delivery_identities(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_dispatch_delivery_attachments_identity | no | dispatch_delivery_identity_id,id | — |
| idx_dispatch_delivery_attachments_sha | no | sha256 | — |

### dispatch_delivery_identities

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| dispatch_snapshot_id | dispatch_snapshots(id) |
| recipient_identity_id | preflight_recipient_identities(id) |
| preflight_recipient_id | preflight_recipients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_dispatch_delivery_identities_client | no | recipient_kind,recipient_ref_id,dispatch_snapshot_id | — |
| idx_dispatch_delivery_identities_email | no | recipient_email_normalized,dispatch_snapshot_id | — |
| idx_dispatch_delivery_identities_snapshot | no | dispatch_snapshot_id,id | — |

### dispatch_delivery_identity_sources

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| dispatch_delivery_identity_id | dispatch_delivery_identities(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_dispatch_delivery_identity_sources_identity | no | dispatch_delivery_identity_id,id | — |

### dispatch_identity_sets

**Primary key:** dispatch_snapshot_id

**Foreign keys**

| Column | References |
|---|---|
| dispatch_snapshot_id | dispatch_snapshots(id) |
| eligibility_set_id | preflight_eligibility_sets(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_dispatch_identity_sets_eligibility | no | eligibility_set_id | — |

### dispatch_recipients

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| dispatch_snapshot_id | dispatch_snapshots(id) |
| eligibility_recipient_id | preflight_eligibility_recipients(id) |
| preflight_recipient_id | preflight_recipients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_dispatch_recipients_email | no | recipient_email,dispatch_snapshot_id | — |
| idx_dispatch_recipients_identity | no | recipient_kind,recipient_ref_id,dispatch_snapshot_id | — |
| idx_dispatch_recipients_snapshot | no | dispatch_snapshot_id,id | — |

### dispatch_snapshot_revisions

**Primary key:** dispatch_snapshot_id,domain

**Foreign keys**

| Column | References |
|---|---|
| dispatch_snapshot_id | dispatch_snapshots(id) |

**Named indexes:** none active in the migration declaration.

### dispatch_snapshots

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| eligibility_set_id | preflight_eligibility_sets(id) |
| attachment_set_id | preflight_attachment_sets(id) |
| recipient_set_id | preflight_recipient_sets(id) |
| preflight_run_id | preflight_runs(id) |
| campaign_id | campaigns(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_dispatch_snapshots_campaign | no | campaign_id,id DESC | — |
| idx_dispatch_snapshots_run | no | preflight_run_id | — |

### documents_catchup_campaigns

**Primary key:** catchup_campaign_id

**Foreign keys**

| Column | References |
|---|---|
| catchup_campaign_id | campaigns(id) |
| root_campaign_id | campaigns(id) |
| source_campaign_id | campaigns(id) |
| batch_id | attachment_batches(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_documents_catchup_period_batch | no | period,batch_id,catchup_campaign_id | — |
| idx_documents_catchup_root | no | root_campaign_id,catchup_campaign_id | — |
| idx_documents_catchup_source | no | source_campaign_id,catchup_campaign_id | — |

### domain_revisions

**Primary key:** domain

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes:** none active in the migration declaration.

### dsn_artifacts

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_dsn_artifacts_created | no | created_at DESC,id DESC | — |
| idx_dsn_artifacts_original_message_id | no | original_message_id_normalized | WHERE original_message_id_normalized<>'' |

### dsn_correlations

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| dsn_recipient_id | dsn_recipient_reports(id) |
| delivery_record_id | delivery_records(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_dsn_correlations_delivery | no | delivery_record_id,id | — |
| idx_dsn_correlations_recipient | no | dsn_recipient_id,id | — |
| idx_dsn_correlations_selected | yes | dsn_recipient_id | WHERE selected=1 |

### dsn_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| artifact_id | dsn_artifacts(id) |
| dsn_recipient_id | dsn_recipient_reports(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_dsn_events_artifact | no | artifact_id,id | — |
| idx_dsn_events_recipient | no | dsn_recipient_id,id | WHERE dsn_recipient_id IS NOT NULL |

### dsn_identity_correlations

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| dsn_recipient_id | dsn_recipient_reports(id) |
| delivery_identity_record_id | delivery_identity_records(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_dsn_identity_correlations_delivery | no | delivery_identity_record_id,id | — |
| idx_dsn_identity_correlations_recipient | no | dsn_recipient_id,id | — |
| idx_dsn_identity_correlations_selected | yes | dsn_recipient_id | WHERE selected=1 |

### dsn_recipient_reports

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| artifact_id | dsn_artifacts(id) |
| correlated_delivery_record_id | delivery_records(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_dsn_recipients_artifact | no | artifact_id,recipient_index | — |
| idx_dsn_recipients_delivery | no | correlated_delivery_record_id | WHERE correlated_delivery_record_id IS NOT NULL |
| idx_dsn_recipients_email | no | recipient_email_normalized | WHERE recipient_email_normalized<>'' |
| idx_dsn_recipients_status | no | correlation_status,id DESC | — |

### import_rows

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| import_run_id | import_runs(id) |
| client_id | clients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_import_rows_run | no | import_run_id | — |

### import_runs

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_import_runs_set | no | import_set_id,id | — |

### inbound_mailbox_connection_tests

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| profile_id | inbound_mailbox_profiles(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_inbound_mailbox_connection_tests_profile | no | profile_id,id DESC | — |

### inbound_mailbox_profile_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| profile_id | inbound_mailbox_profiles(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_inbound_mailbox_profile_events_profile | no | profile_id,id DESC | — |

### inbound_mailbox_profiles

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_inbound_mailbox_profiles_active | no | is_active,id | — |

### inbound_mailbox_scan_items

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| scan_id | inbound_mailbox_scans(id) |
| profile_id | inbound_mailbox_profiles(id) |
| artifact_id | dsn_artifacts(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_inbound_mailbox_scan_items_artifact | no | artifact_id | — |
| idx_inbound_mailbox_scan_items_identity | no | profile_id,uid_validity,uid | — |
| idx_inbound_mailbox_scan_items_scan | no | scan_id,id | — |

### inbound_mailbox_scan_schedules

**Primary key:** profile_id

**Foreign keys**

| Column | References |
|---|---|
| profile_id | inbound_mailbox_profiles(id) |
| last_scan_id | inbound_mailbox_scans(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_inbound_mailbox_scan_schedules_due | no | is_enabled,next_run_at,profile_id | — |

### inbound_mailbox_scan_state

**Primary key:** profile_id

**Foreign keys**

| Column | References |
|---|---|
| profile_id | inbound_mailbox_profiles(id) |
| last_scan_id | inbound_mailbox_scans(id) |

**Named indexes:** none active in the migration declaration.

### inbound_mailbox_scans

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| profile_id | inbound_mailbox_profiles(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_inbound_mailbox_scans_one_running | yes | profile_id | WHERE status='RUNNING' |
| idx_inbound_mailbox_scans_profile | no | profile_id,id DESC | — |

### inbound_mailbox_schedule_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| profile_id | inbound_mailbox_profiles(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_inbound_mailbox_schedule_events_profile | no | profile_id,id DESC | — |

### inbound_mailbox_schedule_runs

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| profile_id | inbound_mailbox_profiles(id) |
| scan_id | inbound_mailbox_scans(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_inbound_mailbox_schedule_runs_one_running | yes | profile_id | WHERE status='RUNNING' |
| idx_inbound_mailbox_schedule_runs_profile | no | profile_id,id DESC | — |

### legacy_import_sets

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_legacy_import_sets_dataset | no | dataset_sha256,id DESC | — |
| idx_legacy_import_sets_status | no | status,id DESC | — |

### mailing_contact_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| contact_id | mailing_contacts(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_mailing_contact_events_contact | no | contact_id,id DESC | — |

### mailing_contact_groups

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes:** none active in the migration declaration.

### mailing_contact_import_rows

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| import_id | mailing_contact_imports(id) |
| contact_id | mailing_contacts(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_mailing_contact_import_rows_contact | no | contact_id,import_id | — |
| idx_mailing_contact_import_rows_import | no | import_id,source_row,id | — |

### mailing_contact_imports

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_mailing_contact_imports_created | no | id DESC | — |
| idx_mailing_contact_imports_hash | no | source_sha256,id DESC | — |

### mailing_contact_tags

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes:** none active in the migration declaration.

### mailing_contacts

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_mailing_contacts_email | no | email_normalized | — |
| idx_mailing_contacts_status_name | no | status,display_name COLLATE NOCASE,id | — |

### mailing_group_members

**Primary key:** group_id,contact_id

**Foreign keys**

| Column | References |
|---|---|
| group_id | mailing_contact_groups(id) |
| contact_id | mailing_contacts(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_mailing_group_members_contact | no | contact_id,group_id | — |

### mailing_tag_members

**Primary key:** tag_id,contact_id

**Foreign keys**

| Column | References |
|---|---|
| tag_id | mailing_contact_tags(id) |
| contact_id | mailing_contacts(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_mailing_tag_members_contact | no | contact_id,tag_id | — |

### mailing_taxonomy_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| contact_id | mailing_contacts(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_mailing_taxonomy_events_contact | no | contact_id,id DESC | — |
| idx_mailing_taxonomy_events_target | no | taxonomy_kind,taxonomy_id,id DESC | — |

### preflight_attachment_files

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| attachment_recipient_id | preflight_attachment_recipients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_attachment_files_recipient | no | attachment_recipient_id,id | — |
| idx_preflight_attachment_files_source | no | source_kind,source_attachment_id | — |

### preflight_attachment_recipients

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| attachment_set_id | preflight_attachment_sets(id) |
| preflight_recipient_id | preflight_recipients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_attachment_recipients_ref | no | recipient_ref_id,attachment_set_id | — |
| idx_preflight_attachment_recipients_set_status | no | attachment_set_id,status,id | — |

### preflight_attachment_sets

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| recipient_set_id | preflight_recipient_sets(id) |
| preflight_run_id | preflight_runs(id) |
| campaign_id | campaigns(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_attachment_sets_campaign | no | campaign_id,id DESC | — |
| idx_preflight_attachment_sets_recipient | no | recipient_set_id | — |
| idx_preflight_attachment_sets_run | no | preflight_run_id | — |

### preflight_eligibility_issues

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| eligibility_recipient_id | preflight_eligibility_recipients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_eligibility_issues_recipient | no | eligibility_recipient_id,id | — |
| idx_preflight_eligibility_issues_source | no | source,source_evidence_id | — |

### preflight_eligibility_recipients

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| eligibility_set_id | preflight_eligibility_sets(id) |
| preflight_recipient_id | preflight_recipients(id) |
| attachment_recipient_id | preflight_attachment_recipients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_eligibility_recipients_ref | no | recipient_ref_id,eligibility_set_id | — |
| idx_preflight_eligibility_recipients_set_status | no | eligibility_set_id,status,id | — |

### preflight_eligibility_sets

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| attachment_set_id | preflight_attachment_sets(id) |
| recipient_set_id | preflight_recipient_sets(id) |
| preflight_run_id | preflight_runs(id) |
| campaign_id | campaigns(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_eligibility_sets_campaign | no | campaign_id,id DESC | — |
| idx_preflight_eligibility_sets_recipient | no | recipient_set_id | — |
| idx_preflight_eligibility_sets_run | no | preflight_run_id | — |

### preflight_recipient_identities

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| recipient_set_id | preflight_recipient_sets(id) |
| preflight_recipient_id | preflight_recipients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_recipient_identities_client_email | no | recipient_kind,recipient_ref_id,recipient_email_normalized,recipient_set_id | — |
| idx_preflight_recipient_identities_parent | no | preflight_recipient_id,id | — |
| idx_preflight_recipient_identities_set_status | no | recipient_set_id,status,id | — |

### preflight_recipient_identity_issues

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| recipient_identity_id | preflight_recipient_identities(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_recipient_identity_issues_identity | no | recipient_identity_id,id | — |

### preflight_recipient_identity_sources

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| recipient_identity_id | preflight_recipient_identities(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_recipient_identity_sources_identity | no | recipient_identity_id,id | — |
| idx_preflight_recipient_identity_sources_ref | no | source_kind,source_ref_id,recipient_identity_id | — |

### preflight_recipient_issues

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| preflight_recipient_id | preflight_recipients(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_recipient_issues_recipient | no | preflight_recipient_id,id | — |

### preflight_recipient_sets

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| preflight_run_id | preflight_runs(id) |
| campaign_id | campaigns(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_recipient_sets_campaign | no | campaign_id,id DESC | — |
| idx_preflight_recipient_sets_run | no | preflight_run_id | — |

### preflight_recipients

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| recipient_set_id | preflight_recipient_sets(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_recipients_ref | no | recipient_kind,recipient_ref_id,recipient_set_id | — |
| idx_preflight_recipients_set_status | no | recipient_set_id,status,id | — |

### preflight_run_revisions

**Primary key:** preflight_run_id,domain

**Foreign keys**

| Column | References |
|---|---|
| preflight_run_id | preflight_runs(id) |

**Named indexes:** none active in the migration declaration.

### preflight_runs

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| campaign_id | campaigns(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_preflight_runs_campaign | no | campaign_id,id DESC | — |
| idx_preflight_runs_created | no | created_at,id | — |

### schema_migrations

**Primary key:** version

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes:** none active in the migration declaration.

### send_attempts

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| queue_id | send_queue_jobs(id) |
| queue_item_id | send_queue_items(id) |
| campaign_id | campaigns(id) |
| dispatch_snapshot_id | dispatch_snapshots(id) |
| dispatch_recipient_id | dispatch_recipients(id) |
| smtp_profile_id | smtp_profiles(id) |
| smtp_session_id | smtp_sessions(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_send_attempts_idempotency_sequence | yes | idempotency_key,attempt_no | WHERE idempotency_key<>'' |
| idx_send_attempts_item | no | queue_item_id,attempt_no DESC | — |
| idx_send_attempts_message_id | no | message_id | WHERE message_id<>'' |
| idx_send_attempts_one_open_per_item | yes | queue_item_id | WHERE state IN ('CREATED','RUNNING') |
| idx_send_attempts_queue | no | queue_id,id | — |
| idx_send_attempts_smtp_session | yes | smtp_session_id | WHERE smtp_session_id IS NOT NULL |
| idx_send_attempts_state | no | state,id DESC | — |
| idx_send_attempts_transport_attempt | no | transport_attempt_id | WHERE transport_attempt_id<>'' |

### send_identity_attempts

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| queue_id | send_queue_jobs(id) |
| identity_queue_item_id | send_identity_queue_items(id) |
| campaign_id | campaigns(id) |
| dispatch_snapshot_id | dispatch_snapshots(id) |
| dispatch_delivery_identity_id | dispatch_delivery_identities(id) |
| smtp_profile_id | smtp_profiles(id) |
| smtp_session_id | smtp_identity_sessions(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_send_identity_attempts_item | no | identity_queue_item_id,attempt_no DESC | — |
| idx_send_identity_attempts_message_id | no | message_id | WHERE message_id<>'' |
| idx_send_identity_attempts_queue | no | queue_id,id | — |
| idx_send_identity_attempts_smtp_session | yes | smtp_session_id | WHERE smtp_session_id IS NOT NULL |
| idx_send_identity_attempts_state | no | state,id DESC | — |

### send_identity_queue_items

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| queue_id | send_queue_jobs(id) |
| dispatch_delivery_identity_id | dispatch_delivery_identities(id) |
| smtp_session_id | smtp_identity_sessions(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_send_identity_queue_items_batch | no | queue_id,batch_no,ordinal | — |
| idx_send_identity_queue_items_queue_state | no | queue_id,state,ordinal | — |
| idx_send_identity_queue_items_session | no | smtp_session_id | WHERE smtp_session_id IS NOT NULL |

### send_identity_retry_state

**Primary key:** identity_queue_item_id

**Foreign keys**

| Column | References |
|---|---|
| identity_queue_item_id | send_identity_queue_items(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_send_identity_retry_due | no | next_retry_at,identity_queue_item_id | WHERE next_retry_at IS NOT NULL |

### send_queue_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| queue_id | send_queue_jobs(id) |
| item_id | send_queue_items(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_send_queue_events_queue | no | queue_id,id | — |

### send_queue_items

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| queue_id | send_queue_jobs(id) |
| dispatch_recipient_id | dispatch_recipients(id) |
| smtp_session_id | smtp_sessions(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_send_queue_items_batch | no | queue_id,batch_no,ordinal | — |
| idx_send_queue_items_cancelled | no | queue_id,cancelled_at,ordinal | — |
| idx_send_queue_items_idempotency_key | yes | idempotency_key | WHERE idempotency_key<>'' |
| idx_send_queue_items_queue_state | no | queue_id,state,ordinal | — |
| idx_send_queue_items_retry_due | no | queue_id,next_retry_at,ordinal | WHERE next_retry_at IS NOT NULL AND cancelled_at IS NULL |
| idx_send_queue_items_session | no | smtp_session_id | WHERE smtp_session_id IS NOT NULL |

### send_queue_jobs

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| campaign_id | campaigns(id) |
| dispatch_snapshot_id | dispatch_snapshots(id) |
| smtp_profile_id | smtp_profiles(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_send_queue_jobs_campaign | no | campaign_id,id DESC | — |
| idx_send_queue_jobs_cancelled | no | cancelled_at,id DESC | — |
| idx_send_queue_jobs_recipient_contract | no | recipient_contract,id DESC | — |
| idx_send_queue_jobs_retry_scheduler | no | retry_auto_resume,id | WHERE retry_auto_resume=1 AND cancelled_at IS NULL |
| idx_send_queue_jobs_state | no | state,id DESC | — |

### sender_profile_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| profile_id | sender_profiles(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_sender_profile_events_profile | no | profile_id,id DESC | — |

### sender_profiles

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes:** none active in the migration declaration.

### smtp_identity_session_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| session_id | smtp_identity_sessions(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_smtp_identity_session_events_session | no | session_id,sequence | — |

### smtp_identity_sessions

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| profile_id | smtp_profiles(id) |
| campaign_id | campaigns(id) |
| dispatch_snapshot_id | dispatch_snapshots(id) |
| dispatch_delivery_identity_id | dispatch_delivery_identities(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_smtp_identity_sessions_dispatch_identity | no | dispatch_delivery_identity_id,id DESC | — |
| idx_smtp_identity_sessions_message_id | no | message_id | — |
| idx_smtp_identity_sessions_profile | no | profile_id,id DESC | — |
| idx_smtp_identity_sessions_status | no | status,id DESC | — |

### smtp_profile_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| profile_id | smtp_profiles(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_smtp_profile_events_profile | no | profile_id,id DESC | — |

### smtp_profiles

**Primary key:** id

**Foreign keys:** none declared in the final CREATE TABLE body.

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_smtp_profiles_active | no | is_active,name COLLATE NOCASE | — |
| idx_smtp_profiles_endpoint | no | host,port | — |

### smtp_session_events

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| session_id | smtp_sessions(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_smtp_session_events_error | no | session_id,smtp_code | WHERE smtp_code>=400 |
| idx_smtp_session_events_session | no | session_id,sequence | — |

### smtp_sessions

**Primary key:** id

**Foreign keys**

| Column | References |
|---|---|
| profile_id | smtp_profiles(id) |

**Named indexes**

| Index | Unique | Columns / expression | Partial predicate |
|---|:---:|---|---|
| idx_smtp_sessions_attempt | no | attempt_id | WHERE attempt_id<>'' |
| idx_smtp_sessions_dispatch_recipient | no | dispatch_recipient_id,id DESC | WHERE dispatch_recipient_id>0 |
| idx_smtp_sessions_message_id | no | message_id | WHERE message_id<>'' |
| idx_smtp_sessions_profile | no | profile_id,id DESC | — |
| idx_smtp_sessions_status | no | status,id DESC | — |

## Design notes

- SQLite foreign_keys are enabled at CoreDB open.
- Schema migration ledger is validated before normal business operation.
- Immutable/evidence tables frequently add UPDATE/DELETE triggers; trigger inventory is intentionally documented separately from this FK/index catalog.
- Index presence does not authorize bypassing domain APIs with direct SQL.
- Identity-aware v49–v52 tables coexist with legacy evidence; they are not a historical rewrite.
