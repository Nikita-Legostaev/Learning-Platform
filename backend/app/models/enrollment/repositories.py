from app.repository.base import BaseRepositories
from app.models.course.model import Course
from app.database import async_session
from app.models.users.model import User
from app.config import settings
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import delete, insert, select, update, join
from app.models.enrollment.model import Enrollment

class EnrollmentRepository(BaseRepositories):
    model = Enrollment

    @classmethod
    async def get_all_enrolled_users(cls, course_id: int):
        async with async_session() as session:
            query = (
                select(User.username, User.email)
                .join(User)
                .join(Enrollment)
                .where(Enrollment.course_id == course_id)
            )
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def register(cls, course_id: int, user_id: int):
        async with async_session() as session:
            query = insert(cls.model).values(course_id=course_id, user_id=user_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def unregister(cls, course_id: int, user_id: int):
        async with async_session() as session:
            query = delete(cls.model).where(cls.model.course_id == course_id, cls.model.user_id == user_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_users(cls, id: int, **data):
        async with async_session() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(**data)
            )
            await session.execute(query)
            await session.commit()