from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from presentation.api.container import container
from presentation.schedulers import SchedulerManager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    manager = SchedulerManager(
        entity_refresher=container.entity_refresher,
        queue_worker=container.queue_worker,
    )
    app.state.scheduler_manager = manager
    await manager.start()
    try:
        yield
    finally:
        await manager.stop()
        try:
            await container.queue_repository.close()
        except Exception:
            logger.exception("failed to close queue repository")
