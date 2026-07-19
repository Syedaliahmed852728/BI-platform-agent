from __future__ import annotations

from fastapi import APIRouter, Depends

from business.examples.service import ExampleService
from business.entity_resolution.resolver import EntityResolver
from presentation.api.dependencies import get_entity_resolver, get_example_service

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(
    example_service: ExampleService = Depends(get_example_service),
    entity_resolver: EntityResolver = Depends(get_entity_resolver),
) -> dict:
    return {
        "examples": example_service.ping(),
        "entities": entity_resolver.ping(),
    }
