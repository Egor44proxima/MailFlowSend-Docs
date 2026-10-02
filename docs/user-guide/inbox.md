# 14 · Вхідна пошта

**Контекст:** CONTROLLED

## Призначення

**Вхідна пошта** керує inbound IMAP profile, credential reference, connection test, mailbox scan evidence та scheduler.

Цей workspace може змінювати configuration і запускати scan, але accepted mailbox intake не повинен мутувати messages на сервері.

## Mailbox profile

Profile містить:

- name;
- IMAP host;
- port;
- TLS mode;
- username;
- folder;
- active/inactive state;
- revision.

## TLS modes

Accepted modes:

~~~text
IMPLICIT_TLS
STARTTLS
PLAIN_ONLY_IF_EXPLICITLY_ALLOWED_FOR_LOCAL_TEST
~~~

Plaintext mode дозволяється тільки для explicit local/loopback test boundary. TLS certificate/hostname verification не повинна вимикатися.

## Credentials

SQLite зберігає credential reference/status, але не raw password.

Secret зберігається через **Windows Credential Manager**. UI дозволяє set/delete credential через explicit actions.

## Connection Test

Connection test не виконує mailbox intake. Він проходить bounded stages:

~~~text
DNS
→ TCP
→ TLS / STARTTLS
→ greeting
→ CAPABILITY
→ AUTH
→ EXAMINE folder
→ logout
~~~

Результат має status/stage/latency/TLS/capability/error evidence.

Typical error classes включають DNS, TCP connect, TLS/certificate, STARTTLS unavailable, AUTH, folder access, protocol, timeout, config.

## Manual scan

Canonical scan читає mailbox evidence і передає DSN у accepted ingestion/correlation pipeline.

Scan evidence включає:

- mailbox identity / UIDVALIDITY;
- cursor state;
- searched/processed counts;
- ingested/duplicate DSN;
- non-DSN;
- oversized;
- parse/fetch failures;
- projection effects;
- scan items.

Mailbox scan не повинен STORE/EXPUNGE/MOVE messages як частину accepted read-only intake contract.

## Scheduler

Scheduler визначає **коли** запускати canonical scan.

Configuration:

- enabled;
- interval;
- max messages;
- next run;
- revision.

Run outcomes можуть включати COMPLETED, PARTIAL, FAILED, SKIPPED_BUSY, SKIPPED_INACTIVE, SKIPPED_CREDENTIAL_MISSING, INTERRUPTED.

Manual та automatic scans використовують shared overlap guard; parallel scans усередині одного process не повинні обходити canonical lock.

## Restart semantics

RUNNING scheduler evidence після crash/restart переводиться у interrupted/recoverable state згідно з accepted contract. Durable due time не губиться.

## Типовий сценарій налаштування

1. Створити profile.
2. Встановити TLS mode.
3. Зберегти credential.
4. Запустити Connection Test.
5. Переконатися в FOLDER_OK / accepted test result.
6. Запустити bounded manual scan.
7. Перевірити scan items і DSN projection.
8. Лише після цього enable scheduler.

## Safety boundary

- Password не зберігається plaintext у SQLite.
- PLAIN не дозволяється для ordinary remote production.
- Connection Test не читає/ingest messages.
- Scan не повинен змінювати mailbox message state.
- Scheduler не має окремого IMAP parser.
- Inbound evidence не є resend command.

## Пов'язані workspace

- **Моніторинг** — scan/scheduler alerts.
- **DSN огляд** — correlation result.
- **Доставка** — resulting projection.
- **Системний журнал** — technical inbound events.
