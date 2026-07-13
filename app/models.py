from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class TeacherModel(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(50))
    specialization: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(100))
    experience_years: Mapped[int]
 