# Entity Resolution

Always resolve inventory entities before generating SQL.

Call

resolve_entities()

for

Item ID

Item Description

Category

SubCategory

Vendor

Building

Warehouse

Store

Never guess values.

Always use the resolved entity returned by the resolver.

Example

User

Show inventory for Ashley Furniture

↓

resolve_entities()

↓

Venddor

Ashley Furniture

↓

Generate SQL using the resolved value.

Never use fuzzy SQL matching.

Entity resolution always occurs before SQL generation.