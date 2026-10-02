# Lifecycle: від кампанії до History

Основний outbound lifecycle складається з окремих domain stages. Кожен stage або готує immutable evidence, або читає вже зафіксований state.

~~~mermaid
flowchart LR
    R["Recipient sources
Clients / GENERAL registry"] --> CAM["Campaign Draft"]
    DOC["Documents / Debt / Attachments"] --> CAM
    TPL["Template + Spintax"] --> CAM

    CAM --> PF["Preflight
resolution + blockers"]
    PF -->|READY| SNAP["Immutable Dispatch Snapshot"]
    PF -->|BLOCKED| STOP["Operator fix / no send"]

    SNAP --> Q["Persistent Queue"]
    Q --> SMTP["SMTP attempt"]
    SMTP -->|accepted| ACC["SMTP ACCEPTED"]
    SMTP -->|retryable| RETRY["Retry policy"]
    RETRY --> Q
    SMTP -->|review required| REV["Review / controlled action"]

    ACC --> DEL["Delivery projection"]
    DEL --> HIST["Immutable History"]

    DSN["Inbound DSN evidence"] --> DEL
    OP["Operator evidence"] --> DEL

    HIST --> EXP["CSV / XLSX export"]
    HIST --> ANA["Analytics / Coverage / Activity"]
~~~

## Campaign / preflight

Campaign draft визначає scope, content та business type. Preflight перевіряє recipient resolution, attachment readiness та інші blockers. Відправка не повинна обходити preflight через frontend action.

## Immutable dispatch snapshot

Після freeze Queue/Retry/SMTP працюють із frozen payload. Зміна template, contact data або Spintax runtime preference не повинна reroll'ити вже створений dispatch.

## Queue та retry

Queue зберігає durable item state та attempt lineage. Retry policy — окремий механізм від **controlled resend**. Ambiguous transport outcome не можна автоматично інтерпретувати як safe resend.

## Delivery / History

SMTP submission evidence стає частиною Delivery projection, але не підтверджує recipient delivery. History залишається read-only evidence projection і може експортуватися без мутації Queue/Delivery/DSN.
