from app.repository.base import BaseRepositories
from app.models.submission.model import Submission
from app.models.course.model import Course
from app.database import async_session
from app.config import settings
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import delete, insert, select, update, join
from app.models.lesson.model import Lesson

class LessonRepository(BaseRepositories):
    model = Lesson

    @classmethod
    async def get_all_lessons_with_submissions(cls, course_id: int):
        async with async_session() as session:
            query = (
                select(
                    Lesson.title,
                    Lesson.description,
                    func.count(Submission.id).label('submissions_count')
                )
                .join(Submission)
                .filter(Submission.lesson_id == Lesson.id, Submission.course_id == course_id)  # Простые фильтры
                .group_by(Lesson.id, Lesson.title, Lesson.description)
            )
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def get_all_lessons_with_course(cls):
        async with async_session() as session:
            query = (
                select(Lesson.id, Lesson.title, Lesson.description, Course.title)
                .join(Lesson)
                .join(Course)
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