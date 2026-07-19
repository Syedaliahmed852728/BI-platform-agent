# SQL Generation

Generate ANSI-compatible SQL.

Only SELECT statements.

Never generate

INSERT

UPDATE

DELETE

ALTER

DROP

CREATE

MERGE

EXEC

TRUNCATE

---

Never use

SELECT *

Always select only the required columns.

---

Use business-friendly aliases.

---

Always use

delivery_date

as the primary date column unless the user explicitly requests another date field.

---

# Counting Rules

When the user requests

Number of Orders

Use

COUNT(DISTINCT ordernumber)

Never use

COUNT(*)

---

When the user requests

Number of Customers

Use

COUNT(DISTINCT customer_id)

Never use

COUNT(*)

---

When the user requests

Number of Trucks

Use

COUNT(DISTINCT truck_no)

---

When the user requests

Number of Stops

Treat a stop as

truck_no

+

stop_no

Count unique truck/stop combinations.

Never count table rows.

---

# Item Level Metrics

The following columns may be aggregated directly.

item_qty

item_sale_price

item_retail

COUNT(*)

SUM()

AVG()

may be used.

---

# Order Level Metrics

The following columns belong to the entire order and are repeated for every item.

pieces

order_sale_price

order_volume

order_weight

distance

travel_time

unload_time

Never aggregate these columns directly.

Aggregate at the order level first.

---

# Delivery Status

Delivered

↓

delivery_confirmed = 1

---

Scheduled / Not Delivered

↓

delivery_confirmed IS NULL

OR

delivery_confirmed = 0

---

Cancelled

↓

cancellation_date IS NOT NULL

---

Rescheduled

↓

rescheduled_date IS NOT NULL

---

# Time Windows

Use

time_window_start

and

time_window_end

for delivery window filtering.

---

# Entity Filtering

Never use wildcard matching.

Always use exact values returned from

resolve_entities().

---

# Result Formatting

Prefer aggregation.

Use

SUM()

COUNT()

AVG()

where appropriate.

Return row-level delivery information only when explicitly requested.

---

Never expose

company_id

customer_id

store_id

unless explicitly requested.

Prefer displaying

storeName

customer_name

item_description

instead of their identifiers.