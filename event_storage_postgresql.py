from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config_reader import env_config
from typing import List, NamedTuple
import calendar
from datetime import date

from sqlalchemy import text


class DayEvents(NamedTuple):
    stars: int
    day_class: str | None
    is_amrita: bool
    moon: str | None
    holiday: str | None


class EventStorageSqlAlchemy:
    def __init__(self):
        connection_str = f"postgresql+pg8000://{env_config.postgresql_username}:{env_config.postgresql_password}@{env_config.postgresql_hostname}:{env_config.postgresql_port}/{env_config.postgresql_database}"
        self.engine = create_engine(connection_str, echo=True)

    def get_events_calendar_view(self, year: int, month: int) -> List[DayEvents]:
        _, month_days = calendar.monthrange(year, month)
        start_date = date(year, month, 1)
        end_date = date(year, month, month_days)

        query = text(
            """
            SELECT 
                e.date,
                e.stars,
                e.base_type,
                e.holiday
                FROM events e
                WHERE e.date BETWEEN :start_date AND :end_date
                ORDER by e.date; 
        """
        )


        with Session(self.engine) as session:
            result = session.execute(
                query, {"start_date": start_date, "end_date": end_date}
            ).fetchall()
            
            events_by_day = [DayEvents(stars=0, day_class=None, is_amrita=False, moon=None, holiday=None) for _ in range(month_days)]
            border_types = {'bm', 'gr', 'dk', 'bsh'}

            for event_date, stars, base_type, holiday in result:
                index = event_date.day - 1
                day = events_by_day[index]
                ev = [t.strip() for t in base_type.split(',')] if base_type else []


                day_class = day.day_class
                moon = day.moon
                is_amrita = day.is_amrita
                
                for x in ev:
                    if x in border_types:
                        day_class = x
                    if x == "tl":
                        moon = "🌑"
                    elif x == "ba":
                        moon = "🌕"
                    if x == "a":
                        is_amrita = True
                        
                events_by_day[index] = DayEvents(
                    stars=stars or 0,
                    day_class=day_class,
                    is_amrita=is_amrita,
                    moon=moon,
                    holiday=holiday
            )
            return events_by_day
        