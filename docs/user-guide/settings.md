# 20 · Налаштування

**Контекст:** CONFIGURATION

## Призначення

**Налаштування** — workspace для explicit runtime/profile configuration. На відміну від authoring campaign content, тут змінюються system-level preferences і transport profiles.

Configuration changes не повинні обходити existing validation, credential boundaries або send guards.

## SMTP configuration

Accepted Settings UX має explicit actions для SMTP profile management.

Типовий flow:

1. Вибрати або створити SMTP profile.
2. Вказати transport parameters згідно з environment policy.
3. Зберегти profile.
4. Зберегти credential через supported secure boundary.
5. Виконати connection/test action, якщо передбачено profile contract.
6. Перевірити result перед production campaign.

**Save SMTP profile** є primary configuration action.

Credential deletion є destructive action і повинна лишатися захищеною explicit confirmation.

## Sender semantics

Visible From / Reply-To / envelope sender визначаються accepted sender policy до dispatch freeze. Settings не повинні змінювати headers уже frozen queue payload.

## Spintax Runtime Control

MAIL-14.2 дозволяє керувати Spintax із UI.

Effective precedence:

~~~text
explicit environment override
→ persisted operator preference
→ safe default OFF
~~~

UI states:

~~~text
Spintax: ВИМКНЕНО
Spintax: УВІМКНЕНО
ENV override
~~~

Якщо active ENV override встановлено, UI не може його обійти.

## Що змінює Spintax toggle

Toggle впливає тільки на:

- future Preview;
- future dispatch freeze.

Не впливає на:

- already frozen dispatch;
- existing Queue payload;
- Retry payload;
- historical History evidence.

## Fail-closed behavior

Якщо Spintax disabled, ordinary template без active syntax продовжує працювати.

Template з active Spintax syntax при disabled feature повинен fail-closed. Raw expression не повинна піти у recipient email.

## Runtime isolation

Persisted operator preference зберігається у runtime-specific configuration boundary. DEV і PROD не повинні непомітно ділити один configuration/DB context.

## Перед production send

Після зміни Settings:

1. Перевірити runtime mode.
2. Перевірити SMTP profile/credential.
3. Перевірити sender identity.
4. Перевірити Spintax effective source/status.
5. Відкрити Campaign Preview.
6. Пройти Preflight.
7. Лише потім freeze/send.

## Safety boundary

- Settings ≠ send.
- Save profile не створює Queue job.
- ENV override не обходиться UI toggle.
- Credential не слід логувати або публікувати.
- Configuration change не переписує historical evidence.

## Пов'язані workspace

- **Кампанії** — preview/preflight.
- **Черга** — frozen execution state.
- **Системний журнал** — configuration/transport diagnostics.
- **Діагностика** — SMTP/runtime health.
