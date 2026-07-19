from business.entity_config.models import DomainConfig, EntityField, TableConfig


general_ledger = DomainConfig(
    name="general_ledger",
    description="""
General Ledger accounting analytics including journal entries,
debit and credit transactions, accounting postings, GL accounts,
revenue recognition, inventory postings, payment postings,
finance fees, GL adjustments and accounting audit trails.
""",
    tables=[
        TableConfig(
            table_name="AI_AccountsDetail",
            description="""
Contains General Ledger journal entry details where each row represents
one debit or credit posting. Multiple rows sharing the same journal_id
form a complete double-entry accounting transaction generated from
business activities such as invoices, revenue recognition, inventory
movements and payments.
""",
            primary_date_column="journal_date",
            default_filters={},
            entity_rules={
                "journal_grouping_column": "journal_id",
                "normalize_columns": ["dc_type"],
                "hidden_columns": [
                    "id",
                ],
            },
            searchable_fields=[
                EntityField(
                    entity_type="journal",
                    column="journal_id",
                    aliases=[
                        "journal",
                        "journal id",
                        "entry",
                        "entry id",
                        "transaction",
                    ],
                    priority=100,
                    description="Accounting Journal Identifier.",
                ),
                EntityField(
                    entity_type="journal_number",
                    column="journal_no_new",
                    aliases=[
                        "journal number",
                        "journal no",
                        "gl number",
                        "posting number",
                    ],
                    priority=95,
                    description="Internal Journal Number.",
                ),
                EntityField(
                    entity_type="invoice",
                    column="journal_no",
                    aliases=[
                        "invoice",
                        "invoice number",
                        "sale",
                        "sale number",
                    ],
                    priority=100,
                    description="Invoice / Sale Number.",
                ),
                EntityField(
                    entity_type="customer",
                    column="description",
                    aliases=[
                        "customer",
                        "customer name",
                        "client",
                    ],
                    priority=90,
                    exact_match_only=False,
                    description="Customer information stored in the journal description.",
                ),
                EntityField(
                    entity_type="account",
                    column="name",
                    aliases=[
                        "account",
                        "gl account",
                        "ledger account",
                        "account name",
                    ],
                    priority=95,
                    exact_match_only=False,
                    description="General Ledger Account Name.",
                ),
                EntityField(
                    entity_type="account_code",
                    column="code",
                    aliases=[
                        "account code",
                        "gl code",
                        "code",
                    ],
                    priority=90,
                    description="General Ledger Account Code.",
                ),
                EntityField(
                    entity_type="transaction_type",
                    column="trans_type",
                    aliases=[
                        "transaction type",
                        "payment",
                        "revenue",
                        "inventory",
                        "reverse entry",
                    ],
                    searchable=False,
                    exact_match_only=False,
                    priority=85,
                    description="Accounting transaction category.",
                ),
                EntityField(
                    entity_type="journal_type",
                    column="journal_type",
                    aliases=[
                        "journal type",
                        "document type",
                        "invoice type",
                    ],
                    priority=80,
                    description="Source Journal Type.",
                ),
                EntityField(
                    entity_type="posting_status",
                    column="is_posted",
                    aliases=[
                        "posted",
                        "unposted",
                        "posting status",
                    ],
                    searchable=False,
                    exact_match_only=False,
                    priority=80,
                    description="Journal Posting Status.",
                ),
            ],
        ),
    ],
)
