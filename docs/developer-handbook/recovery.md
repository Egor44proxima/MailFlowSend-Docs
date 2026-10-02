# Recovery architecture

`internal/recovery` owns filesystem-level recovery orchestration around the canonical SQLite database.

The design is evidence-first and fail-closed.

## Recovery root

For active DB path:

~~~text
<db-directory>/recovery/
~~~

Managed paths include:

~~~text
backups/
safety/
migration/
journal.jsonl
pending_restore.json
last_integrity.json
last_integrity_success.json
backup_automation.json
backup_scheduler_state.json
retirements/
quarantine/
intents/
tmp/
drills/
readiness_exports/
~~~

The exact runtime path depends on environment/database location.

## Source identity

Recovery derives a stable source identity from:

~~~text
normalized absolute DB path
+ runtime mode
~~~

This prevents a backup lifecycle record from being silently reused against a different DB/runtime identity.

## Main policies

Current recovery contracts include:

~~~text
backup automation
managed backup lifecycle
backup catalog health
backup catalog quarantine
restore drill
recovery readiness gate
~~~

Representative policy IDs:

~~~text
mail.recovery.restore_drill.v1
mail.recovery.readiness_gate.v1
~~~

## Backup automation defaults

~~~text
default interval          1440 min
min interval                15 min
max interval             10080 min

default managed limit       30
min managed limit            1
max managed limit          365

default busy defer           5 min
min busy defer               1 min
max busy defer              60 min
~~~

## Backup evidence

A managed backup is not just SQLite bytes.

Accepted evidence can include:

- backup manifest;
- SHA-256;
- size;
- source identity;
- runtime mode;
- operation ID;
- journal evidence;
- lifecycle state.

A file without trusted companion evidence can be classified as an unsafe catalog artifact.

## Catalog health

Catalog health checks relationships among:

- backup bytes;
- manifests;
- lifecycle sidecars;
- journal evidence;
- duplicate IDs/paths;
- source/runtime identity;
- checksums.

Result contains:

~~~text
HEALTHY / WARNING / BLOCKED style status
issues[]
remediation preview[]
automaticRepairAllowed
automaticDeleteAllowed
~~~

The accepted design does not silently “clean up” suspicious recovery evidence.

## Quarantine

Unsafe/orphan artifacts can be moved through a controlled quarantine flow:

~~~mermaid
flowchart LR
    I["Catalog issue"] --> P["Quarantine preflight"]
    P --> C["Explicit confirmation"]
    C --> Q["Move to quarantine"]
    Q --> R["Record hash/evidence"]
    R --> H["Re-run catalog health"]
~~~

Quarantine preserves evidence rather than deleting bytes.

## Backup lifecycle

Managed backups can have controlled lifecycle state such as:

~~~text
ACTIVE
RETIRED
~~~

Retirement/reactivation uses:

- preflight;
- operation token;
- confirmation phrase;
- identity/checksum validation;
- append-oriented evidence.

## Integrity

Recovery integrity checks may include:

~~~text
SQLite quick_check
integrity_check
foreign_key_check
migration ledger validation
startup/domain invariants
~~~

An integrity test is not an automatic repair function.

## Restore drill

A restore drill validates one backup in an isolated work path.

Report can include:

- backup SHA/size;
- source hash unchanged;
- source/final schema;
- migration applied or not;
- quick/integrity/foreign-key checks;
- startup validation;
- temporary DB cleanup;
- runtime mode/source identity;
- record hash.

A successful drill proves much more than “file exists”.

## Actual restore

Restore is guarded by a separate preflight/arm/confirmation sequence.

The design expects checks for:

- selected backup identity;
- backup validation;
- catalog health;
- current unsafe activity;
- pending restore;
- runtime/source identity;
- readiness blockers;
- explicit operator confirmation.

## Startup restore validation

If startup recovery restored a DB candidate, the application does not publish READY immediately.

It opens/validates the restored DB, runs startup invariants and then finalizes external recovery evidence.

If final recovery evidence cannot be made durable, startup remains fail-closed.

## Recovery Readiness Gate

The final readiness snapshot is read-only and derived from existing recovery/runtime evidence.

It can include:

- active DB checks;
- catalog status;
- backup availability/usability;
- matching restore drill evidence;
- pending restore state;
- Queue/SMTP/Inbound unsafe activity;
- recovery evidence chain status.

## Unsafe activity

Recovery coordinates with active operational domains.

A restore/backup action should not assume the database is quiescent merely because the UI looks idle.

## Journal/evidence rule

Recovery evidence is external to the DB being restored so restore operations do not destroy their own audit trail.

Journal/evidence consistency is therefore a separate readiness concern.

## Developer invariants

Do not introduce recovery code that:

- deletes unknown artifacts automatically;
- rewrites manifests to “make them match”;
- ignores checksum/source identity;
- restores over active unsafe operations;
- treats backup existence as usability;
- publishes Core READY before restored DB validation;
- performs hidden business-domain fixes during restore.
