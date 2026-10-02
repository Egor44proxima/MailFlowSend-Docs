# Dependency map

This page maps package ownership rather than every Go import edge.

## Top-level dependency graph

~~~mermaid
flowchart TB
    Vue["frontend/src · Vue/TS"]
    Bind["Wails generated bindings"]
    App["package main · App façade"]

    Core["internal/coredb"]
    Runtime["internal/runtimeenv"]
    Logging["internal/logging"]
    LogStore["internal/logstore"]
    Recovery["internal/recovery"]
    ModuleHost["internal/modulehost"]
    ABI["internal/moduleabi"]
    Transport["internal/mailtransport"]
    Inbound["internal/inboundmailbox"]
    DSN["internal/dsnparser"]
    Template["internal/templateengine"]
    TemplateCtl["internal/templatecontrol"]
    Cred["smtpcredential / wincred"]
    Parsers["attachmentindex / debtparser / generalimport / legacyimport"]
    Match["matchengine / orphanclass / clientsearch / clientsemantics"]

    Vue --> Bind --> App

    App --> Core
    App --> Runtime
    App --> Logging
    App --> Recovery
    App --> ModuleHost
    App --> Transport
    App --> Inbound
    App --> Template
    App --> TemplateCtl

    Logging --> LogStore
    LogStore --> CoreDB[(SQLite SQL handle)]

    Core --> Template
    Core --> Match
    Core --> DSN
    Core --> Parsers

    ModuleHost --> ABI
    ModuleHost --> Native["native ABI DLLs"]
    Native --> Workers["isolated worker EXEs"]
    Workers --> Transport
    Workers --> DebtParser["debtparser"]

    Inbound --> Cred
    Transport --> Cred
    Recovery --> Runtime
~~~

## Ownership versus dependency

A package can depend on another package without taking ownership of its state.

Examples:

- `logging` may correlate `queue_id`, but Queue state remains owned by CoreDB.
- `diagnostic_center.go` reads Queue/SMTP/DSN counters, but does not own or repair those records.
- `recovery` validates/restores a database file, but individual domain semantics still belong to CoreDB after startup validation.
- `templateengine` is business-domain agnostic; campaign code supplies canonical recipient identity and variables.

## Domain dependency chains

### Client / attachment

~~~text
legacyimport/general intake
→ coredb clients/contacts/aliases
→ attachmentindex
→ matchengine
→ coredb matching/reconciliation
→ preflight
~~~

### Campaign / send

~~~text
clients or mailing_contacts
+ attachments/debt
+ templateengine
→ campaigns
→ preflight
→ dispatch snapshot
→ send queue
→ mailtransport
→ delivery/history
~~~

### Inbound delivery evidence

~~~text
inboundmailbox
→ dsnparser
→ coredb DSN correlation
→ Delivery projection
→ History
→ Analytics/Monitoring
~~~

### Observability

~~~text
domain operation
→ internal/logging
→ internal/logstore
→ application_events / application_operations
→ System Log / Diagnostic Center
~~~

### Recovery

~~~text
runtimeenv
+ active DB path
→ recovery.Manager
→ filesystem recovery root
→ backup validation/catalog/readiness
→ guarded restore
→ Core startup validation
~~~

## Circular-dependency avoidance

Important design boundaries that prevent architectural cycles:

- frontend does not import Core packages;
- internal packages do not import package `main`;
- Wails-specific runtime APIs stay in package `main`;
- native C modules do not receive Go interfaces;
- worker EXEs import pure internal packages, not Vue/Wails;
- Core business ownership does not depend on System Log UI.

## Adding a new package

Create a new internal package when logic is:

- pure enough to test independently;
- reusable by a worker/host without Wails;
- security-sensitive enough to deserve a narrow API;
- parser/transport/algorithmic rather than durable DB orchestration.

Keep it inside `coredb` when the behavior is transaction-heavy and tightly coupled to canonical SQLite domain invariants.
