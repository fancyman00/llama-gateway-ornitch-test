from __future__ import annotations

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

_email_pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_email(value: str) -> str:
    if not _email_pattern.match(value):
        raise ValueError("Invalid email address")
    return value


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., max_length=255, validate_default=False)
    is_active: bool = True
    quota_hourly: int = Field(default=100_000, ge=0)
    quota_daily: int = Field(default=500_000, ge=0)
    quota_weekly: int = Field(default=2_000_000, ge=0)

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str) -> str:
        return _validate_email(v)


class EmployeeUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None
    quota_hourly: int | None = Field(default=None, ge=0)
    quota_daily: int | None = Field(default=None, ge=0)
    quota_weekly: int | None = Field(default=None, ge=0)

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str | None) -> str | None:
        if v is not None:
            return _validate_email(v)
        return v


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    is_active: bool
    quota_hourly: int
    quota_daily: int
    quota_weekly: int
    created_at: datetime
    updated_at: datetime
