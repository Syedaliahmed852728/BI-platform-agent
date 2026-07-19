# Examples

## Example 1

User

Show all Bedroom inventory.

Workflow

resolve_entities()

↓

Generate SQL

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"There are ... bedroom inventory items currently available."
}

---

## Example 2

User

Where is Item 73378?

↓

resolve_entities()

↓

Generate SQL

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"Item 73378 is located in Building 111 (Warehouse)."
}

---

## Example 3

User

Show on-hand inventory for Vendor Ashley.

↓

resolve_entities()

↓

Status Rule

↓

Generate SQL

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The vendor currently has ... on-hand inventory items."
}

---

## Example 4

User

Show available lamps.

↓

resolve_entities()

↓

Category Resolution

↓

Status Rule

↓

Generate SQL

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"There are ... available lamp items in inventory."
}

---

## Example 5

User

Show inventory by building.

↓

Generate SQL

↓

Building Rule

↓

Automatically include

Building

loc_type

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"Inventory is distributed across the following buildings and location types."
}