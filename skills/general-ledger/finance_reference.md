# General Ledger Reference

## AI_AccountsDetail

Primary Date

journal_date

---

Journal ID

journal_id

---

Journal Type

journal_type

---

Journal Number

journal_no

---

Internal Journal Number

journal_no_new

---

Transaction Type

trans_type

---

GL Account Name

name

---

GL Account Code

code

---

Debit / Credit Indicator

dc_type

---

Debit Amount

debit_amount

---

Credit Amount

credit_amount

---

Description

description

---

Detailed Description

desc2

---

Posting Status

is_posted

---

Posting Year

post_year

---

Posting Month

post_month

---

Posted Date

postedDate

---

Posted By

postedBy

---

Table Type

table_type

---

File Name

filename

---

Transaction Categories

### PAYMENT

Customer payment, receivable settlement and payment-related journal entries.

---

### REVENUE

Revenue recognition journal entries.

---

### INVENTORY

Inventory movement and Cost of Goods Sold (COGS) journal entries.

---

### REVERSE ENTRY

Accounting reversal journal entries.

---

Accounting Direction

Debit

↓

dc_type = 'D'

Credit

↓

dc_type = 'C'

Always normalize using

UPPER(dc_type)

before comparison.

---

Journal Rules

A complete accounting transaction consists of all rows having the same

journal_id.

Individual rows represent journal lines, not complete accounting transactions.

---

Financial Columns

Debit Amount

↓

debit_amount

Credit Amount

↓

credit_amount

Never derive financial values.

Always use the stored database columns directly.

---

Common Analysis

- Journal Entry Details
- Journal Audit
- Debit Analysis
- Credit Analysis
- Revenue Posting Analysis
- Inventory Posting Analysis
- Payment Posting Analysis
- Reverse Entries
- GL Account Activity
- Account Balance Movement
- Customer Accounting History
- Transaction Breakdown