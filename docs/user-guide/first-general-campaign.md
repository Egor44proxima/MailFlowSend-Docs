# Перша GENERAL кампанія

GENERAL — окремий mailing domain. Він не використовує canonical Clients/CSM як recipient registry.

~~~text
GENERAL contacts
→ groups/tags
→ sender profile
→ GENERAL DRAFT
→ Preview
→ Preflight
→ Dispatch
→ Queue
→ SMTP
~~~

## 1. Підготувати Базу розсилки

Відкрийте **База розсилки**.

Contacts можуть бути:

~~~text
active
inactive
unsubscribed
~~~

Тільки ACTIVE contacts входять у normal campaign scope.

UNSUBSCRIBED не можна повернути в audience імпортом або group/tag membership.

## 2. Імпортувати contacts або створити вручну

Для bulk import використовуйте CSV/XLSX.

Перед Commit:

1. Inspect file.
2. Select worksheet if XLSX.
3. Verify Email mapping.
4. Check duplicate policy.
5. Preview NEW / UPDATE / SKIP / INVALID / UNSUBSCRIBED.
6. Confirm Group/Tag assignments.
7. Commit only after preview review.

Див. [Import Formats Reference](../reference/import-formats.md).

## 3. Groups і Tags

Scope semantics:

~~~text
selected groups: contact must match any selected group
selected tags:   contact must match any selected tag
both blocks:     group condition AND tag condition
none selected:   all ACTIVE GENERAL contacts
~~~

Manual include/exclude state зберігається для rows, які лишаються в scope.

## 4. Створити Sender Profile

GENERAL sender identity зберігається окремо від CSM.

Sender profile містить display name, From email, Reply-To, phone, signature та active/inactive state.

SMTP credential тут не зберігається.

## 5. Створити GENERAL DRAFT

У **Кампанії** виберіть:

~~~text
GENERAL
~~~

Виберіть Group/Tag scope, active Sender Profile, subject, body та attachment policy.

## 6. Attachment policy

GENERAL shared attachments:

~~~text
NONE
OPTIONAL
REQUIRED
~~~

Integrity evidence включає path, SHA-256, size і live state.

Live state:

~~~text
ok
missing
changed
error
~~~

REQUIRED + no valid attachment → BLOCKED.

## 7. Template Variables

Див. [Template Variables Reference](../reference/template-variables.md).

Приклад:

~~~text
Тема:
{campaign_name}

Текст:
Добрий день, {contact_name}!

...

З повагою,
{sender_name}
{sender_phone}
{sender_signature}
~~~

## 8. Preview

GENERAL preview показує sender, exact recipient, rendered subject/body, linked attachments і warnings/blockers.

Preview працює зі saved DRAFT. Якщо editor changes не збережені, спочатку Save.

## 9. Audience safety

Не запускайте Preflight, якщо contact inactive/unsubscribed, sender profile inactive, recipient email invalid, REQUIRED attachments missing/changed або template blocked.

## 10. Preflight → Freeze

Canonical flow:

~~~text
Foundation
→ Recipient Resolution
→ Attachment Resolution
→ Eligibility
→ Dispatch Snapshot
→ Final Handoff
~~~

Умова для freeze:

~~~text
FRESH
BLOCKED = 0
~~~

## 11. Queue / SMTP

Після Handoff READY створіть Queue, виберіть accepted SMTP profile, перевірте credential/runtime, виконайте controlled-send confirmation і запустіть Queue.

## 12. Після send

Перевіряйте:

~~~text
Queue item
→ SMTP attempt
→ Delivery
→ DSN
→ History
~~~

GENERAL contacts не стають canonical Clients через send flow.

## Чек-лист

- [ ] GENERAL contacts active;
- [ ] UNSUBSCRIBED suppressed;
- [ ] groups/tags scope перевірений;
- [ ] Sender Profile active;
- [ ] subject/body Preview correct;
- [ ] attachment policy satisfied;
- [ ] Preflight FRESH;
- [ ] BLOCKED = 0;
- [ ] Dispatch FROZEN;
- [ ] Handoff READY;
- [ ] SMTP/Queue safety verified.
