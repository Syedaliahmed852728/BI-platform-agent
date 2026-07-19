---
name: delivery
description: Handles delivery scheduling, truck routing, customer deliveries, delivery operations, stops, routes, delivery windows, scheduled deliveries, items, pieces, volume, weight and delivery tracking using AI_DeliveryData.
---

# Delivery Domain Skill

This skill answers every delivery and logistics related question.

Examples include

- Scheduled Deliveries
- Delivery Schedule
- Truck Schedule
- Truck Stops
- Customer Deliveries
- Delivery Routes
- Delivery Windows
- Delivery Status
- Delivered Orders
- Pending Deliveries
- Rescheduled Deliveries
- Cancelled Deliveries
- Truck Load
- Pieces by Truck
- Volume by Truck
- Weight by Truck
- Store Deliveries
- Customer Orders
- Order Items
- Delivery Performance

Underlying table

AI_DeliveryData

---

# Workflow

Always follow this sequence.

## Step 1

Understand the user's request.

Determine

- requested company
- requested store
- requested customer
- requested truck
- requested stop
- requested order
- requested item
- requested city
- requested state
- requested delivery date
- requested delivery window
- requested delivery status
- requested delivery type
- requested aggregation

---

## Step 2

Determine whether clarification is required.

Examples

- ambiguous customer
- ambiguous store
- ambiguous truck
- ambiguous order
- missing delivery date
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
- Store
- Truck
- Order
- Item
- City

Never guess entity names.

Always use resolved entities.

---

## Step 4

Determine the requested business objective.

Examples include

- Delivery Schedule
- Truck Schedule
- Customer Deliveries
- Delivery Status
- Truck Stops
- Orders
- Items
- Pieces
- Volume
- Weight
- Sales Value
- Store Deliveries
- Route Information

Use

AI_DeliveryData

for every delivery-related request.

---

## Step 5

Apply Delivery business rules.

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

Never fabricate delivery information.

Always retrieve information from the database.

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