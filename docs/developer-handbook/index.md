# Developer Handbook

Цей розділ описує **внутрішню будову MailFlowSend для розробника**: source layout, startup lifecycle, CoreDB/SQLite, Wails API, transport workers, logging, recovery, runtime security і dependency boundaries.

## Source snapshot

Документація нижче звірена з application repository:

~~~text
Repository   Egor44proxima/MailFlowSend
Branch       main
Source SHA   0aae214a2e6324b09b4ad1b093fae174abc5ebb0

Core         0.16.9
Schema       v53
ABI          1
Go           1.25
Wails        2.15.0
Vue          3.5.x
SQLite       modernc.org/sqlite 1.46.x
~~~

## System shape

~~~mermaid
flowchart LR
    UI["Vue 3 frontend"]
    W["Wails generated binding"]
    A["main.App facade"]
    C["internal/coredb"]
    DB[("SQLite")]
    M["ModuleHost / ABI 1"]
    SMTP["mail.smtp.dll"]
    SMTPW["mail.smtp.worker.exe"]
    DEBT["mail.debt.dll"]
    DEBTW["mail.debt.worker.exe"]
    IMAP["internal/inboundmailbox"]
    LOG["internal/logging + logstore"]
    REC["internal/recovery"]

    UI --> W --> A
    A --> C --> DB
    A --> M
    M --> SMTP --> SMTPW
    M --> DEBT --> DEBTW
    A --> IMAP
    A --> LOG --> DB
    A --> REC
~~~

## Architectural principles

1. **UI is not the business source of truth.** Vue renders state and sends explicit operator intent through Wails.
2. **main.App is the application boundary.** Wails binds one `*App` instance; exported methods form the desktop API.
3. **CoreDB owns durable domain rules.** Most business persistence, invariants and projections live under `internal/coredb`.
4. **SQLite is canonical durable state.** Technical logging also uses SQLite, but does not take ownership of Queue/Delivery/DSN/History.
5. **Transport/runtime isolation is explicit.** Native DLLs use ABI 1; SMTP and debt parsing execute in worker processes.
6. **Fail-closed is preferred at unsafe boundaries.** Runtime environment, migration ledger, transport uncertainty, DSN ambiguity, recovery and template feature gates reject unsafe assumptions.
7. **Evidence is append-oriented.** Historical send/delivery evidence is not rewritten to look like a newer model.

## Handbook map

| Page | What it answers |
|---|---|
| [Source layout](source-layout.md) | Where code lives and which package owns what |
| [Startup lifecycle](startup-lifecycle.md) | How the process reaches Core READY and shuts down |
| [CoreDB / SQLite](coredb-schema.md) | DB opening, migrations, table families and invariants |
| [Wails API](wails-api.md) | How Vue calls Go and what the public desktop methods are |
| [Outbound mail](outbound-mail.md) | Campaign → Preflight → Dispatch → Queue → SMTP → Delivery |
| [Inbound / DSN](inbound-dsn.md) | IMAP scan → DSN parse/correlation → Delivery projection |
| [Modules & workers](modules-workers.md) | ABI 1, DLL discovery and isolated worker processes |
| [Logging](logging-observability.md) | Structured events, operations, correlation and System Log |
| [Recovery](recovery.md) | Backup, catalog, readiness, drills and restore |
| [Runtime security](runtime-security.md) | DEV/PROD isolation, credential boundaries and fail-closed guards |
| [Testing & CI](testing-ci.md) | Unit, smoke, Windows acceptance and clean-checkout CI |
| [Dependency map](dependency-map.md) | Package-level dependency and ownership graph |

## What this is not

This handbook intentionally does **not** publish:

- production credentials;
- private recipient records;
- raw Message-ID values from real sends;
- production database contents;
- diagnostic bundles;
- internal secrets or machine-specific paths.

It describes the implementation contract, not confidential runtime data.
