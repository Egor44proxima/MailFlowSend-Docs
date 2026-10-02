# Future Roadmap · Portable, Linux & Docker

> **Статус:** PLANNED / NOT STARTED  
> **Зафіксовано:** 2026-10-02  
> **Application baseline на момент рішення:** Core 0.16.9 · Schema v53 · ABI 1

Ця сторінка є **історичним планом майбутнього розвитку**. Вона не означає, що описані нижче можливості вже реалізовані або accepted.

Мета — зберегти прийняті архітектурні рішення, порядок робіт і причини, щоб майбутня реалізація не починалася заново з повторного обговорення.

## Зафіксовані рішення

### 1. Portable замість installer

Для наступного production packaging обрано **Portable Production Package**, а не MSI/Setup як основний delivery model.

~~~text
MailFlowSend-x.y.z-windows-amd64/
├─ MailFlow.exe
├─ release-manifest.json
├─ SHA256SUMS.txt
├─ modules/
│  ├─ mail.smtp/
│  │  ├─ mail.smtp.dll
│  │  ├─ mail.smtp.worker.exe
│  │  └─ module.json
│  └─ mail.debt/
│     ├─ mail.debt.dll
│     ├─ mail.debt.worker.exe
│     └─ module.json
└─ runtime-created data/recovery/logging state
~~~

Runtime data не повинні зникати при оновленні application binaries.

### 2. Один source repository для Windows і Linux

Не створювати окремі форки MailFlowSend-Windows / MailFlowSend-Linux.

Ціль:

~~~text
one source tree
→ shared Core/business logic
→ platform adapters
→ Windows artifact
→ Linux artifact
~~~

### 3. Docker не є production GUI runtime

Docker планується для reproducible Linux build, CI, test environment, Mailpit/integration services, native Linux module build та acceptance harness.

Не планується використовувати Docker як основний спосіб запуску Wails desktop GUI через складність Wayland/X11, GTK/WebKit, D-Bus, desktop keyring, file dialogs і desktop integration.

### 4. Credentials залишаються OS-native

Secrets не повинні переноситися в SQLite, manifest або Docker image.

~~~text
Windows → Windows Credential Manager
Linux   → Secret Service / desktop keyring
~~~

Core зберігає тільки credential reference.

### 5. Business contracts мають залишитися спільними

Windows і Linux повинні використовувати однакові Core business rules, SQLite schema, Preflight, Dispatch, Queue, Retry, Delivery, DSN, History, Recovery semantics, Template engine і Logging contracts.

# MAIL-17 · Portable Production Packaging & Release Management

**Статус:** PLANNED

Мета: сформувати canonical portable production package для Windows до початку Linux-port.

## MAIL-17.1 · Portable Package Contract

Зафіксувати обов'язкові application artifacts, directory structure, runtime-created directories, заборонені files та package completeness validation.

Не включати:

~~~text
production DB
WAL / SHM
credentials
private recipient exports
diagnostic bundles
temporary files
development databases
~~~

## MAIL-17.2 · Release Manifest & Artifact Integrity

Додати release-manifest.json і SHA256SUMS.txt з product/release/platform/architecture/Core/Schema/ABI/source SHA/module versions/artifact hashes/build timestamp.

## MAIL-17.3 · Runtime Package Verification

Перевіряти MailFlow binary, module DLLs, workers, manifests, SHA-256, ABI та Core compatibility. Production send може бути fail-closed при package integrity failure.

## MAIL-17.4 · Portable Data Directory Contract

~~~text
PROGRAM: MailFlow.exe + modules + manifest
DATA:    data + recovery + logs + exports
~~~

Upgrade не має видаляти runtime data.

## MAIL-17.5 · Safe Portable Upgrade

~~~text
verify package
→ verify application idle/safe
→ recovery backup
→ stop application
→ replace program artifacts only
→ preserve data/recovery
→ start new version
→ schema validation/migration
→ module verification
→ Core READY
~~~

## MAIL-17.6 · Portable Rollback

Якщо schema не змінилася і compatibility дозволяє — rollback повного application package. Якщо schema перейшла вперед — trusted pre-upgrade backup → guarded restore → compatible previous application package → Core READY.

## MAIL-17.7 · Release ZIP Builder

~~~text
MailFlowSend-x.y.z-windows-amd64.zip
SHA256SUMS.txt
release-manifest.json
~~~

## MAIL-17.8 · GitHub Release Pipeline

Accepted source SHA → package → verify hashes → publish GitHub Release assets.

## MAIL-17.9 · Windows Runtime Acceptance & Closure

Acceptance: clean extraction, first startup, existing-data startup, upgrade, credential preservation, module verification, Recovery readiness, rollback drill і final package SHA evidence.

# MAIL-18 · Cross-Platform Foundation & Linux Port

**Статус:** PLANNED

Мета: запустити MailFlowSend на Linux без fork і без переписування Core.

На момент планування орієнтовно **80–90% application/business logic** придатне для повторного використання.

