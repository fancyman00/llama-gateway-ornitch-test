from __future__ import annotations

import pytest

from llama_gateway.domain.employee import Employee
from llama_gateway.domain.quota_window import QuotaWindow
from llama_gateway.infrastructure.database.sqlite import SQLiteDatabaseAdapter


@pytest.mark.asyncio
async def test_upsert_quota_window_creates_new(db: SQLiteDatabaseAdapter, sample_window: QuotaWindow):
    result = await db.upsert_quota_window(sample_window)
    assert result.id == "qw-001"
    assert result.tokens_used == 1000


@pytest.mark.asyncio
async def test_upsert_quota_window_updates_existing(db: SQLiteDatabaseAdapter, sample_window: QuotaWindow):
    await db.upsert_quota_window(sample_window)
    sample_window.tokens_used = 5000
    await db.upsert_quota_window(sample_window)
    retrieved = await db.get_quota_window(
        "emp-001", QuotaWindow.WINDOW_DAILY, sample_window.window_start
    )
    assert retrieved is not None
    assert retrieved.tokens_used == 5000


@pytest.mark.asyncio
async def test_get_quota_window_returns_none_for_missing(db: SQLiteDatabaseAdapter, sample_window: QuotaWindow):
    result = await db.get_quota_window("emp-001", QuotaWindow.WINDOW_HOURLY, sample_window.window_start)
    assert result is None


@pytest.mark.asyncio
async def test_list_quota_windows(db: SQLiteDatabaseAdapter):
    emp = Employee(id="emp-001", name="Alice", email="alice@example.com")
    await db.create_employee(emp)
    w1 = QuotaWindow(id="qw-001", employee_id="emp-001", window_type=QuotaWindow.WINDOW_DAILY, tokens_used=100)
    w2 = QuotaWindow(id="qw-002", employee_id="emp-001", window_type=QuotaWindow.WINDOW_WEEKLY, tokens_used=200)
    await db.upsert_quota_window(w1)
    await db.upsert_quota_window(w2)
    results = await db.list_quota_windows(employee_id="emp-001")
    assert len(results) == 2


@pytest.mark.asyncio
async def test_quota_window_add_tokens(sample_window: QuotaWindow):
    sample_window.add_tokens(500)
    assert sample_window.tokens_used == 1500
