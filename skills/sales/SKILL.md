---
name: sales
description: Handles sales analytics questions over the ConsolidateData_PBI table. Resolves business entities, applies sales business rules, generates read-only SQL, executes SQL, and prepares structured responses.
---

# Sales Domain Skill

This skill is responsible for answering every sales-related question.

Examples include:

- Sales
- Company performance
- Store performance
- Region performance
- Salesperson performance
- Traffic
- Average Ticket
- Gross Margin
- Effective Margin
- Financing
- Bedding
- FPP
- Delivery
- Credit Applications
- Discounts
- Goals
- YOY metrics
- SPGI
- UPS
- Sales rankings

The underlying table is:

ConsolidateData_PBI

---

# Workflow

Always follow this sequence.

## Step 1

Understand the user's request.

Determine:

- requested metrics
- requested entities
- requested aggregation
- requested date
- ranking requirements
- comparison requirements

---

## Step 2

Determine whether the request is ambiguous.

Examples:

- missing required dates
- missing company/store when required
- ambiguous salesperson
- conflicting filters

If additional information is required:

Call:

need_clarification()

Do not continue until resumed.

---

## Step 3

Resolve business entities.

Always call

resolve_entities()

before generating SQL whenever the user references business entities such as:

- company
- store
- salesperson
- region

Do not guess entity names.

Use the resolved entities returned by the tool.

---

## Step 4

Apply Sales business rules.

See:

business_rules.md

---

## Step 5

Generate SQL.

See:

sql_generation.md

---

## Step 6

Execute SQL.

Use:

run_sql_query()

Never fabricate data.

---

## Step 7

Produce the final response.

Always return

{
  "sql_query": "...",
  "information": "..."
}

information must be written for business users.

Never expose implementation details.

Never expose internal reasoning.