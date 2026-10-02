# Status & Error Reference

This page consolidates the statuses an operator most often needs to interpret.

## Preflight

Final recipient verdict:

~~~text
READY
WARNING
BLOCKED
EXCLUDED
~~~

Severity precedence:

~~~text
BLOCKED > WARNING > READY
~~~

Examples of recipient issues:

~~~text
client_inactive
client_stopped
primary_email_missing
multiple_primary_emails
recipient_email_invalid
additional_active_contacts
current_csm_missing
current_csm_inactive
current_csm_email_invalid

mailing_contact_unsubscribed
mailing_contact_inactive
mailing_contact_status_invalid
sender_profile_missing
sender_profile_inactive
sender_email_invalid
~~~

Attachment integrity:

~~~text
OK
MISSING
CHANGED
EMPTY
ERROR
~~~

A stale preflight chain is not repaired in place; create a new fresh chain after source correction.

## Queue

Job states:

~~~text
READY
RUNNING
PAUSE_REQUESTED
PAUSED
CANCEL_REQUESTED
CANCELLED
COMPLETED
COMPLETED_WITH_ISSUES
~~~

Item states:

~~~text
PENDING
SENDING
ACCEPTED
FAILED
REVIEW_REQUIRED
CANCELLED
~~~

Projected retry states may appear as:

~~~text
RETRY_WAIT
WAITING_RETRY
~~~

## Send Attempt

~~~text
CREATED
RUNNING
SMTP_ACCEPTED
FAILED_RETRYABLE
FAILED_PERMANENT
FAILED_UNCLASSIFIED
DELIVERY_UNKNOWN
~~~

Classification rules:

| Evidence | Attempt state |
|---|---|
| final SMTP 250 | SMTP_ACCEPTED |
| SMTP 4xx | FAILED_RETRYABLE |
| SMTP 5xx | FAILED_PERMANENT |
| pre-accept transport I/O failure | FAILED_RETRYABLE |
| deterministic config/policy guard | FAILED_PERMANENT |
| mixed/insufficient evidence | FAILED_UNCLASSIFIED |
| DATA may have reached relay but final answer unknown | DELIVERY_UNKNOWN |

## DELIVERY_UNKNOWN review

Allowed operator resolutions:

~~~text
KEEP_BLOCKED
CONFIRMED_ACCEPTED
CONFIRMED_NOT_ACCEPTED
~~~

A note is mandatory. Automatic retry stays blocked.

## Delivery

~~~text
UNCONFIRMED
DELIVERED
DELAYED
BOUNCED
UNKNOWN
NOT_APPLICABLE
~~~

Core invariant:

~~~text
SMTP_ACCEPTED != DELIVERED
UNCONFIRMED != FAILED
~~~

## Retry

Automatic retry is allowed only when:

~~~text
latest attempt = FAILED_RETRYABLE
AND retry budget remains
AND queue is not cancelled
~~~

Backoff policy mail.retry.v1:

| Retry | Delay |
|---:|---:|
| 1 | 1 minute |
| 2 | 5 minutes |
| 3 | 15 minutes |

Excluded from auto retry:

~~~text
SMTP_ACCEPTED
FAILED_PERMANENT
FAILED_UNCLASSIFIED
DELIVERY_UNKNOWN
CANCELLED
~~~

## DOCUMENTS Catch-up

~~~text
ALREADY_SENT
NEWLY_READY
STILL_MISSING
BLOCKED
REVIEW_REQUIRED
SOURCE_EXCLUDED
~~~

Only NEWLY_READY is auto-included into a newly created catch-up DRAFT.

A prior SMTP_ACCEPTED recipient is ALREADY_SENT even if later Delivery becomes BOUNCED; bounce requires Controlled Resend, not Catch-up.

## Controlled Bounce Resend

Review state:

~~~text
ACTION_REQUIRED
PREPARED
BLOCKED
~~~

Eligibility requires definitive:

~~~text
SMTP_ACCEPTED + BOUNCED
~~~

Preparing resend creates one new DRAFT only. It does not create preflight/dispatch/queue/SMTP work.

## DSN correlation

~~~text
CORRELATED
AMBIGUOUS
UNMATCHED
~~~

Never guess an ambiguous/unmatched target.

Manual reconciliation is allowed only through the explicit preview + confirmation path and does not rewrite the original automatic correlation evidence.

## Inbound mailbox connection

Statuses:

~~~text
CONNECTED
AUTHENTICATED
FOLDER_OK
FAILED
~~~

Stable connection errors:

~~~text
MAILBOX_DNS_FAILED
MAILBOX_TCP_CONNECT_FAILED
MAILBOX_TLS_HANDSHAKE_FAILED
MAILBOX_TLS_CERT_INVALID
MAILBOX_STARTTLS_UNAVAILABLE
MAILBOX_AUTH_FAILED
MAILBOX_FOLDER_NOT_FOUND
MAILBOX_FOLDER_ACCESS_DENIED
MAILBOX_PROTOCOL_ERROR
MAILBOX_TIMEOUT
MAILBOX_CONFIG_INVALID
~~~

## Inbound scan

Message outcomes:

~~~text
DSN_INGESTED
DSN_DUPLICATE
NON_DSN
SKIPPED_TOO_LARGE
PARSE_FAILED
INGEST_FAILED
~~~

Scan states:

~~~text
RUNNING
COMPLETED
PARTIAL
FAILED
INTERRUPTED
~~~

Scan errors:

~~~text
MAILBOX_SCAN_BUSY
MAILBOX_SEARCH_FAILED
MAILBOX_FETCH_FAILED
MAILBOX_MESSAGE_TOO_LARGE
MAILBOX_DSN_INGEST_FAILED
MAILBOX_DSN_PROJECTION_FAILED
~~~

## Inbound scheduler

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

## Spintax

When active Spintax syntax is present but effective switch is OFF:

~~~text
SPINTAX_FEATURE_DISABLED
~~~

This is blocking. Raw Spintax must not leak into frozen/send output.

## Core invariants

~~~text
SMTP ACCEPTED != DELIVERED
UNCONFIRMED != FAILED
BOUNCED != DORMANT
DORMANT != STOPPED
Coverage != Delivery
Retry != controlled resend
History is read-only evidence
legacy evidence is not rewritten
identity-aware evidence remains identity-aware
no auto-create clients
fuzzy matching advisory only
~~~
