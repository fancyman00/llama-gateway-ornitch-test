from __future__ import annotations

from functools import cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LLAMA_GATEWAY_", extra="ignore")

    database_url: str = "sqlite+aiosqlite:///./llama_gateway.db"
    host: str = "0.0.0.0"
    port: int = 8000
    llm_server_url: str = "http://localhost:8080"
    log_level: Literal["debug", "info", "warning", "error"] = "info"


@cache
def get_settings() -> Settings:
    return Settings()
