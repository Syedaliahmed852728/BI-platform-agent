from __future__ import annotations

from business.entity_resolution.models import EntityMatch, LookupResponse
from business.entity_resolution.normalizer import EntityNormalizer
from business.entity_resolution.scorer import EntityScorer
from data.models.entity import EntityRecord
from data.redis.entity_repository import EntityRedisRepository


def _singular_forms(text: str) -> list[str]:
    """Naive singular candidates for a plural query, e.g. sofas -> sofa."""
    forms = []
    if text.endswith("ies"):
        forms.append(text[:-3] + "y")
    if text.endswith("es"):
        forms.append(text[:-2])
    if text.endswith("s"):
        forms.append(text[:-1])
    return [f for f in forms if f and f != text]


class EntityResolver:
    def __init__(self, repository: EntityRedisRepository) -> None:
        self.repository = repository

    def lookup(
        self,
        *,
        client_name: str,
        search_text: str,
        entity_types: list[str] | None = None,
        domains: list[str] | None = None,
        limit: int = 10,
    ) -> LookupResponse:
        normalized = EntityNormalizer.normalize_query(search_text)
        if not normalized:
            return self._empty(client_name, "Empty search text.", success=False)

        candidates = self.repository.get_candidates(
            client_name=client_name,
            normalized_query=normalized,
            entity_types=entity_types,
        )
        if not candidates:
            # Entities are stored singular ("sofa"); retry plural queries.
            for singular in _singular_forms(normalized):
                candidates = self.repository.get_candidates(
                    client_name=client_name,
                    normalized_query=singular,
                    entity_types=entity_types,
                )
                if candidates:
                    break
        if not candidates:
            return self._empty(client_name, "No matching entities found.")

        candidates = self._filter_domains(candidates, domains)
        if not candidates:
            return self._empty(client_name, "No entities found for requested domain.")

        matches = EntityScorer.rank(search_text, candidates)
        if not matches:
            return self._empty(client_name, "No matching entities found.")

        matches = matches[:limit]
        return self._build_response(client_name, matches)

    def ping(self) -> bool:
        return self.repository.ping()

    @staticmethod
    def _filter_domains(
        candidates: list[EntityRecord], domains: list[str] | None
    ) -> list[EntityRecord]:
        if not domains:
            return candidates
        allowed = set(domains)
        return [c for c in candidates if c.domain in allowed]

    def _build_response(
        self, client_name: str, matches: list[EntityMatch]
    ) -> LookupResponse:
        exact = any(m.confidence == 100 for m in matches)
        return LookupResponse(
            success=True,
            client_name=client_name,
            resolved=True,
            ambiguous=self._is_ambiguous(matches),
            exact_match_found=exact,
            total_matches=len(matches),
            matches=matches,
            metadata={
                "top_confidence": matches[0].confidence,
                "matched_by": matches[0].matched_by,
                "top_entity_type": matches[0].entity.entity_type,
                "top_domain": matches[0].entity.domain,
            },
        )

    @staticmethod
    def _is_ambiguous(matches: list[EntityMatch]) -> bool:
        if len(matches) <= 1:
            return False
        best = matches[0].confidence
        return sum(1 for m in matches if m.confidence == best) > 1

    @staticmethod
    def _empty(client_name: str, message: str, success: bool = True) -> LookupResponse:
        return LookupResponse(
            success=success,
            client_name=client_name,
            resolved=False,
            ambiguous=False,
            exact_match_found=False,
            total_matches=0,
            message=message,
        )




