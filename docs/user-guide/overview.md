# 01 · Огляд

**Контекст:** READ_ONLY

## Призначення

**Огляд** — стартова operational точка MailFlowSend. Його задача — дати оператору швидку орієнтацію в поточному runtime і допомогти перейти до потрібного domain workspace, не виконуючи business mutation.

Це не заміна спеціалізованих екранів Queue, Delivery, Diagnostics або Recovery. Якщо на Огляді видно проблему, детальний source of truth потрібно відкривати у workspace-власнику відповідного стану.

## Що перевіряти після запуску

Рекомендований startup checklist:

1. Переконатися, що application Core запущений і UI не показує startup error.
2. Перевірити runtime mode — особливо перед будь-якою production-операцією.
3. Перевірити SQLite/runtime module health indicators.
4. Якщо є warning/failure — перейти у **Діагностику**.
5. Перед відправкою перейти у **Кампанії → Preflight**, а не робити висновок лише за загальним status.
6. Після відправки перевіряти **Чергу**, **Доставку** та **Історію** окремо.

## Як трактувати summary

Огляд може агрегувати інформацію з різних підсистем, але семантика між ними не зливається:

~~~text
Queue state
≠ Delivery state
≠ DSN correlation
≠ Recovery readiness
~~~

Наприклад, зелений SMTP/Queue status не означає, що всі recipients мають DELIVERED.

## Типовий сценарій

~~~text
Запуск MailFlowSend
→ Огляд
→ перевірка runtime/health
→ Діагностика при warning
→ потрібний operational workspace
~~~

## Safety boundary

Огляд класифікований як **READ_ONLY**. Сам workspace не повинен запускати retry, resend, DSN reconciliation, restore або інші state-changing операції.

## Пов'язані workspace

- **Діагностика** — якщо потрібен health drill-down.
- **Черга** — стан persistent send jobs.
- **Доставка** — recipient delivery projection.
- **Системний журнал** — technical events.
- **Відновлення** — backup/readiness/restore state.
