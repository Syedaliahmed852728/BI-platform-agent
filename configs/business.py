from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, slots=True)
class BusinessSettings:
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    embedding_dimensions: int = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
    embedding_max_batch: int = int(os.getenv("EMBEDDING_MAX_BATCH", "512"))

    orchestration_llm_model: str = os.getenv("ORCHESTRATION_LLM_MODEL", "gpt-5.5")

    intent_llm_model: str = os.getenv("INTENT_LLM_MODEL", "gpt-5.4-mini")

    # Reasoning effort for the SQL-generating models (orchestrator, SQL
    # executor, intent learner). The classifier stays non-reasoning for speed.
    llm_reasoning_effort: str = os.getenv("LLM_REASONING_EFFORT", "medium")

    batch_size: int = int(os.getenv("QUEUE_BATCH_SIZE", "5"))
    batch_timeout_seconds: int = int(os.getenv("QUEUE_BATCH_TIMEOUT_SECONDS", "600"))

    search_top_k: int = int(os.getenv("SEARCH_TOP_K", "5"))
    search_similarity_threshold: float = float(
        os.getenv("SEARCH_SIMILARITY_THRESHOLD", "0.80")
    )
    reusable_sql_similarity_threshold: float = float(
        os.getenv("REUSABLE_SQL_SIMILARITY_THRESHOLD", "0.70")
    )

    stream_key_prefix: str = "sql_stream"
    marker_key_prefix: str = "sql_stream_marker"
    active_clients_key: str = "sql_stream:active_clients"
    output_stream_prefix: str = "sql_context_output"

    openai_chat_model: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-5.4-mini")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")


business_settings = BusinessSettings()
