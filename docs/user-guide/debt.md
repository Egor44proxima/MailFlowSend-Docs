# 07 · Борг

**Контекст:** CONTROLLED

## Призначення

Workspace **Борг** готує canonical debt data для DEBT_NOTICE campaign: import, normalization, client matching, immutable client-level snapshot та eligibility source.

Debt flow працює з financial evidence окремо від ordinary DOCUMENTS attachments.

## Загальний flow

~~~text
source debt file
→ parser
→ normalization
→ client matching
→ immutable debt import/snapshot
→ campaign eligibility
→ DEBT_NOTICE draft
→ Preflight
~~~

## Client-level snapshot

Campaign не повинна працювати напряму з кожним invoice row як із незалежним recipient. Accepted contract агрегує debt на canonical client identity та створює immutable import/snapshot.

Current ownership change не переписує historical debt snapshot: UI може показувати current CSM і historical snapshot CSM окремо.

## Source validation

Перед створенням DEBT_NOTICE campaign Core перевіряє цілісність persisted snapshot/import counters і financial consistency.

Historical defective import може лишатися audit evidence, але не повинен бути campaign-eligible.

## Audience

Для inclusion потрібні accepted debt snapshot і current client state згідно з business guards. Email readiness остаточно контролюється preflight, а не самим debt parser.

Manual include/exclude у campaign audience не повинні змінювати source snapshot.

## Source immutability

Після прив'язки campaign до debt import source не можна тихо підмінити іншим import. Для іншого source створюється новий explicit campaign/draft flow.

## Типовий сценарій

1. Вибрати debt source file.
2. Запустити import/parse.
3. Перевірити summary та errors.
4. Перевірити client matching.
5. Переконатися, що import campaign-eligible.
6. Створити DEBT_NOTICE campaign.
7. Перейти у Campaign Preflight.
8. Усунути recipient blockers до freeze.

## Safety boundary

- Financial precision checks fail-closed.
- Debt snapshot не переписується через current CSM change.
- DEBT_NOTICE API/type не змішується з DOCUMENTS або GENERAL.
- Email/attachment send readiness остаточно вирішує preflight.
- Import data не є дозволом на send.

## Пов'язані workspace

- **Клієнти** — canonical identity.
- **Кампанії** — DEBT_NOTICE authoring.
- **Черга / Доставка / Історія** — execution та evidence.
