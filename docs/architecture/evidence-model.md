# Evidence модель

MailFlowSend розділяє різні рівні evidence:

~~~text
Queue attempt evidence
        ↓
SMTP submission evidence
        ↓
Delivery projection
        ↓
DSN / operator evidence
        ↓
Immutable History
~~~

## Invariants

~~~text
SMTP ACCEPTED != DELIVERED
UNCONFIRMED != FAILED
History is read-only evidence
Retry != controlled resend
legacy evidence is not rewritten
identity-aware evidence remains identity-aware
~~~

Identity-aware model може співіснувати з legacy evidence через union/read projection без historical rewrite.
