from app.repository.base import BaseRepositories
from app.models.users.model import User
from app.database import DatabaseFactory, get_database_factory
from app.config import Settings
from datetime import datetime
from sqlalchemy import delete, insert, select, update

class UserRepository(BaseRepositories):
    model = User
    settings = Settings()

    @classmethod
    async def update_last_login(cls, user_id: int, db_factory: DatabaseFactory = get_database_factory(settings)):
        async with db_factory.session() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == user_id)
                .values(last_login=datetime.utcnow())
            )
            await session.execute(query)
            await session.commit()