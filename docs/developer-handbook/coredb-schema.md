# CoreDB та SQLite schema

`internal/coredb` is the canonical durable domain layer. Current schema version is **v53**.

## Connection policy

`coredb.Open(path)` configures SQLite with:

~~~text
MaxOpenConns = 1
MaxIdleConns = 1
PRAGMA busy_timeout = 5000
startup quick_check
PRAGMA foreign_keys = ON
PRAGMA journal_mode = WAL
PRAGMA synchronous = NORMAL
~~~

The startup quick check runs **before** persistent journal settings/migration work.

## Migration model

Schema ownership is explicit:

~~~go
const SchemaVersion = 53
~~~

`schema_migrations(version, name, applied_at)` is the durable ledger.

Before mutation, Core validates:

- contiguous versions;
- exact canonical migration name for each version;
- no unsupported future schema;
- no application tables without a durable ledger;
- no empty ledger over an existing application schema.

This makes migration validation a recovery/security boundary, not just a convenience.

## Migration history

| Version | Migration |
|---:|---|
| 1 | initial_core_domain |
| 2 | client_data_semantics |
| 3 | attachment_batch_indexer |
| 4 | attachment_expected_period |
| 5 | attachment_matcher |
| 6 | full_legacy_client_import |
| 7 | orphan_resolution_alias_learning |
| 8 | orphan_classification_missing_client_detection |
| 9 | missing_client_registry_intake |
| 10 | deferred_verification_reconciliation_queue |
| 11 | client_csm_ownership_transfer |
| 12 | client_contact_management |
| 13 | campaign_draft_builder |
| 14 | multi_campaign_foundation_and_general_contacts |
| 15 | general_groups_and_tags |
| 16 | general_contact_csv_xlsx_import |
| 17 | general_campaign_type |
| 18 | general_sender_profiles |
| 19 | general_campaign_attachments |
| 20 | debt_client_matching_reconciliation |
| 21 | debt_immutable_import_snapshots |
| 22 | debt_notice_campaign |
| 23 | debt_template_attachments_preview |
| 24 | preflight_foundation |
| 25 | preflight_recipient_resolution |
| 26 | preflight_attachment_resolution |
| 27 | preflight_eligibility_verdict |
| 28 | immutable_dispatch_snapshot |
| 29 | smtp_profiles_and_connectivity |
| 30 | smtp_session_observability |
| 31 | smtp_real_transport_security_evidence |
| 32 | smtp_message_id_domain_setting |
| 33 | persistent_send_queue_batching |
| 34 | send_queue_cooperative_cancellation |
| 35 | smtp_attempt_state_foundation |
| 36 | delivery_unknown_operator_review |
| 37 | smtp_retry_policy_engine |
| 38 | send_idempotency_duplicate_prevention |
| 39 | delivery_history_foundation |
| 40 | dsn_ingestion_message_correlation |
| 41 | documents_catchup_delta_dispatch |
| 42 | catchup_query_indexing_planner_hardening |
| 43 | bounced_recipient_controlled_resend |
| 44 | diagnostic_snapshot_history_incident_timeline |
| 45 | inbound_mailbox_profile_connection_test |
| 46 | inbound_mailbox_scan_dsn_intake |
| 47 | inbound_mailbox_automatic_scheduler |
| 48 | client_cooperation_status_management |
| 49 | multi_recipient_identity_foundation |
| 50 | immutable_dispatch_delivery_identity |
| 51 | identity_aware_queue_smtp_sidecar |
| 52 | identity_retry_dsn_history_sidecars |
| 53 | structured_application_event_store |

## Table inventory

The current migration source creates **115 named application tables**. The most useful way to reason about them is by ownership family.

### Client / CSM / attachment domain

~~~text
csm
csm_legacy_ids
clients
client_contacts
client_attachment_aliases
client_csm_transfer_events
client_contact_events
client_cooperation_status_events

attachment_batches
attachments
attachment_matches
attachment_match_runs
attachment_near_matches
client_attachment_batch_state
attachment_resolution_events
attachment_orphan_classification_runs
attachment_orphan_classifications
attachment_orphan_classification_candidates
attachment_reconciliation_cases
attachment_reconciliation_events
client_registry_intake_events

import_runs
import_rows
legacy_import_sets
domain_revisions
~~~

### GENERAL mailing domain

~~~text
mailing_contacts
mailing_contact_events
mailing_contact_groups
mailing_group_members
mailing_contact_tags
mailing_tag_members
mailing_taxonomy_events
mailing_contact_imports
mailing_contact_import_rows

