# Перша розсилка рахунків

Ця інструкція описує повний безпечний сценарій першої **DOCUMENTS**-кампанії: від підготовки клієнтів і PDF-рахунків до Queue, SMTP submission, Delivery та History.

!!! important
    MailFlowSend не відправляє лист одразу після створення кампанії. Перед реальною відправкою система проходить Preflight, immutable Dispatch Snapshot і Final Handoff.

~~~mermaid
flowchart LR
    C["Клієнти"] --> D["Документи"]
    D --> CAM["DOCUMENTS кампанія"]
    CAM --> PF["Preflight 5.1 → 5.4"]
    PF --> DS["Dispatch Snapshot"]
    DS --> HO["Final Handoff"]
    HO --> Q["Черга"]
    Q --> SMTP["SMTP"]
    SMTP --> DEL["Доставка"]
    DEL --> H["Історія"]
~~~

## 1. Перевірити клієнтів

Відкрийте **Клієнти**.

Для клієнтів, які мають отримати рахунки, перевірте:

- клієнт активний;
- cooperation status не STOPPED / Припинено;
- призначений актуальний CSM;
- є active primary email;
- email валідний;
- немає blocking Data Quality issues.

Типові recipient blockers:

~~~text
primary_email_missing
multiple_primary_emails
recipient_email_invalid
client_stopped
~~~

MailFlowSend не повинен автоматично підставляти secondary email замість canonical primary email.

## 2. Підготувати рахунки

Відкрийте **Документи** та виберіть каталог із PDF-файлами рахунків за потрібний місяць.

Наприклад:

~~~text
Рахунки за вересень 2026
~~~

Натисніть **Індексувати**.

Після індексації перевірте:

- кількість знайдених PDF;
- detected document period;
- unknown / unmatched / ambiguous files;
- orphan evidence;
- помилки читання або fingerprint.

## 3. Підтвердити період документів

Перевірте **Expected Document Period**.

Наприклад:

~~~text
2026-09
~~~

MailFlowSend розділяє:

~~~text
batch_key
detected_document_period
expected_document_period
~~~

Назва папки сама по собі не є підтвердженням business period. Expected period має бути явно підтверджений оператором.

## 4. Перевірити прив'язку PDF до клієнтів

Для normal DOCUMENTS flow кожен рахунок має бути однозначно пов'язаний із canonical client.

Приклад:

~~~text
Клієнт A → invoice_A.pdf
Клієнт B → invoice_B.pdf
Клієнт C → invoice_C.pdf
~~~

Перевірте unmatched, ambiguous, orphan files, duplicate aliases, missing client та неправильні PDF aliases.

!!! warning
    Fuzzy matching у MailFlowSend — **advisory only**. Він не повинен автоматично створювати клієнта або підтверджувати неоднозначний match.

## 5. Створити DOCUMENTS кампанію

Відкрийте:

**Кампанії → Створити кампанію**

Виберіть тип:

~~~text
DOCUMENTS
~~~

Приклад назви:

~~~text
Рахунки · Вересень 2026
~~~

## 6. Вибрати attachment batch і period

У draft виберіть підготовлений batch і правильний business period.

Наприклад:

~~~text
Batch: рахунки вересень 2026
Period: 2026-09
~~~

## 7. Вибрати CSM

Виберіть одного або декількох CSM.

~~~text
☑ CSM 1
☑ CSM 2
☐ CSM 3
~~~

Selected CSM визначає maximum client scope для DOCUMENTS campaign:

~~~text
selected CSMs
→ active clients currently owned by those CSMs
→ cooperation_status != stopped
→ included by default
~~~

## 8. Перевірити аудиторію

Перегляньте список recipients.

Кожен клієнт має campaign-level state:

~~~text
Included
Excluded
~~~

За потреби окремого клієнта можна виключити саме з цієї кампанії. Campaign include/exclude не змінює canonical client record.

## 9. Підготувати тему листа

Приклад:

~~~text
Рахунок за вересень 2026 року
~~~

## 10. Підготувати текст листа

Приклад нейтрального шаблону:

> Шановні партнери!  
> Надсилаємо рахунок за {period}.  
> Документ додається до цього листа.  
> У разі виникнення запитань просимо звернутися до вашого менеджера.  
> З повагою, {csm_name}

## Опис тегів шаблону

Для кампанії типу **DOCUMENTS** Core підтримує такі variables:

| Тег | Що підставляється | Приклад |
|---|---|---|
| `{client_name}` | Canonical назва клієнта з картки **Клієнти** | `Клієнт A` |
| `{client_email}` | Точна email-адреса recipient, для якого виконується Preview / freeze | `client@example.com` |
| `{period}` | Назва місяця українською без року | `Вересень` |
| `{period_code}` | Код періоду кампанії у форматі `YYYY-MM` | `2026-09` |
| `{period_name}` | Назва місяця українською | `Вересень` |
| `{period_year}` | Рік із campaign period | `2026` |
| `{period_label}` | Готовий підпис періоду: назва місяця + рік | `Вересень 2026` |
| `{csm_name}` | Ім'я/назва поточного canonical CSM клієнта | `CSM 1` |
| `{csm_phone}` | Телефон поточного CSM | `+380...` |
| `{csm_email}` | Email поточного CSM; для DOCUMENTS цей CSM є sender context | `csm@example.com` |

