from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from langgraph.checkpoint.memory import InMemorySaver

from agents.classifier import DomainClassifier
from agents.deep_agent import DeepAgent
from agents.llm import get_chat_model
from agents.middleware import ReusableSQLMiddleware
from agents.prompt_loader import load_prompt
from agents.sql_executor import SQLExecutorAgent
from business.embeddings.embedder import Embedder
from business.entity_resolution.resolver import EntityResolver
from business.examples.service import ExampleService
from business.intent_learning.agent import IntentLearningAgent
from business.intent_learning.repository import IntentRepository
from business.orchestration.chat_service import ChatService
from business.tools.domain_summary import get_domain_summary
from business.tools.resolve_entity import build_resolve_entity_tool
from business.tools.sql_tools import run_sql_query
from business.workers.entity_refresher import EntityRefresher
from business.workers.queue_worker import SQLContextWorker
from configs.business import business_settings
from data.redis.client import get_async_redis, get_sync_redis
from data.redis.entity_repository import EntityRedisRepository
from data.redis.example_repository import ExampleRedisRepository
from data.redis.queue_repository import QueueRedisRepository


@dataclass
class Container:
    """
    Single composition root: wires repositories, services, workers,
    and the agent stack.
    """

    # ------------------------------------------------------------------
    # Data layer
    # ------------------------------------------------------------------

    @cached_property
    def entity_repository(self) -> EntityRedisRepository:
        return EntityRedisRepository(get_sync_redis())

    @cached_property
    def example_repository(self) -> ExampleRedisRepository:
        return ExampleRedisRepository(
            get_sync_redis(), business_settings.embedding_dimensions
        )

    @cached_property
    def queue_repository(self) -> QueueRedisRepository:
        return QueueRedisRepository(get_async_redis())

    # ------------------------------------------------------------------
    # Business services
    # ------------------------------------------------------------------

    @cached_property
    def embedder(self) -> Embedder:
        return Embedder()

    @cached_property
    def entity_resolver(self) -> EntityResolver:
        return EntityResolver(self.entity_repository)

    @cached_property
    def example_service(self) -> ExampleService:
        return ExampleService(self.example_repository, self.embedder)

    # ------------------------------------------------------------------
    # Agent stack
    # ------------------------------------------------------------------

    @cached_property
    def classifier(self) -> DomainClassifier:
        return DomainClassifier()

    @cached_property
    def sql_executor(self) -> SQLExecutorAgent:
        return SQLExecutorAgent()

    @cached_property
    def reusable_sql_middleware(self) -> ReusableSQLMiddleware:
        return ReusableSQLMiddleware(
            classifier=self.classifier,
            example_service=self.example_service,
            sql_executor=self.sql_executor,
            similarity_threshold=business_settings.reusable_sql_similarity_threshold,
        )

    @cached_property
    def deep_agent(self) -> DeepAgent:
        return DeepAgent(
            model=get_chat_model(
                business_settings.orchestration_llm_model, reasoning=True
            ),
            system_prompt=load_prompt("AGENT.md"),
            tools=[
                get_domain_summary,
                run_sql_query,
                build_resolve_entity_tool(self.entity_resolver),
            ],
            middleware=[self.reusable_sql_middleware],
            checkpointer=InMemorySaver(),
        )

    @cached_property
    def chat_service(self) -> ChatService:
        return ChatService(
            deep_agent=self.deep_agent,
            queue_repository=self.queue_repository,
        )

    # ------------------------------------------------------------------
    # Workers
    # ------------------------------------------------------------------

    @cached_property
    def entity_refresher(self) -> EntityRefresher:
        return EntityRefresher(self.entity_repository)

    @cached_property
    def queue_worker(self) -> SQLContextWorker:
        return SQLContextWorker(
            queue=self.queue_repository,
            example_service=self.example_service,
            intent_learning_agent_factory=self._intent_agent_factory,
        )

    def _intent_agent_factory(self, client_name: str) -> IntentLearningAgent:
        return IntentLearningAgent(IntentRepository(self.example_repository, client_name))


container = Container()
