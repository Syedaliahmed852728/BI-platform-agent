# Customer Finance Business Rules

These rules are mandatory.

---

# Table Selection

Accounts Receivable questions

↓

AI_AccountReceivable

Unearned Revenue questions

↓

AI_UnearnedRevenue

Questions involving both

↓

Query both tables.

---

# Date Columns

Accounts Receivable

Primary Date

InvoiceDate

Unearned Revenue

Primary Date

OrderDate

Always use the correct primary date.

---

# Accounts Receivable Level Rules

Company

LEVEL = 0

Store

LEVEL = 1

Customer

LEVEL = 2

Default

LEVEL = 2

Never display LEVEL.

---

# Unearned Revenue Level Rules

Company

Level = 1

Customer

Level = 0

Default

Level = 0

Never display Level.

---

# Accounts Receivable Metrics

Outstanding Amount

Balance

Invoice Amount

InvoiceSales

Paid Amount

TotalPaid

---

# Unearned Revenue Metrics

Order Value

Total_Order_Value

Advance Deposit

Advance_Deposit_Received

Earned Revenue

Revenue_Earned

Unearned Revenue

Unearned_Revenue

---

# Delivery Status

Not Delivered

DeliveredDate IS NULL

AND

Revenue_Earned = 0

---

Partially Delivered

Revenue_Earned > 0

AND

Revenue_Earned < Total_Order_Value

---

Fully Delivered

Revenue_Earned >= Total_Order_Value

---

Never derive financial values.

Always use database columns directly.

---

Prefer aggregation.

Use

SUM()

COUNT()

AVG()

where appropriate.

Return row-level data only when explicitly requested.

---

Generate only

SELECT

statements.