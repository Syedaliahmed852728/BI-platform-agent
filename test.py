from __future__ import annotations

from typing import Any

from langchain.tools import tool
from langgraph.prebuilt import ToolRuntime

from agents.models import AgentContext
from business.entity_resolution.resolver import EntityResolver

from presentation.api.container import entity_resolver as resolver


# def build_resolve_entity_tool(resolver: EntityResolver):
# @tool(parse_docstring=True)
def resolve_entities(
    search_text: str,
    domain: str,
    limit: int,
    # runtime: ToolRuntime[AgentContext, Any],
    # entity_types: list[str] | None = None,
):
    """
    Resolve business entities from user input against the client's Redis cache.

    Args:
        search_text: Original user text containing the entity to resolve.
        domain: Business domain to search within.
        limit: Maximum number of matching entities to return.
        entity_types: Optional list of entity types to restrict the search.
    """
    client_name = "my_database.db"
    if not client_name:
        return {
            "success": False,
            "error": "Missing client_name in runtime context. This tool "
            "must be invoked with context={'client_name': ...}.",
        }

    response = resolver.lookup(
        client_name=client_name,
        search_text=search_text,
        entity_types="",
        domains=[domain] if domain else None,
        limit=limit,
    )
    return response.to_dict()


# return resolve_entities


entities = resolve_entities("sofas", domain="inventory", limit=5)

print(entities)
