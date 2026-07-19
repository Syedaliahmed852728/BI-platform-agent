from __future__ import annotations

import re
import unicodedata


_MULTIPLE_SPACES = re.compile(r"\s+")


class EntityNormalizer:
    @classmethod
    def normalize(cls, value: str | None) -> str:
        if value is None:
            return ""
        value = str(value)
        value = unicodedata.normalize("NFKC", value)
        value = _MULTIPLE_SPACES.sub(" ", value)
        value = value.strip()
        return value.casefold()

    @classmethod
    def normalize_query(cls, query: str | None) -> str:
        return cls.normalize(query)

    @classmethod
    def normalize_database_value(cls, value: str | None) -> str:
        return cls.normalize(value)
