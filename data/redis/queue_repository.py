from __future__ import annotations

import redis.asyncio as aioredis

from configs.business import business_settings
from data.models.queue import ClientBatch, QueuedMessage


class QueueRedisRepository:
    def __init__(self, redis_client: aioredis.Redis) -> None:
        self.redis = redis_client

    async def add_message(self, message: QueuedMessage) -> str:
        stream = self._stream_key(message.client_name)
        stream_id = await self.redis.xadd(stream, fields=message.to_redis_fields())
        message.stream_id = stream_id

        await self.redis.sadd(
            business_settings.active_clients_key, message.client_name
        )

        marker = self._marker_key(message.client_name)
        if not await self.redis.exists(marker):
            await self.redis.set(
                marker, "1", ex=business_settings.batch_timeout_seconds
            )
        return stream_id

    async def active_clients(self) -> list[str]:
        clients = await self.redis.smembers(business_settings.active_clients_key)
        return sorted(clients)

    async def pending_count(self, client_name: str) -> int:
        return await self.redis.xlen(self._stream_key(client_name))

    async def batch_ready(self, client_name: str) -> tuple[bool, str | None]:
        count = await self.pending_count(client_name)
        if count == 0:
            return False, None
        if count >= business_settings.batch_size:
            return True, "size"
        if not await self.redis.exists(self._marker_key(client_name)):
            return True, "timeout"
        return False, None

    async def read_batch(self, client_name: str, reason: str) -> ClientBatch:
        entries = await self.redis.xrange(
            self._stream_key(client_name), min="-", max="+"
        )
        messages = [
            QueuedMessage.from_redis_entry(stream_id=sid, fields=fields)
            for sid, fields in entries
        ]
        return ClientBatch(client_name=client_name, messages=messages, reason=reason)

    async def clear_batch(self, batch: ClientBatch) -> None:
        pipe = self.redis.pipeline()
        pipe.delete(self._stream_key(batch.client_name))
        pipe.delete(self._marker_key(batch.client_name))
        pipe.srem(business_settings.active_clients_key, batch.client_name)
        await pipe.execute()

    async def publish_context(self, *, client_name: str, text: str) -> str:
        return await self.redis.xadd(
            self._output_stream_key(client_name),
            {"client_name": client_name, "text": text},
        )

    async def close(self) -> None:
        await self.redis.close()

    @staticmethod
    def _stream_key(client_name: str) -> str:
        return f"{business_settings.stream_key_prefix}:{client_name}"

    @staticmethod
    def _marker_key(client_name: str) -> str:
        return f"{business_settings.marker_key_prefix}:{client_name}"

    @staticmethod
    def _output_stream_key(client_name: str) -> str:
        return f"{business_settings.output_stream_prefix}:{client_name}"
