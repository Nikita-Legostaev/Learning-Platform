from app.repository.base import BaseRepositories
from app.models.users.model import User

class UserRepository(BaseRepositories):
    model = User