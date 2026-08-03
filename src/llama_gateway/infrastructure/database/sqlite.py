from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from llama_gateway.application.ports.database import DatabaseAdapter
from llama_gateway.domain.api_key import ApiKey
from llama_gateway.domain.employee import Employee
from llama_gateway.domain.quota_window import QuotaWindow
from llama_gateway.domain.rate_limit_bucket import RateLimitBucket
from llama_gateway.domain.request import Request
from llama_gateway.infrastructure.database.models import (
    ApiKeyModel,
    EmployeeModel,
    QuotaWindowModel,
    RateLimitBucketModel,
    RequestModel,
)

if TYPE_CHECKING:
    pass


class SQLiteDatabaseAdapter(DatabaseAdapter):
    def __init__(self, database_url: str = "sqlite+aiosqlite:///./llama_gateway.db") -> None:
        self._engine = create_async_engine(database_url, echo=False)

    async def init(self) -> None:
        async with self._engine.begin() as conn:
            from llama_gateway.infrastructure.database.models import Base

            await conn.run_sync(Base.metadata.create_all)

    async def close(self) -> None:
        await self._engine.dispose()

    # --- Employee ---

    async def create_employee(self, employee: Employee) -> Employee:
        async with self._session() as session:
            model = EmployeeModel(
                id=employee.id,
                name=employee.name,
                email=employee.email,
                is_active=employee.is_active,
                quota_hourly=employee.quota_hourly,
                quota_daily=employee.quota_daily,
                quota_weekly=employee.quota_weekly,
                created_at=employee.created_at.isoformat(),
                updated_at=employee.updated_at.isoformat(),
            )
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._to_employee(model)

    async def get_employee(self, employee_id: str) -> Employee | None:
        async with self._session() as session:
            stmt = select(EmployeeModel).where(EmployeeModel.id == employee_id)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self._to_employee(model)

    async def list_employees(self) -> list[Employee]:
        async with self._session() as session:
            stmt = select(EmployeeModel)
            result = await session.execute(stmt)
            return [self._to_employee(m) for m in result.scalars().all()]

    async def update_employee(self, employee: Employee) -> Employee:
        async with self._session() as session:
            stmt = (
                update(EmployeeModel)
                .where(EmployeeModel.id == employee.id)
                .values(
                    name=employee.name,
                    email=employee.email,
                    is_active=employee.is_active,
                    quota_hourly=employee.quota_hourly,
                    quota_daily=employee.quota_daily,
                    quota_weekly=employee.quota_weekly,
                    updated_at=employee.updated_at.isoformat(),
                )
            )
            await session.execute(stmt)
            await session.commit()
            return employee

    async def delete_employee(self, employee_id: str) -> bool:
        async with self._session() as session:
            stmt = select(EmployeeModel).where(EmployeeModel.id == employee_id)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return False
            await session.delete(model)
            await session.commit()
            return True

    # --- API Key ---

    async def create_api_key(self, key: ApiKey) -> ApiKey:
        async with self._session() as session:
            model = ApiKeyModel(
                id=key.id,
                employee_id=key.employee_id,
                key_hash=key.key_hash,
                key_prefix=key.key_prefix,
                is_active=key.is_active,
                created_at=key.created_at.isoformat(),
                last_used_at=key.last_used_at.isoformat() if key.last_used_at else None,
            )
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._to_api_key(model)

    async def get_api_key(self, key_id: str) -> ApiKey | None:
        async with self._session() as session:
            stmt = select(ApiKeyModel).where(ApiKeyModel.id == key_id)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self._to_api_key(model)

    async def get_api_key_by_hash(self, key_hash: str) -> ApiKey | None:
        async with self._session() as session:
            stmt = select(ApiKeyModel).where(ApiKeyModel.key_hash == key_hash)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self._to_api_key(model)

    async def list_api_keys(self, employee_id: str | None = None) -> list[ApiKey]:
        async with self._session() as session:
            stmt = select(ApiKeyModel)
            if employee_id:
                stmt = stmt.where(ApiKeyModel.employee_id == employee_id)
            result = await session.execute(stmt)
            return [self._to_api_key(m) for m in result.scalars().all()]

    async def update_api_key(self, key: ApiKey) -> ApiKey:
        async with self._session() as session:
            stmt = (
                update(ApiKeyModel)
                .where(ApiKeyModel.id == key.id)
                .values(
                    key_hash=key.key_hash,
                    key_prefix=key.key_prefix,
                    is_active=key.is_active,
                    last_used_at=key.last_used_at.isoformat() if key.last_used_at else None,
                )
            )
            await session.execute(stmt)
            await session.commit()
            return key

    async def delete_api_key(self, key_id: str) -> bool:
        async with self._session() as session:
            stmt = select(ApiKeyModel).where(ApiKeyModel.id == key_id)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return False
            await session.delete(model)
            await session.commit()
            return True

    # --- Request ---

    async def create_request(self, request: Request) -> Request:
        async with self._session() as session:
            model = RequestModel(
                id=request.id,
                employee_id=request.employee_id,
                key_id=request.key_id,
                model=request.model,
                tokens_in=request.tokens_in,
                tokens_out=request.tokens_out,
                duration_ms=request.duration_ms,
                timestamp=request.timestamp.isoformat(),
                status=request.status,
                session_id=request.session_id,
            )
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._to_request(model)

    async def list_requests(
        self,
        employee_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Request]:
        async with self._session() as session:
            stmt = select(RequestModel).order_by(RequestModel.timestamp.desc())
            if employee_id:
                stmt = stmt.where(RequestModel.employee_id == employee_id)
            stmt = stmt.limit(limit).offset(offset)
            result = await session.execute(stmt)
            return [self._to_request(m) for m in result.scalars().all()]

    # --- Quota Window ---

    async def get_quota_window(
        self,
        employee_id: str,
        window_type: str,
        window_start: datetime,
    ) -> QuotaWindow | None:
        async with self._session() as session:
            ws = window_start.isoformat()
            stmt = (
                select(QuotaWindowModel)
                .where(
                    QuotaWindowModel.employee_id == employee_id,
                    QuotaWindowModel.window_type == window_type,
                    QuotaWindowModel.window_start == ws,
                )
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self._to_quota_window(model)

    async def upsert_quota_window(self, window: QuotaWindow) -> QuotaWindow:
        async with self._session() as session:
            existing = await self.get_quota_window(
                window.employee_id,
                window.window_type,
                window.window_start,
            )
            if existing is None:
                model = QuotaWindowModel(
                    id=window.id,
                    employee_id=window.employee_id,
                    window_type=window.window_type,
                    window_start=window.window_start.isoformat(),
                    tokens_used=window.tokens_used,
                )
                session.add(model)
            else:
                stmt = (
                    update(QuotaWindowModel)
                    .where(QuotaWindowModel.id == existing.id)
                    .values(tokens_used=window.tokens_used)
                )
                await session.execute(stmt)
            await session.commit()
            return window

    async def list_quota_windows(
        self,
        employee_id: str | None = None,
        window_type: str | None = None,
    ) -> list[QuotaWindow]:
        async with self._session() as session:
            stmt = select(QuotaWindowModel)
            if employee_id:
                stmt = stmt.where(QuotaWindowModel.employee_id == employee_id)
            if window_type:
                stmt = stmt.where(QuotaWindowModel.window_type == window_type)
            result = await session.execute(stmt)
            return [self._to_quota_window(m) for m in result.scalars().all()]

    # --- Rate Limit Bucket ---

    async def get_rate_limit_bucket(
        self,
        employee_id: str,
        window_type: str,
        window_start: datetime,
    ) -> RateLimitBucket | None:
        async with self._session() as session:
            ws = window_start.isoformat()
            stmt = (
                select(RateLimitBucketModel)
                .where(
                    RateLimitBucketModel.employee_id == employee_id,
                    RateLimitBucketModel.window_type == window_type,
                    RateLimitBucketModel.window_start == ws,
                )
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self._to_rate_limit_bucket(model)

    async def upsert_rate_limit_bucket(self, bucket: RateLimitBucket) -> RateLimitBucket:
        async with self._session() as session:
            existing = await self.get_rate_limit_bucket(
                bucket.employee_id,
                bucket.window_type,
                bucket.window_start,
            )
            if existing is None:
                model = RateLimitBucketModel(
                    id=bucket.id,
                    employee_id=bucket.employee_id,
                    window_type=bucket.window_type,
                    window_start=bucket.window_start.isoformat(),
                    request_count=bucket.request_count,
                )
                session.add(model)
            else:
                stmt = (
                    update(RateLimitBucketModel)
                    .where(RateLimitBucketModel.id == existing.id)
                    .values(request_count=bucket.request_count)
                )
                await session.execute(stmt)
            await session.commit()
            return bucket

    async def list_rate_limit_buckets(
        self,
        employee_id: str | None = None,
        window_type: str | None = None,
    ) -> list[RateLimitBucket]:
        async with self._session() as session:
            stmt = select(RateLimitBucketModel)
            if employee_id:
                stmt = stmt.where(RateLimitBucketModel.employee_id == employee_id)
            if window_type:
                stmt = stmt.where(RateLimitBucketModel.window_type == window_type)
            result = await session.execute(stmt)
            return [self._to_rate_limit_bucket(m) for m in result.scalars().all()]

    # --- Conversion helpers ---

    def _to_employee(self, model: EmployeeModel) -> Employee:
        return Employee(
            id=model.id,
            name=model.name,
            email=model.email,
            is_active=model.is_active,
            quota_hourly=model.quota_hourly,
            quota_daily=model.quota_daily,
            quota_weekly=model.quota_weekly,
            created_at=datetime.fromisoformat(model.created_at),
            updated_at=datetime.fromisoformat(model.updated_at),
        )

    def _to_api_key(self, model: ApiKeyModel) -> ApiKey:
        return ApiKey(
            id=model.id,
            employee_id=model.employee_id,
            key_hash=model.key_hash,
            key_prefix=model.key_prefix,
            is_active=model.is_active,
            created_at=datetime.fromisoformat(model.created_at),
            last_used_at=datetime.fromisoformat(model.last_used_at) if model.last_used_at else None,
        )

    def _to_request(self, model: RequestModel) -> Request:
        return Request(
            id=model.id,
            employee_id=model.employee_id,
            key_id=model.key_id,
            model=model.model,
            tokens_in=model.tokens_in,
            tokens_out=model.tokens_out,
            duration_ms=model.duration_ms,
            timestamp=datetime.fromisoformat(model.timestamp),
            status=model.status,
            session_id=model.session_id,
        )

    def _to_quota_window(self, model: QuotaWindowModel) -> QuotaWindow:
        return QuotaWindow(
            id=model.id,
            employee_id=model.employee_id,
            window_type=model.window_type,
            window_start=datetime.fromisoformat(model.window_start),
            tokens_used=model.tokens_used,
        )

    def _to_rate_limit_bucket(self, model: RateLimitBucketModel) -> RateLimitBucket:
        return RateLimitBucket(
            id=model.id,
            employee_id=model.employee_id,
            window_type=model.window_type,
            window_start=datetime.fromisoformat(model.window_start),
            request_count=model.request_count,
        )

    # --- Session factory ---

    def _session(self) -> AsyncSession:
        return AsyncSession(self._engine, expire_on_commit=False)
