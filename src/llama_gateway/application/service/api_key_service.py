from __future__ import annotations

import secrets
from datetime import datetime, timezone

from llama_gateway.application.ports.database import DatabaseAdapter
from llama_gateway.application.dto.api_key import ApiKeyCreateRequest
from llama_gateway.domain.api_key import ApiKey
from llama_gateway.domain.employee import Employee


class ApiKeyService:
    def __init__(self, db: DatabaseAdapter) -> None:
        self._db = db

    @staticmethod
    def _generate_raw_key() -> str:
        return "lgk_" + secrets.token_hex(16)

    @staticmethod
    def _hash_key(raw_key: str) -> str:
        import bcrypt

        return bcrypt.hashpw(raw_key.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    async def create(self, dto: ApiKeyCreateRequest) -> tuple[ApiKey | None, str | None]:
        employee = await self._db.get_employee(dto.employee_id)
        if employee is None:
            return None, None

        raw_key = self._generate_raw_key()
        key_hash = self._hash_key(raw_key)
        key_prefix = raw_key[:6]

        api_key = ApiKey(
            employee_id=employee.id,
            key_hash=key_hash,
            key_prefix=key_prefix,
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
        created = await self._db.create_api_key(api_key)
        return created, raw_key

    async def get(self, key_id: str) -> ApiKey | None:
        return await self._db.get_api_key(key_id)

    async def list_by_employee(self, employee_id: str) -> list[ApiKey]:
        return await self._db.list_api_keys(employee_id=employee_id)

    async def revoke(self, key_id: str) -> ApiKey | None:
        existing = await self._db.get_api_key(key_id)
        if existing is None:
            return None
        existing.revoke()
        return await self._db.update_api_key(existing)

    async def delete(self, key_id: str) -> bool:
        return await self._db.delete_api_key(key_id)
