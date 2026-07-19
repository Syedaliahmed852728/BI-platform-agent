from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from agents.llm import get_structured_model
from agents.models import DomainClassification
from agents.prompt_loader import load_prompt


class DomainClassifier:
    """
    LLM-powered classifier mapping a user question to a business domain.
    """

    def __init__(self) -> None:
        self._llm = get_structured_model(DomainClassification)
        self._system_prompt = load_prompt("DOMAIN_CLASSIFIER.md")

    async def classify(self, question: str) -> DomainClassification:
        return await self._llm.ainvoke(
            [
                SystemMessage(content=self._system_prompt),
                HumanMessage(content=question),
            ]
        )
