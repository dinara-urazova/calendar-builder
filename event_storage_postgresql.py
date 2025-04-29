from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from config_reader import env_config
from entity.event import Event
from typing import List, Optional, NamedTuple
import calendar
from datetime import date

from sqlalchemy import text


class DayEvents(NamedTuple):
    stars: int
    day_class: str | None
    is_amrita: bool
    moon: str | None


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
                EXTRACT(DAY FROM d)::int AS day, 
                array_remove(array_agg(e.base_type), NULL) AS event_types
            FROM generate_series(:start_date, :end_date, '1 day'::interval) d
            LEFT JOIN events e ON d::date = e.date
            GROUP BY day
            ORDER BY day;
        """
        )

        with Session(self.engine) as session:
            result = session.execute(
                query, {"start_date": start_date, "end_date": end_date}
            ).fetchall()
            events_by_day = [[] for _ in range(month_days)]

            def get_day_events(events: list) -> DayEvents:
                stars = 0
                day_class = None
                is_amrita = False
                moon = None

                for event in events:
                    if "stars_" in event:
                        stars = int(event[-1])
                    if event in ['bm', 'gr', 'bsh', 'dk']:
                        day_class = event
                    if "tl" == event:
                        moon = "🌑"
                    if "ba" == event:
                        moon = "🌕"
                    if "a" == event:
                        is_amrita = True

                return DayEvents(
                    stars=stars,
                    day_class=day_class,
                    is_amrita=is_amrita,
                    moon=moon,
                )

            for day, event_types in result:
                events_by_day[day - 1] = get_day_events(event_types)
            return events_by_day
