from __future__ import annotations

from datetime import UTC, datetime

import pytest

from llama_gateway.domain.api_key import ApiKey
from llama_gateway.domain.employee import Employee
from llama_gateway.domain.quota_window import QuotaWindow
from llama_gateway.domain.rate_limit_bucket import RateLimitBucket
from llama_gateway.domain.request import Request
from llama_gateway.infrastructure.database.sqlite import SQLiteDatabaseAdapter


@pytest.fixture
def database_url(tmp_path):
    db_file = tmp_path / "test.db"
    return f"sqlite+aiosqlite:///{db_file}"


@pytest.fixture
async def db(database_url):
    adapter = SQLiteDatabaseAdapter(database_url=database_url)
    await adapter.init()
    yield adapter
    await adapter.close()


@pytest.fixture
def employee():
    return Employee(id="emp-001", name="Alice", email="alice@example.com")


@pytest.fixture
def sample_employee():
    return Employee(
        id="emp-001",
        name="Alice",
        email="alice@example.com",
        is_active=True,
        quota_hourly=50_000,
        quota_daily=200_000,
        quota_weekly=800_000,
    )


@pytest.fixture
def inactive_employee():
    return Employee(
        id="emp-002",
        name="Bob",
        email="bob@example.com",
        is_active=False,
    )


@pytest.fixture
def sample_api_key():
    return ApiKey(
        id="key-001",
        employee_id="emp-001",
        key_hash="hashed_secret_value",
        key_prefix="lgk_",
        is_active=True,
        created_at=datetime(2024, 1, 1, tzinfo=UTC),
    )


@pytest.fixture
def sample_request():
    return Request(
        id="req-001",
        employee_id="emp-001",
        key_id="key-001",
        model="llama-3.1-8b",
        tokens_in=100,
        tokens_out=200,
        duration_ms=1500,
        timestamp=datetime(2024, 6, 1, 12, 0, 0, tzinfo=UTC),
        status="success",
    )


@pytest.fixture
def sample_window():
    return QuotaWindow(
        id="qw-001",
        employee_id="emp-001",
        window_type=QuotaWindow.WINDOW_DAILY,
        window_start=datetime(2024, 6, 1, 0, 0, 0, tzinfo=UTC),
        tokens_used=1000,
    )


@pytest.fixture
def sample_bucket():
    return RateLimitBucket(
        id="rb-001",
        employee_id="emp-001",
        window_type=RateLimitBucket.WINDOW_1MIN,
        window_start=datetime(2024, 6, 1, 12, 0, 0, tzinfo=UTC),
        request_count=50,
    )
