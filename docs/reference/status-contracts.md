# Статуси та інваріанти

## SMTP / Delivery

| Термін | Значення |
|---|---|
| SMTP ACCEPTED | relay прийняв message submission |
| UNCONFIRMED | сильнішого recipient-delivery evidence ще немає |
| DELIVERED | є accepted stronger delivery evidence |
| DELAYED | є temporary delivery delay evidence |
| BOUNCED | є bounce/final non-delivery evidence |
| UNKNOWN | outcome недостатньо визначений |

## Незмінні правила

~~~text
SMTP ACCEPTED != DELIVERED
UNCONFIRMED != FAILED
BOUNCED != DORMANT
DORMANT != STOPPED
Coverage != Delivery
History is read-only evidence
Retry != controlled resend
legacy evidence is not rewritten
identity-aware evidence remains identity-aware
no auto-create clients
fuzzy matching advisory only
~~~
