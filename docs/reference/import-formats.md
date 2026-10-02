# Import Formats Reference

MailFlowSend has separate import domains. Do not mix their source contracts.

## GENERAL contacts · CSV/XLSX

Supported:

~~~text
.csv
.xlsx
~~~

GENERAL import is independent from canonical Clients/CSM.

### Source columns

The import mapping supports:

| Canonical field | Required | Typical header aliases |
|---|---:|---|
| Name | no | name, contact, назва, ім'я, клієнт |
| Email | **yes** | email, mail, пошта, почта |
| Phone | no | phone, telephone, телефон |
| Note | no | note, comment, примітка |
| Group | no | group, category, група, категорія |
| Tags | no | tag, tags, label, тег, мітка |

UI may suggest mappings from headers, but mapping remains explicit operator evidence.

### CSV

Reader supports UTF-8 and Windows-1251 fallback. Delimiter is detected from:

~~~text
;
,
TAB
~~~

### XLSX

The operator can choose a worksheet. Workbook XML is read with bounded safety limits and is not extracted to disk.

### Limits

~~~text
max data rows   100000
max columns        256
sample preview      up to 20
~~~

### Duplicate policy

Default:

~~~text
SKIP
~~~

Optional explicit policy:

~~~text
UPDATE_EXISTING
~~~

Preview dispositions:

~~~text
new
existing
invalid
duplicate_in_file
unsubscribed
~~~

Audit dispositions after commit:

~~~text
added
updated
unchanged
skipped_existing
duplicate_in_file
invalid
suppressed_unsubscribed
~~~

Important invariants:

- Email must be valid.
- One source email produces at most one effective row per import.
- UNSUBSCRIBED is never reactivated/rewritten by import.
- Unknown or inactive Group/Tag is not auto-created.
- Group/Tag import assignment is additive.
- File SHA-256 must still match between preview and commit.
- Import mutates only the GENERAL mailing domain.

## DEBT · CSV/XLSX

Debt source is treated as untrusted input and parsed by the isolated debt worker/module.

Supported source encodings for CSV include:

~~~text
UTF-8
UTF-8 BOM
UTF-16 LE/BE
Windows-1251 fallback
~~~

### Canonical debt fields

| Field | Required | Meaning |
|---|---:|---|
| invoice_ref | no | invoice/document reference |
| invoice_date | no | invoice date |
| counterparty | **yes** | source counterparty identity |
| kam | no | KAM label |
| csm | no | source CSM label |
| work_characteristic | no | work/service characteristic |
| project | no | project |
| amount_total | no | original invoice amount |
| paid_total | no | paid amount |
| debt_total | **yes** | outstanding debt |

Mapping indices are 1-based in the technical worker contract.

Auto-mapping occurs only when one deterministic best source column exists. Ambiguous mappings require explicit operator selection.

### Money

Canonical money is not stored as binary float.

~~~text
raw       → original source text
canonical → decimal with 2 fractional digits
minor     → signed int64 minor units
~~~

Relevant row issues include:

~~~text
counterparty_missing
invoice_missing
invoice_date_invalid
money_missing
money_invalid
non_positive_debt
debt_math_mismatch
required_mapping_missing
mapping_ambiguous
manual_mapping_invalid
~~~

A non-positive debt row may remain evidence but is not send-eligible.

### Matching is a separate stage

File mapping is not client matching.

Debt client matching order:

~~~text
verified debt mapping
→ exact canonical client name
→ exact active alias
→ ambiguous / unresolved
~~~

Fuzzy/search scores are advisory only. Manual reconciliation requires an explicit ACTIVE client and note.

### Immutable snapshot

Only after normalization + accepted matching does Core create immutable:

~~~text
debt_imports
debt_items
debt_client_snapshots
~~~

## Legacy client import

Legacy import expects the old project shape:

~~~text
<legacy-root>/
├─ configs/
│  └─ managers.json
└─ managers/
   ├─ manager_001.csv
   ├─ ...
   └─ manager_NNN.csv
~~~

Run Preflight first.

Blocking conditions include:

- expected manager CSV missing;
- unknown manager CSV without mapping;
- incompatible headers.

Rows without recipient email may still be imported for client/attachment identity evidence, but they are not valid mail recipients.

Import is full-dataset transactional and SHA-256 fingerprinted. Reimporting the identical dataset is NO CHANGE.

After a changed client import, prior Client ↔ PDF matcher evidence becomes stale and should be rerun.

## Attachment batch indexing

Documents are not imported as GENERAL/DEBT tabular data.

The operator indexes a monthly source folder whose directory name is YYYY-MM.

Three concepts remain distinct:

~~~text
batch_key
detected_document_period
expected_document_period
~~~

Expected period is an explicit operator confirmation. Dominant detected period is only a suggestion.

Filename period detector may use the batch year as a year fallback, but must not turn batch identity into expected billing period automatically.
