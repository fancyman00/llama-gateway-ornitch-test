from __future__ import annotations

import uuid
from datetime import datetime, timezone


class Request:
    def __init__(
        self,
        id: str | None = None,
        employee_id: str | None = None,
        key_id: str | None = None,
        model: str = "",
        tokens_in: int = 0,
        tokens_out: int = 0,
        duration_ms: int = 0,
        timestamp: datetime | None = None,
        status: str = "success",
        session_id: str | None = None,
    ) -> None:
        self.id = id or str(uuid.uuid4())
        self.employee_id = employee_id
        self.key_id = key_id
        self.model = model
        self.tokens_in = tokens_in
        self.tokens_out = tokens_out
        self.duration_ms = duration_ms
        self.timestamp = timestamp or datetime.now(timezone.utc)
        self.status = status
        self.session_id = session_id

    @property
    def total_tokens(self) -> int:
        return self.tokens_in + self.tokens_out
