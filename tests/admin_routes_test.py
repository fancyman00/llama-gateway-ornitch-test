from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from llama_gateway.application.service.api_key_service import ApiKeyService
from llama_gateway.application.service.employee_service import EmployeeService
from llama_gateway.infrastructure.database.sqlite import SQLiteDatabaseAdapter
from llama_gateway.presentation.routes.admin_routes import router as admin_router


@pytest.fixture
def database_url(tmp_path):
    db_file = tmp_path / "test_admin.db"
    return f"sqlite+aiosqlite:///{db_file}"


@pytest.fixture
async def db(database_url):
    adapter = SQLiteDatabaseAdapter(database_url=database_url)
    await adapter.init()
    yield adapter
    await adapter.close()


@pytest.fixture
def employee_service(db: SQLiteDatabaseAdapter):
    return EmployeeService(db)


@pytest.fixture
def api_key_service(db: SQLiteDatabaseAdapter):
    return ApiKeyService(db)


def _make_test_app(
    employee_service: EmployeeService,
    api_key_service: ApiKeyService,
) -> FastAPI:
    """Create a FastAPI app with services injected via dependency overrides."""
    application = FastAPI()
    application.include_router(admin_router, prefix="/admin", tags=["admin"])

    from llama_gateway.presentation.routes.admin_routes import (
        _get_api_key_service,
        _get_employee_service,
    )

    application.dependency_overrides[_get_employee_service] = lambda: employee_service
    application.dependency_overrides[_get_api_key_service] = lambda: api_key_service
    return application


@pytest.fixture
def app(
    db: SQLiteDatabaseAdapter,
    employee_service: EmployeeService,
    api_key_service: ApiKeyService,
):
    return _make_test_app(employee_service, api_key_service)


@pytest.fixture
def client(app: FastAPI):
    return TestClient(app)


# --- Employee HTTP tests ---


def test_create_employee(client: TestClient):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "is_active": True,
        "quota_hourly": 100_000,
        "quota_daily": 500_000,
        "quota_weekly": 2_000_000,
    }
    response = client.post("/admin/employees", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["is_active"] is True
    assert data["id"] is not None


def test_create_employee_default_quotas(client: TestClient):
    payload = {"name": "Bob", "email": "bob@example.com"}
    response = client.post("/admin/employees", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["quota_hourly"] == 100_000
    assert data["quota_daily"] == 500_000
    assert data["quota_weekly"] == 2_000_000


def test_create_employee_invalid_email(client: TestClient):
    payload = {"name": "Alice", "email": "not-an-email"}
    response = client.post("/admin/employees", json=payload)
    assert response.status_code == 422


def test_list_employees(client: TestClient):
    response = client.get("/admin/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_employee(client: TestClient):
    payload = {"name": "Alice", "email": "alice@example.com"}
    create_resp = client.post("/admin/employees", json=payload)
    employee_id = create_resp.json()["id"]

    response = client.get(f"/admin/employees/{employee_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_get_employee_not_found(client: TestClient):
    response = client.get("/admin/employees/nonexistent-id")
    assert response.status_code == 404


def test_update_employee(client: TestClient):
    payload = {"name": "Alice", "email": "alice@example.com"}
    create_resp = client.post("/admin/employees", json=payload)
    employee_id = create_resp.json()["id"]

    update_payload = {"name": "Alice Updated"}
    response = client.patch(f"/admin/employees/{employee_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Alice Updated"


def test_update_employee_not_found(client: TestClient):
    update_payload = {"name": "Ghost"}
    response = client.patch("/admin/employees/nonexistent", json=update_payload)
    assert response.status_code == 404


def test_delete_employee(client: TestClient):
    payload = {"name": "Alice", "email": "alice@example.com"}
    create_resp = client.post("/admin/employees", json=payload)
    employee_id = create_resp.json()["id"]

    response = client.delete(f"/admin/employees/{employee_id}")
    assert response.status_code == 204

    get_response = client.get(f"/admin/employees/{employee_id}")
    assert get_response.status_code == 404


def test_delete_employee_not_found(client: TestClient):
    response = client.delete("/admin/employees/nonexistent")
    assert response.status_code == 404


# --- API Key HTTP tests ---


def test_create_api_key(client: TestClient):
    emp_payload = {"name": "Alice", "email": "alice@example.com"}
    emp_resp = client.post("/admin/employees", json=emp_payload)
    employee_id = emp_resp.json()["id"]

    key_payload = {"employee_id": employee_id}
    response = client.post("/admin/api-keys", json=key_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["key"].startswith("lgk_")
    assert data["key_id"] is not None
    assert data["employee_id"] == employee_id


def test_create_api_key_unknown_employee(client: TestClient):
    key_payload = {"employee_id": "nonexistent-id"}
    response = client.post("/admin/api-keys", json=key_payload)
    assert response.status_code == 404


def test_list_api_keys(client: TestClient):
    response = client.get("/admin/api-keys")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_api_keys_filter_by_employee(client: TestClient):
    emp_a_payload = {"name": "Alice", "email": "alice@example.com"}
    emp_a_resp = client.post("/admin/employees", json=emp_a_payload)
    emp_a_id = emp_a_resp.json()["id"]

    emp_b_payload = {"name": "Bob", "email": "bob@example.com"}
    emp_b_resp = client.post("/admin/employees", json=emp_b_payload)
    emp_b_id = emp_b_resp.json()["id"]

    key_payload_a = {"employee_id": emp_a_id}
    client.post("/admin/api-keys", json=key_payload_a)

    key_payload_b = {"employee_id": emp_b_id}
    client.post("/admin/api-keys", json=key_payload_b)

    response = client.get(f"/admin/api-keys?employee_id={emp_a_id}")
    assert response.status_code == 200
    keys = response.json()
    assert len(keys) == 1
    assert keys[0]["employee_id"] == emp_a_id


def test_revoke_api_key(client: TestClient):
    emp_payload = {"name": "Alice", "email": "alice@example.com"}
    emp_resp = client.post("/admin/employees", json=emp_payload)
    employee_id = emp_resp.json()["id"]

    key_payload = {"employee_id": employee_id}
    key_resp = client.post("/admin/api-keys", json=key_payload)
    key_id = key_resp.json()["key_id"]

    response = client.patch(f"/admin/api-keys/{key_id}/revoke")
    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_revoke_api_key_not_found(client: TestClient):
    response = client.patch("/admin/api-keys/nonexistent/revoke")
    assert response.status_code == 404


def test_delete_api_key(client: TestClient):
    emp_payload = {"name": "Alice", "email": "alice@example.com"}
    emp_resp = client.post("/admin/employees", json=emp_payload)
    employee_id = emp_resp.json()["id"]

    key_payload = {"employee_id": employee_id}
    key_resp = client.post("/admin/api-keys", json=key_payload)
    key_id = key_resp.json()["key_id"]

    response = client.delete(f"/admin/api-keys/{key_id}")
    assert response.status_code == 204

    get_response = client.get(f"/admin/api-keys/{key_id}")
    assert get_response.status_code == 404
