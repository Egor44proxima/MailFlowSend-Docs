# Send Recovery Runbooks

Ця сторінка пояснює три різні operational flows, які не можна змішувати:

~~~text
Retry
DOCUMENTS Catch-up
Controlled Bounce Resend
~~~

## 1. Retry

Retry призначений для технічно retry-safe SMTP failure того самого logical send.

Automatic retry дозволений тільки коли:

~~~text
latest SendAttempt = FAILED_RETRYABLE
AND retry budget remains
AND queue not cancelled
~~~

Policy:

| Retry | Delay |
|---:|---:|
| 1 | 1 minute |
| 2 | 5 minutes |
| 3 | 15 minutes |

### RETRY NOW

RETRY NOW лише прискорює вже дозволений retry schedule.

Він не є force resend, override FAILED_PERMANENT, override DELIVERY_UNKNOWN або duplicate-prevention bypass.

### Не retry

~~~text
SMTP_ACCEPTED
FAILED_PERMANENT
FAILED_UNCLASSIFIED
DELIVERY_UNKNOWN
CANCELLED
~~~

## 2. DELIVERY_UNKNOWN

DELIVERY_UNKNOWN означає: DATA міг дійти до relay, але final acceptance result не відомий.

~~~text
DELIVERY_UNKNOWN
→ operator review
→ no automatic retry
~~~

Allowed review resolutions:

~~~text
KEEP_BLOCKED
CONFIRMED_ACCEPTED
CONFIRMED_NOT_ACCEPTED
~~~

A note is mandatory.

## 3. DOCUMENTS Catch-up

Catch-up використовується для recipients, які не були відправлені раніше, але пізніше стали READY.

Preview statuses:

~~~text
ALREADY_SENT
NEWLY_READY
STILL_MISSING
BLOCKED
REVIEW_REQUIRED
SOURCE_EXCLUDED
~~~

Тільки NEWLY_READY автоматично включається в новий catch-up DRAFT.

### Правильний flow

~~~text
root DOCUMENTS campaign
→ Preview Catch-up
→ inspect delta
→ Create Catch-up Campaign
→ only NEWLY_READY included
→ normal Preflight
→ new Dispatch
→ new Queue
~~~

Catch-up creation не відправляє лист і не створює Queue.

### Duplicate prevention

Якщо існує prior SMTP_ACCEPTED, PENDING/UNKNOWN logical send, pending dispatch або recipient already staged in another unfinished catch-up, recipient не повинен автоматично потрапити в новий catch-up.

### BOUNCED не Catch-up

Якщо раніше було SMTP_ACCEPTED, а потім Delivery = BOUNCED:

~~~text
ALREADY_SENT
→ Controlled Resend
~~~

а не Catch-up.

## 4. Controlled Bounce Resend

Controlled Resend призначений для definitive:

~~~text
SMTP_ACCEPTED + BOUNCED
~~~

Review states:

~~~text
ACTION_REQUIRED
PREPARED
BLOCKED
~~~

Перед preparation Core перевіряє current recipient state.

Для client, зокрема:

- client exists;
- active;
- cooperation not stopped;
- exactly one active primary email;
- no fallback to secondary.

Для GENERAL: mailing contact exists, status ACTIVE, email exists.

### Prepare Resend

Prepare creates one new DRAFT campaign for one bounced logical send.

It does not create Preflight automatically, freeze Dispatch, create Queue, trigger Retry або call SMTP.

Після preparation operator проходить normal campaign path.

### Lineage

Resend зберігає source Delivery record, root Delivery record, generation, source campaign, source dispatch/recipient, original/prepared email, source period/batch/debt identity та bounce reason.

## 5. Decision table

| Situation | Correct action |
|---|---|
| SMTP 4xx / FAILED_RETRYABLE | Retry policy |
| FAILED_PERMANENT | fix config/data; new valid flow if needed |
| DELIVERY_UNKNOWN | operator review |
| DOCUMENTS recipient had no prior accepted send and now READY | Catch-up |
| SMTP_ACCEPTED then BOUNCED | Controlled Resend |
| SMTP_ACCEPTED, no bounce | no duplicate resend |
| current email changed after historical bounce | Controlled Resend preview + new DRAFT |
| old campaign attachment became available before first send | Catch-up if recipient becomes NEWLY_READY |

## Safety invariant

~~~text
Retry != Controlled Resend
Catch-up != Resend
SMTP_ACCEPTED != DELIVERED
UNKNOWN != FAILED
~~~
