# Testing & CI

MailFlowSend uses several layers of evidence: unit tests, package regression tests, smoke utilities, static verifier chains, Windows runtime acceptance and clean-checkout CI.

## Canonical current runner

~~~text
scripts/run-audit-current.ps1
~~~

Profiles:

~~~text
-Profile CI
-Profile Windows
~~~

The runner requires a Git checkout and verifies tracked files are clean **before and after** the gate.

## Current baseline

~~~text
Core       0.16.9
Schema     v53
ABI        1
Migration  NONE
~~~

## Verifier manifest

`scripts/acceptance/manifest.json` is the active verifier-chain manifest.

### audit-static

15 current audit-fix verifiers:

~~~text
verify-audit-fix-1.mjs
...
verify-audit-fix-15.mjs
~~~

### accepted-continuity

Current accepted OPS / MAIL-UX continuity includes:

~~~text
OPS-ATT
OPS-DSN
OPS-INBOUND
OPS-CLEANUP
MAIL-15.20
MAIL-UX-1 ... MAIL-UX-8
~~~

### mail15-post20-continuity

One bounded continuity verifier protects accepted MAIL-15.21..28 behavior.

### mail16-current

Eight verifiers:

~~~text
MAIL-16.1
MAIL-16.2
MAIL-16.3
MAIL-16.4
MAIL-16.4a
MAIL-16.4b
MAIL-16.4c
MAIL-16.5
~~~

Historical root-marker replay is preserved for compatibility but is not active current evidence.

## Frontend gate

The current runner performs a clean install:

~~~text
npm ci
~~~

Then:

~~~text
npm run test:async
npm run test:lifecycle
node --test src/workspaces/queueWorkspaceModel.test.mjs
node --test src/workspaces/historyExportModel.test.mjs
npm run typecheck
npm run build
~~~

The build output `frontend/dist` must exist because Go embeds it into the Wails binary.

## Go gate

Common:

~~~text
go vet ./...
~~~

### CI profile

~~~text
go test ./... -count=1 -skip '^TestCONC113Runtime'
~~~

CI skips the test that requires locally built Windows runtime DLL artifacts.

### Windows profile

Requires real runtime module files and then executes:

~~~text
go test ./... -count=1
wails build
~~~

Windows profile supplies the module root for CONC-1.13 DLL runtime acceptance.

## Post-test verifier replay

The current static/continuity chains run again **after** frontend/Go tests.

This catches tests/build tools that accidentally mutate tracked acceptance evidence.

## Clean checkout invariant

Final marker requires:

~~~text
TRACKED CHECKOUT BEFORE GATE: CLEAN
TRACKED CHECKOUT AFTER GATE: CLEAN
~~~

Untracked build artifacts are not the tracked-code contract; modified tracked source/docs/scripts fail the gate.

## GitHub Actions

Current workflow:

~~~text
.github/workflows/audit-fix-11-clean-checkout.yml
~~~

Workflow name:

~~~text
MailFlow Current Clean Checkout
~~~

Triggers:

- push to `main`;
- push to `fix/**`;
- pull request;
- manual workflow dispatch.

Runner:

~~~text
windows-latest
timeout 45 min
~~~

Setup:

~~~text
actions/checkout
Go from go.mod
Node 22
npm cache
~~~

Execution:

~~~powershell
./scripts/run-audit-current.ps1 -Profile CI
~~~

## Smoke commands

`cmd/` contains many narrow smoke/fixture tools.

Examples:

~~~text
core-smoke
attachment-smoke
client-csm-transfer-smoke
campaign-draft-smoke
preflight-*-smoke
dispatch-snapshot-smoke
smtp-*-smoke
send-queue-smoke
delivery-history-smoke
dsn-*-smoke
inbound-mailbox-*-smoke
bounce-resend-smoke
mod0-smoke
~~~

These tools are useful for bounded contract evidence but do not replace the current gate.

## Worker tests

Isolated worker/process boundaries have their own tests:

- SMTP worker;
- debt parser worker;
- module-host native pointer/memory adversarial tests;
- concurrency/runtime cancellation tests.

## Concurrency acceptance

The source contains explicit CONC acceptance tests for:

- application cancellation root;
- managed goroutine lifecycle;
- scheduler lifecycle;
- worker cancellation;
- module execution policy;
- Queue activation;
- parallel SMTP runtime;
- shutdown stress;
- Windows DLL runtime.

This reflects a design principle: goroutine/process lifetime is part of correctness, not only performance.

## Acceptance workflow

Recommended feature lifecycle:

~~~text
design
→ implementation
→ targeted tests
→ FAST/current checks
→ DEV runtime evidence
→ fix
→ Windows acceptance
→ full current gate
→ closure docs/verifier
→ PR CI
→ merge
→ post-merge CI
~~~

## Exact SHA evidence

Runtime acceptance should identify the exact implementation SHA that was executed.

If closure docs/verifier are committed afterward, preserve both:

~~~text
accepted implementation SHA
closure SHA
merged main SHA
post-merge CI run
~~~

Do not imply runtime acceptance happened on a later documentation-only SHA unless it actually did.

## No fabricated markers

An automated verifier may prove static continuity, but it must not print a runtime/operator PASS marker that was never produced by a real run.

Historical acceptance text is evidence only when its origin is explicit.

## Adding tests for a feature

Minimum expectation:

- pure logic unit tests;
- CoreDB transaction/invariant tests for durable state;
- negative/fail-closed cases;
- restart/recovery tests for persistent async state;
- frontend async/state tests when UI behavior changes;
- security/redaction tests for sensitive paths;
- Windows runtime test when native DLL/worker behavior changes;
- current clean-checkout gate.

## Test DB rule

Acceptance fixtures should use isolated test/dev databases.

Do not point destructive/mutating tests at the canonical production DB.
