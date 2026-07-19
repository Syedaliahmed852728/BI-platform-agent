from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from business.workers.entity_refresher import EntityRefresher
from business.workers.queue_worker import SQLContextWorker
from configs.presentation import presentation_settings

logger = logging.getLogger(__name__)


class SchedulerManager:
    def __init__(
        self,
        entity_refresher: EntityRefresher,
        queue_worker: SQLContextWorker,
    ) -> None:
        self.entity_refresher = entity_refresher
        self.queue_worker = queue_worker
        self.scheduler = AsyncIOScheduler(
            timezone=presentation_settings.entity_refresh_timezone
        )

    async def start(self) -> None:
        self.scheduler.add_job(
            self._run_refresh,
            trigger="cron",
            hour=presentation_settings.entity_refresh_hour,
            minute=presentation_settings.entity_refresh_minute,
            id="entity_refresh_job",
            replace_existing=True,
        )
        self.scheduler.start()
        logger.info(
            "entity refresh scheduled daily at %02d:%02d %s",
            presentation_settings.entity_refresh_hour,
            presentation_settings.entity_refresh_minute,
            presentation_settings.entity_refresh_timezone,
        )

        if presentation_settings.refresh_on_startup:
            asyncio.create_task(self._run_refresh(initial=True))

        await self.queue_worker.start()

    async def stop(self) -> None:
        try:
            self.scheduler.shutdown(wait=False)
        except Exception:
            logger.exception("scheduler shutdown failed")
        await self.queue_worker.stop()

    async def _run_refresh(self, initial: bool = False) -> None:
        started = datetime.now()
        results = await self.entity_refresher.refresh_all()
        summary = self.entity_refresher.summarize(results)
        logger.info(
            "%s refresh finished in %.2fs summary=%s",
            "startup" if initial else "scheduled",
            (datetime.now() - started).total_seconds(),
            summary,
        )
