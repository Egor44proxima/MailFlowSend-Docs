# Template Variables Reference

Цей довідник описує canonical template variables для трьох типів MailFlowSend campaign:

~~~text
DOCUMENTS
DEBT_NOTICE
GENERAL
~~~

Рендер виконується в Core. Vue не є джерелом семантики тегів.

## DOCUMENTS

| Тег | Значення | Приклад |
|---|---|---|
| {client_name} | canonical назва client | Клієнт A |
| {client_email} | exact recipient email для preview/freeze identity | client@example.com |
| {csm_name} | current canonical CSM name | CSM 1 |
| {csm_email} | current CSM email | csm@example.com |
| {csm_phone} | current CSM phone | +380... |
| {period} | назва місяця українською | Вересень |
| {period_code} | campaign period YYYY-MM | 2026-09 |
| {period_name} | назва місяця українською | Вересень |
| {period_year} | рік | 2026 |
| {period_label} | назва місяця + рік | Вересень 2026 |

Для period 2026-09:

~~~text
{period}       → Вересень
{period_code}  → 2026-09
{period_name}  → Вересень
{period_year}  → 2026
{period_label} → Вересень 2026
~~~

## DEBT_NOTICE

| Тег | Значення |
|---|---|
| {campaign_name} | canonical campaign name |
| {client_name} | canonical client name |
| {client_email} | exact recipient email |
| {csm_name} | current canonical CSM name |
| {csm_email} | current CSM email |
| {csm_phone} | current CSM phone |
| {csm_signature} | current CSM signature |
| {debt_total} | canonical total debt presentation |
| {debt_amount_total} | total invoice/original amount |
| {debt_original_total} | alias of original total in current contract |
| {debt_paid_total} | total paid amount |
| {debt_invoice_count} | distinct invoice count |
| {debt_row_count} | source debt row count for recipient snapshot |
| {debt_import_id} | immutable debt import ID |
| {debt_source} | source debt filename |
| {debt_snapshot_revision} | frozen debt snapshot revision |
| {debt_table} | generated debt detail representation |

Financial source values come from the immutable debt import/snapshot; recipient routing and CSM come from the accepted current-routing contract at preview/preflight/freeze.

## GENERAL

| Тег | Значення |
|---|---|
| {campaign_name} | canonical campaign name |
| {contact_name} | GENERAL mailing contact display name |
| {contact_email} | canonical GENERAL email |
| {contact_phone} | GENERAL contact phone |
| {sender_name} | sender display name; fallback to profile name |
| {sender_email} | sender From email |
| {sender_reply_to} | Reply-To; fallback to From |
| {sender_phone} | sender profile phone |
| {sender_signature} | sender profile signature |

GENERAL sender identity is independent from client/CSM ownership.

## Spintax and variables

Canonical order:

~~~text
template
→ parse/validate Spintax
→ deterministic variant selection
→ personalization variables
→ immutable rendered output
~~~

If Spintax is disabled and active Spintax syntax exists, render/freeze fails closed with SPINTAX_FEATURE_DISABLED.

## Freeze rule

Preview is observational. The send-side authoritative values are those rendered into the immutable Dispatch Snapshot.

After freeze, current client/contact/CSM/sender-profile edits do not rewrite frozen subject/body.