### Різниця між period-тегами

Якщо у кампанії заданий period:

~~~text
2026-09
~~~

то результат буде:

~~~text
{period}       → Вересень
{period_code}  → 2026-09
{period_name}  → Вересень
{period_year}  → 2026
{period_label} → Вересень 2026
~~~

Тобто `{period}` і `{period_name}` у поточному DOCUMENTS contract дають однакове значення — **назву місяця**. Для тексту на кшталт «рахунок за Вересень 2026» зручніше використовувати `{period_label}`.

### Приклад шаблону

~~~text
Тема:
Рахунок за {period_label}

Текст:
Шановні партнери!

Надсилаємо рахунок за {period_label}.
Документ додається до цього листа.

У разі виникнення запитань:
{csm_name}
{csm_phone}
{csm_email}
~~~

При Preview/Dispatch Freeze значення беруться з canonical campaign/client/CSM context. Якщо current recipient або sender context не проходить перевірки, Preflight/freeze має блокувати відправку, а не залишати невідомий тег у готовому листі.

## 11. Перевірити Preview

Перед Preflight відкрийте Preview для декількох recipients.

Перевірте client name, period, recipient email, CSM, subject, body, attachment і відсутність сирих template variables.

У rendered letter не повинні залишатися:

~~~text
{client_name}
{period}
{a|b}
~~~

## 12. Перевірити Spintax, якщо він використовується

У **Налаштуваннях** перевірте effective Spintax status.

~~~text
Spintax: УВІМКНЕНО
~~~

або:

~~~text
Spintax: ВИМКНЕНО
~~~

Якщо Spintax disabled, але template містить active syntax, render/send має бути заблокований. Сирий Spintax текст не повинен потрапити до recipient.

## 13. Зберегти draft

Campaign має залишатися у стані:

~~~text
DRAFT
~~~

і містити хоча б одного included recipient.

# Preflight

## 14. MAIL-5.1 · Foundation

Створюється immutable capture campaign/source state.

Перевірте:

~~~text
FRESH
~~~

Якщо capture STALE, після виправлення source state створіть новий актуальний capture.

## 15. MAIL-5.2 · Recipient Resolution

MailFlowSend перевіряє:

- active client;
- cooperation status;
- active primary email;
- email validity;
- current CSM;
- sender identity.

Recipient verdict:

~~~text
READY
WARNING
BLOCKED
EXCLUDED
~~~

Приклад:

~~~text
Клієнт A   READY
Клієнт B   READY
Клієнт C   BLOCKED · primary_email_missing
Клієнт D   WARNING · additional_active_contacts
~~~

BLOCKED потрібно усунути до freeze.

## 16. MAIL-5.3 · Attachment Resolution

Для кожного included DOCUMENTS recipient система фіксує attachment evidence.

Physical integrity states:

~~~text
OK
MISSING
CHANGED
EMPTY
ERROR
~~~

Для DOCUMENTS attachment є required.

Типові blockers:

~~~text
required_attachment_missing
attachment_empty
attachment_missing
attachment_integrity_error
~~~

Physical file drift після preflight робить старий evidence stale; система не повинна тихо переписувати старий attachment set.

## 17. MAIL-5.4 · Final Eligibility

Final Eligibility об'єднує recipient та attachment evidence.

~~~text
Recipient Resolution
+
Attachment Resolution
=
Final Eligibility
~~~

Campaign summary:

~~~text
TOTAL
SELECTED
READY
WARNING
BLOCKED
EXCLUDED
ISSUES
~~~

Перед freeze:

~~~text
BLOCKED = 0
~~~

WARNING не обов'язково блокує send, але його потрібно переглянути.

## 18. Якщо є BLOCKED

Не обходьте blocker.

Якщо причина recipient / primary_email_missing — перейдіть у **Клієнти**.

Якщо причина attachment / required_attachment_missing — перейдіть у **Документи**.

Після canonical зміни historical preflight може стати STALE. Це normal behavior: створіть новий fresh preflight chain.

# Dispatch

## 19. Створити immutable Dispatch Snapshot

Якщо:

~~~text
Eligibility = FRESH
BLOCKED = 0
~~~

створіть Dispatch Snapshot.

Snapshot заморожує точні send values:

- recipient identity;
- recipient email;
- sender identity;
- Reply-To;
- rendered subject;
- rendered body;
- attachment reference;
- attachment SHA-256;
- attachment size;
- source/revision evidence.

State:

~~~text
FROZEN
~~~

## 20. Розуміти freeze boundary

