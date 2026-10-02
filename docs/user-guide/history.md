# Історія та експорт

**Історія** — read-only workspace для пошуку та аналізу immutable send/delivery evidence.

## Пошук та фільтри

History підтримує server-side filtering за submission/delivery status, evidence source, campaign type, CSM, датою та текстовим пошуком. Exact Record ID search підтримує форму:

~~~text
#RecordID
~~~

## Export

MAIL-16 додав portable evidence export:

- CSV;
- XLSX;
- configurable column selection;
- attachment filename evidence;
- bounded XLSX column widths.

Export використовує повний filtered cohort, а не лише поточну UI page.

~~~text
same DB state + same normalized filters
→ History total == exported data row count
~~~

Safety bound:

~~~text
max rows = 100000
~~~

Якщо cohort перевищує limit, export fail-closed; silent truncation заборонений.

CSV використовує UTF-8 BOM і CRLF. XLSX має sheet History, formula-safe cells та bounded custom widths. Zero-result export створює header-only evidence.

Export не створює Queue job, retry, resend, DSN reconciliation або History rewrite.
