from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone

from business.examples.service import ExampleService
from business.intent_learning.agent import IntentLearningAgent
from business.intent_learning.models import Domain, TrainingExample
from configs.business import business_settings
from configs.presentation import presentation_settings
from data.models.example import SearchResponse, SQLExample
from data.models.queue import ClientBatch, ContextPayload
from data.redis.queue_repository import QueueRedisRepository

logger = logging.getLogger(__name__)


class SQLContextWorker:
    def __init__(
        self,
        queue: QueueRedisRepository,
        example_service: ExampleService,
        intent_learning_agent_factory=None,
    ) -> None:
        self.queue = queue
        self.example_service = example_service
        self._agent_factory = intent_learning_agent_factory
        self.running = False
        self.last_results: dict[str, dict] = {}
        self.last_learned: dict[str, list[SQLExample]] = {}
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        if self.running:
            return
        self.running = True
        self._task = asyncio.create_task(self._run())
        logger.info("SQL context worker started")

    async def stop(self) -> None:
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            except Exception:
                logger.exception("worker task exited with error during stop")
        logger.info("SQL context worker stopped")

    async def _run(self) -> None:
        interval = presentation_settings.queue_poll_interval_seconds
        while self.running:
            try:
                await self._cycle()
            except Exception:
                logger.exception("worker cycle failed")
            await asyncio.sleep(interval)

    async def _cycle(self) -> None:
        clients = await self.queue.active_clients()
        if not clients:
            return

        ready_clients: list[tuple[str, str]] = []
        for client in clients:
            ready, reason = await self.queue.batch_ready(client)
            if ready:
                ready_clients.append((client, reason))

        if not ready_clients:
            return

        batches = await asyncio.gather(
            *(self.queue.read_batch(c, r) for c, r in ready_clients)
        )
        await asyncio.gather(*(self._process_batch(b) for b in batches))

    async def _process_batch(self, batch: ClientBatch) -> None:
        logger.info(
            "processing batch client=%s size=%d reason=%s",
            batch.client_name,
            batch.size,
            batch.reason,
        )
        try:
            context, response = await self._build_context(batch)
            await self.queue.publish_context(
                client_name=batch.client_name, text=context.text
            )
            self._record_result(
                batch, status="success", context_text=context.text, search=response
            )
            await self._learn_intents(batch)
        except Exception as exc:
            logger.exception("batch failed for %s", batch.client_name)
            self._record_result(batch, status="failed", error=str(exc))
        finally:
            await self.queue.clear_batch(batch)

    async def _build_context(
        self, batch: ClientBatch
    ) -> tuple[ContextPayload, SearchResponse]:
        query = "\n".join(m.original_question for m in batch.messages)
        response = await self.example_service.asearch(
            client_name=batch.client_name,
            query=query,
            domain=batch.messages[0].domain,
            top_k=business_settings.search_top_k,
            similarity_threshold=business_settings.search_similarity_threshold,
        )
        return ContextPayload(
            text=self._build_prompt_text(batch, response),
            client_name=batch.client_name,
        ), response

    @staticmethod
    def _build_prompt_text(batch: ClientBatch, response: SearchResponse) -> str:
        new_lines = "\n".join(
            f"{i}. user question: {m.original_question} :- {m.sql_output}"
            for i, m in enumerate(batch.messages, start=1)
        )
        related_lines = ""
        if response.matched:
            related_lines = "\n".join(
                f"{i}. user question: {m.example.intent} :- {m.example.sql}"
                for i, m in enumerate(response.matches, start=1)
            )
        return (
            f"new user question:\n\n{new_lines}\n\n\n"
            f"already related examples:\n\n{related_lines}\n"
        )

    async def _learn_intents(self, batch: ClientBatch) -> None:
        if self._agent_factory is None:
            return
        try:
            agent: IntentLearningAgent = self._agent_factory(batch.client_name)
            domain = Domain(batch.messages[0].domain)
            training = [
                TrainingExample(
                    domain=domain,
                    user_question=m.original_question,
                    sql_query=m.sql_output,
                )
                for m in batch.messages
            ]
            result = await agent.learn(domain=domain, examples=training)
            examples = self._proposals_to_examples(
                client_name=batch.client_name,
                domain=domain,
                proposals=result.proposals,
                agent=agent,
                batch_questions=[m.original_question for m in batch.messages],
            )
            if examples:
                saved = await asyncio.to_thread(
                    self.example_service.add_examples, examples
                )
                logger.info(
                    "saved %d/%d learned examples for %s",
                    saved,
                    len(examples),
                    batch.client_name,
                )
            self.last_learned[batch.client_name] = examples
        except Exception:
            logger.exception("intent learning failed for %s", batch.client_name)

    @staticmethod
    def _proposals_to_examples(
        *,
        client_name: str,
        domain: Domain,
        proposals,
        agent: IntentLearningAgent,
        batch_questions: list[str],
    ) -> list[SQLExample]:
        if not proposals:
            return []
        existing = {item.intent: item for item in agent.repository.load(domain)}
        now = datetime.now(timezone.utc)
        examples: list[SQLExample] = []
        for proposal in proposals:
            if proposal.action == "IGNORE":
                continue
            if proposal.action == "UPDATE":
                current = existing.get(proposal.existing_intent)
                version = current.version + 1 if current else 1
            else:
                version = 1
            examples.append(
                SQLExample(
                    client_name=client_name,
                    domain=domain.value,
                    intent=proposal.intent,
                    description=proposal.description,
                    sql=proposal.sql,
                    instructions=proposal.instructions,
                    version=version,
                    metadata={
                        "action": proposal.action,
                        "existing_intent": proposal.existing_intent,
                        "confidence": proposal.confidence,
                        "reasoning": proposal.reasoning,
                        "sample_questions": proposal.source_questions or batch_questions,
                    },
                    created_at=now,
                    updated_at=now,
                )
            )
        return examples

    def _record_result(
        self,
        batch: ClientBatch,
        *,
        status: str,
        context_text: str | None = None,
        search=None,
        error: str | None = None,
    ) -> None:
        result: dict = {
            "status": status,
            "client_name": batch.client_name,
            "batch_size": batch.size,
            "reason": batch.reason,
            "questions": [m.original_question for m in batch.messages],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        if status == "success":
            result["context_text"] = context_text
            result["search"] = {
                "matched": search.matched,
                "total_matches": search.total_matches,
                "matches": [
                    {
                        "intent": m.example.intent,
                        "domain": m.example.domain,
                        "sql": m.example.sql,
                        "similarity": m.similarity,
                    }
                    for m in search.matches
                ],
            }
        else:
            result["error"] = error
        self.last_results[batch.client_name] = result
