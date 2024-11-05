from sqlalchemy import  ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base


class Submission(Base):
    __tablename__ = 'submissions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    lesson_id: Mapped[int] = mapped_column(ForeignKey('lessons.id'))
    submitted_at: Mapped[datetime] = mapped_column(server_default=func.now())
    content: Mapped[str] = mapped_column(nullable=False)

    student = relationship('User', back_populates='submissions')
    lesson = relationship('Lesson', back_populates='submissions')
