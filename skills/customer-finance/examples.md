# Examples

## Example 1

User

Show customers with outstanding balances.

↓

resolve_entities()

↓

Use

AI_AccountReceivable

↓

LEVEL = 2

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The following customers have outstanding receivable balances."
}

---

## Example 2

User

Show total accounts receivable by store.

↓

Use

AI_AccountReceivable

↓

LEVEL = 1

↓

Aggregate

SUM(Balance)

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"Outstanding accounts receivable by store are shown below."
}

---

## Example 3

User

Show customers with unearned revenue.

↓

Use

AI_UnearnedRevenue

↓

Level = 0

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The following customers have advance payments that have not yet been fully earned."
}

---

## Example 4

User

Show company unearned revenue.

↓

Use

AI_UnearnedRevenue

↓

Level = 1

↓

Aggregate

SUM(Unearned_Revenue)

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"Company-level unearned revenue is shown below."
}

---

## Example 5

User

Compare Accounts Receivable with Unearned Revenue.

↓

Query

AI_AccountReceivable

↓

Query

AI_UnearnedRevenue

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The comparison between outstanding receivables and unearned revenue is summarized below."
}

---

## Example 6

User

Show orders that are partially delivered.

↓

Use

AI_UnearnedRevenue

↓

Revenue_Earned > 0

AND

Revenue_Earned < Total_Order_Value

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The following sales orders have been partially delivered."
}