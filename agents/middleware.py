from __future__ import annotations

import logging
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.runtime import Runtime

from agents.classifier import DomainClassifier
from agents.sql_executor import SQLExecutorAgent
from business.examples.service import ExampleService
from data.models.example import ExampleMatch

logger = logging.getLogger(__name__)

REUSABLE_SQL_SOURCE = "reusable_sql"

EXECUTION_PROMPT_TEMPLATE = """\
A verified reusable SQL intent exists.

Intent

{intent}

Description

{description}

Reusable SQL

{sql}

Instructions

Reuse this SQL whenever possible.

Only modify

- dates
- entity filters
- company filters
- store filters

Do not redesign the query.

Do not perform planning.

Execute the SQL.

Answer the user using the SQL results.
"""


class ReusableSQLMiddleware(AgentMiddleware):
    """
    Answers a question from a previously learned SQL example when one is
    similar enough, skipping the orchestration LLM entirely.

    Flow: classify domain -> vector-search stored examples -> execute the
    best match with the SQL executor -> short-circuit the agent.

    The cache is an optimization: any failure here is logged and the
    request falls through to the normal LLM path.
    """

    def __init__(
        self,
        *,
        classifier: DomainClassifier,
        example_service: ExampleService,
        sql_executor: SQLExecutorAgent,
        similarity_threshold: float,
    ) -> None:
        super().__init__()
        self._classifier = classifier
        self._example_service = example_service
        self._sql_executor = sql_executor
        self._similarity_threshold = similarity_threshold

    @hook_config(can_jump_to=["end"])
    async def abefore_agent(
        self, state: AgentState, runtime: Runtime
    ) -> dict[str, Any] | None:
        client_name = runtime.context.get("client_name")
        if not client_name:
            logger.warning("no client_name in runtime context; skipping reusable SQL")
            return None

        # abefore_model fires before every model call in the agent loop;
        # only attempt the cache when the model is about to see a fresh
        # user question (mid-loop the last message is a tool result).
        messages = state.get("messages", [])
        if not messages or not isinstance(messages[-1], HumanMessage):
            return None
        question = messages[-1].content

        try:
            match = await self._find_match(client_name=client_name, question=question)
            if match is None:
                return None
            answer = await self._execute(
                match=match, question=question, client_name=client_name
            )
        except Exception:
            logger.exception(
                "reusable SQL path failed for client=%s; falling back to LLM",
                client_name,
            )
            return None

        message = AIMessage(
            content=answer,
            additional_kwargs={
                "source": REUSABLE_SQL_SOURCE,
                "sql": match.example.sql,
                "domain": match.example.domain,
                "similarity": match.similarity,
            },
        )
        return {"messages": [message], "jump_to": "end"}

    async def _find_match(
        self, *, client_name: str, question: str
    ) -> ExampleMatch | None:
        classification = await self._classifier.classify(question)
        logger.info(
            "classified question domain=%s confidence=%.2f",
            classification.domain.value,
            classification.confidence,
        )

        response = await self._example_service.asearch(
            client_name=client_name,
            domain=classification.domain.value,
            query=question,
            similarity_threshold=self._similarity_threshold,
        )
        if not response.matched or not response.matches:
            logger.info("no reusable SQL example above threshold=%.2f", self._similarity_threshold)
            return None

        top = response.matches[0]
        logger.info(
            "reusable SQL hit intent=%r similarity=%.3f", top.example.intent, top.similarity
        )
        return top

    async def _execute(
        self, *, match: ExampleMatch, question: str, client_name: str
    ) -> str:
        prompt = EXECUTION_PROMPT_TEMPLATE.format(
            intent=match.example.intent,
            description=match.example.description,
            sql=match.example.sql,
        )
        result = await self._sql_executor.ainvoke(
            [SystemMessage(content=prompt), HumanMessage(content=question)],
            context={"client_name": client_name},
        )
        return result["messages"][-1].text
