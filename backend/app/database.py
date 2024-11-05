from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import JSON
from app.config import Settings
from contextlib import asynccontextmanager


class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str]: JSON
    }


class DatabaseFactory:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._engine = create_async_engine(self.settings.DB_URL, echo=True)
        self._session_factory = async_sessionmaker(
            bind=self._engine, 
            expire_on_commit=False
        )

    @asynccontextmanager
    async def session(self):
        async with self._session_factory() as session:
            yield session
            await session.close() 

    async def close_engine(self):
        await self._engine.dispose()


def get_database_factory(settings: Settings) -> DatabaseFactory:
    return DatabaseFactory(settings)
