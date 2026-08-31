from __future__ import annotations

import importlib
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    db_path = tmp_path / "test_urls.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_path))
    monkeypatch.setenv("PUBLIC_BASE_URL", "http://testserver")

    import app.database as database
    import app.main as main

    importlib.reload(database)
    importlib.reload(main)

    with TestClient(main.app) as test_client:
        yield test_client


def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_shorten_valid_url(client: TestClient):
    response = client.post(
        "/shorten",
        json={"url": "https://example.com/a/very/long/url"},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["short_code"]) == 6
    assert body["short_code"].isalnum()
    assert body["short_url"] == f"http://testserver/{body['short_code']}"


def test_duplicate_url_returns_existing_code(client: TestClient):
    first = client.post("/shorten", json={"url": "https://example.com/"}).json()
    second = client.post("/shorten", json={"url": "https://example.com/"}).json()
    assert first["short_code"] == second["short_code"]


def test_invalid_url_is_rejected(client: TestClient):
    response = client.post("/shorten", json={"url": "not-a-url"})
    assert response.status_code == 422


def test_redirect(client: TestClient):
    created = client.post(
        "/shorten",
        json={"url": "https://example.com/redirect-target"},
    ).json()
    response = client.get(
        f"/{created['short_code']}",
        follow_redirects=False,
    )
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/redirect-target"


def test_unknown_code_returns_404(client: TestClient):
    response = client.get("/ABC123", follow_redirects=False)
    assert response.status_code == 404


def test_invalid_code_format_returns_404(client: TestClient):
    response = client.get("/bad!", follow_redirects=False)
    assert response.status_code == 404
