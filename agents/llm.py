from __future__ import annotations

from functools import lru_cache
from typing import TypeVar

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from configs.business import business_settings

SchemaT = TypeVar("SchemaT", bound=BaseModel)


@lru_cache(maxsize=None)
def get_chat_model(model: str | None = None, *, reasoning: bool = False) -> ChatOpenAI:
    """
    Shared, cached chat model factory.

    With reasoning=True the model gets the configured reasoning effort
    and no temperature (reasoning models reject non-default temperature).
    """
    name = model or business_settings.openai_chat_model

    if reasoning:
        return ChatOpenAI(
            model=name,
            reasoning_effort=business_settings.llm_reasoning_effort,
            # gpt-5.x only supports tools + reasoning on the Responses API.
            use_responses_api=True,
            api_key=business_settings.openai_api_key,
        )
    return ChatOpenAI(
        model=name,
        temperature=0,
        api_key=business_settings.openai_api_key,
    )


def get_structured_model(schema: type[SchemaT]) -> ChatOpenAI:
    """
    Structured-output wrapper around the shared non-reasoning model.
    """
    return get_chat_model().with_structured_output(schema)
