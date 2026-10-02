# 10 · Недоставка

**Контекст:** CONTROLLED

## Призначення

**Недоставка** — workspace для operator review проблемних recipient outcomes і **controlled resend** там, де accepted safety contract дозволяє нову контрольовану спробу.

Це не автоматичний retry engine і не місце для масового blind resend.

## Які записи потребують уваги

Залежно від evidence, до review можуть потрапляти:

- BOUNCED recipients;
- final SMTP failures;
- UNKNOWN/ambiguous outcomes;
- records, для яких потрібна explicit operator decision перед новим send.

UNCONFIRMED не повинен автоматично вважатися failed лише через відсутність DSN.

## Retry vs controlled resend

~~~text
Retry
= continuation of retryable execution policy

Controlled resend
= explicit operator-authorized new send action
  after evidence review and guards
~~~

Ці механізми мають різні audit/idempotency semantics.

## Рекомендований review flow

1. Відкрити проблемний recipient.
2. Перевірити Queue/SMTP attempt lineage.
3. Перевірити Delivery state.
4. Якщо є DSN — перевірити correlation і reason.
5. Перевірити current recipient email/contact readiness.
6. Переконатися, що outcome не ambiguous.
7. Лише після цього використовувати доступну controlled resend action.
8. Перевірити новий queue/evidence lineage.

## Коли resend небезпечний

Не слід resend'ити автоматично, якщо:

- transport outcome unknown;
- є ризик duplicate delivery;
- DSN correlation ambiguous;
- recipient identity/email змінився без review;
- cooperation status STOPPED;
- current preflight/safety guard блокує send.

## Audit

Controlled resend повинен лишати окреме evidence про operator action і не переписувати original send/History.

## Safety boundary

- BOUNCED ≠ DORMANT.
- UNCONFIRMED ≠ FAILED.
- Retry ≠ controlled resend.
- Original immutable evidence не редагується.
- Resend не повинен запускатися з read-only Analytics/History.

## Пов'язані workspace

- **Доставка** — outcome evidence.
- **DSN огляд** — bounce/correlation evidence.
- **Клієнти** — current recipient/contact state.
- **Черга** — execution нового дозволеного send.
- **Історія** — original + subsequent evidence.
