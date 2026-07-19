# Purchase Order Business Rules

These rules are mandatory.

---

## Primary Date

Use

Order_Date

for purchase order date analysis unless the user explicitly requests another purchase order date.

---

Available date columns

Order_Date

Due_Date

PO_Rec_Date

---

## Legacy Due Dates

Some rows contain

1969-12-31

These represent invalid historical data.

Whenever the query involves

- overdue
- due date
- delivery date
- expected delivery
- date range using Due_Date

Always exclude

Due_Date <= '1970-01-01'

---

## Order Status

Determine order status ONLY from

PO_Rec_Date

---

Received

PO_Rec_Date IS NOT NULL

---

Pending

PO_Rec_Date IS NULL

---

Partially Received

PO_Rec_Date IS NULL

AND

PO_Rec_Qty > 0

AND

PO_Rec_Qty < PO_Ordered_Qty

Although current data does not contain partial receipts, always preserve this business rule.

---

## Overdue Orders

Use the precomputed

Days_Overdue

Never calculate overdue days manually.

Overdue Pending Orders

PO_Rec_Date IS NULL

AND

Days_Overdue > 0

---

Received orders are never overdue.

---

## Pending Quantity

Always use

PO_Qty_On_Order

Never calculate

Ordered - Received

---

## Vendor Names

Vendor names may contain trailing spaces.

Always trim vendor names before comparison.

Use

LTRIM()

RTRIM()

or equivalent.

---

## Hidden Columns

Never display

Id

Company_Id

unless the user explicitly requests them.

---

## Null Values

Never display NULL or empty values in user-facing results.

---

## Aggregation

Prefer aggregated answers.

Use

SUM()

COUNT()

AVG()

where appropriate.

Return row-level details only when explicitly requested.

---

## Read Only

Generate only

SELECT

statements.