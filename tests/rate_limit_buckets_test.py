from __future__ import annotations

import pytest

from llama_gateway.domain.employee import Employee
from llama_gateway.domain.rate_limit_bucket import RateLimitBucket
from llama_gateway.infrastructure.database.sqlite import SQLiteDatabaseAdapter


@pytest.mark.asyncio
async def test_upsert_rate_limit_bucket_creates_new(db: SQLiteDatabaseAdapter, sample_bucket: RateLimitBucket):
    result = await db.upsert_rate_limit_bucket(sample_bucket)
    assert result.id == "rb-001"
    assert result.request_count == 50


@pytest.mark.asyncio
async def test_upsert_rate_limit_bucket_updates_existing(db: SQLiteDatabaseAdapter, sample_bucket: RateLimitBucket):
    await db.upsert_rate_limit_bucket(sample_bucket)
    sample_bucket.request_count = 100
    await db.upsert_rate_limit_bucket(sample_bucket)
    retrieved = await db.get_rate_limit_bucket(
        "emp-001", RateLimitBucket.WINDOW_1MIN, sample_bucket.window_start
    )
    assert retrieved is not None
    assert retrieved.request_count == 100


@pytest.mark.asyncio
async def test_get_rate_limit_bucket_returns_none_for_missing(db: SQLiteDatabaseAdapter):
    from datetime import datetime, timezone
    result = await db.get_rate_limit_bucket(
        "emp-001", RateLimitBucket.WINDOW_1MIN, datetime(2024, 1, 1, tzinfo=timezone.utc)
    )
    assert result is None


@pytest.mark.asyncio
async def test_list_rate_limit_buckets(db: SQLiteDatabaseAdapter):
    emp = Employee(id="emp-001", name="Alice", email="alice@example.com")
    await db.create_employee(emp)
    b1 = RateLimitBucket(id="rb-001", employee_id="emp-001", window_type=RateLimitBucket.WINDOW_1MIN)
    b2 = RateLimitBucket(id="rb-002", employee_id="emp-001", window_type=RateLimitBucket.WINDOW_5MIN)
    await db.upsert_rate_limit_bucket(b1)
    await db.upsert_rate_limit_bucket(b2)
    results = await db.list_rate_limit_buckets(employee_id="emp-001")
    assert len(results) == 2


@pytest.mark.asyncio
async def test_list_rate_limit_buckets_filtered_by_type(db: SQLiteDatabaseAdapter):
    emp = Employee(id="emp-001", name="Alice", email="alice@example.com")
    await db.create_employee(emp)
    b1 = RateLimitBucket(id="rb-001", employee_id="emp-001", window_type=RateLimitBucket.WINDOW_1MIN)
    b2 = RateLimitBucket(id="rb-002", employee_id="emp-001", window_type=RateLimitBucket.WINDOW_5MIN)
    await db.upsert_rate_limit_bucket(b1)
    await db.upsert_rate_limit_bucket(b2)
    results = await db.list_rate_limit_buckets(window_type=RateLimitBucket.WINDOW_1MIN)
    assert len(results) == 1


@pytest.mark.asyncio
async def test_rate_limit_bucket_increment(sample_bucket: RateLimitBucket):
    sample_bucket.increment()
    sample_bucket.increment()
    assert sample_bucket.request_count == 52
