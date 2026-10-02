# Runtime та сховище

MailFlowSend використовує кілька storage boundaries із різною відповідальністю.

~~~mermaid
flowchart TB
    Core["Go Core"]

    subgraph SQLite["SQLite · canonical durable state"]
        Clients["Clients / Contacts / CSM"]
        Campaigns["Campaigns / Dispatch"]
        Queue["Queue / Attempts"]
        Delivery["Delivery / DSN / History"]
        Recovery["Recovery metadata"]
        Logs["application_events / operations"]
    end

    subgraph FS["Filesystem"]
        Attach["Attachment batches"]
        Export["History / Diagnostic exports"]
        Backup["Backup / recovery artifacts"]
        Sidecar["Bounded runtime sidecars"]
    end

    Cred["Windows Credential Manager"]
    Mods["Native DLL modules · ABI 1"]

    Core --> Clients
    Core --> Campaigns
    Core --> Queue
    Core --> Delivery
    Core --> Recovery
    Core --> Logs
    Core --> Attach
    Core --> Export
    Core --> Backup
    Core --> Sidecar
    Core --> Cred
    Core --> Mods
~~~

## SQLite

Поточний accepted baseline:

~~~text
Schema v53
~~~

SQLite містить canonical business state та structured technical observability. Logging tables не набувають ownership над Queue, Delivery, DSN, History або Recovery.

## Filesystem

Filesystem використовується для attachment source files, generated exports, backup/recovery artifacts та окремих bounded configuration sidecars.

History export пишеться через temp → finalize/rename → SHA-256 metadata. Export failure не повинен створювати success metadata або business-state mutation.

## Credentials

Secrets не повинні дублюватися у public documentation або diagnostic bundles. Inbound mailbox profile зберігає credential reference, а secret — у Windows Credential Manager.

## Runtime modules

Accepted ABI baseline:

~~~text
ABI 1
~~~

ModuleHost відповідає за discovery, ABI handshake, execution boundary, memory ownership та safe shutdown/unload.
