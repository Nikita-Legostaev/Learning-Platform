from sqlalchemy import  ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base


class Lesson(Base):
    __tablename__ = 'lessons'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    course = relationship('Course', back_populates='lessons')
    submissions = relationship('Submission', back_populates='lesson')
