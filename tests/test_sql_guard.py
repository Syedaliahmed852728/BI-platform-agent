from __future__ import annotations

import pytest

from business.tools.sql_tools import validate_read_only_sql


def test_select_is_allowed():
    ok, error = validate_read_only_sql("SELECT * FROM sales WHERE year = 2026")
    assert ok
    assert error == ""


@pytest.mark.parametrize(
    "sql",
    [
        "INSERT INTO sales VALUES (1)",
        "DELETE FROM sales",
        "DROP TABLE sales",
        "UPDATE sales SET total = 0",
        "SELECT * FROM sales; DROP TABLE sales",
    ],
)
def test_mutations_are_rejected(sql):
    ok, error = validate_read_only_sql(sql)
    assert not ok
    assert error


def test_non_select_statements_are_rejected():
    ok, error = validate_read_only_sql("PRAGMA table_info(sales)")
    assert not ok
