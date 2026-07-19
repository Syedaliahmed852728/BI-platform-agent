---
name: general-ledger
description: Handles General Ledger journal analysis including journal entries, debit and credit transactions, revenue recognition, inventory postings, payment postings, accounting entries, GL accounts, journal balances, customer accounting activity and financial transaction auditing using AI_AccountsDetail.
---

# General Ledger Domain Skill

This skill answers every General Ledger (GL) and accounting journal related question.

Examples include

- Journal Entries
- Accounting Transactions
- Debit Entries
- Credit Entries
- General Ledger Accounts
- Revenue Recognition
- Inventory Journal Entries
- Payment Journal Entries
- Reverse Entries
- GL Account Activity
- Journal Audit
- Journal Balancing
- Customer Accounting Transactions
- Sale Accounting Details
- Accounting Breakdown
- Transaction History

Underlying tables

AI_AccountsDetail

---

# Workflow

Always follow this sequence.

## Step 1

Understand the user's request.

Determine

- requested customer
- requested company
- requested store
- requested journal
- requested invoice
- requested sale number
- requested GL account
- requested account code
- requested transaction type
- requested debit or credit activity
- requested journal date
- requested aggregation

---

## Step 2

Determine whether clarification is required.

Examples

- ambiguous customer
- ambiguous invoice
- ambiguous journal number
- ambiguous account
- unclear transaction request

If clarification is required

Ask the user for clarification.

Stop execution until resumed.

---

## Step 3

Resolve business entities.

Always call

resolve_entities()

before generating SQL whenever the user references

- Customer
- Invoice
- Sale Number
- Journal Number
- Store
- Company
- GL Account

Never guess entity names.

Always use resolved entities.

---

## Step 4

Determine the required accounting scope.

Use AI_AccountsDetail for

- journal entries
- accounting postings
- debit transactions
- credit transactions
- revenue entries
- inventory entries
- payment entries
- reverse entries
- GL account activity
- accounting audit
- journal balancing
- customer accounting transactions

---

## Step 5

Apply General Ledger business rules.

See

business_rules.md

---

## Step 6

Generate SQL.

See

sql_generation.md

---

## Step 7

Execute SQL.

Use

run_sql_query()

Never fabricate accounting information.

Never derive accounting entries that are not present in the ledger.

---

## Step 8

Produce the final response.

Always return

```json
{
    "sql_query":"...",
    "information":"..."
}
```

The information field must be business friendly.

Never expose internal implementation details.

Never expose internal reasoning.