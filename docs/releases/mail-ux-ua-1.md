# MAIL-UX-UA-1 · Ukrainian Operator Terminology & Mouse Context Menu

Статус: **CLOSED / ACCEPTED · 2026-10-07**

MAIL-UX-UA-1 завершив системне вирівнювання operator-facing термінології українською мовою та додав native mouse context menu для копіювання/вставки у Wails WebView.

## Capability

- українські operator-facing labels у Campaigns, Preflight, Queue, Delivery, History, Clients, Recovery, System Log, DSN, Inbound та суміжних workspaces;
- presentation-only mapping у `frontend/src/uiTerminology.ts`;
- canonical enum/API/SQL/JSON/policy/evidence values не перейменовуються;
- технічні стандарти та acronyms залишаються технічними: SMTP, DSN, PDF, CSV, XLSX, SHA-256, SQLite, Wails, Core, ABI, Message-ID;
- native right-click context menu увімкнений у Wails;
- static/table text можна виділяти мишкою;
- input / textarea підтримують native Cut / Copy / Paste;
- keyboard Ctrl+C / Ctrl+V збережено.

## Acceptance

- Windows canonical gate: PASS;
- MAIL-UX-UA-1 verifier: PASS;
- frontend typecheck/build: PASS;
- Go vet/regression: PASS;
- Wails production build: PASS;
- clean-checkout CI #255: SUCCESS;
- manual Windows visual/runtime acceptance: PASS;
- post-merge main CI #256: SUCCESS.

## Safety boundary

~~~text
presentation-only localization
!=
canonical contract rename
~~~

Не змінено:

- send semantics;
- Queue / Dispatch / SMTP behavior;
- evidence history;
- schema;
- ABI.

~~~text
Core       0.16.9
Schema     v53
ABI        1
Migration  NONE
~~~

Accepted source merge SHA:

~~~text
92685b5f1610f0a836ab124c543517b1ca6c3929
~~~
