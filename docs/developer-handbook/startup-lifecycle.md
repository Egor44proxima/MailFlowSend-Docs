# Startup & shutdown lifecycle

Startup is explicitly staged so the frontend can observe readiness without blocking Wails lifecycle callbacks.

## High-level flow

~~~mermaid
sequenceDiagram
    participant W as Wails
    participant A as App
    participant M as ModuleHost
    participant R as Recovery
    participant DB as CoreDB
    participant L as Logger
    participant S as Schedulers

    W->>A: OnStartup
    A->>A: ensureCoreInitialization()
    A-->>W: return quickly
    A->>M: discover modules
    A->>A: resolve runtime + DB path
    A->>R: PrepareStartup
    A->>DB: Open()
    DB->>DB: quick_check + migration/invariants
    A->>L: attach SQLite logging
    A->>DB: recover schedulers/queues
    A->>DB: sync + validate Delivery/DSN
    A->>R: finalize restore evidence if needed
    A->>A: publish READY
    A->>S: start retry/inbound/backup/log retention
~~~

## Why startup is asynchronous

`startup()` stays lightweight. Heavy SQLite recovery/validation runs in a background goroutine launched by `ensureCoreInitialization()`.

Reason: Wails/WebView lifecycle should not be blocked by long DB work, and the frontend must be able to poll `GetCoreStatus()` / diagnostics while initialization is in progress.

`coreInitOnce` prevents duplicate initialization from `OnStartup` and `OnDomReady`.

## Readiness states

~~~text
INITIALIZING
READY
FAILED
~~~

The application tracks both overall readiness and the exact current stage.

## Startup stages

Current bootstrap in `app.go` includes:

~~~text
CREATED
MODULE_REGISTRY
RUNTIME_ENV_GUARD
RECOVERY_PREFLIGHT
OPENING_DATABASE
RECOVERING_INBOUND_MAILBOX_SCHEDULER
RECOVERING_INBOUND_MAILBOX_SCANS
RECOVERING_SEND_QUEUES
SYNCING_DELIVERY_HISTORY
VALIDATING_DELIVERY_HISTORY
VALIDATING_DSN_INGESTION
VALIDATING_DSN_MANUAL_RECONCILIATION
SYNCING_DSN_DELIVERY_PROJECTION
VALIDATING_DSN_DELIVERY_PROJECTION
LOADING_CORE_STATUS
FINALIZING_RECOVERY_EVIDENCE   (only when required)
READY
~~~

A failure at a mandatory stage prevents publishing the DB handle as READY.

## CoreDB open sequence

`internal/coredb.Open()`:

1. resolves/creates DB directory;
2. opens SQLite;
3. limits pool to one open/idle connection;
4. sets `busy_timeout=5000`;
5. runs startup `quick_check`;
6. enables:
   - foreign keys;
   - WAL;
   - synchronous NORMAL;
7. validates/applies migrations;
8. recovers interrupted SMTP sessions;
9. recovers interrupted send attempts;
10. syncs DELIVERY_UNKNOWN reviews;
11. validates idempotency invariants;
12. syncs Delivery History;
13. validates History;
14. validates DSN ingestion;
15. validates DSN manual reconciliation.

Only then does `Open()` return a usable CoreDB.

## Migration ledger gate

Before migration/backfill mutation, Core validates `schema_migrations`:

- versions must be contiguous;
- names must match canonical migration names;
- future schema is rejected;
- application tables without a ledger are rejected;
- empty ledger + existing app tables is rejected.

This is a fail-closed protection against interrupted or unsupported schema state.

## Logging bootstrap

A StructuredLogger exists from `NewApp()` using a safe initial sink.

After SQLite successfully opens, persistent application logging attaches to the SQLite event store. Pre-SQLite terminal startup failures can activate sanitized emergency JSONL fallback.

Logging persistence failure is intentionally **not** allowed to become business-state ownership or silently alter Core domain transitions.

## Schedulers

Schedulers start only after Core READY and according to `runtimeenv.Config`.

Production defaults:

~~~text
AutoRetryScheduler    true
AutoInboundScheduler  true
~~~

Development/test restrict automatic work according to runtime safety policy.

Additional background components include recovery backup scheduling and log retention.

## Application cancellation root

`App` owns an application-level `context.Context` separate from the Wails/WebView callback context.

Managed background work should derive from this root so shutdown can:

1. seal new launches;
2. cancel the application root;
3. stop schedulers/workers;
4. wait for managed goroutines;
5. flush bounded logging;
6. close DB/module resources.

## Shutdown design principle

Shutdown must not trade “fast exit” for corrupt state.

Long-running transport/worker boundaries use cancellation or bounded settlement. Queue/SMTP/Inbound/Recovery state transitions must leave durable evidence that startup recovery can reconcile after interruption.

## Developer rule

A new mandatory startup check belongs before `publishCoreReady()`.

A new background service should:

- start only after READY;
- obey runtime mode;
- derive from the application cancellation root;
- have restart/interruption semantics;
- expose health/evidence;
- not block Wails startup callback.
