from app.repository.base import BaseRepositories
from app.models.submission.model import Submission
from app.models.notification.model import Notification
from app.models.submission.model import Submission
from app.models.course.model import Course
from app.models.users.model import User
from app.database import async_session
from app.config import settings
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import delete, insert, select, update, join
from app.models.lesson.model import Lesson

class SubmissionRepository(BaseRepositories):
    model = Submission

    @classmethod
    async def get_all_submissions_with_user(cls, user):
        async with async_session() as session:
            query = (
                select(
                    Submission.id,
                    Submission.content,
                    Submission.submitted_at,
                    Submission.lesson_id,
                    User.username
                )
                .join(User, Submission.user_id == User.id)
                .filter(User.id == user.id)
                .order_by(Submission.submitted_at.desc())
            )
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def create_submission(cls, content, user_id, lesson_id):
        async with async_session() as session:
            query = insert(cls.model).values(content=content, user_id=user_id, lesson_id=lesson_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_submission(cls, id, content):
        async with async_session() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(content=content)
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_submission(cls, id):
        async with async_session() as session:
            query = delete(cls.model).where(cls.model.id == id)
            await session.execute(query)
            await session.commit()