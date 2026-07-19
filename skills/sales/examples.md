# Examples

## Example 1

User

Top stores by sales last month

Workflow

resolve_entities()

↓

generate SQL

↓

run_sql_query()

↓

Return

{
  "sql_query":"...",
  "information":"The top 3 stores by sales last month were ..."
}

---

## Example 2

User

How did John perform?

↓

resolve_entities("John")

↓

multiple matches

↓

need_clarification()

---

## Example 3

User

Average ticket for Ashley Manchester yesterday

↓

resolve_entities()

↓

generate SQL

↓

run_sql_query()

↓

{
 "sql_query":"...",
 "information":"The approximate average ticket for Ashley Store Manchester yesterday was ..."
}