---
name: inventory
description: Handles inventory analytics, inventory lookup, warehouse locations, stock availability, product categories, vendors and purchase order information using the AIData_Inventory table.
---

# Inventory Domain Skill

This skill answers every inventory-related question.

Examples include:

- Inventory lookup
- Item search
- SKU lookup
- Product availability
- Warehouse inventory
- Store inventory
- Vendor inventory
- Building inventory
- Category inventory
- SubCategory inventory
- Item location
- Quantity
- Cost
- Selling Price
- Purchase Orders
- Inventory Status

Underlying table

AIData_Inventory

---

# Workflow

Always follow this sequence.

## Step 1

Understand the user's request.

Determine:

- requested items
- requested categories
- requested vendors
- requested buildings
- requested locations
- requested inventory status
- requested dates
- requested aggregation

---

## Step 2

Determine whether clarification is required.

Examples:

- ambiguous item
- multiple vendors with same name
- unclear inventory request
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

- Item
- SKU
- Vendor
- Category
- SubCategory
- Building
- Warehouse
- Store

Never guess entity names.

---

## Step 4

Apply Inventory business rules.

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

Never fabricate inventory information.

---

## Step 7

Produce the final response.

Always return

{
    "sql_query":"...",
    "information":"..."
}

information must be business friendly.

Do not expose implementation details.

Do not expose internal reasoning.