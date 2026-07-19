from __future__ import annotations

from typing import Any

from langchain.agents import create_agent
from langchain_core.messages import BaseMessage

from agents.llm import get_chat_model
from agents.models import AgentContext
from agents.prompt_loader import load_prompt
from business.tools import run_sql_query
from configs.business import business_settings


class SQLExecutorAgent:
    """
    Minimal agent that executes SQL via the run_sql_query tool and
    answers from the results.
    """

    def __init__(self, *, model: str | None = None) -> None:
        self._agent = create_agent(
            model=get_chat_model(
                model or business_settings.orchestration_llm_model,
                reasoning=True,
            ),
            system_prompt=load_prompt("SQL_EXECUTOR.md"),
            tools=[run_sql_query],
            context_schema=AgentContext,
        )

    async def ainvoke(
        self, messages: list[BaseMessage], *, context: AgentContext
    ) -> dict[str, Any]:
        return await self._agent.ainvoke({"messages": messages}, context=context)
