from __future__ import annotations

import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from business.intent_learning.models import (
    Domain,
    IntentLearningResult,
    TrainingExample,
)
from business.intent_learning.prompt import SYSTEM_PROMPT, build_prompt
from business.intent_learning.repository import IntentRepository
from configs.business import business_settings

logger = logging.getLogger(__name__)


class IntentLearningAgent:
    def __init__(
        self,
        repository: IntentRepository,
        *,
        model: str | None = None,
    ) -> None:
        self.repository = repository
        self.llm = ChatOpenAI(
            model=model or business_settings.intent_llm_model,
            reasoning_effort=business_settings.llm_reasoning_effort,
            use_responses_api=True,
        ).with_structured_output(IntentLearningResult)

    async def learn(
        self,
        *,
        domain: Domain,
        examples: list[TrainingExample],
    ) -> IntentLearningResult:
        logger.info(
            "learning intents for domain=%s examples=%d", domain.value, len(examples)
        )

        existing = self.repository.load(domain)
        prompt = build_prompt(
            domain=domain,
            existing_intents=[item.model_dump(mode="json") for item in existing],
            examples=examples,
        )

        result: IntentLearningResult = await self.llm.ainvoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]
        )
        logger.info("LLM returned %d proposal(s)", len(result.proposals))
        return result
