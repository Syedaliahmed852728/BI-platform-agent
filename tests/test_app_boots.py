from __future__ import annotations

from presentation.api.app import create_app


def test_app_constructs_with_expected_routes():
    app = create_app()
    schema = app.openapi()
    paths = set(schema["paths"])

    assert "/chat/{client_name}" in paths
    assert "/health" in paths
    assert "/admin/refresh" in paths
