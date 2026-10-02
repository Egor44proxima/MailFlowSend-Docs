# Inbound / DSN Runbook

Цей runbook описує production-safe setup і review flow для inbound DSN.

## 1. Створити Inbound Mailbox Profile

Відкрийте **Вхідна пошта**.

Profile зберігає connection metadata, але не password. Credential secret зберігається у Windows Credential Manager.

## 2. TLS mode

Supported:

~~~text
IMPLICIT_TLS
STARTTLS
PLAIN_ONLY_IF_EXPLICITLY_ALLOWED_FOR_LOCAL_TEST
~~~

Remote plaintext не дозволяється.

TLS certificate/hostname verification не обходиться через insecure mode.

## 3. Зберегти credential

Після profile save додайте credential через підтримуваний secure action.

SQLite не має password column. Після restart перевірте credential status.

## 4. Connection Test

Connection Test:

~~~text
DNS
→ TCP
→ TLS/STARTTLS
→ CAPABILITY
→ AUTH
→ EXAMINE folder
→ LOGOUT
~~~

Connection Test не читає mailbox messages і не запускає DSN ingestion.

Expected success progression:

~~~text
CONNECTED
AUTHENTICATED
FOLDER_OK
~~~

## 5. Manual Scan

Перший production scan запускайте small batch.

Canonical read-only mailbox flow:

~~~text
EXAMINE
→ UID SEARCH
→ RFC822.SIZE
→ BODY.PEEK[]
→ DSN ingest
→ Delivery projection
~~~

Mailbox mutation commands STORE/EXPUNGE/MOVE/DELETE не використовуються.

Default explicit scan: 50 messages. Hard batch limit: 250. Raw RFC cap: 16 MiB.

## 6. Scan outcomes

Per message:

~~~text
DSN_INGESTED
DSN_DUPLICATE
NON_DSN
SKIPPED_TOO_LARGE
PARSE_FAILED
INGEST_FAILED
~~~

Scan:

~~~text
COMPLETED
PARTIAL
FAILED
INTERRUPTED
~~~

Після першого scan перевірте scan history, processed UIDs, cursor, DSN artifacts, Delivery changes та те, що Queue/Retry не змінилися.

## 7. Scheduler

Scheduler викликає той самий canonical scan boundary.

Він не має окремого IMAP reader.

При enable система перевіряє profile exists, profile ACTIVE і credential present.

Automatic outcomes:

~~~text
COMPLETED
PARTIAL
FAILED
SKIPPED_BUSY
SKIPPED_INACTIVE
SKIPPED_CREDENTIAL_MISSING
INTERRUPTED
~~~

Manual і automatic scans не виконуються паралельно в одному process.

## 8. DSN review

Відкрийте **DSN огляд**.

Correlation:

~~~text
CORRELATED
AMBIGUOUS
UNMATCHED
~~~

CORRELATED може оновити Delivery projection.

AMBIGUOUS / UNMATCHED не повинні автоматично прив'язуватися до “найближчого” send.

## 9. Manual Reconciliation

Manual reconciliation дозволена тільки для unresolved DSN recipient через explicit two-step flow:

~~~text
Preview
→ inspect candidate
→ operator note
→ explicit Confirm
~~~

Preview перевіряє candidate context.

Accepted boundary включає same-recipient diagnostic evidence, eligible transport context, bounded 30-day diagnostic window, accepted PRODUCTION/CORPORATE_RELAY evidence та recipient email identity match.

LOCAL_TEST, stale, pre-accept або unsafe context fail closed.

### Immutable rule

Manual reconciliation не UPDATE-ить original automatic correlation row.

Вона додає append-only operator event, після чого Delivery projection sync виконується повторно.

Already auto-correlated DSN не можна override manual reconciliation.

## 10. Якщо Preview stale

~~~text
preview token mismatch
→ confirmation blocked
→ refresh diagnostics
→ preview again
~~~

Не обходьте stale preview.

## 11. Monitoring

**Моніторинг** показує operational alerts, зокрема new UNMATCHED/AMBIGUOUS DSN, stale backlog, scan/scheduler failures, credential missing, overdue scheduler і bounce spike.

Monitoring read-only і не виконує reconciliation.

## Incident checklist

- [ ] profile ACTIVE;
- [ ] credential present;
- [ ] Connection Test FOLDER_OK;
- [ ] scan cursor sane;
- [ ] no unexpected mailbox mutation;
- [ ] DSN artifact normalized;
- [ ] correlation reason reviewed;
- [ ] manual reconciliation only with eligible candidate;
- [ ] Queue/Retry unaffected by inbound scan;
- [ ] Delivery change has DSN/operator evidence.
