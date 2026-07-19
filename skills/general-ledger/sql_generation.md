# SQL Generation

Generate ANSI-compatible SQL.

Only SELECT statements.

Never generate

INSERT

UPDATE

DELETE

ALTER

DROP

CREATE

MERGE

EXEC

TRUNCATE

---

Never use

SELECT *

Always select only the required columns.

---

Use business-friendly aliases.

---

Always use

journal_date

as the primary date column unless the user explicitly requests another supported date.

---

Always normalize

dc_type

before comparison.

Use

UPPER(dc_type)

when filtering Debit or Credit entries.

Example

```sql
UPPER(dc_type) = 'D'
```

or

```sql
UPPER(dc_type) = 'C'
```

---

Journal transactions consist of multiple journal lines.

When the user asks about

- journal entries
- accounting transactions
- journal balance
- accounting audit

group or filter using

journal_id

unless individual journal lines are explicitly requested.

---

Transaction Type Filters

Revenue

↓

trans_type = 'REVENUE'

---

Payment

↓

trans_type = 'PAYMENT'

---

Inventory

↓

trans_type = 'INVENTORY'

---

Reverse Entries

↓

trans_type = 'REVERSE ENTRY'

Never infer transaction types.

Only use values stored in the database.

---

Financial Columns

Debit Amount

↓

debit_amount

Credit Amount

↓

credit_amount

Never derive debit or credit values.

Always use the stored database columns directly.

---

Prefer aggregation.

Examples

SUM(debit_amount)

SUM(credit_amount)

COUNT(*)

AVG(debit_amount)

AVG(credit_amount)

MIN(journal_date)

MAX(journal_date)

---

Grouping

Group by

journal_id

for complete accounting transactions.

Group by

name

for GL account summaries.

Group by

code

for account-code analysis.

Group by

trans_type

for accounting activity summaries.

Group by

journal_date

for period analysis.

---

Filtering

Always use exact values returned from

resolve_entities().

Never use wildcard matching.

Never use guessed values.

---

Journal Balance Validation

When the user requests

- unbalanced journals
- balanced journals
- journal validation
- accounting audit

aggregate by

journal_id

and compare

SUM(debit_amount)

and

SUM(credit_amount)

Never compare individual journal lines.

---

Revenue Analysis

Use

credit_amount

for revenue totals unless the user explicitly requests debit-side revenue postings.

---

Expense and Inventory Analysis

Use

debit_amount

for inventory and expense postings unless the user explicitly requests credit-side postings.

---

Journal Details

Return row-level journal lines only when the user explicitly requests

- journal details
- accounting entries
- transaction lines

Otherwise prefer summarized results.

---

Ordering

For detailed journal entries

ORDER BY

journal_date,
journal_id,
id

For aggregated results

ORDER BY

the aggregated metric in descending order unless another ordering is requested.