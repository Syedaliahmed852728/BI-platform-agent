from business.entity_config.models import DomainConfig, EntityField, TableConfig


customer_finance = DomainConfig(
    name="customer_finance",
    description="""
Customer financial analytics including
Accounts Receivable, Unearned Revenue,
customer balances, invoices, deposits,
sales orders, outstanding obligations
and customer payment analysis.
""",
    tables=[
        TableConfig(
            table_name="AI_UnearnedRevenue",
            description="""
Contains customer advance deposits, earned revenue, unearned revenue,
sales orders, delivery status and outstanding customer obligations.
""",
            primary_date_column="OrderDate",
            default_filters={"Level": 0},
            entity_rules={
                "level_mapping": {"company": 1, "customer": 0},
                "delivery_status_mapping": {
                    "not_delivered": {"DeliveredDate": "NULL", "Revenue_Earned": 0},
                    "partially_delivered": {
                        "Revenue_Earned": {
                            "gt": 0,
                            "lt_column": "Total_Order_Value",
                        }
                    },
                    "fully_delivered": {
                        "Revenue_Earned": {"gte_column": "Total_Order_Value"}
                    },
                },
                "hidden_columns": [
                    "company_id",
                    "store_id",
                    "Customer_Id",
                    "Level",
                ],
            },
            searchable_fields=[
                EntityField(
                    entity_type="company",
                    column="company_name",
                    aliases=["company", "business"],
                    priority=100,
                    description="Company name.",
                ),
                EntityField(
                    entity_type="store",
                    column="profitcenter_name",
                    aliases=[
                        "store",
                        "profit center",
                        "profitcentre",
                        "branch",
                        "location",
                    ],
                    priority=95,
                    description="Store / Profit Center.",
                ),
                EntityField(
                    entity_type="customer",
                    column="Customer_Name",
                    aliases=["customer", "customer name", "client"],
                    priority=100,
                    exact_match_only=False,
                    description="Customer Name.",
                ),
                EntityField(
                    entity_type="sales_order",
                    column="So_no",
                    aliases=[
                        "sales order",
                        "so",
                        "so number",
                        "order",
                        "order number",
                    ],
                    priority=90,
                    description="Sales Order Number.",
                ),
                EntityField(
                    entity_type="delivery_status",
                    column="DeliveredDate",
                    aliases=[
                        "not delivered",
                        "pending delivery",
                        "partially delivered",
                        "fully delivered",
                        "delivered",
                    ],
                    searchable=False,
                    exact_match_only=False,
                    priority=80,
                    description="Delivery status.",
                ),
            ],
        ),
        TableConfig(
            table_name="AI_AccountReceivable",
            description="""
Contains customer invoices, invoice balances, customer payments,
accounts receivable, store receivables and company receivables.
""",
            primary_date_column="InvoiceDate",
            default_filters={"LEVEL": 2},
            entity_rules={
                "level_mapping": {"company": 0, "store": 1, "customer": 2},
                "hidden_columns": [
                    "company_id",
                    "store_id",
                    "CustomerID",
                    "LEVEL",
                ],
            },
            searchable_fields=[
                EntityField(
                    entity_type="company",
                    column="Company",
                    aliases=["company", "business"],
                    priority=100,
                    description="Company Name.",
                ),
                EntityField(
                    entity_type="store",
                    column="Store",
                    aliases=["store", "branch", "location"],
                    priority=95,
                    description="Store Name.",
                ),
                EntityField(
                    entity_type="customer",
                    column="CustomerName",
                    aliases=["customer", "customer name", "client"],
                    priority=100,
                    exact_match_only=False,
                    description="Customer Name.",
                ),
                EntityField(
                    entity_type="invoice",
                    column="SaleNumber",
                    aliases=[
                        "invoice",
                        "invoice number",
                        "sale number",
                        "sale",
                    ],
                    priority=90,
                    description="Invoice / Sale Number.",
                ),
            ],
        ),
    ],
)
