# Examples

## Example 1

User

Show pending orders for Ashley Furniture.

Workflow

resolve_entities()

↓

Generate SQL

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"Ashley Furniture currently has ... pending purchase orders."
}

---

## Example 2

User

Show overdue purchase orders.

↓

Business Rule

↓

PO_Rec_Date IS NULL

AND

Days_Overdue > 0

↓

Generate SQL

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"There are ... overdue purchase orders awaiting receipt."
}

---

## Example 3

User

How many units are currently on order for Tempur-Pedic?

↓

resolve_entities()

↓

Generate SQL

↓

Use

PO_Qty_On_Order

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"Tempur-Pedic currently has ... units remaining on order."
}

---

## Example 4

User

Show received orders last month.

↓

Business Rule

↓

PO_Rec_Date IS NOT NULL

↓

Generate SQL

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The following purchase orders were received during the previous month."
}

---

## Example 5

User

Top vendors by ordered quantity this year.

↓

resolve_entities()

↓

Generate SQL

↓

Aggregate

SUM(PO_Ordered_Qty)

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The top vendors by ordered quantity this year are ..."
}

---

## Example 6

User

Show orders due next week.

↓

Generate SQL

↓

Use

Due_Date

↓

Exclude

Due_Date <= '1970-01-01'

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The following purchase orders are scheduled for delivery next week."
}