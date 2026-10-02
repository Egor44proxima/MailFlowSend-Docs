# Runtime security

MailFlowSend security is largely implemented as **runtime isolation + fail-closed boundaries**, not as one central security package.

## Runtime environments

`internal/runtimeenv` defines:

~~~text
PRODUCTION
DEVELOPMENT
TEST
INVALID
~~~

Aliases:

~~~text
PROD → PRODUCTION
DEV  → DEVELOPMENT
TESTING → TEST
~~~

An empty `MAILFLOW_ENV` resolves to PRODUCTION for compatibility with the accepted runtime.

## Environment policy

### PRODUCTION

~~~text
Credential namespace      MailFlowSend
Real email sending        allowed
Retry actions             allowed
Auto retry scheduler      enabled
Auto inbound scheduler    enabled
~~~

### DEVELOPMENT

~~~text
Credential namespace      MailFlowSend/DEV
Real email sending        blocked
Retry actions             blocked
Auto retry scheduler      disabled
Auto inbound scheduler    disabled by default
~~~

Development inbound scheduling can only be enabled through the explicit development override accepted by the runtime contract.

### TEST

~~~text
Credential namespace      MailFlowSend/TEST
Real email sending        blocked
Retry actions             blocked
Auto retry scheduler      disabled
Auto inbound scheduler    disabled
~~~

### INVALID

Fails closed:

~~~text
Real email sending        blocked
Retry actions             blocked
Schedulers                disabled
~~~

## Database path guard

Runtime mode and DB path are cross-checked.

Development/test refuse the canonical production DB path.

Production refuses development/test database identities such as:

~~~text
.dev/.../mailflow-dev.sqlite3
.test/.../mailflow-test.sqlite3
~~~

This prevents a development launch from silently operating on the production database and vice versa.

## Credential namespace isolation

Persisted DB records store credential references.

At resolution time, `runtimeenv.CredentialTarget` maps accepted base targets into environment-specific Windows Credential Manager namespaces.

Conceptually:

~~~text
PROD  MailFlowSend/<name>
DEV   MailFlowSend/DEV/<name>
TEST  MailFlowSend/TEST/<name>
~~~

This is a second boundary after DB-path isolation.

## SMTP credentials

SMTP profile records contain:

~~~text
credential_ref
~~~

not plaintext password storage.

`internal/smtpcredential` and the SMTP worker resolve secrets at runtime.

The transport request model explicitly rejects the idea of carrying a password as ordinary module JSON/audit data.

## Inbound credentials

Inbound mailbox profiles also use credential references backed by Windows Credential Manager.

Connection test / scan receives the secret through the accepted credential boundary, not by reading a SQLite password column.

## TLS

### SMTP

Supported transport modes:

~~~text
NONE
STARTTLS
TLS
~~~

Real production policy is enforced by profile validation/controlled-send boundaries.

TLS/certificate failures are explicit transport outcomes; they are not bypassed for convenience.

### IMAP

Supported inbound modes:

~~~text
IMPLICIT_TLS
STARTTLS
PLAIN_ONLY_IF_EXPLICITLY_ALLOWED_FOR_LOCAL_TEST
~~~

Remote plaintext is rejected outside local-test policy.

The accepted inbound contract does not use `InsecureSkipVerify` as a production escape hatch.

## Template feature control

Spintax feature flag:

~~~text
MAILFLOW_TEMPLATE_SPINTAX_ENABLED
~~~

Resolution precedence:

~~~text
explicit environment value
→ persisted operator preference
→ safe default OFF
~~~

If an environment value exists, the UI cannot override it.

Invalid environment values fail closed to the fallback and remain immutable from UI.

## Template control sidecar

Operator preference is stored beside the active runtime DB:

~~~text
mailflow-template-control.json
~~~

That makes normal PROD/DEV database separation also isolate template preference.

The sidecar is written through a temp/replace flow and uses restrictive file mode where supported.

## Spintax fail-closed rule

Plain templates remain usable when Spintax is disabled.

Active Spintax syntax is blocked:

~~~text
SPINTAX_FEATURE_DISABLED
~~~

Raw `{a|b}` content must never leak into a send because the renderer “gave up”.

## Stable freeze boundary

`templatecontrol.BeginStableOperation()` prevents operator preference changes during one immutable dispatch freeze.

This avoids rendering different recipients under different feature states inside the same freeze operation.

## Module loading security

ModuleHost validates:

- manifest path;
- DLL path stays inside manifest directory;
- ABI;
- Core version range;
- required exports;
- runtime identity;
- capabilities;
- response size.

Native responses are bounded by `moduleabi.MaxJSONBytes`.

## Worker process boundaries

SMTP/debt modules launch dedicated worker EXEs with bounded temp-file request/response exchange.

Benefits:

- Go feature logic is outside the Wails host process;
- worker timeout is enforceable;
- request/response size is bounded;
- temporary transport artifacts are cleaned up;
- native ABI remains simple.

## Structured logging security

The logging stack applies:

- typed event/detail contracts;
- redaction;
- correlation validation;
- bounded technical detail;
- emergency fallback sanitization;
- privacy-safe diagnostic export.

Do not rely on redaction as permission to emit secrets.

## Diagnostic export boundary

AI/support diagnostic bundle intentionally excludes classes of data such as:

- production DB;
- credentials/tokens;
- raw SMTP AUTH;
- message/template bodies;
- attachment bytes;
- raw emergency logging payloads where unsafe;
- other private runtime content.

## History export privacy

History export is operator evidence and can contain recipient/business information.

Public documentation should never publish a real History export without review/redaction.

Attachment export evidence uses filename-level frozen evidence rather than leaking local source paths.

## Recovery security

Recovery validates:

- source identity;
- runtime mode;
- SHA-256;
- manifest identity;
- migration ledger;
- catalog state;
- explicit preflight token;
- confirmation phrase;
- unsafe activity.

Unknown artifacts are quarantined/preserved rather than auto-deleted.

## Security design checklist for new code

Ask:

1. Which runtime modes may execute this?
2. Could DEV touch PROD DB or credentials?
3. Does this API accept a secret? If yes, should it instead accept a credential reference?
4. Can user-controlled path escape its allowed root?
5. Is the response bounded?
6. Does a failed/unknown outcome fail closed?
7. Could logging leak recipient/secret/message data?
8. Could retry create duplicate external side effects?
9. Does recovery/startup know how to reconcile interruption?
10. Are UI guards duplicated by backend validation?

## Never rely only on frontend

A disabled Vue button is usability, not security.

Every safety-critical mutation must validate the same guard in Go/Core before durable state or network side effects.
