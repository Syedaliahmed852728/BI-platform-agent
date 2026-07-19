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

Always select only required columns.

---

Use business-friendly aliases.

---

Always apply the correct Level filter.

Accounts Receivable

LEVEL

Unearned Revenue

Level

Never expose these columns.

---

Use the correct primary date.

InvoiceDate

for Accounts Receivable.

OrderDate

for Unearned Revenue.

---

Prefer aggregation.

Examples

SUM(Balance)

SUM(InvoiceSales)

SUM(TotalPaid)

SUM(Unearned_Revenue)

SUM(Revenue_Earned)

SUM(Advance_Deposit_Received)

COUNT(*)

AVG(Balance)

AVG(Unearned_Revenue)

---

Never calculate

Balance

Unearned Revenue

Revenue Earned

Outstanding Amount

These are already stored.

---

Never use wildcard matching.

Always use exact values returned from resolve_entities().