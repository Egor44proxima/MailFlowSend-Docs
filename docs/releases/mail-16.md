# MAIL-16 · Delivery History Export & Evidence Portability

Статус: **CLOSED / ACCEPTED · 2026-10-02**

MAIL-16 додав portable export із canonical History read model.

## Capability

- full filtered cohort export;
- CSV;
- XLSX;
- same filter semantics as History;
- configurable columns;
- attachment filename evidence із frozen dispatch evidence;
- bounded XLSX column widths;
- privacy-aware structured export logging;
- zero-result header-only export;
- atomic file finalization;
- max-row fail-closed bound.

## Acceptance properties

- UI page/page-size не truncates export;
- CSV/XLSX з однаковими filters мають cohort parity;
- Cyrillic/Unicode підтримується;
- identity-aware і legacy evidence не переписуються;
- export не мутує Queue/Delivery/DSN/History;
- Excel сумісність підтверджена operator acceptance.

~~~text
Core       0.16.9
Schema     v53
ABI        1
Migration  NONE
~~~