sender_profiles
sender_profile_events

campaign_general_groups
campaign_general_tags
campaign_general_audience
campaign_general_attachments
~~~

### Campaign / debt domain

~~~text
campaigns
campaign_csm
campaign_audience
campaign_events

debt_counterparty_mappings
debt_reconciliation_cases
debt_reconciliation_events
debt_imports
debt_items
debt_client_snapshots
campaign_debt_audience
campaign_debt_attachments
~~~

### Preflight / dispatch domain

~~~text
preflight_runs
preflight_run_revisions
preflight_recipient_sets
preflight_recipients
preflight_recipient_issues
preflight_attachment_sets
preflight_attachment_recipients
preflight_attachment_files
preflight_eligibility_sets
preflight_eligibility_recipients
preflight_eligibility_issues

dispatch_snapshots
dispatch_snapshot_revisions
dispatch_recipients
dispatch_attachments
~~~

### SMTP / Queue / attempt domain

~~~text
smtp_profiles
smtp_profile_events
smtp_sessions
smtp_session_events

send_queue_jobs
send_queue_items
send_queue_events
send_attempts
delivery_unknown_reviews
delivery_unknown_review_events
~~~

### Delivery / DSN / operational send domain

~~~text
delivery_records
delivery_events

dsn_artifacts
dsn_recipient_reports
dsn_correlations
dsn_events

documents_catchup_campaigns
bounce_resend_campaigns
~~~

### Diagnostic / inbound domain

~~~text
diagnostic_snapshots
diagnostic_snapshot_subsystems
diagnostic_health_transitions

inbound_mailbox_profiles
inbound_mailbox_profile_events
inbound_mailbox_connection_tests
inbound_mailbox_scan_state
inbound_mailbox_scans
inbound_mailbox_scan_items
inbound_mailbox_scan_schedules
inbound_mailbox_schedule_events
inbound_mailbox_schedule_runs
~~~

### Identity-aware sidecars

Schema v49–v52 added an identity-aware path without rewriting legacy historical evidence:

~~~text
preflight_recipient_identities
preflight_recipient_identity_sources
preflight_recipient_identity_issues

dispatch_identity_sets
dispatch_delivery_identities
dispatch_delivery_identity_sources
dispatch_delivery_attachments

smtp_identity_sessions
smtp_identity_session_events

send_identity_queue_items
send_identity_attempts
send_identity_retry_state

delivery_identity_records
delivery_identity_events
dsn_identity_correlations
~~~

The runtime read model can union legacy + identity-aware evidence. Historical legacy rows are not backfilled merely to make them look identity-aware.

### Structured application logging

Schema v53 adds:

~~~text
application_operations
application_events
~~~

These tables are technical observability state, not canonical business ownership.

### Migration ledger

~~~text
schema_migrations
~~~

## Domain revisions

`domain_revisions` separates stale-detection domains. Important examples include client identity, ownership, contacts, campaigns, mailing contacts, sender/SMTP profiles and other accepted mutable projections.

A CSM transfer, for example, should advance ownership semantics without pretending client identity changed.

## Legacy + identity-aware coexistence

Current architecture intentionally supports two historical paths:

~~~mermaid
flowchart LR
    L["legacy dispatch_recipients"] --> LR["delivery_records"]
    I["dispatch_delivery_identities"] --> IR["delivery_identity_records"]
    LR --> U["read-model union"]
    IR --> U
    U --> H["History / Coverage / Analytics"]
~~~

Do not “simplify” this by rewriting old evidence unless a future migration explicitly owns that transformation and has accepted evidence.

## Transaction ownership

Business operations that touch multiple tables should stay inside CoreDB transaction boundaries.

Examples:

- ownership transfer + audit event;
- contact mutation + revision + event;
- preflight snapshot creation;
- immutable dispatch freeze;
- Queue state + event;
- DSN correlation + delivery projection;
- controlled recovery-related DB state.

Avoid multi-step UI orchestration where a partial failure could leave durable tables inconsistent.

## Adding a migration

For a new schema version:

1. increment `SchemaVersion`;
2. append one canonical migration entry;
3. give it a stable immutable name;
4. keep ledger validation compatible;
5. add targeted migration tests;
6. add recovery compatibility tests when backup restore is affected;
7. update documentation only after accepted migration evidence.

Never rename an already released migration row.
