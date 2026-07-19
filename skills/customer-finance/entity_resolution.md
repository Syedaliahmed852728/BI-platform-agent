# Entity Resolution

Always resolve business entities before generating SQL.

Call

resolve_entities()

for

Customer

Company

Store

Invoice

Sale Number

Sales Order

Never guess values.

Always use the resolved entities.

Examples

Customer

↓

CustomerName

or

Customer_Name

depending on the selected table.

Invoice

↓

SaleNumber

Sales Order

↓

So_no

Company

↓

Company

or

company_name

Store

↓

Store

or

profitcenter_name

Entity resolution always occurs before SQL generation.