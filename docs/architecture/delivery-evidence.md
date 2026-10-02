# Delivery / DSN evidence

MailFlowSend навмисно розділяє transport submission і recipient delivery.

~~~mermaid
stateDiagram-v2
    [*] --> QueueItem
    QueueItem --> SMTPAttempt

    SMTPAttempt --> Accepted: relay 2xx
    SMTPAttempt --> RetryWait: retryable failure
    SMTPAttempt --> Review: ambiguous / unsafe outcome
    SMTPAttempt --> Failed: final transport failure

    Accepted --> Unconfirmed: no stronger evidence yet
    Unconfirmed --> Delivered: accepted delivery evidence
    Unconfirmed --> Delayed: temporary DSN
    Unconfirmed --> Bounced: final non-delivery DSN
    Unconfirmed --> Unknown: conflicting / insufficient evidence
    Delayed --> Delivered: later success evidence
    Delayed --> Bounced: later final failure evidence
~~~

## Ключове правило

~~~text
SMTP ACCEPTED != DELIVERED
~~~

Relay acceptance означає лише, що SMTP server прийняв submission для подальшої обробки.

## Inbound evidence flow

~~~mermaid
flowchart LR
    MB["Inbound mailbox"] --> SCAN["Read-only IMAP scan"]
    SCAN --> PARSE["DSN parser"]
    PARSE --> CORR{"Correlation"}
    CORR -->|exact / accepted| PROJ["Delivery projection"]
    CORR -->|ambiguous| AMB["AMBIGUOUS review"]
    CORR -->|no match| UNM["UNMATCHED review"]
    PROJ --> HIST["History evidence"]
~~~

## Safety semantics

~~~text
UNCONFIRMED != FAILED
BOUNCED != DORMANT
Coverage != Delivery
DSN artifact != resend command
~~~

Ambiguous та unmatched DSN залишаються evidence для review, а не приводом для автоматичної зміни recipient identity.
