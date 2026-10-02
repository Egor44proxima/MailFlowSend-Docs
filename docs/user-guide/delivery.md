# 09 · Доставка

**Контекст:** READ_ONLY

## Призначення

Workspace **Доставка** показує recipient-level delivery projection поверх SMTP submission та stronger DSN/operator evidence.

Це read-only operational view. Він не запускає resend або DSN reconciliation.

## Summary

Типові counters:

- Logical sends;
- SMTP accepted;
- UNCONFIRMED;
- DELIVERED;
- DELAYED;
- BOUNCED;
- UNKNOWN;
- DSN/operator authority counters.

## Основні delivery states

| State | Семантика |
|---|---|
| UNCONFIRMED | relay accepted, але stronger recipient evidence відсутній |
| DELIVERED | є accepted evidence фактичної доставки |
| DELAYED | temporary delivery delay evidence |
| BOUNCED | final non-delivery/bounce evidence |
| UNKNOWN | evidence недостатнє або outcome не визначений |
| NOT_APPLICABLE | delivery projection не застосовується до цього send state |

## Record list

Оператор може фільтрувати/шукати recipient, email, campaign, Message-ID, relay queue/queue context та відкривати detail.

Detail зв'язує:

- campaign;
- queue / queue item;
- SMTP session/attempt;
- Message-ID/relay evidence;
- current delivery state;
- evidence timeline.

## Evidence timeline

Timeline append-oriented. Новий DSN/operator evidence може уточнити recipient outcome, але старі queue/SMTP events не переписуються.

~~~text
QUEUE_CREATED
→ SMTP_ATTEMPT
→ SMTP_ACCEPTED
→ DSN / operator evidence
~~~

## Типовий сценарій

1. Перевірити summary.
2. Відфільтрувати BOUNCED/DELAYED/UNKNOWN за потреби.
3. Відкрити recipient record.
4. Перевірити submission і delivery окремо.
5. Переглянути evidence timeline.
6. Для correlation issue перейти у **DSN огляд**.
7. Для trends перейти у **Аналітика**.

## Safety boundary

~~~text
SMTP ACCEPTED != DELIVERED
UNCONFIRMED != FAILED
~~~

Delivery workspace не змінює Queue, не запускає resend і не “виправляє” DSN artifact.

## Пов'язані workspace

- **Черга** — submission attempt source.
- **DSN огляд** — inbound correlation.
- **Аналітика** — aggregated trends.
- **Історія** — immutable cross-send history.
