# SMTP

SMTP subsystem відповідає за transport submission і технічне session/attempt evidence.

~~~text
SMTP 250 / ACCEPTED
≠
recipient DELIVERED
~~~

MailFlowSend зберігає Message-ID/relay context у canonical evidence, але public documentation не публікує реальні production identifiers.

Retry дозволяється лише відповідно до retry policy та відомого attempt state. Ambiguous transport outcome потребує safety review, щоб не створити duplicate delivery.
