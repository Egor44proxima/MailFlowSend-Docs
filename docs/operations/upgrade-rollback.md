# Upgrade & Rollback Runbook

Upgrade MailFlowSend потрібно розглядати як **application + schema + recovery evidence operation**, а не як просту заміну EXE.

## Перед upgrade

Зафіксуйте:

~~~text
current application SHA
Core version
Schema version
ABI version
runtime mode
module versions
~~~

Потім:

1. дочекайтеся завершення активної Queue/SMTP/Inbound роботи;
2. перевірте Recovery Readiness;
3. створіть managed backup;
4. перевірте backup/catalog health;
5. за можливості виконайте restore drill;
6. збережіть hash production package, який замінюється.

## Не оновлювати під час unsafe activity

Не виконуйте production upgrade, якщо є активні або неоднозначні:

~~~text
Queue runner
SMTP attempt
Inbound scan
Recovery operation
pending restore
~~~

або Recovery Readiness має blocker.

## Application upgrade

Використовуйте package, який:

- зібраний із відомого source SHA;
- пройшов accepted Windows gate;
- містить сумісні runtime modules;
- має очікуваний Core/Schema/ABI baseline.

Не змішуйте DLL/worker artifacts з різних builds.

## Startup migration

SQLite migration виконується Core startup path.

Перед business activity Core перевіряє quick_check, migration ledger continuity, canonical migration names, unsupported future schema, startup invariants і recovery state.

Якщо migration/startup validation не пройшла, правильна поведінка — fail closed, а не ручне редагування DB.

## Після upgrade

Перевірте:

~~~text
Core READY
expected Schema
module health
Recovery readiness
Diagnostic Center
System Log
SMTP profile visibility
Inbound profile visibility
Queue idle/consistent
History readable
~~~

## Rollback: головне правило

### Якщо schema не змінилася

Binary/package rollback можливий лише коли release contract підтверджує backward compatibility.

Використовуйте узгоджений комплект:

~~~text
MailFlow.exe
mail.smtp.dll + worker
mail.debt.dll + worker
module.json files
~~~

### Якщо schema змінилася вперед

Не запускайте старішу application версію поверх новішої DB навмання.

Safe rollback path:

~~~text
stop application
→ Recovery preflight
→ trusted pre-upgrade backup
→ validate backup/catalog/source identity
→ explicit restore confirmation
→ restored DB startup validation
→ compatible application package
→ Core READY
~~~

Rollback schema виконується через restore accepted pre-upgrade database, а не ручний SQL downgrade.

## Чого не робити

Не використовуйте як rollback:

- ручне видалення migration ledger rows;
- ручний DROP COLUMN / DROP TABLE;
- копіювання старої DB поверх відкритої production DB;
- видалення WAL/SHM як repair;
- редагування backup manifests;
- підміну checksum;
- запуск старого EXE над future schema;
- змішування PROD і DEV DB.

## DEV перевірка перед production

~~~text
production snapshot
→ DEV environment
→ upgrade startup
→ migrations
→ smoke tests
→ acceptance
→ production change window
~~~

DEV має окремі DB та credential namespaces і блокує real send.

## Decision table

| Ситуація | Дія |
|---|---|
| UI regression, schema unchanged, package compatible | rollback full application package |
| startup migration failed | inspect logs/recovery; do not edit DB manually |
| schema upgraded, new build unusable | restore trusted pre-upgrade backup + compatible old package |
| backup catalog BLOCKED | resolve/quarantine via Recovery workflow first |
| active Queue/SMTP/Inbound | wait/settle before restore |
| unknown DB integrity | run Recovery integrity checks before restore decision |

## Evidence after rollback

Зафіксуйте restored backup ID/hash, source identity, final schema, application package SHA, startup validation, Recovery Readiness і reason for rollback.
