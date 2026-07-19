from business.entity_config.models import DomainConfig, EntityField, TableConfig


delivery = DomainConfig(
    name="delivery",
    description="""
Delivery scheduling, route planning, truck management,
last-mile logistics, customer deliveries, delivery tracking,
scheduled deliveries, stops, items, pieces, volume,
weight and delivery performance analytics.
""",
    tables=[
        TableConfig(
            table_name="AI_DeliveryData",
            description="""
Primary delivery scheduling table.

Contains every scheduled delivery item.

Each row represents one item on a customer order assigned
to a truck stop.

Supports operational reporting including:

- Scheduled deliveries
- Truck routing
- Stops
- Customers
- Delivery windows
- Delivery confirmation
- Items delivered
- Pieces
- Volume
- Weight
- Store performance
""",
            primary_date_column="delivery_date",
            default_filters={},
            entity_rules={
                "table_grain": "order_item",
                "order_identifier": "ordernumber",
                "stop_identifier": [
                    "truck_no",
                    "stop_no",
                ],
                "delivery_status_mapping": {
                    "delivered": {
                        "delivery_confirmed": 1,
                    },
                    "not_delivered": {
                        "delivery_confirmed": [0, None],
                    },
                    "scheduled": {},
                    "cancelled": {
                        "cancellation_date": "NOT NULL",
                    },
                    "rescheduled": {
                        "rescheduled_date": "NOT NULL",
                    },
                },
                "delivery_type_mapping": {
                    "regular": "R",
                    "special": "S",
                },
                "exchange_mapping": {
                    "exchange": "E",
                    "non_exchange": "",
                },
                "store_stop_mapping": {
                    "store_stop": 1,
                    "customer_stop": 0,
                },
                "ecommerce_store_ids": [444, 445],
                "time_window_mapping": {
                    "morning": ("08:00:00", "11:59:59"),
                    "afternoon": ("12:00:00", "16:59:59"),
                    "evening": ("17:00:00", "23:59:59"),
                },
                "hidden_columns": [
                    "company_id",
                    "customer_id",
                    "store_id",
                ],
            },
            searchable_fields=[
                EntityField(
                    entity_type="company",
                    column="company_id",
                    aliases=[
                        "company",
                        "business",
                    ],
                    priority=100,
                    description="Company.",
                ),
                EntityField(
                    entity_type="store",
                    column="storeName",
                    aliases=[
                        "store",
                        "branch",
                        "location",
                        "warehouse",
                    ],
                    priority=100,
                    description="Delivery store.",
                ),
                EntityField(
                    entity_type="customer",
                    column="customer_name",
                    aliases=[
                        "customer",
                        "customer name",
                        "client",
                    ],
                    priority=100,
                    exact_match_only=False,
                    description="Customer name.",
                ),
                EntityField(
                    entity_type="order",
                    column="ordernumber",
                    aliases=[
                        "order",
                        "order number",
                        "sales order",
                        "delivery order",
                    ],
                    priority=100,
                    description="Customer order number.",
                ),
                EntityField(
                    entity_type="truck",
                    column="truck_no",
                    aliases=[
                        "truck",
                        "truck number",
                        "vehicle",
                        "delivery truck",
                    ],
                    priority=98,
                    description="Truck number.",
                ),
                EntityField(
                    entity_type="stop",
                    column="stop_no",
                    aliases=[
                        "stop",
                        "stop number",
                        "delivery stop",
                        "route stop",
                    ],
                    priority=96,
                    description="Truck stop.",
                ),
                EntityField(
                    entity_type="item",
                    column="item_no",
                    aliases=[
                        "item",
                        "sku",
                        "product",
                        "item id",
                        "product id",
                    ],
                    priority=95,
                    description="Inventory item.",
                ),
                EntityField(
                    entity_type="item_description",
                    column="item_description",
                    aliases=[
                        "item description",
                        "product",
                        "product name",
                    ],
                    priority=94,
                    exact_match_only=False,
                    description="Item description.",
                ),
                EntityField(
                    entity_type="city",
                    column="city",
                    aliases=[
                        "city",
                    ],
                    priority=90,
                    description="Customer city.",
                ),
                EntityField(
                    entity_type="state",
                    column="state",
                    aliases=[
                        "state",
                    ],
                    priority=88,
                    description="Customer state.",
                ),
                EntityField(
                    entity_type="zipcode",
                    column="zipcode",
                    aliases=[
                        "zip",
                        "zipcode",
                        "postal code",
                    ],
                    priority=85,
                    description="Customer ZIP code.",
                ),
                EntityField(
                    entity_type="delivery_type",
                    column="delivery_type",
                    aliases=[
                        "regular delivery",
                        "special delivery",
                        "delivery type",
                    ],
                    searchable=False,
                    priority=80,
                    description="Delivery type.",
                ),
                EntityField(
                    entity_type="delivery_status",
                    column="delivery_confirmed",
                    aliases=[
                        "delivered",
                        "not delivered",
                        "scheduled",
                        "cancelled",
                        "rescheduled",
                    ],
                    searchable=False,
                    exact_match_only=False,
                    priority=80,
                    description="Delivery status.",
                ),
            ],
        ),
    ],
)
