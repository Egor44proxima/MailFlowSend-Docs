# Початок роботи

MailFlowSend побудований як Windows desktop-застосунок на **Go + Wails + Vue** з canonical SQLite storage.

~~~text
Клієнти / контакти
        ↓
Кампанія
        ↓
Preflight
        ↓
Immutable dispatch snapshot
        ↓
Persistent Queue
        ↓
SMTP submission
        ↓
Delivery / DSN
        ↓
History / Diagnostics
~~~

Перед реальною відправкою перевіряйте runtime mode, SMTP profile, recipient cohort, attachments та preflight blockers.
