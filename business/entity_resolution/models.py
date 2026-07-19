from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from data.models.entity import EntityRecord


@dataclass(slots=True, frozen=True)
class EntityMatch:
    entity: EntityRecord
    confidence: int
    matched_by: str


@dataclass(slots=True, frozen=True)
class LookupRequest:
    client_name: str
    search_text: str
    entity_types: list[str] | None = None
    domains: list[str] | None = None
    limit: int = 10


@dataclass(slots=True)
class LookupResponse:
    success: bool
    client_name: str
    resolved: bool
    ambiguous: bool
    exact_match_found: bool
    total_matches: int
    matches: list[EntityMatch] = field(default_factory=list)
    message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "client_name": self.client_name,
            "resolved": self.resolved,
            "ambiguous": self.ambiguous,
            "exact_match_found": self.exact_match_found,
            "total_matches": self.total_matches,
            "message": self.message,
            "metadata": self.metadata,
            "entities": [
                {
                    "entity": m.entity.value,
                    "entity_type": m.entity.entity_type,
                    "domain": m.entity.domain,
                    "table": m.entity.table,
                    "column": m.entity.column,
                    "confidence": m.confidence,
                    "matched_by": m.matched_by,
                }
                for m in self.matches
            ],
        }
