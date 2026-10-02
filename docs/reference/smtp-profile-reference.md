# SMTP Profile Reference

SMTP profiles define transport configuration. Credentials are stored separately in Windows Credential Manager.

## Fields

| Field | Purpose |
|---|---|
| Name | operator-facing profile name |
| Scope | LOCAL_TEST / CORPORATE_RELAY / PRODUCTION |
| Host | SMTP host |
| Port | SMTP port |
| Security | NONE / STARTTLS / TLS |
| Auth mode | NONE / PLAIN / LOGIN |
| Username | SMTP authentication username |
| Credential ref | Windows Credential Manager reference, not password |
| Envelope From | SMTP MAIL FROM identity |
| EHLO name | client EHLO/HELO identity |
| Message-ID domain | DNS-style domain used for generated Message-ID |
| Timeout | bounded transport timeout |
| Active | whether profile is selectable for current operations |

## Scope policy

### LOCAL_TEST

Loopback/local test transport. Intended for tools such as Mailpit.

### PRODUCTION

Must use STARTTLS or TLS. Security=NONE is rejected.

### CORPORATE_RELAY

A narrow plaintext exception exists only for:

~~~text
port = 25
security = NONE
auth = NONE
~~~

Authenticated relay profiles must use TLS.

## AUTH

Supported:

~~~text
NONE
PLAIN
LOGIN
~~~

PLAIN/LOGIN execute only after TLS is established.

For STARTTLS, capabilities are re-read after TLS; AUTH support is validated against the post-TLS capability set.

Successful authentication requires SMTP 235.

## Credential storage

SQLite stores only a reference such as:

~~~text
wincred:MailFlowSend/SMTP/<id>
~~~

The password/secret lives in Windows Credential Manager.

Secret material must not appear in SQLite profile data, audit text, native ABI JSON, SMTP journal, diagnostic export or MIME metadata.

## Message-ID domain

Default:

~~~text
mailflow.local
~~~

Custom value must be a valid DNS-style hostname and cannot contain @, whitespace, brackets, slash/backslash or invalid labels.

## Submission semantics

~~~text
MAIL FROM 250  != ACCEPTED
RCPT TO 250    != ACCEPTED
DATA 354       != ACCEPTED
final DATA 250 == SMTP ACCEPTED
~~~

If DATA may have reached the relay but final reply is unavailable:

~~~text
submission_status = UNKNOWN
~~~

UNKNOWN is not safely retryable by assumption.

## Controlled real send

Real-scope sending requires explicit application confirmation at the controlled-send boundary.

Queue/transport validates the guard server-side; a frontend button state is not authorization.

## Profile lifecycle

Profile add/update/activate/deactivate and credential set/delete create audit evidence and advance the SMTP profile revision where applicable.

Historical SMTP sessions freeze transport/security identity so later profile edits do not rewrite old evidence.
