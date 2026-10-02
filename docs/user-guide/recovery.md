# 18 · Відновлення

**Контекст:** CONTROLLED

## Призначення

**Відновлення** — operational workspace для backup, backup catalog health, Recovery Readiness Gate, restore drill і guarded restore lifecycle.

Це один із найбільш критичних workspace: destructive/restore actions виконуються лише через explicit preflight/confirmation contracts.

## Runtime context

UI показує runtime mode, Core/schema identity і recovery status.

У DEV acceptance real send заблокований, а restore drills виконуються на isolated/test boundaries. У PRODUCTION operator має дотримуватися stricter readiness і backup constraints.

## Recovery Readiness Gate

Read-only readiness snapshot агрегує gates, потрібні для безпечного recovery decision.

Оператор може:

- запустити readiness;
- export readiness JSON report;
- перевірити blockers;
- повторити gate після усунення issues.

Readiness report — evidence, а не сам restore.

## Integrity

Workspace підтримує bounded integrity checks. Deep/extended checks запускаються explicit action і можуть бути дорожчими за звичайний health refresh.

Integrity check не повинен “ремонтувати” DB тихо.

## Backup

Доступні controlled operations на кшталт:

- create backup;
- configure backup automation;
- evaluate backup schedule;
- inspect backup manifests/catalog;
- validate backup path.

Backup creation не дорівнює restore readiness: backup ще потрібно перевірити у catalog/integrity chain.

## Catalog health

Catalog audit виявляє orphan/inconsistent artifacts.

Accepted remediation використовує controlled lifecycle, наприклад:

~~~text
issue
→ quarantine preflight
→ explicit confirmation
→ quarantine
→ re-run catalog health
~~~

Quarantine не повинна переписувати manifests або historical recovery evidence.

Для released/quarantined artifact доступний окремий guarded release/reactivation flow, якщо contract дозволяє.

## Restore drill

Restore drill — isolated rehearsal, що перевіряє backup usability без заміни active production state.

Flow:

~~~text
choose backup
→ build restore drill preflight
→ review blockers
→ explicit confirmation
→ isolated drill
→ report
~~~

Successful drill є важливою readiness evidence, але не автоматично запускає production restore.

## Restore

Actual restore має окремий preflight і confirmation.

Перед підтвердженням перевіряйте:

- selected backup identity;
- integrity/catalog state;
- readiness blockers;
- active Queue/SMTP/Inbound operations;
- pending restore state;
- runtime mode;
- operator confirmation phrase/guard.

## Lifecycle

Backup artifacts можуть мати controlled lifecycle operations на кшталт RETIRE / REACTIVATE, які також проходять preflight та confirmation.

## Чого не робити вручну

Не використовуйте filesystem/SQLite manual edits як substitute recovery action:

- не видаляйте WAL/SHM “для ремонту”;
- не переписуйте manifest;
- не копіюйте DB поверх active runtime;
- не змінюйте recovery rows вручну;
- не запускайте restore через сторонній copy while app active.

## Safety boundary

Recovery actions не повинні переписувати immutable Queue/Delivery/DSN/History evidence довільним способом. Restore повертає consistent database state із validated backup, а не selectively edits domains.

## Пов'язані workspace

- **Діагностика** — readiness/health handoff.
- **Системний журнал** — recovery operation evidence.
- **Черга / Вхідна пошта** — active operation checks перед restore.
