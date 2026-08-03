from __future__ import annotations

from datetime import UTC, datetime

from llama_gateway.application.dto.employee import EmployeeCreate, EmployeeUpdate
from llama_gateway.application.ports.database import DatabaseAdapter
from llama_gateway.domain.employee import Employee


class EmployeeService:
    def __init__(self, db: DatabaseAdapter) -> None:
        self._db = db

    async def create(self, dto: EmployeeCreate) -> Employee:
        now = datetime.now(UTC)
        employee = Employee(
            name=dto.name,
            email=dto.email,
            is_active=dto.is_active,
            quota_hourly=dto.quota_hourly,
            quota_daily=dto.quota_daily,
            quota_weekly=dto.quota_weekly,
            created_at=now,
            updated_at=now,
        )
        return await self._db.create_employee(employee)

    async def get(self, employee_id: str) -> Employee | None:
        return await self._db.get_employee(employee_id)

    async def list_all(self) -> list[Employee]:
        return await self._db.list_employees()

    async def update(self, employee_id: str, dto: EmployeeUpdate) -> Employee | None:
        existing = await self._db.get_employee(employee_id)
        if existing is None:
            return None
        if dto.name is not None:
            existing.name = dto.name
        if dto.email is not None:
            existing.email = dto.email
        if dto.is_active is not None:
            existing.is_active = dto.is_active
        if dto.quota_hourly is not None:
            existing.quota_hourly = dto.quota_hourly
        if dto.quota_daily is not None:
            existing.quota_daily = dto.quota_daily
        if dto.quota_weekly is not None:
            existing.quota_weekly = dto.quota_weekly
        existing.updated_at = datetime.now(UTC)
        return await self._db.update_employee(existing)

    async def delete(self, employee_id: str) -> bool:
        return await self._db.delete_employee(employee_id)
