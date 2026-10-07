# Capability Changelog · MAIL-1 → MAIL-16

Public-safe capability timeline поточного MailFlowSend source baseline.

## MAIL-1 · Core client domain

Canonical SQLite client/CSM model та client data semantics.

~~~text
v1 initial_core_domain
v2 client_data_semantics
~~~

Canonical display name відокремлений від legacy subject/internal note; cooperation status став окремим полем.

## MAIL-2 · Attachment batch indexing

PDF catalog/indexing, document kind/period detection та explicit expected document period.

~~~text
v3 attachment_batch_indexer
v4 attachment_expected_period
~~~

Invariant:

~~~text
batch_key != detected_document_period != expected_document_period
~~~

## MAIL-3 · Client ↔ attachment identity operations

Attachment matcher, full legacy client import, orphan resolution/alias learning, orphan classification, missing-client reconciliation, CSM transfer і contact management.

~~~text
v5  attachment_matcher
v6  full_legacy_client_import
v7  orphan_resolution_alias_learning
v8  orphan_classification_missing_client_detection
v9  missing_client_registry_intake
v10 deferred_verification_reconciliation_queue
v11 client_csm_ownership_transfer
v12 client_contact_management
~~~

## MAIL-4 · Campaign domains

Створено DOCUMENTS, DEBT_NOTICE і GENERAL domains; authoring, GENERAL registry/import/sender/attachments/preview та DEBT parser/normalization/matching/snapshot/campaign/preview.

~~~text
v13 campaign_draft_builder
v14 multi_campaign_foundation_and_general_contacts
v15 general_groups_and_tags
v16 general_contact_csv_xlsx_import
v17 general_campaign_type
v18 general_sender_profiles
v19 general_campaign_attachments
v20 debt_client_matching_reconciliation
v21 debt_immutable_import_snapshots
v22 debt_notice_campaign
v23 debt_template_attachments_preview
~~~

## MAIL-5 · Preflight & immutable dispatch

~~~text
Foundation
→ Recipient Resolution
→ Attachment Resolution
→ Eligibility
→ Immutable Dispatch Snapshot
→ Final Handoff
~~~

~~~text
v24 preflight_foundation
v25 preflight_recipient_resolution
v26 preflight_attachment_resolution
v27 preflight_eligibility_verdict
v28 immutable_dispatch_snapshot
~~~

Mutable campaign state не є send payload.

## MAIL-6 · SMTP / MIME transport

SMTP module/connectivity, session observability, MIME composition, Mailpit, controlled real SMTP і Message-ID domain.

~~~text
v29 smtp_profiles_and_connectivity
v30 smtp_session_observability
v31 smtp_real_transport_security_evidence
v32 smtp_message_id_domain_setting
~~~

~~~text
final DATA 250 = SMTP ACCEPTED
SMTP ACCEPTED != DELIVERED
~~~

## MAIL-7 · Persistent Queue

Persistent batching/send queue та cooperative cancellation.

~~~text
v33 persistent_send_queue_batching
v34 send_queue_cooperative_cancellation
~~~

## MAIL-8 · Attempt safety, retry, idempotency

Immutable SendAttempt lineage, failure classification, DELIVERY_UNKNOWN review, retry policy та duplicate prevention.

~~~text
v35 smtp_attempt_state_foundation
v36 delivery_unknown_operator_review
v37 smtp_retry_policy_engine
v38 send_idempotency_duplicate_prevention
~~~

## MAIL-9 · Delivery, DSN, History & intelligence

Delivery history, RFC DSN, correlation, projection, Catch-up, Controlled Resend, History intelligence, monthly coverage, multi-recipient identities та activity/churn signals.

~~~text
v39 delivery_history_foundation
v40 dsn_ingestion_message_correlation
v41 documents_catchup_delta_dispatch
v42 catchup_query_indexing_planner_hardening
v43 bounced_recipient_controlled_resend
~~~

Later identity-aware expansion:

~~~text
v49 multi_recipient_identity_foundation
v50 immutable_dispatch_delivery_identity
v51 identity_aware_queue_smtp_sidecar
v52 identity_retry_dsn_history_sidecars
~~~

MAIL-9.6d adds migration-free **Late Attachment Catch-up Intelligence** for monthly DOCUMENTS: immutable primary missing-PDF evidence, `LATE_ATTACHMENT_READY`, duplicate-safe legacy + identity-aware guards, read-only CSV/XLSX missing-at-primary export, and explicit DRAFT-only catch-up creation through the normal MAIL-5 path.

Legacy evidence was retained rather than rewritten.

## MAIL-10 · Diagnostic Center

Central read-only subsystem health, incident/history views and diagnostic export.

~~~text
v44 diagnostic_snapshot_history_incident_timeline
~~~

Diagnostics do not become an automatic repair engine.

## MAIL-11 · Inbound mailbox / DSN operations

IMAP profile, secure credential reference, connection test, read-only scan, UID cursor, scheduler, DSN review/diagnostics, manual reconciliation і monitoring.

~~~text
v45 inbound_mailbox_profile_connection_test
v46 inbound_mailbox_scan_dsn_intake
v47 inbound_mailbox_automatic_scheduler
~~~

## MAIL-12 · Recovery & Data Safety

Managed backups, integrity/catalog health, controlled quarantine/lifecycle, restore drill, guarded restore та Recovery Readiness Gate.

Recovery evidence розміщене поза DB, яку може бути відновлено. Окремий business-schema version не додавався.

## MAIL-13 · Clients Workspace UX

Registry/quick view, cooperation status management, contacts UX, search/filter/data-quality evidence, duplicate diagnostics і reconciliation shortcuts.

~~~text
v48 client_cooperation_status_management
~~~

## MAIL-14 · Deterministic Spintax

Canonical deterministic template engine, fail-closed kill switch, Preview integration, immutable freeze/no reroll і runtime control UX.

Schema migration не потрібна.

## MAIL-15 · Structured Logging & Observability

Event taxonomy, redaction, SQLite event store, correlation, operations/spans, subsystem instrumentation, panic capture, emergency JSONL, retention/flood protection, System Log і async batching.

~~~text
v53 structured_application_event_store
~~~

Logging не замінює business state.

## MAIL-16 · Delivery History Export

CSV/XLSX evidence export, configurable columns, attachment filenames, snapshot-consistent query та output SHA-256 evidence.

MAIL-16 не змінює schema.

## Current baseline

~~~text
Core       0.16.9
Schema     v53
ABI        1
Migration  NONE
~~~
