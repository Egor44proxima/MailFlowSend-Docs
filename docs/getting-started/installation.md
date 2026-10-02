# Інсталяція та запуск

MailFlowSend — Windows desktop application на Go + Wails + Vue.

Поточний documented baseline:

~~~text
Core       0.16.9
Schema     v53
ABI        1
Go         1.25.x
Wails      2.15.0
Node       22.x
~~~

## Для оператора

У поточному source tree немає одного універсального production installer contract, який можна безпечно описати як canonical MSI/Setup flow.

Тому production installation повинна використовувати **затверджений зібраний package**, а не випадкове копіювання source/build artifacts.

Перед першим запуском production package:

1. переконайтеся, що package відповідає accepted application SHA;
2. перевірте runtime mode;
3. перевірте canonical data directory;
4. не підміняйте production DB копією DEV/TEST;
5. перевірте runtime modules;
6. після startup дочекайтеся Core READY;
7. перед real send перевірте SMTP profile/credential;
8. перед upgrade створіть recovery backup.

## Для розробника

### Prerequisites

Потрібні:

~~~text
Windows x64
Go 1.25.x
Node.js 22.x
npm
Wails 2.15.0
Git
~~~

Для native runtime modules також потрібен:

~~~text
Visual Studio Build Tools
Desktop development with C++
MSVC x64 toolchain / cl.exe
~~~

## Clean source checkout

~~~powershell
git clone <private MailFlowSend repository>
cd MailFlowSend
git status
~~~

Current acceptance gate навмисно вимагає tracked-clean checkout до і після запуску.

## Frontend dependencies

~~~powershell
cd frontend
npm ci
cd ..
~~~

Canonical acceptance runner використовує reproducible npm ci.

## DEV запуск

~~~bat
scripts\dev-mailflow.cmd
~~~

Скрипт встановлює:

~~~text
MAILFLOW_ENV=development
MAILFLOW_DB_PATH=.dev\data\mailflow-dev.sqlite3
MAILFLOW_DEV_ALLOW_INBOUND_SCHEDULER=0
~~~

DEV contract:

~~~text
Credentials  MailFlowSend/DEV/...
Real SMTP    BLOCKED
Retry        BLOCKED
Auto retry   OFF
Auto inbound OFF
~~~

## DEV snapshot production data

~~~bat
scripts\refresh-dev-db.cmd
~~~

Flow:

~~~text
PROD DB
→ consistent SQLite VACUUM INTO snapshot
→ DEV DB
~~~

Це one-way PROD → DEV. Скрипт не копіює DEV назад у PROD.

## Native modules

SMTP:

~~~bat
scripts\rebuild-smtp-msvc.cmd
~~~

Debt:

~~~bat
scripts\rebuild-debt-msvc.cmd
~~~

Native architecture:

~~~text
Wails/Go host
→ stable C ABI
→ native DLL
→ isolated Go worker EXE
~~~

## Current acceptance gate

CI-equivalent:

~~~powershell
./scripts/run-audit-current.ps1 -Profile CI
~~~

Full Windows acceptance:

~~~powershell
./scripts/run-audit-current.ps1 -Profile Windows
~~~

Windows profile додатково виконує full Go regression, CONC-1.13 Windows DLL runtime acceptance та Wails production build.

## Production build

Wails config:

~~~text
Application name  MailFlow
Output filename   MailFlow
Frontend build    npm run build
~~~

Go embeds frontend/dist у desktop executable. Тому frontend build повинен завершитися до production Wails build.

## Після запуску

Перевірте:

~~~text
Core status
Schema version
Runtime mode
Module health
Recovery readiness
SMTP / Inbound configuration
~~~

Не починайте real campaign send, якщо Core не READY або safety subsystem показує blocker.
