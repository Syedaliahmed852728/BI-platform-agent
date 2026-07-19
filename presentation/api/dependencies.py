from __future__ import annotations

from business.entity_resolution.resolver import EntityResolver
from business.examples.service import ExampleService
from business.orchestration.chat_service import ChatService
from business.workers.entity_refresher import EntityRefresher
from business.workers.queue_worker import SQLContextWorker
from presentation.api.container import container


def get_chat_service() -> ChatService:
    return container.chat_service


def get_example_service() -> ExampleService:
    return container.example_service


def get_entity_resolver() -> EntityResolver:
    return container.entity_resolver


def get_entity_refresher() -> EntityRefresher:
    return container.entity_refresher


def get_queue_worker() -> SQLContextWorker:
    return container.queue_worker
