# Sales Business Rules

These rules are mandatory.

## Date

Always use:

From_Date

Never use:

- To_Date
- iMonth
- iYear

---

Reuse the previous conversation date whenever the user does not specify a new one.

---

If no date is supplied and no previous date exists:

Use the current data.

---

## Status

Default:

STATUS = 'W'

unless the user specifies otherwise.

---

## Levels

Default

Level = 0

Company

Level = 0

Store

Level = 1

Region

Level = 2

Region without Outlet

Level = 3

Company with Outlet

Level = 4

Salesperson

Level = 5

Company without Outlet

Level = 6

Grand Total

Level = 7

---

Salesperson queries

Exclude

Name containing

HOU

---

eCommerce

444

445

Exclude them only if the user requests

"exclude ecommerce"

Include only them if the user requests

"ecommerce"

---

Percentages

Always use AVG()

Always use the word

approx

both in aliases and user response.

---

Average Sales

Means

Average Ticket Sale

---

Ranking

If the user says

Top

without a number

Return Top 3.

---

String Columns

Exclude

NULL

empty

None

values

---

LIKE

Never use LIKE.

Always use exact comparisons.

---

Read Only

Only SELECT queries are allowed.