from app.repository.base import BaseRepositories
from app.models.users.model import User
from app.database import async_session
from app.config import settings
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import delete, insert, select, update

class UserRepository(BaseRepositories):
    model = User

    @classmethod
    async def update_last_login(cls, user_id: int):
        async with async_session() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == user_id)
                .values(last_login=func.now())
            )
            await session.execute(query)
            await session.commit()