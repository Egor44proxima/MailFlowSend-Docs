# Черга

**Черга** — persistent send queue зі станами, evidence та контрольованими переходами.

~~~text
PENDING
SENDING
ACCEPTED
RETRY_WAIT
REVIEW
FAILED
CANCELLED
COMPLETED
~~~

## Важливі правила

- ACCEPTED — SMTP submission outcome, не recipient delivery;
- Retry policy окремий від controlled resend;
- unknown/ambiguous transport result не повинен автоматично означати safe-to-resend;
- Queue evidence не переписує delivery history заднім числом.
