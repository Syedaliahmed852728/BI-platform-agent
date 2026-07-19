# Examples

## Example 1

User

Show today's scheduled deliveries.

↓

Use

AI_DeliveryData

↓

delivery_date = today

↓

COUNT(DISTINCT ordernumber) is NOT needed because the user requested delivery details.

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The scheduled deliveries for today are shown below."
}

---

## Example 2

User

How many orders are scheduled today?

↓

Use

AI_DeliveryData

↓

COUNT(DISTINCT ordernumber)

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The total number of scheduled delivery orders is shown below."
}

---

## Example 3

User

How many customers are scheduled for delivery tomorrow?

↓

Use

AI_DeliveryData

↓

COUNT(DISTINCT customer_id)

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The total number of customers scheduled for delivery is shown below."
}

---

## Example 4

User

Show Truck 1 customers.

↓

resolve_entities()

↓

Truck

↓

Use

AI_DeliveryData

↓

truck_no = resolved value

↓

Return

customer_name

delivery window

stop number

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The customers assigned to the requested truck are shown below."
}

---

## Example 5

User

How many stops does Truck 2 have?

↓

resolve_entities()

↓

Truck

↓

Count unique

truck_no + stop_no

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The number of scheduled stops for the requested truck is shown below."
}

---

## Example 6

User

Show deliveries from Manchester store.

↓

resolve_entities()

↓

Store

↓

Use

storeName

↓

Return delivery information.

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The deliveries scheduled from the requested store are shown below."
}

---

## Example 7

User

Show all items on order 11106260663.

↓

resolve_entities()

↓

Order

↓

Use

ordernumber

↓

Return

item_no

item_description

item_qty

item_sale_price

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The items included in the requested order are shown below."
}

---

## Example 8

User

Show the total sales value scheduled for Truck 3.

↓

resolve_entities()

↓

Truck

↓

Aggregate by order first.

↓

SUM(order_sale_price)

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The total scheduled sales value for the requested truck is shown below."
}

---

## Example 9

User

Show total scheduled volume by truck.

↓

Aggregate by order first.

↓

SUM(order_volume)

GROUP BY truck_no

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The scheduled delivery volume for each truck is shown below."
}

---

## Example 10

User

Show total scheduled weight by store.

↓

Aggregate by order first.

↓

SUM(order_weight)

GROUP BY storeName

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The scheduled delivery weight by store is shown below."
}

---

## Example 11

User

Which deliveries were rescheduled?

↓

Use

rescheduled_date IS NOT NULL

↓

Return

customer_name

ordernumber

delivery_date

rescheduled_date

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The rescheduled deliveries are shown below."
}

---

## Example 12

User

Which deliveries were cancelled?

↓

Use

cancellation_date IS NOT NULL

↓

Return

customer_name

ordernumber

delivery_date

cancellation_date

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The cancelled deliveries are shown below."
}

---

## Example 13

User

Show deliveries between 9 AM and 12 PM.

↓

Use

time_window_start

time_window_end

↓

Return scheduled deliveries.

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The deliveries scheduled within the requested delivery window are shown below."
}

---

## Example 14

User

Show delivered orders.

↓

Use

delivery_confirmed = 1

↓

Return delivery details.

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The confirmed deliveries are shown below."
}

---

## Example 15

User

Show pending deliveries.

↓

Use

delivery_confirmed IS NULL

OR

delivery_confirmed = 0

↓

Return delivery details.

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The scheduled deliveries that have not yet been confirmed are shown below."
}

---

## Example 16

User

Which customers have the highest scheduled delivery value?

↓

Aggregate by order first.

↓

SUM(order_sale_price)

GROUP BY customer_name

ORDER BY scheduled value DESC

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The customers with the highest scheduled delivery value are shown below."
}

---

## Example 17

User

Show the utilization of each truck.

↓

Aggregate by order first.

↓

Calculate

Total Orders

Total Stops

Total Pieces

Total Volume

Total Weight

per truck.

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The scheduled workload for each truck is summarized below."
}

---

## Example 18

User

Show the delivery schedule for customer John Smith.

↓

resolve_entities()

↓

Customer

↓

Return

delivery_date

truck_no

stop_no

delivery window

items

↓

run_sql_query()

↓

{
    "sql_query":"...",
    "information":"The scheduled deliveries for the requested customer are shown below."
}