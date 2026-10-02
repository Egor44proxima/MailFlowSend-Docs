# Доставка

Workspace **Доставка** показує recipient-level delivery projection поверх canonical submission та stronger delivery evidence.

~~~text
UNCONFIRMED
DELIVERED
DELAYED
BOUNCED
UNKNOWN
NOT_APPLICABLE
~~~

SMTP ACCEPTED означає прийняття relay-сервером. Поки немає stronger DSN/operator evidence, recipient delivery лишається UNCONFIRMED.

!!! important
    UNCONFIRMED не означає FAILED.
