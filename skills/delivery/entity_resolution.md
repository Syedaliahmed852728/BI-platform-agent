# Entity Resolution

Always resolve business entities before generating SQL.

Call

resolve_entities()

for

Customer

Store

Truck

Order

Item

City

State

Never guess values.

Always use the resolved entities.

---

Examples

Customer

↓

customer_name

---

Store

↓

storeName

---

Truck

↓

truck_no

---

Order

↓

ordernumber

---

Item

↓

item_no

or

item_description

depending on the user's request.

---

City

↓

city

---

State

↓

state

---

Entity resolution always occurs before SQL generation.

---

Never use wildcard matching.

Never infer entity names.

Always use the exact values returned by

resolve_entities().

---

If multiple entities are resolved for the same user input

Call

need_clarification()

before generating SQL.

---

Resolve entities before applying any business rules or SQL filters.