from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.app import models  # noqa: F401
from backend.app.core.config import settings
from backend.app.db import Base, get_db_session
from backend.app.main import create_app


@pytest_asyncio.fixture
async def api_client(tmp_path) -> AsyncGenerator[AsyncClient, None]:
    database_path = tmp_path / "test.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{database_path}", echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async def override_get_db_session():
        async with session_factory() as session:
            yield session

    previous_auto_create_tables = settings.auto_create_tables
    settings.auto_create_tables = False

    app = create_app()
    app.dependency_overrides[get_db_session] = override_get_db_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
    settings.auto_create_tables = previous_auto_create_tables
    await engine.dispose()
