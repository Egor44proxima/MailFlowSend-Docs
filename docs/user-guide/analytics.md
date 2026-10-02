# 12 · Аналітика

**Контекст:** READ_ONLY

## Призначення

**Аналітика** — read-only Bounce & Delivery Intelligence поверх canonical Delivery History. Workspace агрегує real-transport outcomes для operational analysis, не виконуючи send/retry/resend або DSN mutation.

LOCAL_TEST evidence виключається з real-transport rates.

## Time window

Оператор може вибрати bounded window:

- 7 days;
- 30 days;
- 90 days;
- 180 days;
- 365 days.

## Transport scope

Поточний workspace розрізняє, залежно від runtime evidence:

- ALL REAL transport;
- PRODUCTION;
- CORPORATE_RELAY.

## Summary metrics

Основні counters:

- SMTP Accepted;
- Delivered;
- Delayed;
- Bounced;
- Unknown;
- Unconfirmed;
- Problems;
- Recurring recipients.

Rates для bounce/delay/unknown рахуються від accepted SMTP submission cohort, а не від усіх draft recipients.

## Що можна аналізувати

### Problem trend

Time-series buckets для BOUNCED + DELAYED + UNKNOWN допомагають побачити зростання transport/delivery problems.

### Reasons

Reason taxonomy агрегує diagnostic reason categories та останнє evidence.

### Recipients

Показує recipients із recurring problems, їх BOUNCED/DELAYED/UNKNOWN counts та останній delivery record.

### Domains

Дозволяє помітити домени, де problems концентруються непропорційно.

### Campaigns / SMTP profiles

Допомагає відрізнити recipient/domain issue від конкретної campaign/profile/transport конфігурації.

## Copy report

Workspace може сформувати text report із поточного snapshot для support/analysis. Перед передачею такого report назовні перевіряйте privacy policy, оскільки operational data може містити recipient-level identifiers.

## Типовий сценарій

1. Вибрати window.
2. Вибрати real transport scope.
3. Оцінити Delivered/Delayed/Bounced/Unknown rates.
4. Перейти до trend.
5. Перевірити top reasons.
6. Перевірити recurring recipients і domains.
7. Для конкретного Record ID перейти в **Історію** або **Доставку**.
8. Для unresolved DSN pattern перейти у **DSN огляд**.

## Safety boundary

Workspace **ніколи** не повинен:

- send;
- retry;
- resend;
- змінювати DSN correlation;
- mutate Queue;
- трактувати rate як automatic action trigger.

Analytics — diagnostic/decision-support projection, а не business state owner.

## Пов'язані workspace

- **Доставка** — individual recipient records.
- **Історія** — immutable cross-send evidence.
- **DSN огляд** — correlation/root-cause review.
- **Моніторинг** — current alerts і bounce-rate spike detection.
