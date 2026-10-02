# Структура вихідного коду

MailFlowSend is a Go/Wails monorepo: desktop host, frontend, Core packages, native modules, worker executables, smoke tools and acceptance scripts live in one application repository.

## Root layout

~~~text
MailFlowSend/
├─ main.go
├─ app.go
├─ app_*.go
├─ diagnostic_*.go
├─ history_export*.go
├─ system_log.go
├─ frontend/
├─ internal/
├─ native/
├─ cmd/
├─ scripts/
├─ docs/
├─ go.mod
└─ wails.json
~~~

## Desktop host

### `main.go`

Creates the Wails application, embeds `frontend/dist`, and binds a single `*App` instance.

Important lifecycle callbacks:

~~~text
OnStartup  → app.startupWithPanicCapture
OnDomReady → app.domReadyWithPanicCapture
OnShutdown → app.shutdownWithPanicCapture
~~~

### `app.go`

Application root object and bootstrap orchestration.

`App` owns:

- application cancellation root;
- managed background goroutines;
- ModuleHost registry;
- CoreDB handle;
- Recovery manager;
- runtime environment config;
- StructuredLogger;
- readiness/startup diagnostics;
- Queue execution state;
- inbound scan/scheduler state;
- template-control state.

### Root façade/support files

Representative ownership:

| File family | Responsibility |
|---|---|
| `app_queue_facade.go` | Queue-facing Wails API |
| `app_retry_scheduler*.go` | automatic retry scheduler and visibility |
| `app_recovery*.go` | Recovery façade + backup scheduler |
| `app_logging_mail15_*.go` | application instrumentation |
| `diagnostic_*.go` | Diagnostic Center/read models/export |
| `history_export*.go` | History CSV/XLSX export |
| `system_log.go` | System Log query/detail API |
| `attachment_availability_actions.go` | bounded attachment availability operations |

## `frontend/`

~~~text
frontend/
├─ src/
│  ├─ App.vue
│  ├─ ClientsRegistryPanel.vue
│  ├─ ClientQuickView.vue
│  ├─ ClientMonthMatrixPanel.vue
│  ├─ DeliveryIntelligencePanel.vue
│  ├─ DSNOperationsPanel.vue
│  ├─ InboundMailboxPanel.vue
│  ├─ InboundMonitoringPanel.vue
│  ├─ RecoveryPanel.vue
│  ├─ SystemLogPanel.vue
│  ├─ WorkspaceStatePanel.vue
│  ├─ async/
│  └─ workspaces/
└─ wailsjs/
   └─ go/main/App.d.ts
~~~

Frontend stack:

~~~text
Vue 3.5
TypeScript 5.9
Vite 7
Tailwind CSS 4
~~~

`frontend/wailsjs/go/main/App.d.ts` is the generated typed surface for Wails-bound Go methods.

## `internal/` packages

Current source contains **24 internal package directories**.

| Package | Responsibility |
|---|---|
| `attachmentindex` | filesystem attachment batch indexing |
| `clientsearch` | client candidate/search helpers |
| `clientsemantics` | parsed client display/cooperation/note semantics |
| `coredb` | canonical domain persistence, migrations, Queue/Delivery/DSN/etc. |
| `debtparser` | CSV/XLSX debt parsing and normalization |
| `dsnparser` | DSN MIME/status parsing |
| `emergencylog` | emergency append-only JSONL fallback |
| `generalimport` | GENERAL contact import reader |
| `inboundmailbox` | IMAP profile validation/probe/scan and credential boundary |
| `legacyimport` | legacy client/import migration path |
| `logging` | structured logging contracts/logger/redaction/correlation |
| `logstore` | SQLite technical event/operation persistence/query/retention |
| `mailtransport` | SMTP contract, MIME composition, TLS/auth/send |
| `matchengine` | attachment/client matching engine |
| `moduleabi` | Core/ABI manifest contracts |
| `modulehost` | native module discovery/load/execute/health |
| `orphanclass` | orphan attachment classification |
| `recovery` | backup/catalog/drill/restore/readiness manager |
| `runtimeenv` | PROD/DEV/TEST isolation and runtime guards |
| `smtpcredential` | SMTP credential store/resolver |
| `templatecontrol` | persisted Spintax operator control |
| `templateengine` | parser/validator/deterministic renderer |
| `wincred` | Windows Credential Manager wrapper |
| `wininterop` | Windows interop helpers |

### Why `coredb` is large

`internal/coredb` is intentionally the central durable business layer. It contains domain slices rather than separate database services:

~~~text
clients / contacts / ownership
attachments / matching / reconciliation
campaigns / mailing / debt
preflight / dispatch
SMTP session evidence
Queue / attempts / retry
Delivery / History
DSN / inbound scheduler state
Coverage / client-month signals
Recovery DB-side checks
structured logging migration
~~~

This means architectural separation is primarily by **file/domain contract inside one package**, while transaction ownership remains close to the SQLite connection.

## `native/`

Native ABI modules:

~~~text
native/
├─ smtp/
│  ├─ module.c
│  └─ module.json
├─ debt/
│  ├─ module.c
│  └─ module.json
└─ dummy/
~~~

The native layer is deliberately small. Feature logic that needs Go libraries runs in isolated worker executables rather than embedding a second Go runtime into the Wails process.

## `cmd/`

Contains:

- worker executables such as `smtp-worker` and `debt-parser-worker`;
- fixture generators;
- smoke/acceptance utilities;
- targeted runtime evidence tools;
- migration/recovery preflight tools.

This directory is part of the engineering test/support surface, not the operator UI.

## `scripts/`

Build, verify, acceptance and current-gate scripts live here. The repository uses stage-specific scripts plus a canonical current audit runner for clean-checkout validation.

## Source ownership rule

When adding a feature, prefer the narrowest owner:

~~~text
UI-only behavior              → frontend/src
desktop/Wails orchestration   → root app_*.go
durable domain rule           → internal/coredb
pure parsing/transport logic  → dedicated internal package
native ABI bridge             → internal/modulehost + native/*
acceptance utility            → cmd + scripts
~~~

Avoid moving canonical business rules into Vue or diagnostic code.
