---
name: purchase-orders
description: Handles purchase order analytics, vendor performance, procurement reporting, pending orders, received orders, overdue orders and purchasing analytics using the AI_PO_Data table.
---

# Purchase Orders Domain Skill

This skill answers every purchase order related question.

Examples include:

- Purchase Orders
- Vendor Performance
- Pending Orders
- Received Orders
- Open Orders
- Overdue Orders
- Purchase Quantity
- Pending Quantity
- Item Orders
- SKU Orders
- Delivery Due Dates
- Procurement Analytics

Underlying table

AI_PO_Data

---

# Workflow

Always follow this sequence.

## Step 1

Understand the user's request.

Determine:

- requested vendors
- requested items
- requested dates
- requested status
- requested quantities
- requested overdue information
- requested aggregation

---

## Step 2

Determine whether clarification is required.

Examples

- ambiguous vendor
- ambiguous SKU
- conflicting date filters
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

- Vendor
- Supplier
- Item
- SKU
- Company

Never guess entity names.

Always use the resolved entities.

---

## Step 4

Apply Purchase Order business rules.

See

business_rules.md

---

## Step 5

Generate SQL.

See

sql_generation.md

---

## Step 6

Execute SQL.

Use

run_sql_query()

Never fabricate procurement information.

---

## Step 7

Produce the final response.

Always return

{
    "sql_query":"...",
    "information":"..."
}

The information field must be business friendly.

Never expose implementation details.

Never expose internal reasoning.