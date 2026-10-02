# MailFlowSend

**MailFlowSend** — desktop-застосунок для контрольованих email-розсилок, persistent Queue, SMTP submission, delivery evidence, DSN, історії відправок, діагностики та operational observability.

## Актуальність документації

<div id="docs-source-status"></div>

Документація прив'язана до конкретного `MailFlowSend/main` SHA. Якщо application repository піде вперед, цей індикатор автоматично зміниться на **OUTDATED** до фактичного оновлення документації.

## Поточний accepted baseline

~~~text
Core       0.16.9
Schema     v53
ABI        1
Migration  NONE
~~~

## Основні принципи

!!! important "Семантика доставки"
    SMTP ACCEPTED означає, що relay прийняв повідомлення для подальшої доставки. Це не є доказом доставки одержувачу.

~~~text
SMTP ACCEPTED != DELIVERED
UNCONFIRMED != FAILED
BOUNCED != DORMANT
DORMANT != STOPPED
Coverage != Delivery
Retry != controlled resend
~~~

History є read-only evidence. Legacy evidence не переписується під identity-aware модель.

!!! note "Public-safe"
    Цей сайт навмисно не містить credentials, приватних recipient records, raw Message-ID, production DB, diagnostic bundles або інших чутливих runtime artifacts.
