from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class EntityField:
    entity_type: str
    column: str
    aliases: List[str]
    priority: int = 1
    exact_match_only: bool = True
    case_sensitive: bool = False
    searchable: bool = True
    return_column: Optional[str] = None
    description: str = ""


@dataclass(frozen=True)
class TableConfig:
    table_name: str
    description: str
    searchable_fields: List[EntityField]
    primary_date_column: Optional[str] = None
    default_filters: Dict[str, Any] = field(default_factory=dict)
    entity_rules: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DomainConfig:
    name: str
    description: str
    tables: List[TableConfig]
