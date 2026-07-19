from __future__ import annotations

from typing import Generator

from business.entity_config.models import DomainConfig, EntityField, TableConfig
from business.entity_config.registry import ENTITY_CONFIG
from business.entity_resolution.normalizer import EntityNormalizer
from data.models.entity import EntityRecord


class EntityLoader:
    def __init__(self, connection) -> None:
        self.connection = connection

    def iter_entities(self) -> Generator[EntityRecord, None, None]:
        for domain_name, domain in ENTITY_CONFIG.items():
            yield from self._iter_domain(domain_name, domain)

    def count_entities(self) -> int:
        total = 0
        for domain in ENTITY_CONFIG.values():
            for table in domain.tables:
                for field in table.searchable_fields:
                    if not field.searchable:
                        continue
                    query = (
                        f"SELECT COUNT(DISTINCT [{field.column}]) "
                        f"FROM [{table.table_name}] "
                        f"WHERE [{field.column}] IS NOT NULL "
                        f"AND TRIM([{field.column}]) <> ''"
                    )
                    row = self.connection.execute(query).fetchone()
                    if row:
                        total += int(row[0])
        return total

    def _iter_domain(
        self, domain_name: str, domain: DomainConfig
    ) -> Generator[EntityRecord, None, None]:
        for table in domain.tables:
            yield from self._iter_table(domain_name, table)

    def _iter_table(
        self, domain_name: str, table: TableConfig
    ) -> Generator[EntityRecord, None, None]:
        for field in table.searchable_fields:
            if not field.searchable:
                continue
            yield from self._iter_field(
                domain_name=domain_name, table=table, field=field
            )

    def _iter_field(
        self,
        *,
        domain_name: str,
        table: TableConfig,
        field: EntityField,
    ) -> Generator[EntityRecord, None, None]:
        query = self._distinct_query(table.table_name, field.column)
        cursor = self.connection.execute(query)
        for row in cursor:
            raw = self._extract(row)
            if raw is None:
                continue
            value = str(raw).strip()
            if not value:
                continue
            normalized = EntityNormalizer.normalize_database_value(value)
            if not normalized:
                continue
            yield EntityRecord(
                value=value,
                normalized=normalized,
                entity_type=field.entity_type,
                domain=domain_name,
                table=table.table_name,
                column=field.column,
                priority=field.priority,
            )

    @staticmethod
    def _distinct_query(table_name: str, column: str) -> str:
        return (
            f"SELECT DISTINCT [{column}] "
            f"FROM [{table_name}] "
            f"WHERE [{column}] IS NOT NULL "
            f"AND TRIM([{column}]) <> '' "
            f"ORDER BY [{column}]"
        )

    @staticmethod
    def _extract(row):
        if row is None:
            return None
        try:
            return row[0]
        except Exception:
            if isinstance(row, dict) and row:
                return next(iter(row.values()))
            return None
