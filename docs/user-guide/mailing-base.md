# 05 · База розсилки

**Контекст:** AUTHORING

## Призначення

**База розсилки** — canonical registry для **GENERAL** mailing contacts. Це окремий recipient domain від business **Клієнтів / CSM**.

~~~text
GENERAL contact
→ optional groups/tags
→ sender profile
→ GENERAL campaign
→ Preflight
~~~

GENERAL registry навмисно не має автоматичної прив'язки до canonical clients або CSM.

## Contact lifecycle

Основні safety states:

- **active** — може бути candidate для future GENERAL preflight;
- **inactive** — виключений із normal future audience, але може бути explicitly restored згідно з accepted flow;
- **unsubscribed** — terminal suppression state у поточному contract.

Unsubscribed contact не повинен повертатися у send audience лише через group/tag membership.

## Email identity

У GENERAL registry normalized email є canonical unique identity. Це відрізняється від client contacts domain, де один email може мати складнішу business identity semantics.

## Groups і tags

Contact може мати багато groups і tags.

**Group** — reusable audience segment, наприклад business category або campaign cohort.

**Tag** — гнучка ознака для додаткової сегментації.

Accepted lifecycle taxonomy — activate/deactivate без destructive hard delete. Membership history та audit evidence зберігаються.

## Основні дії

- створити/редагувати GENERAL contact;
- імпортувати contacts accepted import flow;
- активувати/deactivate там, де дозволено;
- працювати з groups/tags;
- bulk assign/remove taxonomy;
- filter audience за group/tag/status;
- перейти до GENERAL campaign authoring.

## Safety boundary

- GENERAL registry не auto-creates canonical clients.
- Groups/tags не обходять UNSUBSCRIBED suppression.
- Editing registry не змінює frozen dispatches.
- GENERAL contacts не повинні непомітно потрапляти у DOCUMENTS/DEBT client flows.

## Пов'язані workspace

- **Кампанії** — GENERAL campaign.
- **Налаштування** — sender/SMTP configuration.
- **Черга / Доставка / Історія** — evidence після actual send.