## MAIL-18.1 · Platform Boundary Audit

Відокремити DLL/SO, EXE/ELF worker, Windows Credential Manager/Secret Service, Win32/POSIX process launch та platform-specific file/open behavior.

## MAIL-18.2 · Cross-Platform Credential Store

~~~text
CredentialStore
├─ windows → Windows Credential Manager
└─ linux   → Secret Service / keyring
~~~

Secret не потрапляє в SQLite або logs; backend status visible in diagnostics.

## MAIL-18.3 · Cross-Platform ModuleHost

~~~text
native module
├─ Windows → .dll
└─ Linux   → .so
~~~

ABI 1 semantics мають залишитися незмінними там, де це можливо.

## MAIL-18.4 · Worker Process Abstraction

~~~text
Windows: mail.smtp.worker.exe / mail.debt.worker.exe
Linux:   mail.smtp.worker / mail.debt.worker
~~~

Process start/wait/cancel/timeout переходить за platform interface.

## MAIL-18.5 · Linux Native Modules

Створити mail.smtp.so та mail.debt.so з максимальним повторним використанням worker protocol і JSON contracts.

## MAIL-18.6 · Linux Desktop Runtime Integration

Перевірити Wails build, GTK/WebKit, file/folder dialogs, Wayland, X11, runtime paths, Unicode filenames та temporary files.

## MAIL-18.7 · Recovery / Logging / Runtime Path Parity

Перевірити Linux semantics для SQLite WAL, recovery directories, backup atomicity, file rename/replace, permissions, emergency JSONL, exports та lock/error behavior.

## MAIL-18.8 · Linux Portable Package

Початковий target: MailFlowSend-x.y.z-linux-amd64.tar.gz. Пізніше можливо AppImage або distro packages.

# MAIL-18.5 · Docker Build & Test Environment

**Статус:** PLANNED

Docker вводиться як infrastructure layer для Linux/cross-platform development.

Scope: Dockerfile, Dockerfile.dev, docker-compose.yml, .dockerignore, entrypoint/healthcheck та profiles dev/ci/build-linux.

### dev

Mailpit, integration helpers, test services.

### ci

Go, Node, Wails dependencies, GCC, tests, typecheck, vet.

### build-linux

Linux application build, .so modules, workers, portable package, hash/manifest generation.

### Docker non-goals

Не робити docker run MailFlowSend GUI основною production model. Не зберігати credentials у image/environment files. Не зберігати production SQLite усередині ephemeral container filesystem.

# MAIL-19 · Linux Runtime Acceptance & Cross-Platform Closure

**Статус:** PLANNED

Перший Linux target:

~~~text
Linux x86_64
Manjaro / Arch family
KDE Plasma
Wayland + X11 compatibility
~~~

Після accepted first platform: Ubuntu LTS / Debian; далі інші distributions за потреби.

Acceptance areas: first startup, schema migration, Clients/CSM, Documents, DOCUMENTS, DEBT_NOTICE, GENERAL, Preflight, Dispatch, SMTP, credentials, Queue concurrency, Retry, Delivery, DSN, Inbound IMAP, History/Analytics, Recovery, Logging, module lifecycle, shutdown/concurrency і package verification.

## Planned release artifacts

~~~text
MailFlowSend-x.y.z-windows-amd64.zip
MailFlowSend-x.y.z-linux-amd64.tar.gz
SHA256SUMS.txt
release-manifest.json
~~~

# Орієнтовна оцінка

Це planning estimate, не commitment.

~~~text
Linux proof-of-concept      3–5 робочих днів
Linux functional beta       10–15 робочих днів
Linux production parity     20–30 робочих днів
Linux + Docker together     ~23–32 робочі дні
Cross-platform closure      ~5–7 тижнів
~~~

Docker окремо оцінюється приблизно в 5–7 робочих днів, але при спільній реалізації з Linux-port значна частина роботи перекривається.

# Planned dependency order

~~~mermaid
flowchart TD
    A["Current accepted baseline<br/>Core 0.16.9 · Schema v53 · ABI 1"]
    B["MAIL-17<br/>Portable Production Packaging"]
    C["MAIL-18<br/>Cross-Platform Foundation"]
    D["MAIL-18.5<br/>Docker Build & Test"]
    E["MAIL-19<br/>Linux Runtime Acceptance"]
    F["Dual-platform releases"]
    G["Future self-update system"]
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
~~~

## Historical decision

На 2026-10-02 зафіксовано:

1. Portable package має пріоритет над installer.
2. Linux реалізується в тому самому MailFlowSend repository.
3. Docker використовується для build/test/CI/integration, а не як preferred desktop runtime.
4. Credentials залишаються в OS-native secure store.
5. Windows і Linux повинні зберігати одну business/schema architecture.
6. Linux target починається з Manjaro/Arch + KDE, потім розширюється.
7. Реалізація не починається до окремого explicit start/acceptance рішення.
