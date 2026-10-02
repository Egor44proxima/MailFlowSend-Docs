# 08 · Черга

**Контекст:** CONTROLLED

## Призначення

**Черга** — persistent send queue. Вона відповідає за durable execution state між frozen dispatch і SMTP attempts.

Queue не визначає recipient delivery самостійно: вона володіє send execution/attempt evidence.

## Що бачить оператор

Queue workspace показує:

- queue jobs;
- campaign/dispatch identity;
- job completion state;
- total/PENDING/SENDING/ACCEPTED/RETRY/REVIEW/FAILED counters;
- recipient queue items;
- SMTP/attempt evidence;
- retry/action boundary;
- safety/event timeline для selected item.

## Основні стани

~~~text
PENDING
SENDING
ACCEPTED
RETRY_WAIT
REVIEW
FAILED
CANCELLED
COMPLETED
COMPLETED_WITH_ISSUES
~~~

Точний набор статусів у detail залежить від queue item/job layer, але ключовий принцип незмінний: state transition виконує Core, а не UI.

## SMTP ACCEPTED

~~~text
Queue item ACCEPTED
= SMTP relay accepted submission
≠ recipient DELIVERED
~~~

Після ACCEPTED recipient delivery може лишатися UNCONFIRMED.

## Retry

Retry policy працює за accepted attempt/error classification. Retry — продовження того самого logical send contract, а не новий business resend.

Ambiguous transport outcome повинен переходити у safe review boundary, а не автоматично повторювати submission.

## Operator workflow

1. Відкрити queue job.
2. Перевірити job summary.
3. Вибрати recipient item.
4. Переглянути latest attempt і SMTP evidence.
5. Якщо є RETRY_WAIT — перевірити reason/policy.
6. Якщо є REVIEW — не запускати blind resend; перейти до relevant evidence.
7. Для accepted item перевіряти recipient outcome у **Доставка**.

## Completion

Queue job може бути completed навіть якщо recipient delivery ще не підтверджена: completion означає завершення queue execution, не universal DELIVERED.

## Safety boundary

- Не трактувати ACCEPTED як DELIVERED.
- Не змінювати queue rows вручну у SQLite.
- Не обходити idempotency/duplicate guards.
- Retry ≠ controlled resend.
- Export/Diagnostics не повинні створювати новий queue job.

## Пов'язані workspace

- **Кампанії** — frozen dispatch source.
- **Доставка** — recipient outcome.
- **Недоставка** — controlled review/resend.
- **Історія** — immutable evidence.
- **Системний журнал** — technical queue/retry events.
