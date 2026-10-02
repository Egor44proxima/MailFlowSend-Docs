# 13 · Моніторинг

**Контекст:** READ_ONLY

## Призначення

**Моніторинг** — read-only operational alert layer над inbound IMAP scans/scheduler, unresolved DSN correlation та real-transport bounce-rate anomalies.

Alerts derive from canonical evidence. Workspace не записує власний acknowledge/resolve state.

## Що контролюється

Summary включає:

- overall status;
- total alerts;
- CRITICAL / WARNING counts;
- new UNMATCHED DSN;
- new AMBIGUOUS DSN;
- unresolved DSN backlog;
- stale unresolved backlog;
- inbound scan issues;
- scheduler issues;
- overdue schedules;
- current accepted/bounced and bounce rate;
- previous baseline window для порівняння.

LOCAL_TEST excluded із bounce-rate rules.

## Alert categories

Поточні category families включають:

- DSN_UNMATCHED_NEW;
- DSN_AMBIGUOUS_NEW;
- DSN_UNRESOLVED_STALE;
- INBOUND_SCAN_ISSUE;
- INBOUND_SCHEDULER_ISSUE;
- INBOUND_SCHEDULER_OVERDUE;
- BOUNCE_RATE_SPIKE.

## Фільтри

Оператор може швидко переключати:

- ALL;
- CRITICAL;
- WARNING;
- DSN;
- INBOUND;
- BOUNCE.

## Navigation / triage

Alert може вести у canonical owner:

~~~text
DSN alert          → DSN огляд
Inbound alert      → Вхідна пошта
Bounce-rate spike  → Аналітика
~~~

Для inbound issue navigation може передати context: profile, source, reason, root cause, error code.

## Bounce-rate comparison

Monitoring порівнює current window із historical baseline. Це signal для investigation, а не доказ конкретної причини.

Не робіть automatic resend або profile change лише тому, що bounce rate виріс.

## Copy report

Можна скопіювати bounded monitoring report із summary та alerts. Використовуйте його як support evidence, а не як заміну canonical DSN/Inbound/Delivery detail.

## Типовий сценарій

1. Відкрити Monitoring.
2. Перевірити Overall, Critical, Warning.
3. Відфільтрувати problem family.
4. Відкрити target workspace.
5. Перевірити canonical evidence.
6. Виконувати state-changing action лише в owner workspace і лише якщо guard дозволяє.

## Safety boundary

- READ ONLY.
- Немає acknowledge/resolve mutation.
- Немає retry/resend.
- Немає mailbox configuration mutation.
- Немає DSN correlation rewrite.
- Alert ≠ root cause until evidence review.

## Пов'язані workspace

- **Вхідна пошта** — scan/scheduler/profile issue.
- **DSN огляд** — unresolved correlation.
- **Аналітика** — bounce-rate trend.
- **Системний журнал** — technical event detail.
