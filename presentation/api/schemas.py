from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)


class ChatResponsePayload(BaseModel):
    source: str
    answer: str
    sql: str | None = None
    domain: str | None = None
    similarity: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class EntityLookupRequest(BaseModel):
    search_text: str = Field(min_length=1)
    entity_types: list[str] | None = None
    domains: list[str] | None = None
    limit: int = 10


class RefreshRequest(BaseModel):
    clients: list[str] | None = None
