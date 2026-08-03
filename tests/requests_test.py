from __future__ import annotations

import pytest

from llama_gateway.domain.employee import Employee
from llama_gateway.domain.request import Request
from llama_gateway.infrastructure.database.sqlite import SQLiteDatabaseAdapter


@pytest.mark.asyncio
async def test_create_request_returns_request_with_id(db: SQLiteDatabaseAdapter, sample_request: Request):
    emp = Employee(id="emp-001", name="Alice", email="alice@example.com")
    await db.create_employee(emp)
    result = await db.create_request(sample_request)
    assert result.id == "req-001"
    assert result.model == "llama-3.1-8b"


@pytest.mark.asyncio
async def test_create_request_total_tokens(sample_request: Request):
    assert sample_request.total_tokens == 300


@pytest.mark.asyncio
async def test_list_requests_returns_all(db: SQLiteDatabaseAdapter):
    emp = Employee(id="emp-001", name="Alice", email="alice@example.com")
    await db.create_employee(emp)
    req1 = Request(id="req-001", employee_id="emp-001", key_id="key-001")
    req2 = Request(id="req-002", employee_id="emp-001", key_id="key-001")
    await db.create_request(req1)
    await db.create_request(req2)
    results = await db.list_requests()
    assert len(results) == 2


@pytest.mark.asyncio
async def test_list_requests_filtered_by_employee(db: SQLiteDatabaseAdapter):
    emp1 = Employee(id="emp-001", name="Alice", email="alice@example.com")
    emp2 = Employee(id="emp-002", name="Bob", email="bob@example.com")
    await db.create_employee(emp1)
    await db.create_employee(emp2)
    req1 = Request(id="req-001", employee_id="emp-001", key_id="key-001")
    req2 = Request(id="req-002", employee_id="emp-002", key_id="key-002")
    await db.create_request(req1)
    await db.create_request(req2)
    results = await db.list_requests(employee_id="emp-001")
    assert len(results) == 1
    assert results[0].id == "req-001"


@pytest.mark.asyncio
async def test_list_requests_pagination(db: SQLiteDatabaseAdapter):
    emp = Employee(id="emp-001", name="Alice", email="alice@example.com")
    await db.create_employee(emp)
    for i in range(5):
        req = Request(id=f"req-{i:03d}", employee_id="emp-001", key_id="key-001")
        await db.create_request(req)
    results = await db.list_requests(limit=2, offset=0)
    assert len(results) == 2
    results2 = await db.list_requests(limit=2, offset=2)
    assert len(results2) == 2
