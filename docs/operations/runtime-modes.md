# Runtime режими

MailFlowSend розділяє середовища та operational intent.

## DEV

Призначений для тестів, isolated fixtures та local transport. Real production send має бути заблокований policy.

## PROD

Використовує production SMTP/runtime data і вимагає повного preflight та safety boundaries.

## READ-ONLY

Підходить для evidence inspection без business mutations, коли це підтримує конкретна робоча область.

DEV і PROD не повинні непомітно використовувати одну й ту саму canonical DB або credentials context.
