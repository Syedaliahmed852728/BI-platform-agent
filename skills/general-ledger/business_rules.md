# General Ledger Business Rules

These rules are mandatory.

---

# Table Selection

All General Ledger, Journal Entry, Accounting Posting, Debit/Credit, Revenue Recognition, Inventory Posting and Payment questions

↓

AI_AccountsDetail

---

# Primary Date

Primary Date

journal_date

Always use

journal_date

for date filtering.

---

# Journal Grouping

A single accounting transaction consists of multiple journal lines.

Always use

journal_id

to identify a complete accounting transaction.

Never treat an individual row as a complete transaction unless the user explicitly requests journal line details.

---

# Transaction Types

Use

trans_type

to identify accounting activity.

Supported transaction types include

PAYMENT

↓

Customer payment and settlement entries.

---

REVENUE

↓

Revenue recognition entries.

---

INVENTORY

↓

Inventory and Cost of Goods Sold postings.

---

REVERSE ENTRY

↓

Accounting reversal entries.

Never infer additional transaction types.

Only use values stored in the database.

---

# Debit and Credit Rules

Debit entries

↓

dc_type = 'D'

Credit entries

↓

dc_type = 'C'

Normalize dc_type before comparison because stored values may contain lowercase letters.

Always compare using

UPPER(dc_type)

---

# Financial Amounts

Debit Amount

↓

debit_amount

Credit Amount

↓

credit_amount

Never calculate debit or credit amounts from other columns.

Always use the stored values.

---

# Journal Balance

A journal transaction should normally balance.

Group by

journal_id

when validating complete accounting transactions.

Never validate balancing using individual journal lines.

---

# Revenue Analysis

Revenue analysis should use

trans_type = 'REVENUE'

unless the user explicitly requests another accounting transaction type.

---

# Inventory Analysis

Inventory accounting should use

trans_type = 'INVENTORY'

---

# Payment Analysis

Payment accounting should use

trans_type = 'PAYMENT'

---

# Reverse Entries

Accounting reversals should use

trans_type = 'REVERSE ENTRY'

---

# GL Account

GL Account Name

↓

name

GL Account Code

↓

code

Prefer

code

when performing exact account filtering.

Display the account name whenever available.

---

# Customer Information

Customer information is stored inside

description

and

desc2

Never parse customer names if a resolved entity is available.

Always use resolved entities.

---

# Aggregation

Prefer aggregation.

Use

SUM()

COUNT()

AVG()

where appropriate.

Return journal line details only when explicitly requested.

---

# SQL Safety

Generate only

SELECT

statements.

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