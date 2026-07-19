from business.entity_config.models import DomainConfig, EntityField, TableConfig


purchase_orders = DomainConfig(
    name="purchase_orders",
    description="""
Purchase Order reporting, vendor analysis, order tracking,
pending orders, received orders, overdue purchase orders,
SKU level purchasing and procurement analytics.
""",
    tables=[
        TableConfig(
            table_name="AI_PO_Data",
            description="""
Primary Purchase Order reporting table.

Contains purchase orders placed with vendors including:

- Vendor
- Item SKU
- Order Dates
- Due Dates
- Received Dates
- Ordered Quantity
- Pending Quantity
- Overdue Information

Used for procurement, vendor performance,
purchase order tracking and overdue analysis.
""",
            primary_date_column="Order_Date",
            default_filters={},
            entity_rules={
                "status_mapping": {
                    "received": {"PO_Rec_Date": "NOT NULL"},
                    "pending": {"PO_Rec_Date": "NULL"},
                    "not received": {"PO_Rec_Date": "NULL"},
                    "partially received": {
                        "PO_Rec_Date": "NULL",
                        "PO_Rec_Qty": {"gt": 0, "lt_column": "PO_Ordered_Qty"},
                    },
                    "overdue": {"PO_Rec_Date": "NULL", "Days_Overdue": {"gt": 0}},
                },
                "vendor_trim_whitespace": True,
                "hidden_columns": ["Id", "Company_Id"],
            },
            searchable_fields=[
                EntityField(
                    entity_type="vendor",
                    column="Vendor_Name",
                    aliases=["vendor", "supplier", "manufacturer", "company"],
                    priority=100,
                    exact_match_only=False,
                    description="Vendor or supplier name.",
                ),
                EntityField(
                    entity_type="item",
                    column="ItemID",
                    aliases=[
                        "item",
                        "sku",
                        "product",
                        "product id",
                        "item id",
                        "item code",
                    ],
                    priority=95,
                    description="Purchase Order Item SKU.",
                ),
                EntityField(
                    entity_type="company_id",
                    column="Company_Id",
                    aliases=["company id"],
                    priority=80,
                    description="Internal Company Identifier.",
                ),
                EntityField(
                    entity_type="order_status",
                    column="PO_Rec_Date",
                    aliases=[
                        "pending",
                        "received",
                        "not received",
                        "partially received",
                        "overdue",
                        "completed",
                        "open orders",
                    ],
                    priority=90,
                    exact_match_only=False,
                    searchable=False,
                    description="Purchase Order status derived from PO_Rec_Date.",
                ),
                EntityField(
                    entity_type="order_date",
                    column="Order_Date",
                    aliases=["order date", "purchase date", "ordered on"],
                    priority=60,
                    searchable=False,
                    description="Purchase Order creation date.",
                ),
                EntityField(
                    entity_type="due_date",
                    column="Due_Date",
                    aliases=["due date", "expected delivery", "delivery date"],
                    priority=60,
                    searchable=False,
                    description="Expected delivery date.",
                ),
                EntityField(
                    entity_type="received_date",
                    column="PO_Rec_Date",
                    aliases=["received date", "receipt date", "received on"],
                    priority=60,
                    searchable=False,
                    description="Purchase Order received date.",
                ),
            ],
        ),
    ],
)
