# Системний журнал

MAIL-15 створив centralized structured logging / observability layer.

~~~text
DEBUG
INFO
WARNING
ERROR
CRITICAL
~~~

~~~text
STARTED
SUCCESS
FAILED
BLOCKED
CANCELLED
SKIPPED
~~~

Structured logging — це **observability evidence**, а не власник бізнес-стану.

~~~text
log event
→ знайти canonical owner
→ перевірити Queue / Delivery / DSN / History / Recovery
→ виконувати лише підтримувану operator action
~~~

Retention технічного логу не видаляє canonical Queue/Delivery/DSN/History evidence.
