from __future__ import annotations

import uuid
from datetime import datetime, timezone


class RateLimitBucket:
    WINDOW_1MIN = "1min"
    WINDOW_5MIN = "5min"

    VALID_TYPES = {WINDOW_1MIN, WINDOW_5MIN}

    def __init__(
        self,
        id: str | None = None,
        employee_id: str = "",
        window_type: str = WINDOW_1MIN,
        window_start: datetime | None = None,
        request_count: int = 0,
    ) -> None:
        self.id = id or str(uuid.uuid4())
        self.employee_id = employee_id
        self.window_type = window_type
        self.window_start = window_start or datetime.now(timezone.utc)
        self.request_count = request_count

    def increment(self) -> None:
        self.request_count += 1
