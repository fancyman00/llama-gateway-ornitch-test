from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class EmployeeModel(Base):
    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    quota_hourly: Mapped[int] = mapped_column(Integer, default=100_000)
    quota_daily: Mapped[int] = mapped_column(Integer, default=500_000)
    quota_weekly: Mapped[int] = mapped_column(Integer, default=2_000_000)
    created_at: Mapped[str] = mapped_column(String(32))
    updated_at: Mapped[str] = mapped_column(String(32))

    api_keys: Mapped[list["ApiKeyModel"]] = relationship(
        back_populates="employee",
        cascade="all, delete-orphan",
    )
    requests: Mapped[list["RequestModel"]] = relationship(
        back_populates="employee",
        cascade="all, delete-orphan",
    )
    quota_windows: Mapped[list["QuotaWindowModel"]] = relationship(
        back_populates="employee",
        cascade="all, delete-orphan",
    )
    rate_limit_buckets: Mapped[list["RateLimitBucketModel"]] = relationship(
        back_populates="employee",
        cascade="all, delete-orphan",
    )


class ApiKeyModel(Base):
    __tablename__ = "api_keys"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    employee_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("employees.id"),
        nullable=False,
    )
    key_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    key_prefix: Mapped[str] = mapped_column(String(4), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[str] = mapped_column(String(32))
    last_used_at: Mapped[str | None] = mapped_column(String(32), nullable=True)

    employee: Mapped["EmployeeModel"] = relationship(back_populates="api_keys")
    requests: Mapped[list["RequestModel"]] = relationship(
        back_populates="api_key",
    )


class RequestModel(Base):
    __tablename__ = "requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    employee_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("employees.id"),
        nullable=False,
    )
    key_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("api_keys.id"),
        nullable=False,
    )
    model: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    tokens_in: Mapped[int] = mapped_column(Integer, default=0)
    tokens_out: Mapped[int] = mapped_column(Integer, default=0)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    timestamp: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="success")
    session_id: Mapped[str | None] = mapped_column(String(36), nullable=True)

    employee: Mapped["EmployeeModel"] = relationship(back_populates="requests")
    api_key: Mapped["ApiKeyModel"] = relationship(back_populates="requests")


class QuotaWindowModel(Base):
    __tablename__ = "quota_windows"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    employee_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("employees.id"),
        nullable=False,
    )
    window_type: Mapped[str] = mapped_column(String(16), nullable=False)
    window_start: Mapped[str] = mapped_column(String(32), nullable=False)
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)

    employee: Mapped["EmployeeModel"] = relationship(back_populates="quota_windows")


class RateLimitBucketModel(Base):
    __tablename__ = "rate_limit_buckets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    employee_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("employees.id"),
        nullable=False,
    )
    window_type: Mapped[str] = mapped_column(String(16), nullable=False)
    window_start: Mapped[str] = mapped_column(String(32), nullable=False)
    request_count: Mapped[int] = mapped_column(Integer, default=0)

    employee: Mapped["EmployeeModel"] = relationship(
        back_populates="rate_limit_buckets",
    )
