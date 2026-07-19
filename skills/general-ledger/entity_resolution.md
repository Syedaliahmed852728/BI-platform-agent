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

Journal Number

GL Account

Account Code

Never guess values.

Always use the resolved entities.

---

# Entity Mapping

Customer

↓

description

or

desc2

depending on the selected search field.

---

Invoice

↓

journal_no

---

Sale Number

↓

journal_no

---

Journal Number

↓

journal_id

---

GL Account

↓

name

---

Account Code

↓

code

---

Store

↓

name

when the account name contains a store-specific account such as

- Sales Revenue- ASHLEY STORE MANCHESTER
- Cost of Goods Sold-ASHLEY STORE NEWINGTON
- Finance Fee- ASHLEY STORE NEWINGTON

Always resolve the store before generating SQL.

---

Company

↓

Resolve first.

Use the resolved value only if the corresponding account or description references the company.

Never invent company names.

---

# Exact Matching

Never perform wildcard matching.

Never perform fuzzy SQL matching.

Always use the exact values returned by

resolve_entities().

---

# Multiple Entities

If the user mentions multiple entities

Examples

- multiple customers
- multiple invoices
- multiple GL accounts

resolve every entity before generating SQL.

---

Entity resolution always occurs before SQL generation.