from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True, frozen=True)
class SQLExample:
    client_name: str
    domain: str
    intent: str
    description: str
    sql: str
    instructions: str
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def embedding_text(self) -> str:
        # Embedded text must read like the user questions it is matched
        # against, so prefer real sample questions over the generalized
        # intent; description/instructions are stored but not embedded.
        questions = self.metadata.get("sample_questions", [])
        return "\n".join(questions) if questions else self.intent


@dataclass(slots=True, frozen=True)
class ExampleMatch:
    example: SQLExample
    similarity: float


@dataclass(slots=True)
class SearchResponse:
    success: bool
    client_name: str
    query: str
    matched: bool
    total_matches: int
    matches: list[ExampleMatch] = field(default_factory=list)
    message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "client_name": self.client_name,
            "query": self.query,
            "matched": self.matched,
            "total_matches": self.total_matches,
            "message": self.message,
            "metadata": self.metadata,
            "examples": [
                {
                    "client_name": m.example.client_name,
                    "domain": m.example.domain,
                    "intent": m.example.intent,
                    "description": m.example.description,
                    "sql": m.example.sql,
                    "instructions": m.example.instructions,
                    "version": m.example.version,
                    "similarity": round(m.similarity, 4),
                    "metadata": m.example.metadata,
                    "created_at": m.example.created_at.isoformat()
                    if m.example.created_at
                    else None,
                    "updated_at": m.example.updated_at.isoformat()
                    if m.example.updated_at
                    else None,
                }
                for m in self.matches
            ],
        }
