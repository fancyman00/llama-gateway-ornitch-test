from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ApiKeyCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    employee_id: str = Field(..., min_length=1)


class ApiKeyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    employee_id: str
    key_prefix: str
    is_active: bool
    created_at: datetime
    last_used_at: datetime | None = None


class ApiKeyCreateResponse(BaseModel):
    """Response returned only at creation time, containing the raw key."""

    key: str
    key_id: str
    employee_id: str
    key_prefix: str
    created_at: datetime
