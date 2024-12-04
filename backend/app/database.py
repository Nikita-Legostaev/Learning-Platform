from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import JSON
from app.config import settings
from contextlib import asynccontextmanager

engine = create_async_engine(settings.DB_URL)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str]: JSON
    }


