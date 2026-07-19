# SQL Generation

Generate ANSI-compatible SQL.

Only SELECT statements.

Never generate

INSERT

UPDATE

DELETE

MERGE

DROP

ALTER

TRUNCATE

EXEC

CREATE

---

Always fully qualify column names whenever ambiguity exists.

---

Never use

SELECT *

Always select only required columns.

---

Always generate readable SQL.

Example

SELECT
    Company_Name,
    SUM(Sales) AS TotalSales
FROM ConsolidateData_PBI
WHERE ...
GROUP BY Company_Name

---

Percentages

Always use AVG()

---

Company names

Exact equality

Store names

Exact equality

Salesperson names

Exact equality

Never use LIKE.

---

Use aliases that business users understand.