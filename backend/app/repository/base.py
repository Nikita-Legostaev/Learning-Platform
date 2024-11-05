from fastapi import HTTPException, Depends
from sqlalchemy import delete, insert, select, update
from app.database import DatabaseFactory, get_database_factory
from app.expection import CannotAddDataToDatabase, CannotDeleteDataFromDatabase, CannotUpdateDataInDatabase, NotFoundException

class BaseRepositories:
    model = None
    
    session_db = get_database_factory()
    @classmethod
    async def get_all(cls, db_factory: DatabaseFactory = Depends(get_database_factory),  **filter ):
        try:
            async with db_factory.session() as session:
                query = select(cls.model).filter_by(**filter)
                result = await session.execute(query)
                return result.scalars().all()
        except HTTPException:
            raise NotFoundException
            
        
    @classmethod
    async def add(cls, db_factory: DatabaseFactory = Depends(get_database_factory), **data):
        try:
            async with db_factory.session() as session:
                query = insert(cls.model).values(**data)
                await session.execute(query)
                await session.commit()
        except HTTPException:
            raise CannotAddDataToDatabase
            
    @classmethod
    async def update(cls, id: int, db_factory: DatabaseFactory = Depends(get_database_factory), **data):
        try:
            async with db_factory.session() as session:
                query = (
                    update(cls.model)
                    .where(cls.model.id == id)
                    .values(**data)
                )
                await session.execute(query)
                await session.commit()
        except HTTPException:
            raise CannotUpdateDataInDatabase
        
        
    @classmethod
    async def delete(cls, id, db_factory: DatabaseFactory = Depends(get_database_factory)):
        try:
            async with db_factory.session() as session:
                query = delete(cls.model).where(cls.model.id == id)
                await session.execute(query)
                await session.commit()
        except HTTPException:
            raise CannotDeleteDataFromDatabase     
            
    @classmethod
    async def find_one_or_none(cls, db_factory: DatabaseFactory = Depends(get_database_factory), **filter):
        async with db_factory.session() as session:
            query = select(cls.model).filter_by(**filter).limit(1)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_by_id(cls, id, db_factory: DatabaseFactory = Depends(get_database_factory)):
        async with db_factory.session() as session:
            query = select(cls.model).where(cls.model.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
            