from __future__ import annotations

from datetime import datetime
from enum import Enum
from hashlib import sha256
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class Domain(str, Enum):
    SALES = "sales"
    INVENTORY = "inventory"
    PURCHASE_ORDERS = "purchase_orders"
    CUSTOMER_FINANCE = "customer_finance"


class TrainingExample(BaseModel):
    model_config = ConfigDict(extra="forbid")

    example_id: str = Field(default_factory=lambda: str(uuid4()))
    domain: Domain
    user_question: str
    sql_query: str
    sql_hash: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def model_post_init(self, __context):
        if self.sql_hash is None:
            self.sql_hash = sha256(self.sql_query.encode()).hexdigest()


class IntentExample(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent: str
    description: str
    sql: str
    instructions: str
    version: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class IntentProposal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["CREATE", "UPDATE", "IGNORE"]
    existing_intent: str | None = None
    intent: str
    description: str
    sql: str
    instructions: str
    source_questions: list[str] = Field(
        default_factory=list,
        description="Original user questions this intent covers, verbatim.",
    )
    version: int = 1
    confidence: float = Field(ge=0, le=1)
    reasoning: str


class TrainingBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    examples: list[TrainingExample]


class IntentLearningResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    proposals: list[IntentProposal]
