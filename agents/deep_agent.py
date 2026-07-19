from __future__ import annotations

import logging
from typing import Any

from deepagents import create_deep_agent, register_harness_profile, HarnessProfile
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from deepagents.backends.filesystem import FilesystemBackend
from pathlib import Path


from agents.middleware import REUSABLE_SQL_SOURCE
from agents.models import AgentContext, AgentResponse

logger = logging.getLogger(__name__)


class DeepAgent:
    """
    Facade over the LangGraph deep agent.

    Callers get an AgentResponse; LangChain messages and graph state
    never leave this class.
    """

    def __init__(
        self,
        *,
        model: str | BaseChatModel,
        system_prompt: str,
        tools: list[Any],
        middleware: list[Any] | None = None,
        checkpointer: Any | None = None,
    ) -> None:

        if isinstance(model, str):
            model_key = model
        elif isinstance(model, BaseChatModel):
            model_name = getattr(model, "model_name", None)
            if model_name is None:
                raise ValueError(
                    f"Could not determine model_name from {type(model).__name__}"
                )
            model_key = f"openai:{model_name}"
        else:
            raise TypeError(f"Unsupported model type: {type(model).__name__}")

        backend = FilesystemBackend(
            root_dir=".",
            virtual_mode=False,
        )

        register_harness_profile(
            model_key,
            HarnessProfile(
                base_system_prompt=system_prompt,
                excluded_tools={
                    "ls",
                    "write_file",
                    "edit_file",
                    "glob",
                    "grep",
                    "execute",
                    "write_todos",
                },
            ),
        )

        self._agent = create_deep_agent(
            model=model,
            backend=backend,
            system_prompt=system_prompt,
            tools=tools,
            middleware=middleware or [],
            checkpointer=checkpointer,
            context_schema=AgentContext,
            skills=[str(Path("skills").resolve())],
        )

    async def ask(
        self,
        *,
        client_name: str,
        question: str,
        thread_id: str | None = None,
    ) -> AgentResponse:
        state = await self._agent.ainvoke(
            {"messages": [HumanMessage(content=question)]},
            # Read by the middleware and tools via runtime.context.
            context={"client_name": client_name},
            config={
                "configurable": {
                    # Per-client threads so tenants never share memory.
                    "thread_id": thread_id or f"client:{client_name}",
                }
            },
        )

        messages = state.get("messages", [])
        if not messages:
            logger.warning("agent returned no messages for client=%s", client_name)
            return AgentResponse(answer="", source="deep_agent")

        final = messages[-1]

        # A reusable-SQL cache hit carries its own structured metadata.
        meta = getattr(final, "additional_kwargs", {}) or {}
        if meta.get("source") == REUSABLE_SQL_SOURCE:
            return AgentResponse(
                answer=final.text,
                source=REUSABLE_SQL_SOURCE,
                sql=meta.get("sql"),
                domain=meta.get("domain"),
                similarity=meta.get("similarity"),
            )

        return AgentResponse(
            answer=final.text,
            source="deep_agent",
            sql=self._extract_last_sql(messages),
            domain=self._extract_domain(messages),
        )

    @staticmethod
    def _iter_tool_calls(messages: list[Any]):
        for message in messages:
            for call in getattr(message, "tool_calls", None) or []:
                if isinstance(call, dict):
                    yield call.get("name"), call.get("args", {})
                else:
                    yield getattr(call, "name", None), getattr(call, "args", {})

    @classmethod
    def _extract_last_sql(cls, messages: list[Any]) -> str | None:
        """Return the last SQL passed to run_sql_query, if any."""
        sql = None
        for name, args in cls._iter_tool_calls(messages):
            if name == "run_sql_query" and args.get("sql_query"):
                sql = args["sql_query"]
        return sql

    @classmethod
    def _extract_domain(cls, messages: list[Any]) -> str | None:
        """Return the domain the agent inspected via get_domain_summary."""
        for name, args in cls._iter_tool_calls(messages):
            if name == "get_domain_summary" and args.get("domain"):
                return args["domain"]
        return None
