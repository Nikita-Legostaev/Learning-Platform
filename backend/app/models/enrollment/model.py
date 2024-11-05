from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base

class Enrollment(Base):
    __tablename__ = 'enrollments'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    enrollment_date: Mapped[datetime] = mapped_column(server_default=func.now())

    user = relationship('User', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')
