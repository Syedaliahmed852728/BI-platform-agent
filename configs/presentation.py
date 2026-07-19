from __future__ import annotations

import os
from dataclasses import dataclass
from zoneinfo import ZoneInfo


@dataclass(frozen=True, slots=True)
class PresentationSettings:
    host: str = os.getenv("APP_HOST", "0.0.0.0")
    port: int = int(os.getenv("APP_PORT", "8000"))

    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    entity_refresh_hour: int = int(os.getenv("ENTITY_REFRESH_HOUR", "7"))
    entity_refresh_minute: int = int(os.getenv("ENTITY_REFRESH_MINUTE", "5"))
    entity_refresh_timezone: ZoneInfo = ZoneInfo(
        os.getenv("ENTITY_REFRESH_TIMEZONE", "America/New_York")
    )

    queue_poll_interval_seconds: float = float(os.getenv("QUEUE_POLL_INTERVAL", "5.0"))

    refresh_on_startup: bool = os.getenv("REFRESH_ON_STARTUP", "true").lower() == "true"

    max_concurrent_refreshes: int = int(os.getenv("MAX_CONCURRENT_REFRESHES", "4"))


presentation_settings = PresentationSettings()
