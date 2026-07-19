from __future__ import annotations

from functools import lru_cache
from pathlib import Path

_PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


@lru_cache(maxsize=None)
def load_prompt(filename: str) -> str:
    """
    Load a prompt from the agents/prompts directory.

    Prompts are cached after the first read to avoid repeated disk I/O.

    Parameters
    ----------
    filename
        Prompt filename, e.g. "AGENT.md" or "SQL_EXECUTOR.md".

    Returns
    -------
    str
        Prompt contents.

    Raises
    ------
    FileNotFoundError
        If the prompt file does not exist.
    """

    path = _PROMPTS_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")

    return path.read_text(encoding="utf-8")
