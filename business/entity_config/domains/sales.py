from business.entity_config.models import DomainConfig, EntityField, TableConfig


sales = DomainConfig(
    name="sales",
    description="""
Sales reporting, company performance, stores,
salespersons, financing, traffic, goals,
discounts, margins and KPI analytics.
""",
    tables=[
        TableConfig(
            table_name="ConsolidateData_PBI",
            description="""
Primary Power BI Sales reporting table.

Contains sales information aggregated at:

- Company
- Store (Profit Center)
- Region
- Salesperson

Includes all major KPIs such as:

Sales, Traffic, Margins, Financing, Delivery, Bedding, FPP,
Goals, Discounts, Average Ticket, SPGI, UPS, Credit Applications.
""",
            primary_date_column="From_Date",
            default_filters={
                "STATUS": "W",
                "Level": 0,
            },
            entity_rules={
                "salesperson": {"exclude_contains": ["HOU"]},
                "ecommerce_store_ids": [444, 445],
                "level_mapping": {
                    "company": 0,
                    "store": 1,
                    "region": 2,
                    "region_without_outlet": 3,
                    "company_with_outlet": 4,
                    "salesperson": 5,
                    "company_without_outlet": 6,
                    "grand_total": 7,
                    "default(if user didn't mention level or company/store etc)": 0,
                },
                "primary_date_column": "From_Date",
                "disallowed_date_columns": ["To_Date", "iMonth", "iYear"],
            },
            searchable_fields=[
                EntityField(
                    entity_type="company",
                    column="Company_Name",
                    aliases=["company", "company name", "business", "organization"],
                    priority=100,
                    description="Company Name",
                ),
                EntityField(
                    entity_type="company_id",
                    column="Company_Id",
                    aliases=["company id", "company code"],
                    priority=95,
                    description="Company Identifier",
                ),
                EntityField(
                    entity_type="store",
                    column="Profitcenter_Name",
                    aliases=[
                        "store",
                        "store name",
                        "profit center",
                        "profit centre",
                        "profitcenter",
                        "profit centre name",
                        "branch",
                        "branch name",
                        "location",
                        "outlet",
                    ],
                    priority=100,
                    description="Store / Profit Center",
                ),
                EntityField(
                    entity_type="store_id",
                    column="profitcenter_id",
                    aliases=[
                        "store id",
                        "branch id",
                        "profit center id",
                        "profitcentre id",
                        "location id",
                    ],
                    priority=95,
                    description="Store Identifier",
                ),
                EntityField(
                    entity_type="region",
                    column="region_name",
                    aliases=["region", "region name", "territory", "sales region"],
                    priority=90,
                    description="Sales Region",
                ),
                EntityField(
                    entity_type="region_id",
                    column="region_id",
                    aliases=["region id", "territory id"],
                    priority=85,
                    description="Region Identifier",
                ),
                EntityField(
                    entity_type="salesperson",
                    column="Name",
                    aliases=[
                        "salesperson",
                        "sales person",
                        "sales people",
                        "salespeople",
                        "employee",
                        "employee name",
                        "associate",
                        "rep",
                        "representative",
                        "seller",
                        "performer",
                        "staff",
                        "name",
                    ],
                    priority=100,
                    description="Salesperson Name",
                ),
                EntityField(
                    entity_type="salesperson_id",
                    column="usr_Id",
                    aliases=[
                        "user id",
                        "employee id",
                        "salesperson id",
                        "sales person id",
                        "associate id",
                        "rep id",
                    ],
                    priority=95,
                    description="Salesperson Identifier",
                ),
                EntityField(
                    entity_type="status",
                    column="STATUS",
                    aliases=[
                        "status",
                        "sales status",
                        "weekly",
                        "monthly",
                        "week",
                        "month",
                    ],
                    priority=60,
                    exact_match_only=False,
                    description="Sales Reporting Status",
                ),
                EntityField(
                    entity_type="level",
                    column="Level",
                    aliases=[
                        "company level",
                        "store level",
                        "region level",
                        "salesperson level",
                        "overall",
                        "grand total",
                    ],
                    priority=50,
                    exact_match_only=False,
                    searchable=False,
                    description="Aggregation Level",
                ),
            ],
        )
    ],
)
