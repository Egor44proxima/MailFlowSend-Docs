# 03 · CSM

**Контекст:** CONTROLLED

## Призначення

Workspace **CSM** показує менеджерів і current client ownership. Його ключова operational задача — дозволити оператору знайти clients конкретного CSM та виконати контрольовану передачу ownership без зміни client identity.

## Типовий flow

~~~text
CSM
→ вибрати менеджера
→ Показати клієнтів цього CSM
→ Клієнти з CSM filter
→ вибрати client
→ Передати іншому CSM
~~~

## Ownership semantics

CSM transfer змінює current owner projection. Він не повинен:

- створювати нового client;
- змінювати client ID;
- видаляти contacts;
- змінювати PDF aliases;
- переписувати attachment history;
- переписувати historical campaign/delivery evidence.

Manual ownership після accepted transfer є canonical current state і не повинен бути тихо перезаписаний legacy import.

## Transfer guards

Операція відхиляється, якщо:

- client відсутній або inactive;
- target CSM відсутній або inactive;
- target CSM уже є current owner;
- reason порожній.

Після успіху client ownership revision змінюється, а identity revision не повинна змінюватися лише через transfer.

## Що перевірити після передачі

1. Client detail показує нового CSM.
2. Старий/new CSM counters оновилися.
3. Client ID залишився тим самим.
4. Contacts та aliases збереглися.
5. Transfer history містить previous → new CSM і reason.
6. Existing attachment matcher evidence не стає stale лише через ownership transfer.

## Safety boundary

CSM workspace не повинен використовувати ownership transfer як спосіб “переприв'язати” historical recipient identity. Historical dispatch records залишаються immutable.

## Пов'язані workspace

- **Клієнти** — actual transfer action та client detail.
- **Кампанії** — selected CSM scope формує DOCUMENTS audience.
- **Історія** — CSM є filter/evidence dimension, але current ownership не переписує past sends.
