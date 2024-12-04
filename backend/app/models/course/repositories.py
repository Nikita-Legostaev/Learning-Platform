from app.repository.base import BaseRepositories
from app.models.course.model import Course
from app.database import async_session
from app.config import settings
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import delete, insert, select, update, join
from app.models.enrollment.model import Enrollment

class CourceRepository(BaseRepositories):
    model = Course

    @classmethod
    async def get_all_courses_with_enrolled_students(cls, **filter):
        async with async_session() as session:
            query = (
                select(
                    Course.title,
                    Course.description,
                    func.count(Enrollment.user_id).label('enrolled_students')
                )
                .join(Enrollment)
                .filter_by(**filter)  # Простые фильтры
                .group_by(Course.id, Course.title, Course.description)
            )
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, id: int, **data):
        async with async_session() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(**data)
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, id):
        async with async_session() as session:
            query = delete(cls.model).where(cls.model.id == id)
            await session.execute(query)
            await session.commit()
            