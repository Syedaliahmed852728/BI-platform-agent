from __future__ import annotations

from business.orchestration.chat_service import ChatResponse
from tests.conftest import StubChatService


def test_chat_round_trip(client):
    stub = StubChatService(
        response=ChatResponse(
            source="reusable_sql",
            answer="Total sales were $1,234.",
            sql="SELECT SUM(total) FROM sales",
            domain="sales",
            similarity=0.91,
        )
    )
    http = client(stub)

    response = http.post("/chat/my_database.db", json={"question": "total sales?"})

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "reusable_sql"
    assert body["answer"] == "Total sales were $1,234."
    assert body["sql"] == "SELECT SUM(total) FROM sales"
    assert body["similarity"] == 0.91


def test_chat_failure_returns_json_error_not_traceback(client):
    http = client(StubChatService(error=RuntimeError("boom")))

    response = http.post(
        "/chat/my_database.db",
        json={"question": "total sales?"},
    )

    assert response.status_code == 500
    body = response.json()
    assert body["error"]["type"] == "internal"
    assert "boom" not in body["error"]["message"]
