from __future__ import annotations

from business.embeddings.embedder import Embedder
from business.intent_learning.models import Domain
from configs.business import business_settings
from data.models.example import ExampleMatch, SearchResponse, SQLExample
from data.redis.example_repository import ExampleRedisRepository


class ExampleService:
    def __init__(
        self,
        repository: ExampleRedisRepository,
        embedder: Embedder,
    ) -> None:
        self.repository = repository
        self.embedder = embedder

    def add_example(self, example: SQLExample) -> None:
        vector = self.embedder.embed(example.embedding_text)
        self.repository.save(example, vector)

    def add_examples(self, examples: list[SQLExample]) -> int:
        if not examples:
            return 0
        vectors = self.embedder.embed_many(e.embedding_text for e in examples)
        return self.repository.save_many(examples, vectors)

    async def asearch(
        self,
        *,
        client_name: str,
        query: str,
        domain: str | None = None,
        top_k: int | None = None,
        similarity_threshold: float | None = None,
    ) -> SearchResponse:
        vector = await self.embedder.aembed(query)
        return self._build_search_response(
            client_name=client_name,
            query=query,
            vector=vector,
            domain=domain,
            top_k=top_k or business_settings.search_top_k,
            similarity_threshold=(
                similarity_threshold
                if similarity_threshold is not None
                else business_settings.search_similarity_threshold
            ),
        )

    def _build_search_response(
        self,
        *,
        client_name: str,
        query: str,
        vector: list[float],
        domain: str | None,
        top_k: int,
        similarity_threshold: float,
    ) -> SearchResponse:
        matches = self.repository.vector_search(
            client_name=client_name,
            embedding=vector,
            domain=domain,
            top_k=top_k,
        )
        filtered = [
            ExampleMatch(example=m.example, similarity=m.similarity)
            for m in matches
            if m.similarity >= similarity_threshold
        ]
        if not filtered:
            return SearchResponse(
                success=True,
                client_name=client_name,
                query=query,
                matched=False,
                total_matches=0,
                message="No sufficiently similar SQL examples found.",
                metadata={"threshold": similarity_threshold, "domain": domain},
            )
        return SearchResponse(
            success=True,
            client_name=client_name,
            query=query,
            matched=True,
            total_matches=len(filtered),
            matches=filtered,
            metadata={
                "threshold": similarity_threshold,
                "top_similarity": filtered[0].similarity,
                "domain": domain,
            },
        )

    def reembed_client(self, client_name: str) -> dict[str, int]:
        """
        Recompute and store embeddings for every stored example.

        Run after a change to SQLExample.embedding_text so existing
        examples match the new embedding scheme.
        """
        counts: dict[str, int] = {}
        for domain in Domain:
            examples = self.repository.get_domain(client_name, domain.value)
            if examples:
                vectors = self.embedder.embed_many(e.embedding_text for e in examples)
                self.repository.save_many(examples, vectors)
            counts[domain.value] = len(examples)
        return counts

    def clear_client(self, client_name: str) -> int:
        return self.repository.clear_client(client_name)

    def ping(self) -> bool:
        return self.embedder.ping() and self.repository.ping()
