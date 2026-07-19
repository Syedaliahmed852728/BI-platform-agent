from __future__ import annotations

import logging
import time

from fastapi import APIRouter, Depends, Path

from business.orchestration.chat_service import ChatService
from configs.data import data_settings
from presentation.api.dependencies import get_chat_service
from presentation.api.schemas import ChatRequest, ChatResponsePayload

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/{client_name}", response_model=ChatResponsePayload)
async def chat(
    client_name: str = Path(..., min_length=1),
    request: ChatRequest = ...,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponsePayload:
    client_name = data_settings.canonical_client_name(client_name)
    logger.info("chat request client=%s", client_name)
    started = time.perf_counter()

    response = await chat_service.ask(
        client_name=client_name,
        question=request.question,
    )

    logger.info(
        "chat response client=%s source=%s duration=%.2fs",
        client_name,
        response.source,
        time.perf_counter() - started,
    )
    return ChatResponsePayload(
        source=response.source,
        answer=response.answer,
        sql=response.sql,
        domain=response.domain,
        similarity=response.similarity,
        metadata=response.metadata,
    )
