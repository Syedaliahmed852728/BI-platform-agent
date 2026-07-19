from __future__ import annotations

import json
import logging
from datetime import datetime

import numpy as np
from redis import Redis
from redis.client import Pipeline
from redis.commands.search.field import (
    NumericField,
    TagField,
    TextField,
    VectorField,
)
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query

from data.models.example import ExampleMatch, SQLExample

logger = logging.getLogger(__name__)


class ExampleRedisRepository:
    def __init__(self, redis_client: Redis, embedding_dimensions: int) -> None:
        self.redis = redis_client
        self.embedding_dimensions = embedding_dimensions

    def pipeline(self) -> Pipeline:
        return self.redis.pipeline(transaction=False)

    def save(self, example: SQLExample, embedding: list[float]) -> None:
        self.ensure_index(example.client_name)
        pipe = self.pipeline()
        self._queue_save(pipe, example, embedding)
        pipe.execute()

    def save_many(
        self,
        examples: list[SQLExample],
        embeddings: list[list[float]],
    ) -> int:
        if not examples:
            return 0
        self.ensure_index(examples[0].client_name)
        pipe = self.pipeline()
        for example, embedding in zip(examples, embeddings):
            self._queue_save(pipe, example, embedding)
        pipe.execute()
        return len(examples)

    def _queue_save(
        self,
        pipe: Pipeline,
        example: SQLExample,
        embedding: list[float],
    ) -> None:
        mapping = self._serialize(example)
        mapping["embedding"] = np.asarray(embedding, dtype=np.float32).tobytes()
        pipe.hset(
            self._example_key(example.client_name, example.intent), mapping=mapping
        )
        pipe.sadd(self._intents_key(example.client_name), example.intent)
        pipe.sadd(self._domain_key(example.client_name, example.domain), example.intent)

    def get_domain(self, client_name: str, domain: str) -> list[SQLExample]:
        intents = self.redis.smembers(self._domain_key(client_name, domain))
        if not intents:
            return []
        pipe = self.pipeline()
        for intent in intents:
            pipe.hgetall(self._example_key(client_name, self._decode(intent)))
        rows = pipe.execute()
        return [self._deserialize(self._decode_hash(r)) for r in rows if r]

    def vector_search(
        self,
        *,
        client_name: str,
        embedding: list[float],
        domain: str | None = None,
        top_k: int = 5,
    ) -> list[ExampleMatch]:
        if not self.index_exists(client_name):
            self.ensure_index(client_name)
            return []

        vector = np.asarray(embedding, dtype=np.float32).tobytes()
        filters = "@client_name:{$client}"
        if domain:
            filters += " @domain:{$domain}"

        query = (
            Query(f"({filters})=>[KNN {top_k} @embedding $vector AS score]")
            .sort_by("score")
            .paging(0, top_k)
            .dialect(2)
            .return_fields(
                "client_name",
                "domain",
                "intent",
                "description",
                "sql",
                "instructions",
                "version",
                "metadata",
                "created_at",
                "updated_at",
                "score",
            )
        )
        params = {"client": client_name, "vector": vector}
        if domain:
            params["domain"] = domain

        try:
            results = self.redis.ft(self._index_name(client_name)).search(
                query, query_params=params
            )
        except Exception:
            logger.exception("vector search failed for %s", client_name)
            return []

        matches: list[ExampleMatch] = []
        for doc in results.docs:
            similarity = 1.0 - float(doc.score)
            example = SQLExample(
                client_name=doc.client_name,
                domain=doc.domain,
                intent=doc.intent,
                description=doc.description,
                sql=doc.sql,
                instructions=doc.instructions,
                version=int(doc.version),
                metadata=json.loads(getattr(doc, "metadata", "{}")),
                created_at=datetime.fromisoformat(doc.created_at)
                if getattr(doc, "created_at", "")
                else None,
                updated_at=datetime.fromisoformat(doc.updated_at)
                if getattr(doc, "updated_at", "")
                else None,
            )
            matches.append(ExampleMatch(example=example, similarity=similarity))
        return matches

    def ensure_index(self, client_name: str) -> None:
        index_name = self._index_name(client_name)
        try:
            self.redis.ft(index_name).info()
            return
        except Exception:
            pass

        schema = (
            TagField("client_name"),
            TagField("domain"),
            TagField("intent"),
            NumericField("version"),
            TextField("description"),
            TextField("instructions"),
            VectorField(
                "embedding",
                "HNSW",
                {
                    "TYPE": "FLOAT32",
                    "DIM": self.embedding_dimensions,
                    "DISTANCE_METRIC": "COSINE",
                    "M": 16,
                    "EF_CONSTRUCTION": 200,
                },
            ),
        )
        definition = IndexDefinition(
            prefix=[f"example:{client_name}:"],
            index_type=IndexType.HASH,
        )
        self.redis.ft(index_name).create_index(fields=schema, definition=definition)

    def index_exists(self, client_name: str) -> bool:
        try:
            indexes = self.redis.execute_command("FT._LIST")
        except Exception:
            return False
        decoded = {self._decode(n) for n in indexes}
        return self._index_name(client_name) in decoded

    def clear_client(self, client_name: str) -> int:
        deleted = 0
        for key in self.redis.scan_iter(f"example:{client_name}:*"):
            self.redis.delete(key)
            deleted += 1
        self.redis.delete(self._intents_key(client_name))
        for key in self.redis.scan_iter(f"examples:domain:{client_name}:*"):
            self.redis.delete(key)
        self.redis.delete(self._metadata_key(client_name))
        return deleted

    def ping(self) -> bool:
        try:
            return bool(self.redis.ping())
        except Exception:
            return False

    @staticmethod
    def _serialize(example: SQLExample) -> dict:
        return {
            "client_name": example.client_name,
            "domain": example.domain,
            "intent": example.intent,
            "description": example.description,
            "sql": example.sql,
            "instructions": example.instructions,
            "version": str(example.version),
            "metadata": json.dumps(example.metadata),
            "created_at": example.created_at.isoformat() if example.created_at else "",
            "updated_at": example.updated_at.isoformat() if example.updated_at else "",
        }

    @staticmethod
    def _deserialize(data: dict) -> SQLExample:
        return SQLExample(
            client_name=data["client_name"],
            domain=data["domain"],
            intent=data["intent"],
            description=data["description"],
            sql=data["sql"],
            instructions=data["instructions"],
            version=int(data["version"]),
            metadata=json.loads(data.get("metadata", "{}")),
            created_at=datetime.fromisoformat(data["created_at"])
            if data.get("created_at")
            else None,
            updated_at=datetime.fromisoformat(data["updated_at"])
            if data.get("updated_at")
            else None,
        )

    @classmethod
    def _decode_hash(cls, data: dict) -> dict:
        decoded = {}
        for key, value in data.items():
            k = cls._decode(key)
            if k == "embedding":
                continue
            decoded[k] = cls._decode(value)
        return decoded

    @staticmethod
    def _decode(value) -> str:
        return value.decode() if isinstance(value, bytes) else value

    @staticmethod
    def _example_key(client_name: str, intent: str) -> str:
        return f"example:{client_name}:{intent}"

    @staticmethod
    def _intents_key(client_name: str) -> str:
        return f"examples:intents:{client_name}"

    @staticmethod
    def _domain_key(client_name: str, domain: str) -> str:
        return f"examples:domain:{client_name}:{domain}"

    @staticmethod
    def _metadata_key(client_name: str) -> str:
        return f"examples:meta:{client_name}"

    @staticmethod
    def _index_name(client_name: str) -> str:
        return f"idx:examples:{client_name}"
