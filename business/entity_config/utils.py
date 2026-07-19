from __future__ import annotations

from business.entity_config.models import DomainConfig, TableConfig


def get_tables(domain: DomainConfig) -> list[str]:
    return [t.table_name for t in domain.tables]


def get_table_description(table: TableConfig) -> str:
    return table.description.strip()


def get_primary_date_column(table: TableConfig) -> str | None:
    return table.primary_date_column


def get_default_filters(table: TableConfig) -> dict:
    return dict(table.default_filters)


def get_entity_rules(table: TableConfig) -> dict:
    return dict(table.entity_rules)


def get_searchable_fields(table: TableConfig) -> list[dict]:
    return [
        {
            "entity_type": f.entity_type,
            "column": f.column,
            "aliases": f.aliases,
            "description": f.description,
            "searchable": f.searchable,
        }
        for f in table.searchable_fields
    ]


def get_table_details(domain: DomainConfig) -> dict:
    return {
        table.table_name: {
            "description": get_table_description(table),
            "primary_date_column": get_primary_date_column(table),
            "default_filters": get_default_filters(table),
            "entity_rules": get_entity_rules(table),
            "searchable_fields": get_searchable_fields(table),
        }
        for table in domain.tables
    }
