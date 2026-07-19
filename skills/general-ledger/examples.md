# Examples

## Example 1

User

Show all journal entries for invoice 11103250296.

↓

resolve_entities()

↓

Use

AI_AccountsDetail

↓

Filter

journal_no

↓

run_sql_query()

↓

```json
{
    "sql_query":"...",
    "information":"The accounting journal entries for the requested invoice are shown below."
}
```

---

## Example 2

User

Show total revenue recognized yesterday.

↓

Use

AI_AccountsDetail

↓

trans_type = 'REVENUE'

↓

Aggregate

SUM(credit_amount)

↓

run_sql_query()

↓

```json
{
    "sql_query":"...",
    "information":"The total revenue recognized for the selected period is shown below."
}
```

---

## Example 3

User

Show all payment journal entries for customer John Smith.

↓

resolve_entities()

↓

Use

AI_AccountsDetail

↓

trans_type = 'PAYMENT'

↓

run_sql_query()

↓

```json
{
    "sql_query":"...",
    "information":"The payment journal entries for the requested customer are shown below."
}
```

---

## Example 4

User

Show inventory accounting entries for invoice 22204250649.

↓

resolve_entities()

↓

Use

AI_AccountsDetail

↓

trans_type = 'INVENTORY'

↓

run_sql_query()

↓

```json
{
    "sql_query":"...",
    "information":"The inventory-related journal entries for the requested invoice are shown below."
}
```

---

## Example 5

User

Show revenue by GL account.

↓

Use

AI_AccountsDetail

↓

trans_type = 'REVENUE'

↓

Aggregate

SUM(credit_amount)

GROUP BY

name

↓

run_sql_query()

↓

```json
{
    "sql_query":"...",
    "information":"Revenue has been summarized by General Ledger account."
}
```

---

## Example 6

User

Show journals that contain reverse entries.

↓

Use

AI_AccountsDetail

↓

trans_type = 'REVERSE ENTRY'

↓

run_sql_query()

↓

```json
{
    "sql_query":"...",
    "information":"The following journal transactions contain accounting reversal entries."
}
```

---

## Example 7

User

Show journal activity for GL account Capital Surplus.

↓

resolve_entities()

↓

Use

AI_AccountsDetail

↓

Filter

name

↓

run_sql_query()

↓

```json
{
    "sql_query":"...",
    "information":"The journal activity for the requested General Ledger account is shown below."
}
```

---

## Example 8

User

Show debit and credit totals by transaction type.

↓

Use

AI_AccountsDetail

↓

Aggregate

SUM(debit_amount)

SUM(credit_amount)

GROUP BY

trans_type

↓

run_sql_query()

↓

```json
{
    "sql_query":"...",
    "information":"Debit and credit totals have been summarized by accounting transaction type."
}
```

---

## Example 9

User

Show journals that are not balanced.

↓

Use

AI_AccountsDetail

↓

Group by

journal_id

↓

Compare

SUM(debit_amount)

SUM(credit_amount)

↓

run_sql_query()

↓

```json
{
    "sql_query":"...",
    "information":"The following journal transactions are not balanced."
}
```

---

## Example 10

User

Show accounting activity for sale number 20282030.

↓

resolve_entities()

↓

Use

AI_AccountsDetail

↓

Filter

journal_no

↓

run_sql_query()

↓

```json
{
    "sql_query":"...",
    "information":"The accounting activity associated with the requested sale number is shown below."
}
```