# Logging & observability

MAIL-15 introduced a centralized structured logging subsystem. It is intentionally **fail-isolated from business state machines**.

## Package split

~~~text
internal/logging   → contracts, redaction, correlation, operations, async sink
internal/logstore  → SQLite persistence/query/retention
internal/emergencylog → append-only JSONL fallback before/without SQLite
system_log.go      → Wails read-only query/detail API
diagnostic_*       → aggregated subsystem health
~~~

## Event contract

Policy versions:

~~~text
mail.logging.event.v1
mail.logging.operation.v1
mail.logging.redaction.v1
mail.logging.security.v1
~~~

### Severity

~~~text
DEBUG
INFO
WARNING
ERROR
CRITICAL
~~~

### Status

~~~text
STARTED
SUCCESS
FAILED
BLOCKED
CANCELLED
SKIPPED
~~~

### Canonical subsystems

~~~text
CORE
STARTUP
SQLITE
WAILS
COMPANIES
CAMPAIGNS
TEMPLATE
ATTACHMENTS
PREFLIGHT
QUEUE
RETRY
SMTP
DELIVERY
DSN
INBOUND
HISTORY
COVERAGE
DIAGNOSTICS
RECOVERY
MODULES
SECURITY
~~~

## Durable tables

Schema v53:

~~~text
application_operations
application_events
~~~

These are purgeable technical observability records.

They are **not** authoritative Queue/Delivery/DSN/History/Recovery state.

## Event shape

Important fields include:

~~~text
event_id
operation_id
span_id
parent_span_id
occurred_at
sequence_no
duration_ms
severity
subsystem
code
stage
status
title/message
detail_json
correlation
environment
app_version
module_name/version
process_instance_id
redacted
event_fingerprint
~~~

## Correlation

Structured correlation keeps distinct identifiers rather than collapsing them:

~~~text
client_id
campaign_id
dispatch_snapshot_id
dispatch_recipient_id
dispatch_delivery_identity_id
queue_id
queue_item_id
send_attempt_id
transport_attempt_id
smtp_profile_id
smtp_session_id
delivery_record_id
delivery_identity_record_id
dsn_artifact_id
dsn_recipient_id
inbound_scan_id
recipient_contract
message_id
~~~

Important example:

~~~text
send_attempt_id       = durable DB attempt row
transport_attempt_id  = SMTP transport identity
~~~

These two concepts must remain separate.

## Operations and spans

A long operation can be represented as:

~~~text
StartOperation
  → events/spans
  → Finish
~~~

This gives a queryable technical timeline without moving business ownership into the logger.

## Validation

Before persistence, events validate:

- timestamp;
- severity;
- status;
- subsystem;
- event-code format;
- event-code → subsystem ownership;
- correlation shape;
- detail payload contract.

Unknown event codes are rejected.

## Representative event families

### Startup / SQLite

~~~text
STARTUP_STARTED
ENVIRONMENT_RESOLVED
DB_PATH_RESOLVED
STARTUP_READY
STARTUP_FAILED
SQLITE_OPEN_STARTED
SQLITE_OPENED
SQLITE_SCHEMA_VALIDATED
SQLITE_MIGRATION_*
~~~

### Queue / Retry

~~~text
QUEUE_CREATED
QUEUE_STARTED
QUEUE_PAUSED
QUEUE_RESUMED
QUEUE_CANCEL_REQUESTED
QUEUE_COMPLETED
QUEUE_ITEM_STARTED
QUEUE_ITEM_STATE_CHANGED
RETRY_SCHEDULED
RETRY_STARTED
RETRY_EXHAUSTED
RETRY_BLOCKED
~~~

### SMTP

~~~text
SMTP_MESSAGE_PREPARED
SMTP_CONNECTED
SMTP_TLS_ESTABLISHED
SMTP_AUTH_SUCCEEDED
SMTP_ENVELOPE_ACCEPTED
SMTP_DATA_TRANSMITTED
SMTP_MESSAGE_ACCEPTED
SMTP_*_FAILED
~~~

### History export

~~~text
HISTORY_EXPORT_STARTED
HISTORY_EXPORT_COMPLETED
HISTORY_EXPORT_FAILED
~~~

### Recovery

~~~text
BACKUP_CREATED
BACKUP_VALIDATION_FAILED
CATALOG_ORPHAN_FOUND
CATALOG_BLOCKED
ARTIFACT_QUARANTINED
RESTORE_DRILL_*
RECOVERY_READINESS_BLOCKED
~~~

## Redaction boundary

Logging details are sanitized before durable persistence.

Do not put secrets into:

- event title;
- message;
- detail JSON;
- path fields;
- custom correlation values;
- module error payloads.

The fact that logging redacts data does not make it acceptable to intentionally emit secrets.

## Async logging

Policy:

~~~text
mail.logging.async_batch.v1
~~~

Defaults:

~~~text
queue capacity     2048
batch size         64
flush interval     25 ms
write timeout      5 s
~~~

The queue is bounded. On saturation, the caller drains the oldest batch rather than silently dropping an accepted record.

The async sink tracks health counters such as:

- current/max queue depth;
- enqueued/flushed records;
- flushed batches;
- overflow drains;
- event/operation failures;
- latest sink errors.

## Failure isolation

Structured logging sink failure must not change a successful/failed Queue/SMTP/domain transition into a different business result.

Observability is secondary evidence.

## Emergency fallback

Before SQLite is available, a terminal startup/logging failure can use sanitized append-only JSONL fallback.

Fallback is deliberately narrow. Raw business payloads and credentials must not be copied there.

## Retention

Policy:

~~~text
mail.logging.retention.v1
~~~

Default retention:

~~~text
DEBUG / INFO                45 days
WARNING / ERROR / CRITICAL 180 days
batch size                 250
max events/run            5000
max operations/run        2500
~~~

Retention deletes only technical logging tables.

It does **not**:

- VACUUM;
- delete Queue;
- delete Delivery;
- delete DSN/History;
- retry/resend;
- trigger recovery;
- alter schema.

## System Log API

Wails endpoints:

~~~text
QuerySystemLog
GetSystemLogEventDetail
~~~

System Log is a bounded read-only projection with server-side pagination.

## Diagnostic Center

Diagnostics aggregate canonical subsystem state and logging health.

A Diagnostic warning is a signal to inspect the owner domain, not a command to mutate state.

## Developer rule

For new instrumentation:

1. choose the canonical subsystem;
2. define/reuse an event code;
3. define a bounded detail contract;
4. provide correlation IDs that already exist;
5. never copy ownership into logging;
6. preserve redaction;
7. keep logging failure isolated;
8. add tests for sensitive-data leakage.
