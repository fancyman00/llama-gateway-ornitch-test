from __future__ import annotations

from datetime import datetime, timezone

import pytest

from llama_gateway.domain.employee import Employee
from llama_gateway.infrastructure.database.sqlite import SQLiteDatabaseAdapter


@pytest.mark.asyncio
async def test_create_employee_returns_employee_with_id(db: SQLiteDatabaseAdapter, sample_employee: Employee):
    result = await db.create_employee(sample_employee)
    assert result.id == "emp-001"
    assert result.name == "Alice"
    assert result.email == "alice@example.com"
    assert result.is_active is True


@pytest.mark.asyncio
async def test_get_employee_returns_employee(db: SQLiteDatabaseAdapter, sample_employee: Employee):
    await db.create_employee(sample_employee)
    result = await db.get_employee("emp-001")
    assert result is not None
    assert result.name == "Alice"
    assert result.email == "alice@example.com"


@pytest.mark.asyncio
async def test_get_employee_returns_none_for_missing_id(db: SQLiteDatabaseAdapter):
    result = await db.get_employee("nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_list_employees_returns_all(db: SQLiteDatabaseAdapter, sample_employee: Employee, inactive_employee: Employee):
    await db.create_employee(sample_employee)
    await db.create_employee(inactive_employee)
    results = await db.list_employees()
    assert len(results) == 2


@pytest.mark.asyncio
async def test_update_employee_changes_values(db: SQLiteDatabaseAdapter, sample_employee: Employee):
    await db.create_employee(sample_employee)
    sample_employee.name = "Alice Updated"
    sample_employee.updated_at = datetime.now(timezone.utc)
    result = await db.update_employee(sample_employee)
    assert result.name == "Alice Updated"
    retrieved = await db.get_employee("emp-001")
    assert retrieved.name == "Alice Updated"


@pytest.mark.asyncio
async def test_delete_employee_removes_it(db: SQLiteDatabaseAdapter, sample_employee: Employee):
    await db.create_employee(sample_employee)
    deleted = await db.delete_employee("emp-001")
    assert deleted is True
    result = await db.get_employee("emp-001")
    assert result is None


@pytest.mark.asyncio
async def test_delete_employee_returns_false_for_missing(db: SQLiteDatabaseAdapter):
    deleted = await db.delete_employee("nonexistent")
    assert deleted is False
