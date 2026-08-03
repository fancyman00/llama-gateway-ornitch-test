from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from llama_gateway.domain.api_key import ApiKey
from llama_gateway.domain.employee import Employee
from llama_gateway.domain.quota_window import QuotaWindow
from llama_gateway.domain.rate_limit_bucket import RateLimitBucket
from llama_gateway.domain.request import Request


class DatabaseAdapter(ABC):
    """Abstract database adapter defining the persistence contract.

    Implementations (SQLite, PostgreSQL) live in the infrastructure layer.
    The application layer depends only on this interface.
    """

    @abstractmethod
    async def init(self) -> None:
        """Create tables and prepare the database for use."""

    @abstractmethod
    async def close(self) -> None:
        """Release database resources."""

    # --- Employee ---

    @abstractmethod
    async def create_employee(self, employee: Employee) -> Employee:
        """Persist a new employee and return it with its id populated."""

    @abstractmethod
    async def get_employee(self, employee_id: str) -> Employee | None:
        """Return the employee with the given id, or None."""

    @abstractmethod
    async def list_employees(self) -> list[Employee]:
        """Return all employees."""

    @abstractmethod
    async def update_employee(self, employee: Employee) -> Employee:
        """Persist changes to an existing employee."""

    @abstractmethod
    async def delete_employee(self, employee_id: str) -> bool:
        """Remove an employee. Returns True if one was deleted."""

    # --- API Key ---

    @abstractmethod
    async def create_api_key(self, key: ApiKey) -> ApiKey:
        """Persist a new api key and return it with its id populated."""

    @abstractmethod
    async def get_api_key(self, key_id: str) -> ApiKey | None:
        """Return the api key with the given id, or None."""

    @abstractmethod
    async def get_api_key_by_hash(self, key_hash: str) -> ApiKey | None:
        """Return the api key with the given hash, or None."""

    @abstractmethod
    async def list_api_keys(self, employee_id: str | None = None) -> list[ApiKey]:
        """Return api keys, optionally filtered by employee_id."""

    @abstractmethod
    async def update_api_key(self, key: ApiKey) -> ApiKey:
        """Persist changes to an existing api key."""

    @abstractmethod
    async def delete_api_key(self, key_id: str) -> bool:
        """Remove an api key. Returns True if one was deleted."""

    # --- Request ---

    @abstractmethod
    async def create_request(self, request: Request) -> Request:
        """Persist a new request and return it with its id populated."""

    @abstractmethod
    async def list_requests(
        self,
        employee_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Request]:
        """Return requests, optionally filtered by employee_id."""

    # --- Quota Window ---

    @abstractmethod
    async def get_quota_window(
        self,
        employee_id: str,
        window_type: str,
        window_start: datetime,
    ) -> QuotaWindow | None:
        """Return the quota window for an employee at a given start time."""

    @abstractmethod
    async def upsert_quota_window(self, window: QuotaWindow) -> QuotaWindow:
        """Insert or update a quota window. Returns the persisted window."""

    @abstractmethod
    async def list_quota_windows(
        self,
        employee_id: str | None = None,
        window_type: str | None = None,
    ) -> list[QuotaWindow]:
        """Return quota windows, optionally filtered."""

    # --- Rate Limit Bucket ---

    @abstractmethod
    async def get_rate_limit_bucket(
        self,
        employee_id: str,
        window_type: str,
        window_start: datetime,
    ) -> RateLimitBucket | None:
        """Return the rate limit bucket for an employee at a given start time."""

    @abstractmethod
    async def upsert_rate_limit_bucket(self, bucket: RateLimitBucket) -> RateLimitBucket:
        """Insert or update a rate limit bucket. Returns the persisted bucket."""

    @abstractmethod
    async def list_rate_limit_buckets(
        self,
        employee_id: str | None = None,
        window_type: str | None = None,
    ) -> list[RateLimitBucket]:
        """Return rate limit buckets, optionally filtered."""
