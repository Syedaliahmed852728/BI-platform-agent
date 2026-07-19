# Inventory Business Rules

These rules are mandatory.

---

## Primary Date

Always use

Location Date

for inventory date questions.

Never substitute another date column unless the user explicitly requests it.

---

## Status Rules

Apply Status filters ONLY using the following mappings.

"in stock"

"items to sell"

"available to sell"

↓

Status = 'AVAILABLE'

---

"on hand"

"items on hand"

"on-hand inventory"

↓

Status IN

AVAILABLE

NAILED DOWN

DAMAGED

---

All other wording

↓

Do NOT apply a Status filter.

---

## Item Search Priority

Always resolve inventory items using this hierarchy.

1. item_cat

2. Category

3. SubCategory

Only ONE of these columns should be used in the final WHERE clause.

---

If the user asks for

Bedroom

Living Room

Dining Room

Office

↓

Use

item_cat

---

If the user asks for

Lamp

Sofa

Chair

Table

↓

Use

Category

---

If the user asks for the most specific product type

↓

Use

SubCategory

---

## Vendor

Always use

Venddor

Note

The physical column name intentionally contains a double d.

Never rename it.

---

## Building Rule

Whenever Building appears in

SELECT

GROUP BY

WHERE

also include

loc_type

---

## Location Questions

If the user asks

Where is Item X?

Return only

Building

loc_type

Do not include

Aisle

Level

Bay

Quantity

unless explicitly requested.

---

## Aggregation

Prefer aggregated answers.

Use

SUM(Quantity)

GROUP BY

where appropriate.

Return row-level details only when the user explicitly requests individual records.

---

## Read Only

Only SELECT statements are permitted.