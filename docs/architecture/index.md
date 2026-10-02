# Архітектура MailFlowSend

MailFlowSend — Windows desktop application із чітким розподілом відповідальності між UI, Wails/App layer, Core, canonical SQLite state та зовнішніми transport/runtime boundaries.

~~~mermaid
flowchart LR
    U[Оператор] --> UI[Vue UI]
    UI --> W[Wails bindings / App actions]
    W --> C[Go Core / coredb]
    C --> DB[(SQLite canonical state)]
    C --> FS[Filesystem evidence]
    C --> MOD[Runtime modules]
    C --> SMTP[SMTP transport]
    C --> IMAP[Inbound IMAP]
    C --> WC[Windows Credential Manager]

    SMTP --> EXT[Mail infrastructure]
    IMAP --> EXT
~~~

## Ownership

| Layer | Відповідальність |
|---|---|
| Vue UI | presentation, navigation, operator intent |
| Wails/App | explicit application actions та boundary orchestration |
| Core / coredb | canonical rules, validation, transactions, projections |
| SQLite | durable canonical state та technical observability |
| Runtime modules | bounded ABI extension points |
| SMTP / IMAP | transport boundaries |
| Filesystem | attachments, exports, recovery artifacts та bounded sidecars |

UI не повинна реконструювати canonical business logic із DOM або локального cache.

## Основні схеми

- [Системний контекст](system-context.md) — компоненти та зовнішні boundaries.
- [Lifecycle від кампанії до History](send-lifecycle.md) — основний outbound flow.
- [Delivery / DSN evidence](delivery-evidence.md) — чому SMTP ACCEPTED не дорівнює DELIVERED.
- [Runtime та сховище](runtime-storage.md) — SQLite, filesystem, credentials і modules.
- [Evidence модель](evidence-model.md) — ownership та незмінні семантичні межі.
