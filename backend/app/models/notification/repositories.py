from app.repository.base import BaseRepositories
from app.models.submission.model import Submission
from app.models.notification.model import Notification
from app.models.course.model import Course
from app.models.users.model import User
from app.database import async_session
from app.config import settings
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import delete, insert, select, update, join
from app.models.lesson.model import Lesson

class NotificationRepository(BaseRepositories):
    model = Notification

    @classmethod
    async def get_all_notifications_with_user(cls, user):
        async with async_session() as session:
            query = (
                select(
                    Notification.id,
                    Notification.message,
                    Notification.created_at,
                    User.username
                )
                .join(User, Notification.user_id == User.id)
                .filter(User.id == user.id)
                .order_by(Notification.created_at.desc())
            )
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def create_notification(cls, message, user_id):
        async with async_session() as session:
            query = insert(cls.model).values(message=message, user_id=user_id)
            await session.execute(query)
            await session.commit()
        
    @classmethod
    async def delete_notification(cls, notification_id):
        async with async_session() as session:
            query = delete(cls.model).where(cls.model.id == notification_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_notification(cls, id: int, **data):
        async with async_session() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(**data)
            )
            await session.execute(query)
            await session.commit()