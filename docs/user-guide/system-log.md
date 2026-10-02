# 17 · Системний журнал

**Контекст:** READ_ONLY

## Призначення

**Системний журнал** — read-only UI над structured application observability MAIL-15. Він використовує server-side filtering/pagination і не є інструментом repair.

Current UI policy: bounded query window до **31 days**.

## Пошук і фільтри

Доступні:

- text search: title / message / code / operation / Message-ID context;
- severity;
- subsystem;
- status;
- event code;
- environment;
- process ID;
- date/time from/to.

Час у таблиці відображається у local timezone; UTC доступний як technical evidence.

## Severity

~~~text
DEBUG
INFO
WARNING
ERROR
CRITICAL
~~~

## Event / operation status

~~~text
STARTED
SUCCESS
FAILED
BLOCKED
CANCELLED
SKIPPED
~~~

## Subsystems

Accepted taxonomy включає, зокрема:

~~~text
CORE STARTUP SQLITE WAILS COMPANIES CAMPAIGNS TEMPLATE
ATTACHMENTS PREFLIGHT QUEUE RETRY SMTP DELIVERY DSN INBOUND
HISTORY COVERAGE DIAGNOSTICS RECOVERY MODULES SECURITY
~~~

## Event list

Таблиця показує:

- local timestamp;
- severity;
- subsystem;
- code;
- status;
- event title/message;
- operation ID.

Summary counters допомагають швидко побачити distribution за severity.

## Detail panel

Для selected event можна переглянути structured detail і correlation context:

- event ID;
- UTC/local time;
- operation ID;
- span / parent span;
- correlation identifiers;
- sanitized detail payload;
- operation timeline, якщо доступна.

UI дозволяє copy correlation IDs і copy sanitized event JSON для support.

## Як читати журнал

Не починайте з ERROR text у відриві від business owner.

Рекомендований flow:

~~~text
event
→ subsystem
→ operation/correlation
→ canonical owner record
→ business evidence
→ supported action
~~~

Наприклад, SMTP ERROR не означає автоматично, що recipient failed назавжди; потрібні attempt classification і Delivery evidence.

## Redaction

Structured logging застосовує redaction/sanitization. Не намагайтеся обходити її, записуючи secrets у title, detail, correlation, path або custom metadata.

## Retention

Technical event retention може очищати старі logging records відповідно до policy, але не видаляє canonical Queue/Delivery/DSN/History evidence.

## Safety boundary

System Log не має:

- retry;
- resend;
- repair;
- delete business evidence;
- DSN reconciliation;
- restore actions.

Журнал пояснює **що сталося технічно**, але не володіє business state.

## Пов'язані workspace

- **Діагностика** — subsystem health.
- **Черга** — queue/retry owner.
- **Вхідна пошта** — inbound owner.
- **Відновлення** — recovery owner.
