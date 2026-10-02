# Outbound mail flow

Outbound sending is a chain of explicit ownership boundaries. The system is designed so a frontend action cannot jump directly from mutable campaign content to uncontrolled SMTP.

## End-to-end flow

~~~mermaid
flowchart LR
    SRC["Recipient/source data"] --> CAM["Campaign draft"]
    CAM --> PF1["Preflight foundation"]
    PF1 --> PF2["Recipient resolution"]
    PF2 --> PF3["Attachment resolution"]
    PF3 --> PF4["Eligibility"]
    PF4 -->|READY| DISP["Immutable dispatch snapshot"]
    PF4 -->|BLOCKED| FIX["Operator fixes source state"]

    DISP --> Q["Persistent Queue"]
    Q --> ATT["Send attempt"]
    ATT --> MOD["mail.smtp module"]
    MOD --> WORKER["mail.smtp.worker.exe"]
    WORKER --> SMTP["SMTP server"]

    SMTP -->|2xx accepted| ACC["SMTP ACCEPTED"]
    SMTP -->|retryable failure| RETRY["Retry state"]
    SMTP -->|ambiguous| REVIEW["REVIEW_REQUIRED"]
    SMTP -->|final failure| FAIL["FAILED"]

    ACC --> DEL["Delivery projection"]
    DEL --> HIST["History"]
~~~

## 1. Campaign authoring

Campaign type determines source semantics:

~~~text
DOCUMENTS   → canonical clients / CSM / attachment batch
DEBT_NOTICE → immutable debt import/snapshot
GENERAL     → independent mailing_contacts registry
~~~

Campaign draft is mutable. It is **not** transport evidence.

## 2. Preflight

The accepted preflight pipeline is decomposed into durable stages:

1. foundation;
2. recipient resolution;
3. attachment resolution;
4. eligibility.

CoreDB persists explicit run/set/revision tables so downstream freeze can prove what it consumed.

Recipient blockers, missing attachments, invalid recipient state or stale source revisions fail closed according to the active campaign policy.

## 3. Template rendering

Canonical rendering is handled by `internal/templateengine`.

Order:

~~~text
raw template
→ spintax parse/validation + feature gate
→ deterministic selection
→ personalization
→ personalization validation
→ immutable rendered value
~~~

Contract:

~~~text
mail.template.render.v1
mail.template.spintax.v1
~~~

Deterministic seed includes campaign ID, canonical recipient identity, field and template hash.

Personalization values are opaque data and are not re-parsed as Spintax grammar.

## 4. Immutable dispatch snapshot

`CreateCampaignDispatchSnapshot` freezes send-relevant state.

Freeze separates mutable authoring/current data from execution:

~~~text
current client/contact/template state
          ↓ freeze
immutable dispatch evidence
          ↓
Queue / Retry / SMTP
~~~

Once frozen:

- template changes do not rewrite payload;
- contact changes do not rewrite payload;
- Spintax toggle does not reroll payload;
- retry consumes the same logical frozen evidence.

Identity-aware dispatch uses dedicated identity tables while preserving legacy dispatch evidence.

## 5. Persistent Queue

Wails façade:

~~~text
CreateSendQueue
StartSendQueue
PauseSendQueue
ResumeSendQueue
CancelSendQueue
RetrySendQueueItemNow
GetSendQueueDetail
ListSendQueues
ListSendAttempts
~~~

Queue creation performs no network I/O.

Queue owns durable execution state and attempt lineage.

## 6. Runtime mode guard

`internal/runtimeenv` controls real sending:

~~~text
PRODUCTION  → real send allowed, retry scheduler enabled
DEVELOPMENT → real send blocked, retry actions blocked
TEST        → real send blocked, retry actions blocked
~~~

Real SMTP scopes require an explicit controlled-send boundary.

## 7. SMTP module and worker

The runtime chain is:

~~~mermaid
flowchart LR
    App["Go/Wails host"] --> Host["ModuleHost"]
    Host --> DLL["mail.smtp.dll · native C ABI"]
    DLL -->|request temp file| Worker["mail.smtp.worker.exe"]
    Worker --> MT["internal/mailtransport"]
    MT --> Cred["smtpcredential resolver"]
    MT --> Net["SMTP network"]
    Worker -->|bounded response file| DLL
    DLL --> Host
~~~

The native DLL is a process bridge, not the SMTP implementation.

`mail.smtp.worker.exe` imports `internal/mailtransport` and resolves credentials inside the worker process.

## 8. SMTP contract

Current module identity:

~~~text
id       mail.smtp
version  0.5.0
ABI      1
policy   parallel
~~~

Capabilities:

~~~text
mail.transport.smtp
smtp.contract.describe
smtp.profile.validate
smtp.message.validate
smtp.message.compose
smtp.send
smtp.test_connection
smtp.protocol_trace
~~~

Transport contract:

~~~text
mail.transport.smtp.v1
mail.dispatch.handoff.v1
~~~

Profile scopes:

~~~text
LOCAL_TEST
CORPORATE_RELAY
PRODUCTION
~~~

Security modes:

~~~text
NONE
STARTTLS
TLS
~~~

Auth:

~~~text
NONE
PLAIN
LOGIN
~~~

## 9. Credential boundary

SMTP profile persisted in SQLite stores a **credential reference**, not the raw secret.

`mailtransport.SMTPProfile.Password` is explicitly rejected as an ABI/audit path. Secret resolution occurs outside the module JSON payload.

## 10. MIME composition

MIME composition happens inside the transport worker.

Raw RFC 5322/MIME bytes do **not** cross the ABI as response data. The result exposes privacy-safe metadata such as:

- message ID;
- media type;
- size;
- SHA-256;
- attachment counts/bytes;
- header metadata;
- line endings;
- TLS/auth/SMTP protocol metadata.

This avoids turning raw message content or attachment bytes into module JSON/audit evidence.

## 11. Submission semantics

Transport outcomes:

~~~text
NOT_ATTEMPTED
ACCEPTED
FAILED
UNKNOWN
~~~

Critical invariant:

~~~text
SMTP ACCEPTED != DELIVERED
~~~

A final SMTP 2xx proves relay acceptance, not recipient mailbox delivery.

## 12. Retry / ambiguous outcome

Retry policy is durable and separate from controlled resend.

Unknown/ambiguous transport state must not be converted into blind resend because the original message may actually have been accepted.

Queue review/idempotency protections exist specifically to reduce duplicate-delivery risk.

## 13. Delivery / History handoff

After send/attempt evidence is durable:

~~~text
Queue / SMTP evidence
→ Delivery projection
→ DSN/operator updates
→ History
~~~

History export is a read-only downstream capability and must not mutate Queue/Delivery/DSN.

## Developer invariants

When changing outbound code, preserve:

~~~text
mutable campaign != frozen dispatch
Queue ACCEPTED != DELIVERED
Retry != controlled resend
credential ref != credential secret
UNKNOWN != safe-to-resend
legacy evidence is not rewritten
identity-aware evidence remains identity-aware
~~~