Після FROZEN майбутні зміни current client/template state не повинні переписувати snapshot.

Для нового recipient state потрібен новий valid dispatch flow.

## 21. Final Handoff

Final Handoff read-only перевіряє frozen snapshot перед send-side stage.

READY вимагає, зокрема:

- snapshot = FROZEN;
- recipient/sender email valid;
- subject non-empty;
- final eligibility READY/WARNING;
- attachment існує;
- attachment non-empty;
- size збігається;
- SHA-256 збігається.

Результат:

~~~text
READY
~~~

Якщо PDF змінено після freeze, handoff має блокувати send.

# Queue та SMTP

## 22. Створити Send Queue

Коли Final Handoff = READY, відкрийте **Черга** і створіть persistent queue з цього Dispatch Snapshot.

Queue використовує frozen dispatch як authoritative payload source.

## 23. Перевірити SMTP profile

Перед production send перевірте:

- SMTP profile active;
- credential status = present;
- host/port;
- TLS/security mode;
- sender/envelope policy;
- connection test.

## 24. Перевірити batching/pacing

Queue підтримує batching, concurrency та pacing policy.

Для першої production campaign використовуйте conservative values, сумісні з policy вашого SMTP relay.

## 25. Перевірити runtime mode

Перед реальною відправкою:

~~~text
Runtime: PRODUCTION
~~~

У DEVELOPMENT / TEST real send має бути blocked runtime policy.

## 26. Запустити Queue

Для real transport MailFlowSend використовує controlled send boundary.

Основні item states:

~~~text
PENDING
SENDING
ACCEPTED
FAILED
REVIEW_REQUIRED
CANCELLED
~~~

## 27. Контролювати Queue

Normal successful SMTP submission:

~~~text
PENDING
→ SENDING
→ SMTP 2xx accepted
→ ACCEPTED
~~~

Якщо result UNKNOWN / REVIEW_REQUIRED, не робіть blind resend.

# Delivery та History

## 28. Не плутати ACCEPTED із доставкою

Ключовий invariant:

~~~text
SMTP ACCEPTED != DELIVERED
~~~

ACCEPTED означає, що SMTP relay прийняв message submission. Це не підтвердження доставки у mailbox recipient.

## 29. Перевірити Доставку

Відкрийте **Доставка**.

Delivery states:

~~~text
UNCONFIRMED
DELIVERED
DELAYED
BOUNCED
UNKNOWN
NOT_APPLICABLE
~~~

UNCONFIRMED не означає FAILED.

## 30. Перевірити DSN

Якщо налаштована inbound mailbox:

~~~text
Mailbox
→ IMAP scan
→ DSN parser
→ Correlation
→ Delivery projection
~~~

Correlation outcomes:

~~~text
CORRELATED
AMBIGUOUS
UNMATCHED
~~~

AMBIGUOUS або UNMATCHED не повинні автоматично запускати resend.

## 31. Перевірити Історію

Відкрийте **Історія**.

History зв'язує immutable evidence:

- campaign;
- dispatch;
- recipient;
- queue;
- SMTP attempts;
- delivery;
- DSN;
- attachments;
- timestamps.

History є read-only evidence.

## 32. Експортувати звіт за потреби

У **Історії** відфільтруйте потрібну кампанію та експортуйте CSV або XLSX.

Export використовує весь filtered cohort, а не лише visible page, і не запускає send/retry/resend.

# Чек-лист перед Start Queue

- [ ] Клієнти active.
- [ ] Cooperation status не STOPPED.
- [ ] У recipients є valid active primary email.
- [ ] PDF batch проіндексований.
- [ ] Expected period підтверджений.
- [ ] PDF правильно matched до clients.
- [ ] Campaign type = DOCUMENTS.
- [ ] Вибрані правильні CSM.
- [ ] Audience перевірена.
- [ ] Subject/body перевірені через Preview.
- [ ] Spintax effective state перевірений, якщо використовується.
- [ ] MAIL-5.1 Foundation = FRESH.
- [ ] Recipient Resolution перевірений.
- [ ] Attachment Resolution перевірений.
- [ ] Final Eligibility: BLOCKED = 0.
- [ ] Dispatch Snapshot = FROZEN.
- [ ] Final Handoff = READY.
- [ ] SMTP profile active.
- [ ] SMTP credential available.
- [ ] SMTP connection test успішний.
- [ ] Runtime = PRODUCTION.
- [ ] Queue policy перевірена.
- [ ] Controlled-send confirmation виконаний.

## Короткий правильний flow

~~~text
DOCUMENTS campaign
→ FRESH Preflight
→ BLOCKED 0
→ FROZEN Dispatch
→ READY Handoff
→ Queue
→ SMTP ACCEPTED
→ Delivery evidence
→ History
~~~

!!! warning
    Не переходьте до production send, якщо бачите BLOCKED, STALE, REVIEW_REQUIRED або UNKNOWN і причина не зрозуміла.
