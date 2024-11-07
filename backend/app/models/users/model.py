from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import func
from datetime import datetime
from app.database import Base
from pydantic import EmailStr

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default='student')
    date_joined: Mapped[datetime] = mapped_column(server_default=func.now())
    last_login: Mapped[datetime] = mapped_column(nullable=True)

    
