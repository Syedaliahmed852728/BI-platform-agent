from __future__ import annotations

import logging

import openai
import redis.exceptions
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from business.embeddings.embedder import EmbeddingError

logger = logging.getLogger(__name__)


def _error_response(status_code: int, error_type: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"type": error_type, "message": message}},
    )


async def _handle_upstream_error(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("upstream AI service error on %s %s", request.method, request.url.path)
    return _error_response(
        502, "upstream", "The AI service is currently unavailable. Please retry."
    )


async def _handle_redis_error(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("redis unavailable on %s %s", request.method, request.url.path)
    return _error_response(
        503, "dependency_unavailable", "A required backend service is unavailable."
    )


async def _handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled error on %s %s", request.method, request.url.path)
    return _error_response(500, "internal", "An internal error occurred.")


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(EmbeddingError, _handle_upstream_error)
    app.add_exception_handler(openai.OpenAIError, _handle_upstream_error)
    app.add_exception_handler(redis.exceptions.RedisError, _handle_redis_error)
    app.add_exception_handler(Exception, _handle_unexpected_error)
