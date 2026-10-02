# Повний посібник користувача

MailFlowSend має **20 canonical operator workspaces**. Глобальний header показує контекст дії: read-only evidence, controlled operations, authoring або configuration. Цей індикатор допомагає орієнтуватися, але не замінює backend guards і confirmations.

| # | Workspace | Контекст | Основне призначення |
|---:|---|---|---|
| 01 | Огляд | READ_ONLY | Загальна operational орієнтація та перехід до потрібного домену |
| 02 | Клієнти | CONTROLLED | Canonical client registry, contacts, cooperation, data quality |
| 03 | CSM | CONTROLLED | Менеджери, client ownership та контрольована передача клієнта |
| 04 | Документи | CONTROLLED | Attachment batches, periods, indexing та availability |
| 05 | База розсилки | AUTHORING | Незалежний GENERAL contact registry, groups/tags |
| 06 | Кампанії | AUTHORING | Draft, audience, template, preflight та dispatch preparation |
| 07 | Борг | CONTROLLED | Debt import/snapshot/matching та DEBT_NOTICE source |
| 08 | Черга | CONTROLLED | Persistent send queue, attempts, retry/review boundaries |
| 09 | Доставка | READ_ONLY | Recipient delivery projection та immutable evidence timeline |
| 10 | Недоставка | CONTROLLED | Review проблемних/bounced recipients та controlled resend |
| 11 | Історія | READ_ONLY | Search, grouping, immutable timeline, coverage/activity та export |
| 12 | Аналітика | READ_ONLY | Bounce/Delivery intelligence для real transport |
| 13 | Моніторинг | READ_ONLY | Inbound/DSN operational alerts та bounce-rate anomalies |
| 14 | Вхідна пошта | CONTROLLED | IMAP profiles, credentials, scans та scheduler |
| 15 | DSN огляд | CONTROLLED | DSN artifacts, correlation review та explicit reconciliation |
| 16 | Діагностика | READ_ONLY | Health ключових підсистем і support evidence |
| 17 | Системний журнал | READ_ONLY | Structured technical observability |
| 18 | Відновлення | CONTROLLED | Backup/catalog/readiness/restore workflows |
| 19 | Модулі | READ_ONLY | Runtime module discovery, ABI та health |
| 20 | Налаштування | CONFIGURATION | SMTP/runtime configuration та Spintax control |

## Як користуватися цим розділом

На кожній сторінці описані:

1. **Призначення** — за що відповідає workspace.
2. **Що бачить оператор** — ключові projections, counters та filters.
3. **Основні дії** — що можна робити через UI.
4. **Типовий сценарій** — рекомендований робочий flow.
5. **Safety boundary** — чого workspace не повинен робити автоматично.
6. **Пов'язані workspace** — куди переходити далі.

!!! important
    Якщо manual і поточний UI розходяться, canonical Core/backend contract та accepted runtime build мають вищий пріоритет. Документацію слід оновити разом із наступним accepted UI change.
