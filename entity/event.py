from sqlalchemy import Date, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from entity.base import Base


class Event(Base):
    __tablename__ = "events"  # название таблицы в БД (смотри через DBeaver)

    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    stars: Mapped[int] = mapped_column(Integer)
    base_type: Mapped[str] = mapped_column(String)
    holiday: Mapped[str] = mapped_column(String)
 