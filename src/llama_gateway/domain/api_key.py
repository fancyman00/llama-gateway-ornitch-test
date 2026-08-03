from __future__ import annotations

import uuid
from datetime import UTC, datetime


class ApiKey:
    def __init__(
        self,
        id: str | None = None,
        employee_id: str | None = None,
        key_hash: str = "",
        key_prefix: str = "",
        is_active: bool = True,
        created_at: datetime | None = None,
        last_used_at: datetime | None = None,
    ) -> None:
        self.id = id or str(uuid.uuid4())
        self.employee_id = employee_id
        self.key_hash = key_hash
        self.key_prefix = key_prefix
        self.is_active = is_active
        self.created_at = created_at or datetime.now(UTC)
        self.last_used_at = last_used_at

    def revoke(self) -> None:
        self.is_active = False
