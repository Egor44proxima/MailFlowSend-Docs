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
- Campaign type isolation не повинна обходитися вручну.

## Пов'язані workspace

- **Клієнти / CSM / База розсилки** — recipient source.
- **Документи / Борг** — business source evidence.
- **Черга** — send execution.
- **Історія** — immutable result/evidence.
