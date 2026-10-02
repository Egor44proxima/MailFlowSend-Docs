# 15 · DSN огляд

**Контекст:** CONTROLLED

## Призначення

**DSN огляд** — workspace для immutable normalized DSN artifacts, recipient correlation review та explicit operator reconciliation там, де accepted contract це дозволяє.

DSN artifact є evidence про mail transport/delivery event, а не автоматичною командою retry/resend.

## Summary

Поточний workspace показує:

- artifacts;
- recipient reports;
- effective correlated;
- ambiguous;
- unmatched;
- warnings.

## Filters

Correlation filter:

- ALL;
- UNRESOLVED;
- CORRELATED;
- AMBIGUOUS;
- UNMATCHED.

Search може використовувати artifact context, Message-ID, source, Reporting MTA або SHA-256 evidence.

## Artifact list

Кожен artifact має immutable normalized evidence. Detail може показувати:

- source/provenance;
- reporting MTA;
- artifact Message-ID;
- observed timestamp;
- recipient reports;
- classification;
- diagnostic codes;
- correlation basis;
- linked delivery record;
- semantic diagnostics.

Raw MIME не використовується як operator-editable state у цьому workspace.

## Correlation

Canonical outcomes:

~~~text
CORRELATED
AMBIGUOUS
UNMATCHED
~~~

Exact/accepted correlation може створити Delivery projection evidence. Ambiguous або unmatched повинні лишатися unresolved до explicit review.

## Semantic diagnostics

DSN action/status/SMTP diagnostic code перевіряються на internal consistency. Diagnostic conflict не повинен тихо переписувати established classification.

## Manual reconciliation

Коли accepted workflow дозволяє explicit operator reconciliation, воно має бути:

- one-shot;
- append-only;
- із reason/evidence;
- без переписування raw historical artifact.

Manual action не повинна створювати fake transport evidence.

## Diagnostic handoff

Diagnostic/Monitoring можуть відкрити DSN workspace із preset filter і context. Це лише navigation/triage, не automatic resolve.

## Типовий сценарій unresolved DSN

1. Відкрити UNRESOLVED.
2. Вибрати artifact.
3. Перевірити Message-ID/recipient/correlation basis.
4. Перевірити semantic diagnostic code.
5. Якщо evidence достатнє — використати allowed explicit reconciliation.
6. Якщо evidence недостатнє — залишити AMBIGUOUS/UNMATCHED.
7. Перевірити Delivery projection після accepted reconciliation.

## Safety boundary

- Ambiguous ≠ correlated.
- Unmatched ≠ failed recipient identity.
- DSN artifact ≠ resend instruction.
- Manual reconciliation append-only.
- Original artifact не редагується.
- Delivery changes only through accepted correlation/projection rules.

## Пов'язані workspace

- **Вхідна пошта** — artifact ingestion source.
- **Моніторинг** — unresolved alerts.
- **Доставка** — recipient projection.
- **Історія** — immutable cross-send timeline.
