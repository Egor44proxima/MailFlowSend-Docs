# Inbound / DSN flow

Inbound processing turns mailbox evidence into normalized DSN records and, only after accepted correlation, into Delivery projection updates.

## End-to-end flow

~~~mermaid
flowchart LR
    CFG["Inbound mailbox profile"] --> TEST["Connection Test"]
    CFG --> SCHED["Scheduler"]
    SCHED --> SCAN["Canonical mailbox scan"]
    MAN["Manual Scan"] --> SCAN

    SCAN --> IMAP["internal/inboundmailbox"]
    IMAP --> MIME["Fetched message"]
    MIME --> PARSE["internal/dsnparser"]
    PARSE --> ART["dsn_artifacts / reports"]
    ART --> CORR{"Correlation"}
    CORR -->|CORRELATED| PROJ["Delivery projection"]
    CORR -->|AMBIGUOUS| REVIEW1["review"]
    CORR -->|UNMATCHED| REVIEW2["review"]
    PROJ --> HIST["History"]
~~~

## Mailbox profile

Schema v45 introduced:

~~~text
inbound_mailbox_profiles
inbound_mailbox_profile_events
inbound_mailbox_connection_tests
~~~

Configuration includes host, port, TLS mode, username, folder, active state and revision.

Secret material is not stored as a plaintext DB password column.

## Credential boundary

Accepted reference format uses Windows Credential Manager semantics.

Runtime environment namespaces isolate credentials across PROD/DEV/TEST so development does not accidentally resolve production secrets.

## TLS modes

~~~text
IMPLICIT_TLS
STARTTLS
PLAIN_ONLY_IF_EXPLICITLY_ALLOWED_FOR_LOCAL_TEST
~~~

Remote plaintext is rejected outside explicit local-test policy.

TLS uses certificate-chain/hostname validation; `InsecureSkipVerify` is not an accepted bypass.

## Connection Test

Connection test validates connectivity without performing mailbox intake.

Sequence:

~~~text
DNS
→ TCP
→ TLS if implicit
→ greeting
→ CAPABILITY
→ STARTTLS when configured
→ CAPABILITY again
→ authentication
→ EXAMINE folder
→ best-effort LOGOUT
~~~

No normal intake SEARCH/FETCH mutation occurs as part of the connection test.

## Scan state

Schema v46 adds durable scan/cursor evidence:

~~~text
inbound_mailbox_scan_state
inbound_mailbox_scans
inbound_mailbox_scan_items
~~~

The scan tracks mailbox identity/UIDVALIDITY and a durable UID cursor.

A scan result records counts such as:

- searched;
- processed;
- DSN ingested;
- duplicate DSN;
- non-DSN;
- oversized;
- parse failures;
- fetch failures;
- projection effects.

## Scheduler

Schema v47 adds:

~~~text
inbound_mailbox_scan_schedules
inbound_mailbox_schedule_events
inbound_mailbox_schedule_runs
~~~

The scheduler decides **when** a canonical scan may run. It does not implement an independent IMAP reader.

Run outcomes include:

~~~text
RUNNING
COMPLETED
PARTIAL
FAILED
SKIPPED_BUSY
SKIPPED_INACTIVE
SKIPPED_CREDENTIAL_MISSING
INTERRUPTED
~~~

## Overlap control

Manual and scheduled scans share an application process lock. An automatic run that cannot acquire the scan boundary records a safe skip/defer outcome instead of launching parallel intake.

## Restart recovery

Startup recovers interrupted scheduler runs and scans before Core READY.

An interrupted `RUNNING` row is not silently treated as success.

## DSN parsing

`internal/dsnparser` parses delivery status evidence. Parsed artifacts are persisted in normalized tables:

~~~text
dsn_artifacts
dsn_recipient_reports
dsn_correlations
dsn_events
~~~

Identity-aware DSN correlation has a dedicated sidecar path:

~~~text
dsn_identity_correlations
~~~

## Correlation outcomes

~~~text
CORRELATED
AMBIGUOUS
UNMATCHED
~~~

Correlation is deliberately fail-closed.

### CORRELATED

Evidence is strong enough to link the DSN recipient report to a canonical send/delivery identity.

### AMBIGUOUS

Multiple plausible targets or conflicting evidence exist. No guessing.

### UNMATCHED

No accepted target can be established.

## Diagnostic correlation layers

The codebase contains dedicated diagnostics for:

- Message-ID correlation;
- transport-context time window;
- semantic conflicts between DSN action/status/diagnostic evidence;
- identity-aware correlation.

Diagnostics may explain why a record is unresolved, but do not invent a match.

## Manual reconciliation

MAIL-11.5 adds explicit operator reconciliation.

The reconciliation path is append-only and separately validated during startup. It is not a generic “edit correlation row” escape hatch.

## Delivery projection

After accepted DSN correlation:

~~~text
DSN evidence
→ SyncDSNDeliveryProjection
→ ValidateDSNDeliveryProjection
→ Delivery records/events
→ History
~~~

Startup performs both sync and validation before publishing READY.

## Monitoring

`GetInboundMonitoringAlerts` builds a read-only operational projection over:

- new UNMATCHED/AMBIGUOUS DSN;
- unresolved/stale backlog;
- scan/scheduler failures;
- overdue schedules;
- bounce-rate anomalies.

Monitoring never becomes the owner of DSN/Delivery state.

## Developer invariants

~~~text
Connection Test != mailbox scan
Scheduler != independent IMAP reader
DSN artifact != resend command
AMBIGUOUS != correlated
UNMATCHED != guessed identity
UNCONFIRMED != FAILED
~~~

A new inbound feature should preserve read-only mailbox semantics unless a future contract explicitly introduces mailbox mutation.
