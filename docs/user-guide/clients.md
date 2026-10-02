# 02 · Клієнти

**Контекст:** CONTROLLED

## Призначення

**Клієнти** — canonical registry бізнес-клієнтів. Тут оператор працює з client identity, CSM ownership, cooperation status, recipient contacts, PDF aliases та data-quality evidence.

Клієнти не повинні автоматично створюватися з fuzzy match або attachment evidence.

## Пошук і фільтри

Поточний registry підтримує server-side/operator filtering за:

- назвою;
- email;
- PDF alias;
- note/source evidence;
- exact `#ID`;
- CSM;
- cooperation status;
- data-quality state.

Data-quality filters відокремлюють clean records від проблем, зокрема recipient/email issues, alias issues та duplicates.

## Data quality

Типові issue categories:

- немає active email;
- немає primary email;
- кілька primary email;
- CSM inactive;
- немає PDF alias;
- shared primary email;
- shared PDF alias.

Для duplicate evidence можна відкрити detail і перейти до пов'язаного client record.

## Client detail

У detail/quick view перевіряйте:

- canonical client ID;
- display name;
- CSM;
- cooperation status;
- primary/active contacts;
- aliases;
- data-quality evidence;
- audit/history для контрольованих змін.

## Основні дії

Залежно від стану запису UI дозволяє:

- відкрити client detail;
- керувати контактами;
- змінювати cooperation status через explicit action;
- передати клієнта іншому CSM;
- переглядати duplicate/data-quality evidence;
- виконувати accepted legacy import/reconciliation flow.

## Передача іншому CSM

Canonical transfer змінює **ownership**, а не client identity.

~~~text
client ID              зберігається
contacts               зберігаються
PDF aliases            зберігаються
historical evidence    зберігається
current CSM            змінюється
~~~

Для transfer потрібні valid target CSM та explicit reason. Transfer audit є окремим evidence.

## Cooperation status

Статус **Припинено / STOPPED** блокує майбутню участь у відповідних send flows згідно з campaign/preflight policy. Зміна current status не переписує історичні dispatch/send records.

## Safety boundary

- **No auto-create clients.**
- **Fuzzy matching advisory only.**
- Ambiguous evidence не створює canonical binding.
- Client editing не повинно переписувати frozen dispatch або History.
- Shared email/alias evidence потрібно review'ити, а не автоматично “виправляти”.

## Пов'язані workspace

- **CSM** — ownership та manager scope.
- **Документи** — attachment/client matching.
- **Кампанії** — audience formation.
- **Історія** — historical send evidence.
