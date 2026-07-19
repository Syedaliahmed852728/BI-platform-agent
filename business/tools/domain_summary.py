from __future__ import annotations

from langchain.tools import tool

from business.entity_config.registry import ENTITY_CONFIG
from business.entity_config.utils import get_table_details, get_tables
# from business.skills import load_domain_skill


@tool(parse_docstring=True)
def get_domain_summary(domain: str) -> dict:
    """
    Return the complete metadata and rules for a business domain.

    Args:
        domain: name of business domain.

    Returns:
        Domain metadata including description, tables, table details, and
        the domain's mandatory guidance (business rules, SQL generation
        rules, KPI reference, examples).
    """
    config = ENTITY_CONFIG.get(domain)
    if config is None:
        return {
            "domain": "Unknown",
            "description": (
                "please enter the correct domain Options "
                "(sales, inventory, purchase_orders, customer_finance)"
            ),
            "tables": [],
            "table_details": {},
        }
    return {
        "domain": config.name,
        "description": config.description.strip(),
        "tables": get_tables(config),
        "table_details": get_table_details(config),
        # "guidance": load_domain_skill(domain), TODO
        "guidance": "",
    }
