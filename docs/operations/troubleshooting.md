# Troubleshooting

Цей довідник починається з симптому і веде до owner subsystem. Він не рекомендує ручний repair canonical SQLite.

## Core не READY

Перевірте Diagnostic Center, System Log, SQLite health, migration ledger, Recovery Readiness і module health.

Не запускайте Queue/SMTP, поки Core startup не завершив canonical validation.

## SQLite / migration error

Типові причини:

- quick_check failure;
- unsupported future schema;
- migration ledger gap;
- migration name mismatch;
- application tables без ledger;
- recovery/pending-restore inconsistency.

Безпечна дія:

~~~text
stop mutation attempts
→ inspect Diagnostic/System Log
→ run Recovery integrity/readiness checks
→ managed backup/restore flow if needed
~~~

Не редагуйте schema_migrations вручну.

## Module FAILED / missing

Перевірте module directory, module.json, ABI 1, Core version compatibility, required DLL/worker files, runtime identity та ModuleHost diagnostics.

Для Windows source build:

~~~bat
scripts\rebuild-smtp-msvc.cmd
scripts\rebuild-debt-msvc.cmd
~~~

Не підміняйте тільки DLL із іншого build.

## SMTP connection FAILED

Перевірте exact stage:

~~~text
DNS
TCP
TLS / STARTTLS
EHLO
AUTH
MAIL FROM
RCPT TO
DATA
final reply
~~~

Для PRODUCTION потрібен TLS/STARTTLS. Credential зберігається у Windows Credential Manager.

## AUTH failed

Перевірте credential status, username, auth mode, TLS established і post-STARTTLS EHLO capabilities.

AUTH PLAIN/LOGIN не повинні виконуватися до TLS.

## SMTP UNKNOWN / DELIVERY_UNKNOWN

Не робіть blind resend.

~~~text
DATA may have reached relay
+ final acceptance unavailable
→ DELIVERY_UNKNOWN
→ operator review
~~~

Automatic retry заблокований через duplicate risk.

## Queue не рухається

Перевірте job state, Pause/Cancel request, latest attempt, retry wait, credentials, runtime mode, Queue runner ownership і System Log.

RETRY NOW працює лише для вже retry-safe scheduled item.

## FAILED_RETRYABLE

~~~text
retry #1 → 1 min
retry #2 → 5 min
retry #3 → 15 min
~~~

Після budget exhaustion потрібен operator review/fix.

## FAILED_PERMANENT

Потрібна зміна data/configuration. Не конвертуйте permanent failure у automatic retry.

## PDF missing / changed / empty

~~~text
Diagnostics
→ unavailable attachment issue
→ read-only probe
→ Clients/Documents/folder
→ explicit re-index if source fixed
~~~

Не змінюйте frozen Dispatch evidence.

## Matcher STALE

Причини:

~~~text
batch_reindexed
client_dataset_changed
batch_and_clients_changed
~~~

Запустіть matcher заново. Не переписуйте historical run.

## Preflight STALE

~~~text
fix canonical source
→ create new Preflight chain
→ verify FRESH
→ freeze new Dispatch
~~~

## Spintax blocked

~~~text
SPINTAX_FEATURE_DISABLED
~~~

Перевірте environment override, persisted preference та Settings indicator.

## Inbound Connection Test failed

Основні codes:

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

## Inbound Scan PARTIAL/FAILED

Перевірте cursor/UIDVALIDITY, fetch errors, oversized messages, parse failures, DSN ingestion і Delivery projection.

Raw RFC cap — 16 MiB.

## DSN AMBIGUOUS / UNMATCHED

Не прив'язуйте до найближчого Delivery record автоматично.

Перевірте Message-ID evidence, same-recipient history, transport context, time window і semantic conflict.

Якщо candidate eligible — Manual Reconciliation Preview → note → Confirm.

## BOUNCED

~~~text
BOUNCED
→ Non-delivery review
→ Controlled Resend
→ new DRAFT
→ normal Preflight/Dispatch/Queue
~~~

## DOCUMENTS client став READY пізніше

~~~text
NEWLY_READY
→ Catch-up DRAFT
~~~

Не resend і не retry.

## Recovery BLOCKED

Перевірте backup catalog, orphan artifacts, checksums, source identity, pending restore, restore drill і unsafe activity.

Unknown/orphan artifacts обробляються через controlled quarantine/release, а не delete.

## System Log warning/error

System Log — observability, не owner business state.

Використовуйте correlation IDs, щоб перейти до Queue/SMTP/DSN/Recovery owner evidence.

## Коли зупинити операцію

Не запускайте send/restore, якщо є:

~~~text
UNKNOWN transport outcome
Core not READY
Recovery BLOCKED
schema/integrity uncertainty
module ABI mismatch
unexplained preflight blocker
~~~
