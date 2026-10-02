# Діагностика

**Diagnostic Center** агрегує health ключових підсистем:

- SQLite;
- SMTP;
- Queue / Retry;
- Delivery / History;
- DSN / Inbound;
- Attachments;
- Recovery;
- runtime Modules;
- Structured Logging.

Diagnostic Center за замовчуванням read-only. Він не повинен автоматично виконувати repair, VACUUM, restore, resend, WAL deletion або інші небезпечні зміни.

## AI diagnostic export

Diagnostic export формує bounded support bundle без production DB, raw credentials, raw message bodies та attachment bytes.
