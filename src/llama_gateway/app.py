from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from llama_gateway.config import get_settings
from llama_gateway.infrastructure.database.sqlite import SQLiteDatabaseAdapter
from llama_gateway.presentation.routes.admin_routes import router as admin_router


def _get_db(request: Request) -> SQLiteDatabaseAdapter:
    return request.app.state.db


def create_app() -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        adapter = SQLiteDatabaseAdapter(database_url=settings.database_url)
        await adapter.init()
        app.state.db = adapter
        yield
        await adapter.close()

    application = FastAPI(
        title="Llama Gateway",
        version="0.1.0",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(admin_router, prefix="/admin")

    return application


app = create_app()
