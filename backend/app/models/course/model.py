from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base


class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    teacher_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    teacher = relationship('User', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course')
    lessons = relationship('Lesson', back_populates='course')
