from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True, slots=True)
class DataSettings:
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    databases_root: Path = PROJECT_ROOT

    clients: tuple[str, ...] = field(
        default_factory=lambda: tuple(
            filter(
                None,
                os.getenv("CLIENT_DATABASES", "my_database").split(","),
            )
        )
    )

    database_extension: str = ".db"

    redis_prefix_min_length: int = 3

    redis_prefix_max_length: int = 12

    def canonical_client_name(self, client_name: str) -> str:
        """
        Canonical client identifier used for all storage keys:
        the database name without its extension.
        """
        return client_name.removesuffix(self.database_extension)

    def database_path(self, client_name: str) -> Path:
        name = client_name
        if not name.endswith(self.database_extension):
            name = f"{name}{self.database_extension}"
        return self.databases_root / name


data_settings = DataSettings()
