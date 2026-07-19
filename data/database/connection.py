from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Iterator

from configs.data import data_settings


class SQLiteClientDatabase:
    def __init__(self, client_name: str) -> None:
        self.client_name = client_name
        self.path = data_settings.database_path(client_name)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(str(self.path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

def get_client_database(client_name: str) -> SQLiteClientDatabase:
    return SQLiteClientDatabase(client_name)
