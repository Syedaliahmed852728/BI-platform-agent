from __future__ import annotations

from enum import Enum
from typing import Any, TypedDict

from pydantic import BaseModel, ConfigDict, Field


class AgentContext(TypedDict):
    """Run-scoped context shared with middleware and tools."""

    client_name: str


class BusinessDomain(str, Enum):
    """
    Supported business domains.

    These values should remain aligned with the business skills
    available to the DeepAgent.
    """

    SALES = "sales"
    INVENTORY = "inventory"
    PURCHASE_ORDERS = "purchase_orders"
    CUSTOMER_FINANCE = "customer_finance"
    DELIVERY = "delivery"
    GENERAL_LEDGER = "general_ledger"


class DomainClassification(BaseModel):
    """
    Result returned by the domain classifier.
    """

    model_config = ConfigDict(frozen=True)

    domain: BusinessDomain = Field(description="Predicted business domain.")

    confidence: float = Field(ge=0, le=1, description="Classifier confidence.")

    reasoning: str | None = Field(
        default=None,
        description="Optional explanation for debugging.",
    )


class AgentResponse(BaseModel):
    """
    Final response returned by the DeepAgent.

    This is the only response model the Business layer should
    consume. The Business layer should never depend on LangChain
    messages or LangGraph state.
    """

    answer: str = Field(
        description="Final natural-language response returned to the user."
    )

    source: str = Field(
        description="Source that generated the response (e.g. reusable_sql, deep_agent)."
    )

    sql: str | None = Field(
        default=None,
        description="SQL executed to answer the request.",
    )

    domain: str | None = Field(
        default=None,
        description="Business domain selected by the agent.",
    )

    similarity: float | None = Field(
        default=None,
        description="Similarity score when a reusable SQL was used.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional execution metadata.",
    )
