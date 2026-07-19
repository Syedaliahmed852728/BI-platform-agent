from __future__ import annotations

import hashlib
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Iterable

from redis import Redis
from redis.client import Pipeline

from configs.data import data_settings
from data.models.entity import EntityRecord


class EntityRedisRepository:
    def __init__(self, redis_client: Redis) -> None:
        self.redis = redis_client
        self.prefix_min = data_settings.redis_prefix_min_length
        self.prefix_max = data_settings.redis_prefix_max_length

    def pipeline(self) -> Pipeline:
        return self.redis.pipeline(transaction=False)

    def save_entity(self, client_name: str, entity: EntityRecord) -> None:
        pipe = self.pipeline()
        self._queue_save(pipe, client_name, entity)
        pipe.execute()

    def save_entities(
        self, client_name: str, entities: Iterable[EntityRecord]
    ) -> int:
        pipe = self.pipeline()
        count = 0
        for entity in entities:
            self._queue_save(pipe, client_name, entity)
            count += 1
            if count % 500 == 0:
                pipe.execute()
                pipe = self.pipeline()
        pipe.execute()
        return count

    def _queue_save(
        self, pipe: Pipeline, client_name: str, entity: EntityRecord
    ) -> None:
        entity_id = self._entity_id(entity)
        pipe.hset(
            self._entity_key(client_name, entity_id),
            mapping=self._serialize(entity),
        )
        pipe.sadd(
            self._exact_key(client_name, entity.entity_type, entity.normalized),
            entity_id,
        )
        for prefix in self._prefixes(entity.normalized):
            pipe.sadd(
                self._prefix_key(client_name, entity.entity_type, prefix),
                entity_id,
            )
        pipe.sadd(self._entity_types_key(client_name), entity.entity_type)

    def get_exact(
        self, client_name: str, entity_type: str, normalized: str
    ) -> list[EntityRecord]:
        ids = self.redis.smembers(
            self._exact_key(client_name, entity_type, normalized)
        )
        return self._load_ids(client_name, ids)

    def get_prefix(
        self, client_name: str, entity_type: str, prefix: str
    ) -> list[EntityRecord]:
        prefix = prefix.strip()
        if len(prefix) < self.prefix_min:
            return []
        prefix = prefix[: self.prefix_max]
        ids = self.redis.smembers(self._prefix_key(client_name, entity_type, prefix))
        return self._load_ids(client_name, ids)

    def get_candidates(
        self,
        client_name: str,
        normalized_query: str,
        entity_types: list[str] | None = None,
    ) -> list[EntityRecord]:
        entity_types = entity_types or self.get_entity_types(client_name)
        candidates: list[EntityRecord] = []
        for entity_type in entity_types:
            exact = self.get_exact(client_name, entity_type, normalized_query)
            if exact:
                candidates.extend(exact)
                continue
            candidates.extend(self.get_prefix(client_name, entity_type, normalized_query))
        return candidates

    def get_entity_types(self, client_name: str) -> list[str]:
        values = self.redis.smembers(self._entity_types_key(client_name))
        return sorted(self._decode(v) for v in values)

    def _load_ids(self, client_name: str, ids) -> list[EntityRecord]:
        if not ids:
            return []
        pipe = self.pipeline()
        decoded_ids = [self._decode(i) for i in ids]
        for entity_id in decoded_ids:
            pipe.hgetall(self._entity_key(client_name, entity_id))
        rows = pipe.execute()
        out: list[EntityRecord] = []
        for row in rows:
            if not row:
                continue
            decoded = {self._decode(k): self._decode(v) for k, v in row.items()}
            out.append(self._deserialize(decoded))
        return out

    def clear_client(self, client_name: str) -> int:
        deleted = 0
        patterns = (
            f"entity:{client_name}:*",
            f"exact:{client_name}:*",
            f"prefix:{client_name}:*",
            f"meta:{client_name}*",
        )
        for pattern in patterns:
            cursor = 0
            while True:
                cursor, keys = self.redis.scan(cursor=cursor, match=pattern, count=500)
                if keys:
                    deleted += self.redis.delete(*keys)
                if cursor == 0:
                    break
        return deleted

    def replace_client_entities(
        self,
        client_name: str,
        entities: Iterable[EntityRecord],
        **metadata,
    ) -> int:
        self.clear_client(client_name)
        count = self.save_entities(client_name, entities)
        metadata.setdefault("entity_count", count)
        metadata.setdefault("last_refresh", datetime.now(timezone.utc).isoformat())
        self.set_metadata(client_name, **metadata)
        return count

    def set_metadata(self, client_name: str, **metadata) -> None:
        if not metadata:
            return
        self.redis.hset(
            self._metadata_key(client_name),
            mapping={k: str(v) for k, v in metadata.items()},
        )

    def get_metadata(self, client_name: str) -> dict[str, str]:
        values = self.redis.hgetall(self._metadata_key(client_name))
        return {self._decode(k): self._decode(v) for k, v in values.items()}

    def exists(self, client_name: str) -> bool:
        return self.redis.exists(self._metadata_key(client_name)) == 1

    def ping(self) -> bool:
        try:
            return bool(self.redis.ping())
        except Exception:
            return False

    def statistics(self, client_name: str) -> dict:
        entity_types = self.get_entity_types(client_name)
        return {
            "client": client_name,
            "entity_types": entity_types,
            "total_entity_types": len(entity_types),
            "metadata": self.get_metadata(client_name),
        }

    @staticmethod
    def _entity_id(entity: EntityRecord) -> str:
        text = "|".join(
            (
                entity.entity_type,
                entity.domain,
                entity.table,
                entity.column,
                entity.normalized,
            )
        )
        return hashlib.sha1(text.encode("utf-8")).hexdigest()

    @staticmethod
    def _serialize(entity: EntityRecord) -> dict:
        data = asdict(entity)
        data.pop("metadata", None)
        return {k: str(v) for k, v in data.items()}

    @staticmethod
    def _deserialize(data: dict) -> EntityRecord:
        return EntityRecord(
            value=data["value"],
            normalized=data["normalized"],
            entity_type=data["entity_type"],
            domain=data["domain"],
            table=data["table"],
            column=data["column"],
            priority=int(data["priority"]),
        )

    @staticmethod
    def _decode(value) -> str:
        return value.decode() if isinstance(value, bytes) else value

    def _prefixes(self, normalized: str):
        normalized = normalized.strip()
        if len(normalized) < self.prefix_min:
            return
        limit = min(len(normalized), self.prefix_max)
        for i in range(self.prefix_min, limit + 1):
            yield normalized[:i]

    @staticmethod
    def _entity_key(client_name: str, entity_id: str) -> str:
        return f"entity:{client_name}:{entity_id}"

    @staticmethod
    def _exact_key(client_name: str, entity_type: str, normalized: str) -> str:
        return f"exact:{client_name}:{entity_type}:{normalized}"

    @staticmethod
    def _prefix_key(client_name: str, entity_type: str, prefix: str) -> str:
        return f"prefix:{client_name}:{entity_type}:{prefix}"

    @staticmethod
    def _metadata_key(client_name: str) -> str:
        return f"meta:{client_name}"

    @staticmethod
    def _entity_types_key(client_name: str) -> str:
        return f"meta:{client_name}:entity_types"
