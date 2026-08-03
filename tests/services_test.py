from __future__ import annotations

from dataclasses import dataclass

import pytest

from llama_gateway.application.dto.employee import EmployeeCreate, EmployeeUpdate
from llama_gateway.application.service.api_key_service import ApiKeyService
from llama_gateway.application.service.employee_service import EmployeeService
from llama_gateway.infrastructure.database.sqlite import SQLiteDatabaseAdapter


@dataclass
class _KeyCreateDto:
    employee_id: str


@pytest.fixture
async def db():
    import os
    import tempfile

    fd, db_file = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db_url = f"sqlite+aiosqlite:///{db_file}"
    adapter = SQLiteDatabaseAdapter(database_url=db_url)
    await adapter.init()
    yield adapter
    await adapter.close()
    try:
        os.unlink(db_file)
    except OSError:
        pass


@pytest.fixture
def employee_service(db: SQLiteDatabaseAdapter):
    return EmployeeService(db)


@pytest.fixture
def api_key_service(db: SQLiteDatabaseAdapter):
    return ApiKeyService(db)


@pytest.mark.asyncio
async def test_create_employee(employee_service: EmployeeService):
    dto = EmployeeCreate(
        name="Alice",
        email="alice@example.com",
        is_active=True,
        quota_hourly=100_000,
        quota_daily=500_000,
        quota_weekly=2_000_000,
    )
    employee = await employee_service.create(dto)
    assert employee.id is not None
    assert employee.name == "Alice"
    assert employee.email == "alice@example.com"
    assert employee.is_active is True
    assert employee.quota_hourly == 100_000


@pytest.mark.asyncio
async def test_get_employee(employee_service: EmployeeService):
    dto = EmployeeCreate(name="Bob", email="bob@example.com")
    created = await employee_service.create(dto)
    fetched = await employee_service.get(created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.name == "Bob"


@pytest.mark.asyncio
async def test_get_employee_not_found(employee_service: EmployeeService):
    result = await employee_service.get("nonexistent-id")
    assert result is None


@pytest.mark.asyncio
async def test_list_employees(employee_service: EmployeeService):
    dto1 = EmployeeCreate(name="Alice", email="alice@example.com")
    dto2 = EmployeeCreate(name="Bob", email="bob@example.com")
    await employee_service.create(dto1)
    await employee_service.create(dto2)
    all_employees = await employee_service.list_all()
    assert len(all_employees) == 2


@pytest.mark.asyncio
async def test_update_employee(employee_service: EmployeeService):
    dto = EmployeeCreate(name="Alice", email="alice@example.com")
    created = await employee_service.create(dto)
    update = EmployeeUpdate(name="Alice Updated")
    updated = await employee_service.update(created.id, update)
    assert updated is not None
    assert updated.name == "Alice Updated"
    assert updated.email == "alice@example.com"


@pytest.mark.asyncio
async def test_update_employee_not_found(employee_service: EmployeeService):
    update = EmployeeUpdate(name="Ghost")
    result = await employee_service.update("nonexistent", update)
    assert result is None


@pytest.mark.asyncio
async def test_delete_employee(employee_service: EmployeeService):
    dto = EmployeeCreate(name="Alice", email="alice@example.com")
    created = await employee_service.create(dto)
    deleted = await employee_service.delete(created.id)
    assert deleted is True
    result = await employee_service.get(created.id)
    assert result is None


@pytest.mark.asyncio
async def test_delete_employee_not_found(employee_service: EmployeeService):
    deleted = await employee_service.delete("nonexistent")
    assert deleted is False


@pytest.mark.asyncio
async def test_create_api_key(api_key_service: ApiKeyService):
    employee = await EmployeeService(api_key_service._db).create(
        EmployeeCreate(name="Alice", email="alice@example.com"),
    )
    api_key, raw_key = await api_key_service.create(_KeyCreateDto(employee_id=employee.id))
    assert api_key is not None
    assert raw_key is not None
    assert raw_key.startswith("lgk_")
    assert len(raw_key) == 36  # "lgk_" + 32 hex chars


@pytest.mark.asyncio
async def test_create_api_key_unknown_employee(api_key_service: ApiKeyService):
    api_key, raw_key = await api_key_service.create(_KeyCreateDto(employee_id="nonexistent"))
    assert api_key is None
    assert raw_key is None


@pytest.mark.asyncio
async def test_get_api_key(api_key_service: ApiKeyService):
    employee = await EmployeeService(api_key_service._db).create(
        EmployeeCreate(name="Alice", email="alice@example.com"),
    )
    api_key, _ = await api_key_service.create(_KeyCreateDto(employee_id=employee.id))
    fetched = await api_key_service.get(api_key.id)
    assert fetched is not None
    assert fetched.id == api_key.id


@pytest.mark.asyncio
async def test_revoke_api_key(api_key_service: ApiKeyService):
    employee = await EmployeeService(api_key_service._db).create(
        EmployeeCreate(name="Alice", email="alice@example.com"),
    )
    api_key, _ = await api_key_service.create(_KeyCreateDto(employee_id=employee.id))
    revoked = await api_key_service.revoke(api_key.id)
    assert revoked is not None
    assert revoked.is_active is False


@pytest.mark.asyncio
async def test_revoke_api_key_not_found(api_key_service: ApiKeyService):
    result = await api_key_service.revoke("nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_delete_api_key(api_key_service: ApiKeyService):
    employee = await EmployeeService(api_key_service._db).create(
        EmployeeCreate(name="Alice", email="alice@example.com"),
    )
    api_key, _ = await api_key_service.create(_KeyCreateDto(employee_id=employee.id))
    deleted = await api_key_service.delete(api_key.id)
    assert deleted is True


@pytest.mark.asyncio
async def test_delete_api_key_not_found(api_key_service: ApiKeyService):
    deleted = await api_key_service.delete("nonexistent")
    assert deleted is False


@pytest.mark.asyncio
async def test_list_api_keys_by_employee(api_key_service: ApiKeyService):
    employee = await EmployeeService(api_key_service._db).create(
        EmployeeCreate(name="Alice", email="alice@example.com"),
    )
    key1, _ = await api_key_service.create(_KeyCreateDto(employee_id=employee.id))
    key2, _ = await api_key_service.create(_KeyCreateDto(employee_id=employee.id))
    keys = await api_key_service.list_by_employee(employee.id)
    assert len(keys) == 2
