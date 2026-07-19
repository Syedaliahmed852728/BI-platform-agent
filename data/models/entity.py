from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class EntityRecord:
    value: str
    normalized: str
    entity_type: str
    domain: str
    table: str
    column: str
    priority: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)
