# Перша DEBT_NOTICE кампанія

Ця інструкція описує перший production-safe flow для розсилки повідомлень про борг.

~~~text
Debt source
→ parse / normalize
→ client matching
→ immutable debt snapshot
→ DEBT_NOTICE DRAFT
→ Preview
→ Preflight
→ Dispatch Snapshot
→ Queue
→ SMTP
→ Delivery / History
~~~

## 1. Підготувати source file

Відкрийте **Борг** і виберіть CSV або XLSX.

Перед snapshot обов'язково пройдіть:

1. source inspection;
2. column mapping;
3. normalization;
4. client matching;
5. reconciliation unresolved/ambiguous rows;
6. immutable debt snapshot.

## 2. Перевірити mapping

Required canonical fields:

~~~text
counterparty
debt_total
~~~

Optional fields:

~~~text
invoice_ref
invoice_date
kam
csm
work_characteristic
project
amount_total
paid_total
~~~

Ambiguous mapping не підтверджується автоматично.

## 3. Перевірити normalization

Row status:

~~~text
ready
warning
invalid
~~~

Не створюйте campaign-safe snapshot, доки critical invalid rows не зрозумілі.

Особливо перевірте:

~~~text
counterparty_missing
money_missing
money_invalid
debt_math_mismatch
mapping_ambiguous
required_mapping_missing
~~~

Non-positive debt не є send-eligible.

## 4. Перевірити Client Matching

Auto-match використовує тільки strong identity evidence:

~~~text
verified debt mapping
→ exact canonical client name
→ exact active alias
~~~

Якщо результат:

~~~text
AMBIGUOUS
UNRESOLVED
~~~

потрібна operator reconciliation.

Search score/fuzzy candidate — лише advisory evidence.

## 5. Створити immutable debt snapshot

Після accepted normalization/matching створіть snapshot.

Core зберігає:

~~~text
debt_imports
debt_items
debt_client_snapshots
~~~

Source rows не переписуються після snapshot.

Перевірте:

- eligible client count;
- total debt;
- aggregated rows;
- snapshot revision;
- source SHA-256.

## 6. Створити DEBT_NOTICE DRAFT

Відкрийте **Кампанії** і створіть тип:

~~~text
DEBT_NOTICE
~~~

Campaign прив'язується до одного immutable debt import. Source import не можна тихо замінити пізніше.

## 7. Перевірити audience

До audience входять snapshot clients, які:

- send-eligible за debt snapshot;
- current client active;
- cooperation status не stopped.

Email readiness остаточно перевіряє Preflight.

Manual include/exclude не змінює immutable debt source.

## 8. Налаштувати attachment policy

DEBT_NOTICE може мати campaign attachments.

Policy:

~~~text
NONE
OPTIONAL
REQUIRED
~~~

REQUIRED має пройти integrity checks перед freeze.

## 9. Підготувати subject/body

Див. [Template Variables Reference](../reference/template-variables.md).

Приклад:

~~~text
Тема:
Інформація щодо заборгованості

Текст:
Шановні партнери!

За даними обліку поточна заборгованість становить {debt_total}.

{debt_table}

З повагою,
{csm_name}
{csm_phone}
{csm_email}
~~~

## 10. Preview

Preview має показати exact recipient identity, current routing CSM та immutable debt values.

Перевірте:

- recipient email;
- current CSM;
- debt total;
- invoice rows/table;
- attachments;
- rendered subject/body;
- blockers/warnings.

Preview не створює send-side state.

## 11. Preflight

Пройдіть canonical chain:

~~~text
Foundation
→ Recipient Resolution
→ Attachment Resolution
→ Final Eligibility
~~~

Перед freeze:

~~~text
FRESH
BLOCKED = 0
~~~

## 12. Dispatch Snapshot

Freeze зберігає exact recipient identity/email, sender/Reply-To, rendered subject/body, attachments, debt import ID, debt snapshot revision, debt total та invoice count.

Після freeze current source changes не переписують evidence.

## 13. Final Handoff

Handoff має бути:

~~~text
READY
~~~

Якщо attachment або routing evidence більше не відповідає frozen state — send блокується.

## 14. Queue / SMTP

Створіть Queue тільки з READY handoff.

Перед production start перевірте runtime=PRODUCTION, active SMTP profile, credential, controlled-send confirmation і batching/concurrency policy.

## 15. Після send

Перевірте:

~~~text
Черга
→ Доставка
→ DSN
→ Історія
~~~

SMTP ACCEPTED не означає DELIVERED.

## Чек-лист

- [ ] source mapping перевірений;
- [ ] invalid money/identity issues розібрані;
- [ ] unresolved/ambiguous matching resolved або excluded;
- [ ] immutable debt snapshot створений;
- [ ] DEBT_NOTICE DRAFT прив'язаний до правильного import;
- [ ] Preview перевірений;
- [ ] Preflight FRESH;
- [ ] BLOCKED = 0;
- [ ] Dispatch FROZEN;
- [ ] Handoff READY;
- [ ] SMTP/Queue safety перевірена.
