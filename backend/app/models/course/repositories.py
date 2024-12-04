from app.repository.base import BaseRepositories
from app.models.users.model import User
from app.database import async_session
from app.config import settings
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import delete, insert, select, update

class CourceRepository(BaseRepositories):
    model = User