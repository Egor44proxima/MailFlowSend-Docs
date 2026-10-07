# 06 · Кампанії

**Контекст:** AUTHORING

## Призначення

**Кампанії** — workspace, де оператор формує draft майбутньої розсилки: business type, audience scope, template, attachments/source data та preflight intent.

Campaign authoring не є відправкою. Реальний send починається лише після accepted preflight/freeze/queue boundaries.

## Типи кампаній

MailFlowSend підтримує окремі business flows:

- **DOCUMENTS** — client/CSM-oriented monthly documents;
- **DEBT_NOTICE** — debt snapshot–oriented notifications;
- **GENERAL** — незалежний GENERAL contact registry.

Ці типи мають різні source/audience semantics і не повинні змішувати API або recipient domains.

## Draft

У draft зберігаються, залежно від type:

- campaign name;
- period/source batch;
- selected CSM або GENERAL audience scope;
- per-recipient include/exclude decisions;
- subject/body/template;
- attachment policy;
- sender/profile context.

Editing draft не повинно змінювати client/contact/ownership revisions без окремої domain action.

## Audience

Для client-oriented campaign selected CSM визначає maximum scope:

~~~text
selected CSM
→ active clients
→ cooperation != stopped
→ default inclusion
→ explicit include/exclude overrides
~~~

Для GENERAL campaign audience формується з окремого mailing registry.

## Template і Spintax

MAIL-14 додав deterministic Spintax.

- Preview/render йде через canonical Core renderer.
- Якщо Spintax feature disabled і template містить active syntax, render/send fail-closed.
- Уже frozen dispatch не reroll'иться при retry/resend.
- ENV override має вищий priority за UI preference.

## Preflight

Перед freeze перевіряються recipient resolution, contact/email readiness, attachments та інші campaign-specific blockers.

~~~text
Draft
→ Preflight
→ READY / WARNING / BLOCKED
→ immutable dispatch snapshot
~~~

BLOCKED recipient не повинен потрапити у send лише через frontend action.

## Immutable dispatch

Після freeze campaign content/recipient evidence стає source для Queue. Подальші зміни client contact, template або runtime Spintax preference не переписують frozen payload.

## Late Attachment Catch-up для DOCUMENTS

MAIL-9.6d додає focused panel **«Пізно готові рахунки»** для monthly DOCUMENTS campaign.

Він відповідає на вузьке питання:

> Які клієнти були заблоковані саме через відсутній required PDF на primary boundary, але тепер мають READY attachment?

Основний status:

~~~text
LATE_ATTACHMENT_READY
~~~

Primary boundary визначається immutable evidence, а не hard-coded календарним днем:

~~~text
Primary Eligibility
+ Primary Dispatch
+ Primary Send Day
~~~

Оператор може:

1. оновити late-attachment projection;
2. перевірити Missing at primary / Late ready / Still missing / Already sent / Review;
3. експортувати missing-at-primary cohort у CSV або XLSX;
4. явно створити catch-up DRAFT тільки для `LATE_ATTACHMENT_READY`.

Create action не створює Dispatch або Queue і не запускає SMTP. Новий DRAFT проходить звичайний MAIL-5 Preflight.

## Типовий сценарій

1. Створити draft правильного type.
2. Вибрати source/period/audience.
3. Перевірити включення/виключення.
4. Підготувати subject/body/template.
5. Перевірити Preview.
6. Запустити Preflight.
7. Усунути blockers.
8. Створити immutable dispatch snapshot.
9. Передати в Queue.

## Safety boundary

- Campaign draft ≠ send.
- UI preview ≠ frozen payload.
- BLOCKED ≠ READY.
- Retry ≠ controlled resend.
- Catch-up ≠ controlled resend.
- `LATE_ATTACHMENT_READY` не обходить MAIL-5 Preflight.
- Campaign type isolation не повинна обходитися вручну.

## Пов'язані workspace

- **Клієнти / CSM / База розсилки** — recipient source.
- **Документи / Борг** — business source evidence.
- **Черга** — send execution.
- **Історія** — immutable result/evidence.
