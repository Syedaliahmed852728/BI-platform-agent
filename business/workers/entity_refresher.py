from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone

from business.entity_resolution.loader import EntityLoader
from configs.data import data_settings
from configs.presentation import presentation_settings
from data.database.connection import get_client_database
from data.redis.entity_repository import EntityRedisRepository

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class RefreshResult:
    success: bool
    client_name: str
    entity_count: int
    duration_seconds: float
    refreshed_at: str
    message: str | None = None


class EntityRefresher:
    def __init__(self, repository: EntityRedisRepository) -> None:
        self.repository = repository
        self._semaphore = asyncio.Semaphore(
            presentation_settings.max_concurrent_refreshes
        )

    async def refresh_all(self, clients: list[str] | None = None) -> list[RefreshResult]:
        targets = clients or list(data_settings.clients)
        tasks = [self.refresh_client(client) for client in targets]
        return await asyncio.gather(*tasks)

    async def refresh_client(self, client_name: str) -> RefreshResult:
        async with self._semaphore:
            return await asyncio.to_thread(self._refresh_client_sync, client_name)

    def _refresh_client_sync(self, client_name: str) -> RefreshResult:
        started = time.perf_counter()
        refreshed_at = datetime.now(timezone.utc).isoformat()
        try:
            db = get_client_database(client_name)
            with db.connect() as conn:
                loader = EntityLoader(conn)
                entities = list(loader.iter_entities())

            count = self.repository.replace_client_entities(
                client_name=client_name,
                entities=entities,
                refreshed_at=refreshed_at,
            )
            duration = round(time.perf_counter() - started, 3)
            logger.info(
                "refreshed client=%s entities=%d duration=%.3fs",
                client_name,
                count,
                duration,
            )
            return RefreshResult(
                success=True,
                client_name=client_name,
                entity_count=count,
                duration_seconds=duration,
                refreshed_at=refreshed_at,
                message="Refresh completed.",
            )
        except Exception as exc:
            duration = round(time.perf_counter() - started, 3)
            logger.exception("refresh failed for %s", client_name)
            return RefreshResult(
                success=False,
                client_name=client_name,
                entity_count=0,
                duration_seconds=duration,
                refreshed_at=refreshed_at,
                message=str(exc),
            )

    @staticmethod
    def summarize(results: list[RefreshResult]) -> dict:
        return {
            "total_clients": len(results),
            "successful": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success),
            "total_entities": sum(r.entity_count for r in results),
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }
