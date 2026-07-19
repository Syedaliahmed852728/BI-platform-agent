# SQL Generation

Generate ANSI-compatible read-only SQL.

Only SELECT statements.

Never generate

INSERT

UPDATE

DELETE

DROP

ALTER

MERGE

TRUNCATE

CREATE

EXEC

---

Never use

SELECT *

Always select only the columns required to answer the question.

---

Prefer aggregation.

Use

SUM(Quantity)

COUNT(*)

AVG(Cost)

AVG(Price)

when appropriate.

---

Location queries

If the user only asks

Where is Item X?

Return

Building

loc_type

Do not return

Aisle

Level

Bay

Quantity

unless requested.

---

Whenever Building appears

also include

loc_type

---

Use business-friendly aliases.

Never expose internal column names unless the user explicitly asks.

---

Never use wildcard matching.

Always use exact comparisons using values returned from resolve_entities().