from sqlalchemy import Date, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from entity.base import Base


class Event(Base):
    __tablename__ = "events"  # название таблицы в БД (смотри через DBeaver)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    base_type: Mapped[str] = mapped_column(String)
 