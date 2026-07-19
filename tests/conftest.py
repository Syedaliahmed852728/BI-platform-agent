from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

# The app fails fast without an API key; tests never call OpenAI.
os.environ.setdefault("OPENAI_API_KEY", "test-key")

from business.orchestration.chat_service import ChatResponse  # noqa: E402
from presentation.api.app import create_app  # noqa: E402
from presentation.api.dependencies import get_chat_service  # noqa: E402


class StubChatService:
    """Stands in for ChatService without touching Redis or OpenAI."""

    def __init__(
        self,
        response: ChatResponse | None = None,
        error: Exception | None = None,
    ) -> None:
        self._response = response
        self._error = error

    async def ask(self, *, client_name: str, question: str) -> ChatResponse:
        if self._error is not None:
            raise self._error
        return self._response


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    def make(chat_service: StubChatService | None = None) -> TestClient:
        if chat_service is not None:
            app.dependency_overrides[get_chat_service] = lambda: chat_service
        # No lifespan (it starts schedulers and needs Redis); don't re-raise
        # server exceptions so the JSON error handlers are exercised.
        return TestClient(app, raise_server_exceptions=False)

    return make
