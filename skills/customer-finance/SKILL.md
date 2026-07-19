---
name: customer-finance
description: Handles customer financial analytics including Accounts Receivable, Unearned Revenue, customer balances, invoices, sales orders, deposits, outstanding receivables and delivery-related financial obligations using AI_AccountReceivable and AI_UnearnedRevenue.
---

# Customer Finance Domain Skill

This skill answers every customer finance related question.

Examples include

- Accounts Receivable
- Outstanding Balances
- Customer Balances
- Invoice Analysis
- Customer Payments
- Unearned Revenue
- Revenue Earned
- Advance Deposits
- Sales Orders
- Outstanding Obligations
- Delivery Status
- Customer Financial Summary

Underlying tables

AI_AccountReceivable

AI_UnearnedRevenue

---

# Workflow

Always follow this sequence.

## Step 1

Understand the user's request.

Determine

- requested customer
- requested company
- requested store
- requested invoice
- requested sales order
- requested financial metric
- requested delivery status
- requested date
- requested aggregation

---

## Step 2

Determine whether clarification is required.

Examples

- ambiguous customer
- ambiguous company
- unclear invoice
- missing required information

If clarification is required

Call

need_clarification()

Stop execution until resumed.

---

## Step 3

Resolve business entities.

Always call

resolve_entities()

before generating SQL whenever the user references

- Customer
- Company
- Store
- Sales Order
- Invoice

Never guess entity names.

Always use resolved entities.

---

## Step 4

Determine which table(s) are required.

Use

AI_AccountReceivable

when the request involves

- invoices
- receivables
- balances
- payments
- outstanding invoices
- invoice sales

Use

AI_UnearnedRevenue

when the request involves

- deposits
- advance payments
- revenue earned
- unearned revenue
- delivery obligations
- sales orders

If the request spans both business areas

Use both tables.

---

## Step 5

Apply Customer Finance business rules.

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

Never fabricate financial information.

---

## Step 8

Produce the final response.

Always return

{
    "sql_query":"...",
    "information":"..."
}

The information field must be business friendly.

Never expose internal implementation details.

Never expose internal reasoning.