from __future__ import annotations

import asyncio

from fastapi import APIRouter, Depends, Path

from business.entity_resolution.resolver import EntityResolver
from business.examples.service import ExampleService
from business.workers.entity_refresher import EntityRefresher
from business.workers.queue_worker import SQLContextWorker
from configs.data import data_settings
from presentation.api.dependencies import (
    get_entity_refresher,
    get_entity_resolver,
    get_example_service,
    get_queue_worker,
)
from presentation.api.schemas import EntityLookupRequest, RefreshRequest

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/refresh")
async def refresh_clients(
    request: RefreshRequest,
    refresher: EntityRefresher = Depends(get_entity_refresher),
) -> dict:
    results = await refresher.refresh_all(request.clients)
    return {
        "summary": refresher.summarize(results),
        "results": [
            {
                "client_name": r.client_name,
                "success": r.success,
                "entity_count": r.entity_count,
                "duration_seconds": r.duration_seconds,
                "message": r.message,
            }
            for r in results
        ],
    }


@router.post("/entities/{client_name}/lookup")
async def entity_lookup(
    client_name: str = Path(..., min_length=1),
    request: EntityLookupRequest = ...,
    resolver: EntityResolver = Depends(get_entity_resolver),
) -> dict:
    response = resolver.lookup(
        client_name=data_settings.canonical_client_name(client_name),
        search_text=request.search_text,
        entity_types=request.entity_types,
        domains=request.domains,
        limit=request.limit,
    )
    return response.to_dict()


@router.post("/examples/{client_name}/reembed")
async def reembed_examples(
    client_name: str = Path(..., min_length=1),
    example_service: ExampleService = Depends(get_example_service),
) -> dict:
    client_name = data_settings.canonical_client_name(client_name)
    counts = await asyncio.to_thread(example_service.reembed_client, client_name)
    return {"client_name": client_name, "reembedded": counts}


@router.get("/queue/last-result/{client_name}")
async def queue_last_result(
    client_name: str = Path(..., min_length=1),
    worker: SQLContextWorker = Depends(get_queue_worker),
) -> dict:
    result = worker.last_results.get(data_settings.canonical_client_name(client_name))
    return {"result": result}
