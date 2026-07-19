from __future__ import annotations

from datetime import datetime, timezone

from business.intent_learning.models import Domain, IntentExample
from data.redis.example_repository import ExampleRedisRepository


class IntentRepository:
    def __init__(self, repository: ExampleRedisRepository, client_name: str) -> None:
        self.repository = repository
        self.client_name = client_name

    def load(self, domain: Domain) -> list[IntentExample]:
        rows = self.repository.get_domain(self.client_name, domain.value)
        now = datetime.now(timezone.utc)
        return [
            IntentExample(
                intent=e.intent,
                description=e.description,
                sql=e.sql,
                instructions=e.instructions,
                version=e.version,
                created_at=e.created_at or now,
                updated_at=e.updated_at or now,
            )
            for e in rows
        ]
