from fastapi import HTTPException, Depends
from sqlalchemy import delete, insert, select, update
from app.database import DatabaseFactory, get_database_factory
from app.config import Settings

class BaseRepositories:
    model = None
    settings = Settings()
    @classmethod
    async def get_all(cls, db_factory: DatabaseFactory = get_database_factory(settings),  **filter ):
        async with db_factory.session() as session:
            query = select(cls.model).filter_by(**filter)
            result = await session.execute(query)
            return result.scalars().all()
                        
    @classmethod
    async def add(cls, db_factory: DatabaseFactory = get_database_factory(settings), **data):
        async with db_factory.session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
        
    @classmethod
    async def update(cls, id: int, db_factory: DatabaseFactory = get_database_factory(settings), **data):
        async with db_factory.session() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(**data)
            )
            await session.execute(query)
            await session.commit()
        
        
    @classmethod
    async def delete(cls, id, db_factory: DatabaseFactory = get_database_factory(settings)):
        async with db_factory.session() as session:
            query = delete(cls.model).where(cls.model.id == id)
            await session.execute(query)
            await session.commit()
            
    @classmethod
    async def find_one_or_none(cls, db_factory: DatabaseFactory = get_database_factory(settings), **filter):
        async with db_factory.session() as session:
            query = select(cls.model).filter_by(**filter).limit(1)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_by_id(cls, id, db_factory: DatabaseFactory = get_database_factory(settings)):
        async with db_factory.session() as session:
            query = select(cls.model).where(cls.model.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
            