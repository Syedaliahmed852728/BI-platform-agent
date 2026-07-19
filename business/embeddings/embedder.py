from __future__ import annotations

import os
from typing import Iterable

from openai import AsyncOpenAI, OpenAI

from configs.business import business_settings


class EmbeddingError(RuntimeError):
    pass


class Embedder:
    """
    Thin wrapper around OpenAI embeddings with dimension validation.

    Sync methods exist for worker code running in threads; async
    methods serve the request path.
    """

    def __init__(
        self,
        *,
        model: str | None = None,
        dimensions: int | None = None,
        client: OpenAI | None = None,
        async_client: AsyncOpenAI | None = None,
    ) -> None:
        self.model = model or business_settings.embedding_model
        self.dimensions = dimensions or business_settings.embedding_dimensions
        self._max_batch = business_settings.embedding_max_batch
        api_key = os.environ.get("OPENAI_API_KEY")
        self.client = client or OpenAI(api_key=api_key)
        self.async_client = async_client or AsyncOpenAI(api_key=api_key)

    def embed(self, text: str) -> list[float]:
        return self._extract_one(self._request(self._clean_one(text)))

    async def aembed(self, text: str) -> list[float]:
        return self._extract_one(await self._arequest(self._clean_one(text)))

    def embed_many(self, texts: Iterable[str]) -> list[list[float]]:
        cleaned = self._clean_many(texts)
        if not cleaned:
            return []
        if len(cleaned) > self._max_batch:
            raise EmbeddingError(f"max batch is {self._max_batch}")
        return self._extract_many(self._request(cleaned))

    async def aembed_many(self, texts: Iterable[str]) -> list[list[float]]:
        cleaned = self._clean_many(texts)
        if not cleaned:
            return []
        return self._extract_many(await self._arequest(cleaned))

    def ping(self) -> bool:
        try:
            self.embed("ping")
            return True
        except Exception:
            return False

    @staticmethod
    def _clean_one(text: str) -> str:
        text = text.strip()
        if not text:
            raise EmbeddingError("cannot embed empty text")
        return text

    @staticmethod
    def _clean_many(texts: Iterable[str]) -> list[str]:
        return [t.strip() for t in texts if t.strip()]

    def _request(self, text_or_texts):
        try:
            return self.client.embeddings.create(
                model=self.model, input=text_or_texts, dimensions=self.dimensions
            )
        except Exception as exc:
            raise EmbeddingError(f"embedding failed: {exc}") from exc

    async def _arequest(self, text_or_texts):
        try:
            return await self.async_client.embeddings.create(
                model=self.model, input=text_or_texts, dimensions=self.dimensions
            )
        except Exception as exc:
            raise EmbeddingError(f"embedding failed: {exc}") from exc

    def _extract_one(self, response) -> list[float]:
        vector = response.data[0].embedding
        self._validate(vector)
        return vector

    def _extract_many(self, response) -> list[list[float]]:
        vectors = [item.embedding for item in response.data]
        for vector in vectors:
            self._validate(vector)
        return vectors

    def _validate(self, vector: list[float]) -> None:
        if len(vector) != self.dimensions:
            raise EmbeddingError(
                f"expected dim {self.dimensions}, got {len(vector)}"
            )
