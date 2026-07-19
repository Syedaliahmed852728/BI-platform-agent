from business.entity_config.models import DomainConfig, EntityField, TableConfig


inventory = DomainConfig(
    name="inventory",
    description="""
Inventory management, warehouse inventory, store inventory,
item lookup, product categories, vendors, stock availability,
locations, purchase order information and inventory analytics.
""",
    tables=[
        TableConfig(
            table_name="AIData_Inventory",
            description="""
Primary Inventory table.

Contains inventory located across stores and warehouses.
Includes SKU / Item IDs, Categories, Vendors, Locations, Buildings,
Warehouse information, Quantities, Purchase Orders, Costs, Prices
and Inventory Status.
""",
            primary_date_column="Location Date",
            default_filters={},
            entity_rules={
                "item_search_priority": ["item_cat", "Category", "SubCategory"],
                "status_mapping": {
                    "in stock": ["AVAILABLE"],
                    "items to sell": ["AVAILABLE"],
                    "available to sell": ["AVAILABLE"],
                    "on hand": ["AVAILABLE", "NAILED DOWN", "DAMAGED"],
                    "items on hand": ["AVAILABLE", "NAILED DOWN", "DAMAGED"],
                    "on-hand inventory": ["AVAILABLE", "NAILED DOWN", "DAMAGED"],
                },
                "building_requires": ["loc_type"],
                "ignored_columns": ["Item Description2"],
            },
            searchable_fields=[
                EntityField(
                    entity_type="item",
                    column="Item ID",
                    aliases=[
                        "item",
                        "item id",
                        "sku",
                        "sku id",
                        "product",
                        "product id",
                        "item code",
                    ],
                    priority=100,
                    description="Unique inventory item identifier.",
                ),
                EntityField(
                    entity_type="item_class",
                    column="item_cat",
                    aliases=[
                        "room",
                        "room type",
                        "department",
                        "class",
                        "item class",
                        "living room",
                        "bedroom",
                        "dining room",
                        "office",
                        "accessories",
                    ],
                    priority=95,
                    exact_match_only=False,
                    description="Highest inventory classification.",
                ),
                EntityField(
                    entity_type="category",
                    column="Category",
                    aliases=["category", "product category", "group"],
                    priority=90,
                    exact_match_only=False,
                    description="Inventory category.",
                ),
                EntityField(
                    entity_type="subcategory",
                    column="SubCategory",
                    aliases=["subcategory", "sub category", "type", "product type"],
                    priority=85,
                    exact_match_only=False,
                    description="Inventory subcategory.",
                ),
                EntityField(
                    entity_type="item_description",
                    column="Item Description",
                    aliases=[
                        "description",
                        "item description",
                        "product name",
                        "item name",
                    ],
                    priority=92,
                    exact_match_only=False,
                    description="Primary inventory description.",
                ),
                EntityField(
                    entity_type="vendor",
                    column="Venddor",
                    aliases=["vendor", "supplier", "manufacturer", "brand"],
                    priority=90,
                    description="Inventory vendor. Column name really is 'Venddor' (double d).",
                ),
                EntityField(
                    entity_type="building",
                    column="Building",
                    aliases=["building", "warehouse", "store", "location"],
                    priority=88,
                    description="Inventory building.",
                ),
                EntityField(
                    entity_type="location_type",
                    column="loc_type",
                    aliases=["location type", "warehouse", "store"],
                    priority=80,
                    description="Store or Warehouse.",
                ),
                EntityField(
                    entity_type="aisle",
                    column="Aisle",
                    aliases=["aisle"],
                    priority=70,
                    description="Warehouse aisle.",
                ),
                EntityField(
                    entity_type="shelf_level",
                    column="Level",
                    aliases=["level", "shelf", "rack level"],
                    priority=70,
                    description="Shelf level.",
                ),
                EntityField(
                    entity_type="bay",
                    column="Bay",
                    aliases=["bay", "bin"],
                    priority=70,
                    description="Storage bay.",
                ),
                EntityField(
                    entity_type="inventory_status",
                    column="Status",
                    aliases=[
                        "status",
                        "available",
                        "reserved",
                        "damaged",
                        "nailed down",
                        "delivered",
                    ],
                    priority=75,
                    exact_match_only=False,
                    description="Inventory status.",
                ),
                EntityField(
                    entity_type="purchase_order",
                    column="PO No",
                    aliases=["purchase order", "po", "po number"],
                    priority=65,
                    description="Purchase order number.",
                ),
            ],
        ),
    ],
)
