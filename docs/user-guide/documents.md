# 04 · Документи

**Контекст:** CONTROLLED

## Призначення

Workspace **Документи** керує attachment batches та індексацією document files. Він відділяє фізичний source batch від business document period і готує canonical attachment evidence для campaign preflight.

## Batch key і document period

Це різні поняття:

~~~text
batch_key                = operational/source folder identity
detected_document_period = period, розпізнаний із filename
expected_document_period = period, явно підтверджений оператором
~~~

Назва batch folder у форматі YYYY-MM **не означає автоматично**, що це expected billing/document period.

## Index flow

Рекомендований сценарій:

1. Вибрати конкретну monthly batch directory.
2. Натиснути **Індексувати**.
3. Перевірити PDF counts і detector states.
4. Переглянути dominant detected-period suggestion.
5. Явно підтвердити expected period.
6. Перевірити mismatch/ambiguous/unknown records.
7. Виправити source data або matching issues перед campaign preflight.

Dominant-period suggestion є лише підказкою і не auto-confirms expected period.

## Period detector

Detector використовує filename evidence та захищений від очевидних year outliers. Якщо year у filename недостовірний, він може бути збережений як diagnostic evidence, але не використовуватися як canonical document year.

## Availability

Current catalog availability та historical sendability — не одне й те саме. Missing physical file залишається unavailable, доки explicit re-index не підтвердить відновлений source.

Для unavailable attachment operational flow:

~~~text
Діагностика
→ issue
→ read-only Check now
→ за потреби Documents/folder
→ explicit confirmed re-index
~~~

Read-only probe не повинен сам запускати re-index.

## Safety boundary

- Attachment root не повинен індексуватися як normal monthly batch.
- Expected period не встановлюється автоматично.
- Missing required attachment лишається blocker.
- Re-index не переписує immutable dispatch/delivery/history evidence.
- Documents workspace не визначає recipient delivery status.

## Пов'язані workspace

- **Клієнти** — aliases/matching identity.
- **Кампанії** — attachment source та preflight.
- **Діагностика** — unavailable attachment issues.
- **Історія** — frozen attachment evidence після send.
