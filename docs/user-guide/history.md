# 11 · Історія

**Контекст:** READ_ONLY

## Призначення

**Історія** — canonical read-only workspace для пошуку, групування та аналізу immutable send/delivery evidence. Тут оператор дивиться не поточний queue state, а вже зафіксований зв'язок між campaign, dispatch, recipient, SMTP attempts, delivery projection та attachment evidence.

History не запускає send, retry, resend або DSN reconciliation.

## Пошук і фільтри

Поточний History query підтримує:

- text search;
- SMTP submission status;
- delivery status;
- evidence source;
- campaign type;
- CSM;
- send-day date range.

Для exact record lookup використовуйте:

~~~text
#RecordID
~~~

Exact search корисний, коли Record ID отримано з Delivery, Analytics, support evidence або exported file.

## Grouped / Table view

History підтримує canonical grouping за send day / dispatch context і звичайний table view. Server-side pagination означає, що visible page — лише частина matching cohort.

## Detail panel

Для selected record detail пов'язує:

- Record ID;
- campaign;
- dispatch;
- queue / queue item;
- send/attempt lineage;
- recipient identity;
- SMTP status;
- delivery status/source;
- attachments;
- immutable evidence timeline.

Identity-aware records можуть мати negative public History ID. Це нормальна canonical representation; UI/export не повинні переписувати їх у legacy-looking IDs.

## Monthly DOCUMENTS Coverage

Read-only coverage panel відповідає на питання **кого покрив monthly DOCUMENTS flow і чому ні**.

Coverage states включають, залежно від evidence:

- SENT_PRIMARY;
- DEFERRED_MISSING_PDF;
- DEFERRED_MISSING_EMAIL;
- DEFERRED_STOPPED;
- NEWLY_READY;
- SENT_CATCHUP;
- STILL_MISSING;
- REVIEW_REQUIRED.

Ключова межа:

~~~text
Coverage != Delivery
~~~

Coverage не створює catch-up/send action із History.

## Матриця активності

History також містить client-month activity projection:

- 3 / 6 / 12 місяців або explicit range;
- search за client / ID / CSM;
- CSM filter;
- latest-month signal;
- cooperation filter;
- one row per canonical client;
- one cell per calendar month;
- DOC / Coverage / Delivery evidence drill-down.

Activity signals можуть включати NEW_ACTIVITY, ACTIVE_THIS_MONTH, RETURNED_AFTER_GAP, DORMANT_1M/2M/3M_PLUS, NO_DOCUMENT_THIS_MONTH, NO_HISTORY.

~~~text
BOUNCED != DORMANT
DORMANT != STOPPED
Document Activity != Coverage != Delivery
~~~

## Export CSV / XLSX

MAIL-16 додав export повного filtered cohort.

~~~text
same DB state + same normalized filters
→ History total == exported data row count
~~~

UI Page/PageSize **не** обмежують export.

Формати:

- CSV: UTF-8 BOM, comma, CRLF;
- XLSX: sheet History, literal IDs/timestamps, formula-safe cells;
- configurable selected columns;
- Attachment Files із frozen dispatch evidence;
- bounded custom XLSX widths;
- zero-result export = header only.

Safety bound:

~~~text
max rows = 100000
~~~

При перевищенні limit export fail-closed; silent truncation заборонений.

## Attachment Files

Attachment filename evidence береться з frozen dispatch records. Local source path не повинен потрапляти у public export column.

Для кількох файлів використовується видимий separator:

~~~text
file1.pdf | file2.pdf
~~~

## Fresh snapshot nuance

Export створює fresh DB read snapshot. Якщо UI давно не refresh'ився і в DB з'явилося нове legitimate evidence, export row count може відрізнятися від stale number на екрані до refresh.

## Safety boundary

- History = read-only.
- Export не створює Queue job.
- Export не запускає retry/resend.
- Export не змінює Delivery/DSN.
- Legacy evidence не переписується.
- Identity-aware evidence лишається identity-aware.

## Пов'язані workspace

- **Доставка** — current recipient delivery projection.
- **DSN огляд** — correlation evidence.
- **Аналітика** — aggregated delivery trends.
- **Клієнти** — current client state, який не переписує historical record.
