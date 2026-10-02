# 16 · Діагностика

**Контекст:** READ_ONLY

## Призначення

**Діагностика** — централізований health/observability workspace для ключових підсистем MailFlowSend. Він допомагає знайти problem domain і перейти до canonical owner, але за замовчуванням не виконує repair.

## Підсистеми

Diagnostic Center агрегує evidence для таких областей, як:

- SQLite;
- SMTP;
- Send Queue / Retry;
- Delivery / History;
- DSN / Inbound;
- Attachments;
- Structured Logging;
- Recovery;
- runtime Modules.

Поточний UI використовує health states на кшталт:

~~~text
HEALTHY
WARNING
FAILED
INITIALIZING
~~~

Exact status визначається canonical diagnostic rules, а не кольором картки у frontend.

## Що робити з WARNING / FAILED

1. Відкрити subsystem detail.
2. Перевірити останній successful stage.
3. Перевірити current error category/code.
4. Переглянути bounded timeline/counters.
5. Перейти у owner workspace:
   - Queue issue → **Черга**;
   - Delivery/DSN → **Доставка / DSN огляд**;
   - Inbound → **Вхідна пошта**;
   - Logging → **Системний журнал**;
   - Recovery → **Відновлення**;
   - Attachment availability → відповідний attachment handoff.
6. Виконувати state-changing action тільки там, де існує explicit supported contract.

## Attachment availability handoff

Для unavailable attachment Diagnostic Center може вести у bounded operational flow:

~~~text
Diagnostic issue
→ read-only Check now
→ Client / Documents / folder navigation
→ explicit confirmed re-index
→ refresh
~~~

**Check now** лише перевіряє filesystem state за canonical attachment ID. Він не повинен сам запускати re-index.

## Structured Logging health

Diagnostic Center показує state logging subsystem, зокрема primary/fallback persistence mode, async queue/counters, redaction/lifecycle failures, retention/flood evidence.

Fallback logging — health signal, а не дозвіл автоматично retry/replay business action.

## AI Diagnostic Export

Support bundle призначений для аналізу без повного production data dump.

Він виключає:

- canonical SQLite DB;
- credentials/tokens;
- raw SMTP AUTH;
- message/template bodies;
- attachment bytes;
- raw emergency JSONL;
- інші заборонені sensitive payloads.

Bundle містить bounded technical evidence, достатнє для support triage.

## Типовий сценарій

~~~text
Problem
→ Діагностика
→ subsystem
→ exact error/stage/evidence
→ owner workspace
→ supported operator action
→ refresh diagnostics
~~~

## Safety boundary

Diagnostic Center не повинен автоматично:

- repair DB;
- VACUUM;
- delete WAL/SHM;
- retry/resend;
- restore;
- rewrite DSN;
- re-index attachments без explicit confirmation.

## Пов'язані workspace

- **Системний журнал** — event-level technical detail.
- **Відновлення** — recovery action owner.
- **Модулі** — module health detail.
- **Моніторинг** — operational inbound/DSN alerts.
