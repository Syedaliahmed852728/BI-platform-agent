from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True)
class QueuedMessage:
    client_name: str
    domain: str | None
    original_question: str
    sql_output: str
    stream_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_redis_fields(self) -> dict[str, str]:
        return {
            "client_name": self.client_name,
            "domain": self.domain or "",
            "original_question": self.original_question,
            "sql_output": self.sql_output,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_redis_entry(
        cls, stream_id: str, fields: dict[str, str]
    ) -> "QueuedMessage":
        return cls(
            client_name=fields["client_name"],
            domain=fields.get("domain") or None,
            original_question=fields["original_question"],
            sql_output=fields["sql_output"],
            stream_id=stream_id,
            created_at=datetime.fromisoformat(fields["created_at"]),
        )


@dataclass(slots=True)
class ClientBatch:
    client_name: str
    messages: list[QueuedMessage]
    reason: str

    @property
    def size(self) -> int:
        return len(self.messages)


@dataclass(slots=True)
class ContextPayload:
    text: str
    client_name: str

    def to_dict(self) -> dict[str, str]:
        return {"text": self.text, "client_name": self.client_name}
