from __future__ import annotations

import pytest

from llama_gateway.domain.api_key import ApiKey
from llama_gateway.domain.employee import Employee
from llama_gateway.infrastructure.database.sqlite import SQLiteDatabaseAdapter


@pytest.mark.asyncio
async def test_create_api_key_returns_key_with_id(db: SQLiteDatabaseAdapter, sample_api_key: ApiKey):
    result = await db.create_api_key(sample_api_key)
    assert result.id == "key-001"
    assert result.key_hash == "hashed_secret_value"
    assert result.key_prefix == "lgk_"


@pytest.mark.asyncio
async def test_get_api_key_returns_key(db: SQLiteDatabaseAdapter, sample_api_key: ApiKey):
    emp = Employee(id="emp-001", name="Alice", email="alice@example.com")
    await db.create_employee(emp)
    await db.create_api_key(sample_api_key)
    result = await db.get_api_key("key-001")
    assert result is not None
    assert result.employee_id == "emp-001"


@pytest.mark.asyncio
async def test_get_api_key_by_hash(db: SQLiteDatabaseAdapter, sample_api_key: ApiKey):
    emp = Employee(id="emp-001", name="Alice", email="alice@example.com")
    await db.create_employee(emp)
    await db.create_api_key(sample_api_key)
    result = await db.get_api_key_by_hash("hashed_secret_value")
    assert result is not None
    assert result.id == "key-001"


@pytest.mark.asyncio
async def test_get_api_key_by_hash_returns_none_for_missing(db: SQLiteDatabaseAdapter):
    result = await db.get_api_key_by_hash("nonexistent_hash")
    assert result is None


@pytest.mark.asyncio
async def test_list_api_keys_filtered_by_employee(db: SQLiteDatabaseAdapter):
    emp = Employee(id="emp-001", name="Alice", email="alice@example.com")
    await db.create_employee(emp)
    key1 = ApiKey(id="key-001", employee_id="emp-001", key_hash="hash1", key_prefix="lgk_")
    key2 = ApiKey(id="key-002", employee_id="emp-001", key_hash="hash2", key_prefix="lgk_")
    await db.create_api_key(key1)
    await db.create_api_key(key2)
    results = await db.list_api_keys(employee_id="emp-001")
    assert len(results) == 2


@pytest.mark.asyncio
async def test_list_api_keys_empty_when_no_keys(db: SQLiteDatabaseAdapter):
    emp = Employee(id="emp-001", name="Alice", email="alice@example.com")
    await db.create_employee(emp)
    results = await db.list_api_keys(employee_id="emp-001")
    assert len(results) == 0


@pytest.mark.asyncio
async def test_revoke_api_key(db: SQLiteDatabaseAdapter, sample_api_key: ApiKey):
    emp = Employee(id="emp-001", name="Alice", email="alice@example.com")
    await db.create_employee(emp)
    await db.create_api_key(sample_api_key)
    sample_api_key.revoke()
    await db.update_api_key(sample_api_key)
    result = await db.get_api_key("key-001")
    assert result is not None
    assert result.is_active is False


@pytest.mark.asyncio
async def test_delete_api_key(db: SQLiteDatabaseAdapter, sample_api_key: ApiKey):
    emp = Employee(id="emp-001", name="Alice", email="alice@example.com")
    await db.create_employee(emp)
    await db.create_api_key(sample_api_key)
    deleted = await db.delete_api_key("key-001")
    assert deleted is True
    result = await db.get_api_key("key-001")
    assert result is None


@pytest.mark.asyncio
async def test_delete_api_key_returns_false_for_missing(db: SQLiteDatabaseAdapter):
    deleted = await db.delete_api_key("nonexistent")
    assert deleted is False
