# Delivery Business Rules

These rules are mandatory.

---

# Table Selection

All delivery, routing and logistics questions

↓

AI_DeliveryData

Always use

AI_DeliveryData

for delivery-related requests.

---

# Primary Date

Primary Date

↓

delivery_date

Always use

delivery_date

for date filtering unless the user explicitly requests another date field.

---

# Table Granularity

Each row represents

One Item

on

One Customer Order

assigned to

One Truck Stop.

Multiple rows may belong to

- the same order
- the same customer
- the same truck stop

Never assume each row represents a unique order.

---

# Order Rules

An order is uniquely identified by

ordernumber

When users ask for

- number of orders
- scheduled orders
- delivered orders
- cancelled orders
- rescheduled orders

Always count

COUNT(DISTINCT ordernumber)

Never use

COUNT(*)

---

# Customer Rules

A customer is uniquely identified by

customer_id

When users ask

- number of customers
- scheduled customers
- delivered customers

Always count

COUNT(DISTINCT customer_id)

Never use

COUNT(*)

---

# Truck Stop Rules

A truck stop is uniquely identified by

truck_no

+

stop_no

When users ask

- number of stops
- truck stops
- stops by truck

Always count unique truck/stop combinations.

Never count rows.

---

# Item Rules

Each row represents

One Item

Item level metrics may be aggregated directly.

Examples

COUNT(*)

SUM(item_qty)

SUM(item_sale_price)

SUM(item_retail)

---

# Order Level Metrics

The following columns belong to the entire order and are repeated for every item.

- pieces
- order_sale_price
- order_volume
- order_weight
- distance
- travel_time
- unload_time

Never aggregate these directly.

Always aggregate at the order level first.

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

Previous Delivery

previous_delivery_date

contains the previous scheduled delivery date.

Use only when the user explicitly requests previous deliveries or rescheduled deliveries.

---

# Delivery Windows

Morning

↓

08:00 - 11:59

---

Afternoon

↓

12:00 - 16:59

---

Evening

↓

17:00 onwards

Use

time_window_start

and

time_window_end

when filtering delivery windows.

---

# Store Rules

Display

storeName

Never display

store_id

unless explicitly requested.

---

# Customer Rules

Display

customer_name

Never display

customer_id

unless explicitly requested.

---

# Order Rules

Display

ordernumber

when returning order-level details.

---

# Item Rules

Display

item_description

instead of

item_no

unless the user explicitly requests item numbers.

---

# Geographic Rules

City

↓

city

State

↓

state

Zip Code

↓

zipcode

Use these fields for location-based delivery questions.

---

# Aggregation

Prefer aggregation.

Use

SUM()

COUNT()

AVG()

where appropriate.

Return row-level delivery details only when explicitly requested.

---

Generate only

SELECT

statements.