from __future__ import annotations

from rapidfuzz import fuzz

from business.entity_resolution.models import EntityMatch
from business.entity_resolution.normalizer import EntityNormalizer
from data.models.entity import EntityRecord


class EntityScorer:
    @classmethod
    def score(cls, query: str, entity: EntityRecord) -> EntityMatch | None:
        normalized_query = EntityNormalizer.normalize_query(query)
        if not normalized_query:
            return None
        confidence, matched_by = cls._calculate_score(
            normalized_query, entity.normalized
        )
        if confidence == 0:
            return None
        return EntityMatch(
            entity=entity, confidence=confidence, matched_by=matched_by
        )

    @classmethod
    def rank(cls, query: str, entities: list[EntityRecord]) -> list[EntityMatch]:
        matches = [m for m in (cls.score(query, e) for e in entities) if m]
        matches.sort(
            key=lambda m: (-m.confidence, -m.entity.priority, m.entity.value)
        )
        return matches

    @classmethod
    def _calculate_score(cls, query: str, candidate: str) -> tuple[int, str]:
        if not query or not candidate:
            return 0, "none"
        if query == candidate:
            return 100, "exact"
        if candidate.startswith(query):
            return 97, "prefix"
        if query in candidate:
            return 94, "contains"
        token_set = fuzz.token_set_ratio(query, candidate)
        if token_set >= 95:
            return int(token_set), "token_set"
        token_sort = fuzz.token_sort_ratio(query, candidate)
        if token_sort >= 92:
            return int(token_sort), "token_sort"
        partial = fuzz.partial_ratio(query, candidate)
        if partial >= 90:
            return int(partial), "partial"
        weighted = fuzz.WRatio(query, candidate)
        if weighted >= 85:
            return int(weighted), "weighted"
        return 0, "none"
