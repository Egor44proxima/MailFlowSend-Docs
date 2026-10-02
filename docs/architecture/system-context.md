# Системний контекст

Ця схема показує operational boundaries MailFlowSend без прив'язки до конкретних production hostnames або credentials.

~~~mermaid
flowchart TB
    Operator[Оператор MailFlowSend]

    subgraph Desktop["MailFlowSend Desktop"]
        UI["Vue UI · 20 workspaces"]
        App["Wails App API"]
        Core["Go Core / coredb"]
        Logger["Structured Logging"]
        ModuleHost["ModuleHost · ABI 1"]
    end

    DB[("SQLite canonical DB")]
    Attach["Attachment / export filesystem"]
    Cred["Windows Credential Manager"]
    SMTP["SMTP relay"]
    IMAP["Inbound IMAP mailbox"]
    Native["Native runtime DLL modules"]

    Operator --> UI
    UI --> App
    App --> Core
    Core --> DB
    Core --> Attach
    Core --> Cred
    Core --> SMTP
    Core --> IMAP
    Core --> ModuleHost
    ModuleHost --> Native
    Core --> Logger
    Logger --> DB

    SMTP --> MailNet["Recipient mail infrastructure"]
    MailNet --> IMAP
~~~

## Важливі межі

**Vue не є source of truth.** Вона передає operator intent і відображає Core-owned state.

**SQLite є canonical persistence layer.** Queue, Delivery, DSN, History, Recovery та інші domain states мають власників і не повинні змінюватися через побічні UI/diagnostic операції.

**Credentials не зберігаються як відкритий secret у SQLite.** Для inbound mailbox accepted contract використовує Windows Credential Manager; SMTP credential storage також має залишатися за відповідною security boundary.

**Modules ізольовані ABI-контрактом.** Accepted architecture використовує стабільний C ABI для native DLL boundary; production feature modules не повинні без окремого safety design завантажувати незалежні Go runtimes у Wails host.

## Public documentation boundary

Схема навмисно не містить реальних production paths, server names, recipient addresses, Message-ID або credential references.
