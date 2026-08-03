from __future__ import annotations

import uuid
from datetime import datetime, timezone


class Employee:
    def __init__(
        self,
        id: str | None = None,
        name: str = "",
        email: str = "",
        is_active: bool = True,
        quota_hourly: int = 100_000,
        quota_daily: int = 500_000,
        quota_weekly: int = 2_000_000,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.is_active = is_active
        self.quota_hourly = quota_hourly
        self.quota_daily = quota_daily
        self.quota_weekly = quota_weekly
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)
