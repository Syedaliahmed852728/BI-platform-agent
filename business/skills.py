from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger(__name__)

SKILLS_ROOT = Path(__file__).resolve().parent.parent / "skills"

DOMAIN_DIRS = {
    "sales": "sales",
    "inventory": "inventory",
    "purchase_orders": "purchase-orders",
    "customer_finance": "customer-finance",
}

# Order matters: rules first, then how to write SQL, then references.
# SKILL.md is excluded — it is a workflow wrapper duplicating AGENT.md.
SKILL_FILES = (
    "business_rules.md",
    "sql_generation.md",
    "entity_resolution.md",
    "kpi_reference.md",
    "inventory_reference.md",
    "po_reference.md",
    "finance_reference.md",
    "examples.md",
)


@lru_cache(maxsize=None)
def load_domain_skill(domain: str) -> str | None:
    """
    Concatenated skill guidance for a business domain, or None when the
    domain has no skill folder.
    """
    directory = DOMAIN_DIRS.get(domain)
    if directory is None:
        return None

    sections: list[str] = []
    for filename in SKILL_FILES:
        path = SKILLS_ROOT / directory / filename
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8").strip()
        if content:
            sections.append(content)

    if not sections:
        logger.warning("no skill files found for domain=%s in %s", domain, SKILLS_ROOT)
        return None
    return "\n\n---\n\n".join(sections)
