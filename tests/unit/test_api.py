import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def mock_db():
    """Prevent any real database connection during API tests."""
    with patch("backend.models.database.init_db", return_value=None):
        with patch("backend.models.database.SessionLocal") as mock:
            session = MagicMock()
            session.query.return_value.filter.return_value.first.return_value = None
            session.query.return_value.order_by.return_value.all.return_value = []
            mock.return_value = session
            yield session


@pytest.fixture
def client(mock_db):
    from backend.main import app
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_health_check_has_service_name(client):
    response = client.get("/health")
    data = response.json()
    assert "service" in data


def test_all_routes_registered(client):
    routes = [route.path for route in client.app.routes]
    assert "/health" in routes
    assert "/api/v1/code/upload" in routes
    assert "/api/v1/code" in routes
    assert "/api/v1/code/{id}" in routes
    assert "/api/v1/analysis/parse" in routes
    assert "/api/v1/analysis/complexity" in routes
    assert "/api/v1/analysis/bugs" in routes
    assert "/api/v1/analysis/security" in routes
    assert "/api/v1/docs/generate" in routes
    assert "/api/v1/qa" in routes
    assert "/api/v1/qa/history" in routes
    assert "/api/v1/review" in routes
    assert "/api/v1/refactor" in routes


def test_upload_empty_file_returns_error(client):
    response = client.post("/api/v1/code/upload", files={})
    assert response.status_code in (400, 422)


def test_upload_without_language_returns_error(client):
    response = client.post(
        "/api/v1/code/upload",
        files={"file": ("test.py", "print('hello')", "text/plain")},
    )
    assert response.status_code in (400, 422)


def test_get_nonexistent_code_returns_404(client):
    response = client.get("/api/v1/code/nonexistent-id-12345")
    assert response.status_code == 404


def test_delete_nonexistent_code(client):
    response = client.delete("/api/v1/code/nonexistent-id-12345")
    assert response.status_code == 200


def test_root_docs_redirect(client):
    response = client.get("/docs", follow_redirects=False)
    assert response.status_code in (200, 307, 303)


def test_openapi_schema_exists(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
