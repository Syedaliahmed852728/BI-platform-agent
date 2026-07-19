from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from agents.deep_agent import DeepAgent
from agents.middleware import REUSABLE_SQL_SOURCE
from data.models.queue import QueuedMessage
from data.redis.queue_repository import QueueRedisRepository

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ChatResponse:
    source: str
    answer: str
    sql: str | None = None
    domain: str | None = None
    similarity: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ChatService:
    """
    Coordinates one user chat request: invoke the DeepAgent, queue any
    freshly generated SQL for intent learning, return the response.

    The AI workflow itself (routing, reusable SQL, planning, tools)
    is owned entirely by the agent layer.
    """

    def __init__(
        self,
        *,
        deep_agent: DeepAgent,
        queue_repository: QueueRedisRepository,
    ) -> None:
        self._deep_agent = deep_agent
        self._queue = queue_repository

    async def ask(self, *, client_name: str, question: str) -> ChatResponse:
        result = await self._deep_agent.ask(
            client_name=client_name,
            question=question,
        )

        if result.sql and result.source != REUSABLE_SQL_SOURCE:
            await self._queue_for_learning(client_name, question, result)

        return ChatResponse(
            source=result.source,
            answer=result.answer,
            sql=result.sql,
            domain=result.domain,
            similarity=result.similarity,
            metadata=result.metadata,
        )

    async def _queue_for_learning(self, client_name, question, result) -> None:
        # Learning is best-effort: a queue failure must not fail the answer.
        try:
            await self._queue.add_message(
                QueuedMessage(
                    client_name=client_name,
                    domain=result.domain,
                    original_question=question,
                    sql_output=result.sql,
                )
            )
        except Exception:
            logger.exception(
                "failed to queue SQL example for learning client=%s", client_name
            )
