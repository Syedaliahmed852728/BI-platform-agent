from __future__ import annotations

import re
from typing import Any

from langchain.tools import tool
from langgraph.prebuilt import ToolRuntime

from agents.models import AgentContext
from data.database.connection import get_client_database


FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "MERGE",
    "GRANT",
    "REVOKE",
}


def validate_read_only_sql(sql_query: str) -> tuple[bool, str]:
    normalized = sql_query.upper()
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", normalized):
            return False, f"Forbidden SQL operation detected: {keyword}"
    if not normalized.strip().startswith("SELECT"):
        return False, "Only SELECT queries are allowed"
    return True, ""


def format_rows(
    columns: list[str], rows: list[tuple[Any, ...]]
) -> list[dict[str, Any]]:
    return [{columns[i]: value for i, value in enumerate(row)} for row in rows]


@tool
def run_sql_query(sql_query: str, runtime: ToolRuntime[AgentContext, Any]) -> dict:
    """Execute a read-only SELECT against the client's business database."""

    client_name = (runtime.context or {}).get("client_name")
    if not client_name:
        return {
            "success": False,
            "error": "Missing client_name in runtime context. This tool must "
            "be invoked with context={'client_name': ...}.",
            "rows": [],
        }

    is_valid, error = validate_read_only_sql(sql_query)
    if not is_valid:
        return {"success": False, "error": error, "rows": []}

    try:
        db = get_client_database(client_name)
        with db.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]

        return {
            "success": True,
            "columns": columns,
            "rows": format_rows(columns, rows),
            "row_count": len(rows),
        }
    except Exception as exc:
        return {"success": False, "error": str(exc), "rows": []}
