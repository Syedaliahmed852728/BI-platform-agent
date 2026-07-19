# SQL Generation

Generate ANSI-compatible SQL.

Only SELECT statements.

Never generate

INSERT

UPDATE

DELETE

MERGE

DROP

ALTER

TRUNCATE

EXEC

CREATE

---

Never use

SELECT *

Always project only the required columns.

---

Use business-friendly aliases.

---

Prefer aggregation.

Examples

SUM(PO_Ordered_Qty)

SUM(PO_Qty_On_Order)

COUNT(*)

AVG(Days_Overdue)

---

Never calculate

Pending Quantity

Use

PO_Qty_On_Order

directly.

---

Never calculate

Days Overdue

Use

Days_Overdue

directly.

---

Status must always be derived from

PO_Rec_Date

Never infer order status from

PO_Rec_Qty

except for the Partial Receipt rule.

---

Whenever the query involves

Due_Date

exclude

Due_Date <= '1970-01-01'

---

Vendor filters

Always trim whitespace before comparison.

---

Never expose hidden columns.

---

Never use wildcard matching.

Always use exact comparisons with values returned by resolve_entities().