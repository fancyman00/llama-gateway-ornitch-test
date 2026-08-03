from __future__ import annotations

import uuid
from datetime import UTC, datetime


class QuotaWindow:
    WINDOW_HOURLY = "hourly"
    WINDOW_DAILY = "daily"
    WINDOW_WEEKLY = "weekly"

    VALID_TYPES = {WINDOW_HOURLY, WINDOW_DAILY, WINDOW_WEEKLY}

    def __init__(
        self,
        id: str | None = None,
        employee_id: str = "",
        window_type: str = WINDOW_DAILY,
        window_start: datetime | None = None,
        tokens_used: int = 0,
    ) -> None:
        self.id = id or str(uuid.uuid4())
        self.employee_id = employee_id
        self.window_type = window_type
        self.window_start = window_start or datetime.now(UTC)
        self.tokens_used = tokens_used

    def add_tokens(self, count: int) -> None:
        self.tokens_used += count
