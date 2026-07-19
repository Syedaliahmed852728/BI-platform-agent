# Entity Resolution

Always resolve business entities before generating SQL.

Call

resolve_entities()

for

Vendor

Supplier

Item

SKU

Company

Never guess values.

Always use the resolved entity.

Example

User

Show Ashley pending orders

↓

resolve_entities()

↓

Vendor_Name

ASHLEY FURNITURE INDUSTRIES,INC.

↓

Generate SQL using the resolved vendor.

Never use fuzzy SQL matching.

Entity resolution always happens before SQL generation.